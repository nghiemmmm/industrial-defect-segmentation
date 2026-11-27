import os
import shutil
import tempfile
import pytest
import numpy as np
import cv2
import yaml
import json

from data_engine.sample import Sample
from data_engine.base import BaseProcessor, Pipeline
from data_engine.loaders.mvtec_loader import MVTecLoader
from data_engine.loaders.visa_loader import VisALoader
from data_engine.exporters.yolo_seg_exporter import YOLOSegExporter


class DummyInvertProcessor(BaseProcessor):
    """Simple processor for testing pipeline chaining: inverts pixel values."""
    def process(self, sample: Sample) -> Sample:
        inverted = 255 - sample.image
        sample.image = inverted
        return sample


class TestSample:
    def test_sample_creation_with_mask(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        mask = np.zeros((100, 100), dtype=np.uint8)
        mask[20:40, 20:40] = 255

        sample = Sample(
            image=img,
            mask=mask,
            category="bottle",
            defect_type="broken",
            is_anomaly=True,
            image_path="test_img.png"
        )
        assert sample.shape == (100, 100, 3)
        assert sample.height == 100
        assert sample.width == 100
        assert sample.has_mask() is True
        # Area: 20 * 20 = 400 pixels out of 10,000 = 0.04
        assert pytest.approx(sample.defect_area_ratio(), 0.001) == 0.04

    def test_sample_defect_free_auto_mask(self):
        img = np.ones((50, 60, 3), dtype=np.uint8) * 128
        sample = Sample(
            image=img,
            mask=None,
            category="cable",
            defect_type="good",
            is_anomaly=False
        )
        assert sample.mask is not None
        assert sample.mask.shape == (50, 60)
        assert np.all(sample.mask == 0)
        assert sample.has_mask() is False
        assert sample.defect_area_ratio() == 0.0

    def test_sample_shape_mismatch_raises(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        mask = np.zeros((50, 50), dtype=np.uint8)
        with pytest.raises(ValueError, match="do not match"):
            Sample(image=img, mask=mask)

    def test_sample_clone(self):
        img = np.zeros((30, 30, 3), dtype=np.uint8)
        sample = Sample(image=img, category="hazelnut", defect_type="scratch", is_anomaly=True)
        cloned = sample.clone()
        assert cloned is not sample
        assert np.array_equal(cloned.image, sample.image)
        cloned.image[0, 0, 0] = 255
        assert sample.image[0, 0, 0] == 0


class TestPipeline:
    def test_pipeline_execution(self):
        img = np.zeros((10, 10, 3), dtype=np.uint8)
        sample = Sample(image=img, category="test")
        
        pipeline = Pipeline([DummyInvertProcessor()])
        assert len(pipeline) == 1
        
        result = pipeline.run([sample])[0]
        assert np.all(result.image == 255)


class TestVisALoader:
    @pytest.fixture
    def mock_visa_dataset(self):
        tmp_dir = tempfile.mkdtemp()
        cat = "candle"
        cat_dir = os.path.join(tmp_dir, cat)

        normal_dir = os.path.join(cat_dir, "normal")
        anomaly_dir = os.path.join(cat_dir, "anomaly")
        gt_dir = os.path.join(cat_dir, "ground_truth")

        for d in [normal_dir, anomaly_dir, gt_dir]:
            os.makedirs(d, exist_ok=True)

        for i in range(4):
            img = np.full((80, 80, 3), 120, dtype=np.uint8)
            cv2.imwrite(os.path.join(normal_dir, f"{i:03d}.png"), img)

        for i in range(6):
            img = np.full((80, 80, 3), 200, dtype=np.uint8)
            mask = np.zeros((80, 80), dtype=np.uint8)
            mask[10:30, 10:30] = 255
            cv2.imwrite(os.path.join(anomaly_dir, f"{i:03d}.png"), img)
            cv2.imwrite(os.path.join(gt_dir, f"{i:03d}.png"), mask)

        yield tmp_dir
        shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_visa_loader_loading_and_balancing(self, mock_visa_dataset):
        loader = VisALoader(
            root_dir=mock_visa_dataset,
            split_ratio=0.8,
            good_ratio=0.25, # 25% of anomaly train count (int(4 * 0.25) = 1 normal)
            seed=42
        )
        cats = loader.get_categories()
        assert "candle" in cats

        train_samples = loader.load(split="train")
        anomalies = [s for s in train_samples if s.is_anomaly]
        normals = [s for s in train_samples if not s.is_anomaly]
        assert len(anomalies) == 4
        assert len(normals) == 1

        val_samples = loader.load(split="val")
        assert len(val_samples) == 2
        assert all(s.is_anomaly for s in val_samples)


class TestCLIEndToEnd:
    def test_run_preprocess_cli(self, tmp_path):
        # Create minimal synthetic dataset
        mock_root = tmp_path / "mock_mvtec"
        cat_dir = mock_root / "tile"
        (cat_dir / "train" / "good").mkdir(parents=True)
        (cat_dir / "test" / "crack").mkdir(parents=True)
        (cat_dir / "ground_truth" / "crack").mkdir(parents=True)

        # Write sample images
        img = np.full((64, 64, 3), 180, dtype=np.uint8)
        mask = np.zeros((64, 64), dtype=np.uint8)
        mask[10:20, 10:20] = 255
        cv2.imwrite(str(cat_dir / "train" / "good" / "000.png"), img)
        cv2.imwrite(str(cat_dir / "test" / "crack" / "000.png"), img)
        cv2.imwrite(str(cat_dir / "ground_truth" / "crack" / "000_mask.png"), mask)

        out_dir = tmp_path / "processed_yolo"

        import subprocess
        import sys
        cmd = [
            sys.executable,
            "tools/run_preprocess.py",
            "--dataset", "mvtec",
            "--root", str(mock_root),
            "--out", str(out_dir),
            "--split-ratio", "1.0",
            "--good-ratio", "1.0"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        assert res.returncode == 0, f"CLI failed: {res.stderr}"
        assert (out_dir / "dataset.yaml").exists()
        assert (out_dir / "pipeline_meta.json").exists()
        assert (out_dir / "images" / "train").exists()
        assert (out_dir / "labels" / "train").exists()




class TestMVTecLoaderAndExporter:
    @pytest.fixture
    def mock_mvtec_dataset(self):
        """Creates a temporary synthetic MVTec AD directory structure."""
        tmp_dir = tempfile.mkdtemp()
        cat = "bottle"
        cat_dir = os.path.join(tmp_dir, cat)

        # Create subfolders
        train_good = os.path.join(cat_dir, "train", "good")
        test_defect = os.path.join(cat_dir, "test", "broken_small")
        test_good = os.path.join(cat_dir, "test", "good")
        gt_defect = os.path.join(cat_dir, "ground_truth", "broken_small")

        for d in [train_good, test_defect, test_good, gt_defect]:
            os.makedirs(d, exist_ok=True)

        # 1. Create 5 train good images
        for i in range(5):
            img = np.full((100, 100, 3), 100, dtype=np.uint8)
            cv2.imwrite(os.path.join(train_good, f"{i:03d}.png"), img)

        # 2. Create 10 test defect images + masks
        for i in range(10):
            img = np.full((100, 100, 3), 150, dtype=np.uint8)
            mask = np.zeros((100, 100), dtype=np.uint8)
            # Add a rectangular defect
            mask[30:50, 30:50] = 255
            cv2.imwrite(os.path.join(test_defect, f"{i:03d}.png"), img)
            cv2.imwrite(os.path.join(gt_defect, f"{i:03d}_mask.png"), mask)

        yield tmp_dir
        shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_mvtec_loader(self, mock_mvtec_dataset):
        loader = MVTecLoader(
            root_dir=mock_mvtec_dataset,
            split_ratio=0.8,
            include_good_train=True,
            good_ratio=0.25, # 25% of defect train count (8 * 0.25 = 2 good images)
            seed=42
        )

        categories = loader.get_categories()
        assert categories == ["bottle"]

        train_samples = loader.load(split="train")
        # 10 defect * 0.8 = 8 defect train samples + 2 good train samples = 10 total
        assert len(train_samples) == 10
        anomalies = [s for s in train_samples if s.is_anomaly]
        goods = [s for s in train_samples if not s.is_anomaly]
        assert len(anomalies) == 8
        assert len(goods) == 2

        val_samples = loader.load(split="val")
        # 10 defect * 0.2 = 2 defect val samples
        assert len(val_samples) == 2
        assert all(s.is_anomaly for s in val_samples)

    def test_yolo_seg_exporter(self, mock_mvtec_dataset):
        loader = MVTecLoader(
            root_dir=mock_mvtec_dataset,
            split_ratio=0.8,
            include_good_train=True,
            good_ratio=0.25,
            seed=42
        )
        train_samples = loader.load(split="train")
        val_samples = loader.load(split="val")

        out_tmp = tempfile.mkdtemp()
        try:
            exporter = YOLOSegExporter(
                output_dir=out_tmp,
                save_debug_masks=True,
            )
            train_stats = exporter.export(train_samples, split="train")
            val_stats = exporter.export(val_samples, split="val")

            # Check export stats
            assert train_stats["total_exported"] == 10
            assert train_stats["anomalies"] == 8
            assert train_stats["defect_free"] == 2

            # Check file system layout
            assert os.path.exists(os.path.join(out_tmp, "dataset.yaml"))
            assert os.path.exists(os.path.join(out_tmp, "pipeline_meta.json"))
            assert os.path.exists(os.path.join(out_tmp, "images", "train"))
            assert os.path.exists(os.path.join(out_tmp, "labels", "train"))
            assert os.path.exists(os.path.join(out_tmp, "masks_debug", "train"))

            # Verify dataset.yaml content
            with open(os.path.join(out_tmp, "dataset.yaml"), "r") as f:
                yaml_data = yaml.safe_load(f)
            assert yaml_data["train"] == "images/train"
            assert yaml_data["names"][0] == "bottle"

            # Check that good samples have 0-byte label files
            lbl_files = os.listdir(os.path.join(out_tmp, "labels", "train"))
            empty_files = [f for f in lbl_files if os.path.getsize(os.path.join(out_tmp, "labels", "train", f)) == 0]
            non_empty_files = [f for f in lbl_files if os.path.getsize(os.path.join(out_tmp, "labels", "train", f)) > 0]
            assert len(empty_files) == 2  # exactly the 2 good samples
            assert len(non_empty_files) == 8  # exactly the 8 anomaly samples

            # Check polygon format in non-empty label
            sample_lbl = os.path.join(out_tmp, "labels", "train", non_empty_files[0])
            with open(sample_lbl, "r") as f:
                content = f.read().strip()
                tokens = content.split()
                assert tokens[0] == "0"  # class_id
                # Polygons have x y pairs (normalized between 0 and 1)
                assert len(tokens) >= 7
                for val in tokens[1:]:
                    flt = float(val)
                    assert 0.0 <= flt <= 1.0

        finally:
            shutil.rmtree(out_tmp, ignore_errors=True)

    def test_mvtec_loader_strict_defect_free_mode(self, tmp_path):
        """Verifies strict defect-free training regime: zero real defects in train/val, full test isolation."""
        cat_dir = tmp_path / "bottle"
        (cat_dir / "train" / "good").mkdir(parents=True)
        (cat_dir / "test" / "good").mkdir(parents=True)
        (cat_dir / "test" / "broken_small").mkdir(parents=True)
        (cat_dir / "ground_truth" / "broken_small").mkdir(parents=True)

        for i in range(10):
            img = np.full((64, 64, 3), 100 + i, dtype=np.uint8)
            cv2.imwrite(str(cat_dir / "train" / "good" / f"{i:03d}.png"), img)
        for i in range(4):
            img = np.full((64, 64, 3), 120 + i, dtype=np.uint8)
            cv2.imwrite(str(cat_dir / "test" / "good" / f"{i:03d}.png"), img)
        for i in range(6):
            img = np.full((64, 64, 3), 180 + i, dtype=np.uint8)
            mask = np.zeros((64, 64), dtype=np.uint8)
            mask[16:32, 16:32] = 255
            cv2.imwrite(str(cat_dir / "test" / "broken_small" / f"{i:03d}.png"), img)
            cv2.imwrite(str(cat_dir / "ground_truth" / "broken_small" / f"{i:03d}_mask.png"), mask)

        loader = MVTecLoader(
            root_dir=str(tmp_path),
            split_ratio=0.8,
            seed=42,
            defect_free=True,
        )

        train_samples = loader.load(split="train")
        val_samples = loader.load(split="val")
        test_samples = loader.load(split="test")

        assert len(train_samples) == 8
        assert len(val_samples) == 2
        assert all(not s.is_anomaly for s in train_samples)
        assert all(not s.is_anomaly for s in val_samples)

        test_defects = [s for s in test_samples if s.is_anomaly]
        test_goods = [s for s in test_samples if not s.is_anomaly]
        assert len(test_defects) == 6
        assert len(test_goods) == 4
        assert all(s.has_mask() for s in test_defects)
        assert all(not s.has_mask() for s in test_goods)


# ==============================================================================
# Standardized 9-Experiment Protocol (EXP-00 to EXP-08) & Material-Adaptive Tests
# ==============================================================================
class TestNineExperimentProtocol:
    def test_all_nine_yaml_configs_are_valid_and_standardized(self):
        import glob
        import os
        from experiments.run_experiment import build_pipelines_from_config, load_yaml

        config_files = sorted(glob.glob(os.path.join("configs", "experiments", "*.yaml")))
        assert len(config_files) == 9, f"Expected 9 experiment configs, found {len(config_files)}: {config_files}"

        expected_robustness = {"exp01_cutpaste", "exp05_cutpaste_dwt"}
        for path in config_files:
            cfg = load_yaml(path)
            exp_id = cfg["experiment_id"]
            assert cfg["dataset"]["defect_free"] is True, f"{exp_id} must enforce defect_free=True"
            assert cfg["model"]["weights"] == "yolo11l-seg.pt", f"{exp_id} must use yolo11l-seg.pt"
            assert cfg["model"]["imgsz"] == 640, f"{exp_id} must use imgsz=640"

            train_pipe, eval_pipe = build_pipelines_from_config(cfg["data_engine"])
            assert len(train_pipe) >= 1, f"{exp_id} train_pipeline must include a spatial synthesizer"

            if cfg["data_engine"].get("frequency_filter") is not None:
                assert len(eval_pipe) == 1, f"{exp_id} eval_pipeline must apply T_freq identically"
            else:
                assert len(eval_pipe) == 0, f"{exp_id} eval_pipeline must be empty when frequency_filter is null"

            rob_flag = bool(cfg.get("evaluation", {}).get("robustness_benchmark", False))
            assert rob_flag == (exp_id in expected_robustness), f"Unexpected robustness_benchmark for {exp_id}"

    def test_exp08_material_adaptive_routing(self):
        from data_engine.base import MaterialAdaptiveRouter
        from experiments.run_experiment import build_pipelines_from_config, load_yaml

        cfg = load_yaml("configs/experiments/exp08_full_adaptive.yaml")
        train_pipe, eval_pipe = build_pipelines_from_config(cfg["data_engine"])

        assert len(train_pipe) == 2
        assert isinstance(train_pipe.processors[0], MaterialAdaptiveRouter)
        assert isinstance(train_pipe.processors[1], MaterialAdaptiveRouter)
        assert len(eval_pipe) == 1
        assert isinstance(eval_pipe.processors[0], MaterialAdaptiveRouter)

        # Verify both texture ('grid') and object ('bottle') samples pass cleanly through train & eval
        tex_img = np.random.randint(30, 220, (128, 128, 3), dtype=np.uint8)
        obj_img = np.random.randint(30, 220, (128, 128, 3), dtype=np.uint8)
        tex_sample = Sample(image=tex_img.copy(), category="grid", defect_type="good", is_anomaly=False)
        obj_sample = Sample(image=obj_img.copy(), category="bottle", defect_type="good", is_anomaly=False)

        out_train = train_pipe.run([tex_sample, obj_sample])
        assert len(out_train) == 2
        assert out_train[0].image.shape == (128, 128, 3)
        assert out_train[1].image.shape == (128, 128, 3)

        eval_tex = Sample(image=tex_img.copy(), category="grid", defect_type="good", is_anomaly=False)
        eval_obj = Sample(image=obj_img.copy(), category="bottle", defect_type="good", is_anomaly=False)
        out_eval = eval_pipe.run([eval_tex, eval_obj])
        assert len(out_eval) == 2
        assert not out_eval[0].is_anomaly
        assert not out_eval[1].is_anomaly

import os
import shutil
import tempfile
import pytest
import numpy as np
import cv2

from data_engine.sample import Sample
from data_engine.synthesizers.cutpaste_synthesizer import CutPasteSynthesizer
from data_engine.synthesizers.draem_synthesizer import DRAEMSynthesizer, rand_perlin_2d_np
from data_engine.synthesizers.nsa_synthesizer import NSASynthesizer
from data_engine.exporters.yolo_seg_exporter import YOLOSegExporter


@pytest.fixture
def clean_texture_sample():
    """Generates a clean texture-like sample (e.g. grid / carpet)."""
    h, w = 128, 128
    # Create periodic grid-like pattern
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[::8, :, :] = 200
    img[:, ::8, :] = 200
    img[img == 0] = 50
    return Sample(
        image=img,
        mask=None,
        category="grid",
        defect_type="good",
        is_anomaly=False,
    )


@pytest.fixture
def clean_object_sample():
    """Generates a clean object-like sample (e.g. screw / pill with dark background)."""
    h, w = 128, 128
    # Black background, central bright object
    img = np.zeros((h, w, 3), dtype=np.uint8)
    cv2.circle(img, (64, 64), 36, (180, 180, 190), -1)
    cv2.rectangle(img, (58, 20), (70, 108), (140, 140, 150), -1)
    return Sample(
        image=img,
        mask=None,
        category="screw",
        defect_type="good",
        is_anomaly=False,
    )


class TestCutPasteSynthesizer:
    def test_cutpaste_scar_synthesis(self, clean_texture_sample):
        synth = CutPasteSynthesizer(mode="scar", scar_width=(4, 8), scar_height=(15, 25), seed=42)
        out = synth(clean_texture_sample)

        # 1. Output shape must match
        assert out.shape == clean_texture_sample.shape
        assert out.mask is not None
        assert out.mask.shape == clean_texture_sample.shape[:2]

        # 2. Mask values must be strictly uint8 {0, 255}
        assert out.mask.dtype == np.uint8
        unique_vals = set(np.unique(out.mask))
        assert unique_vals.issubset({0, 255})
        assert 255 in unique_vals  # Anomaly must be present

        # 3. Anomaly flags
        assert out.is_anomaly is True
        assert out.has_mask() is True
        assert out.defect_type == "cutpaste_scar"

    def test_cutpaste_normal_synthesis(self, clean_texture_sample):
        synth = CutPasteSynthesizer(mode="normal", area_ratio=(0.04, 0.08), seed=42)
        out = synth(clean_texture_sample)

        assert out.shape == clean_texture_sample.shape
        assert out.mask.dtype == np.uint8
        unique_vals = set(np.unique(out.mask))
        assert unique_vals.issubset({0, 255})
        assert 255 in unique_vals
        assert out.is_anomaly is True
        assert out.defect_type == "cutpaste_normal"

    def test_cutpaste_anomaly_probability_zero(self, clean_texture_sample):
        # With prob=0.0, sample must remain defect-free
        synth = CutPasteSynthesizer(anomaly_prob=0.0, seed=42)
        out = synth(clean_texture_sample)
        assert out.is_anomaly is False
        assert out.has_mask() is False
        assert np.all(out.mask == 0)


class TestDRAEMSynthesizer:
    def test_rand_perlin_2d_np_raw(self):
        shape = (64, 64)
        res = (4, 4)
        noise = rand_perlin_2d_np(shape, res)
        assert noise.shape == shape
        assert isinstance(noise, np.ndarray)
        assert not np.isnan(noise).any()

    def test_draem_synthesis_self_texture(self, clean_texture_sample):
        synth = DRAEMSynthesizer(perlin_threshold=0.3, beta_range=(0.3, 0.7), seed=42)
        out = synth(clean_texture_sample)

        assert out.shape == clean_texture_sample.shape
        assert out.mask.dtype == np.uint8
        unique_vals = set(np.unique(out.mask))
        assert unique_vals.issubset({0, 255})
        assert 255 in unique_vals
        assert out.is_anomaly is True
        assert out.defect_type == "draem_perlin"

    def test_draem_non_power_of_two_dimensions(self):
        # Test real-world MVTec dimensions that are not multiples of 32
        non_divisible_shapes = [
            (900, 900),  # bottle
            (800, 800),  # pill
            (840, 840),  # tile
        ]
        synth = DRAEMSynthesizer(perlin_threshold=0.3, seed=42)
        for h, w in non_divisible_shapes:
            img = np.full((h, w, 3), 128, dtype=np.uint8)
            sample = Sample(image=img, category="test_cat")
            out = synth(sample)

            assert out.image.shape == (h, w, 3)
            assert out.mask.shape == (h, w)
            assert out.mask.dtype == np.uint8
            unique_vals = set(np.unique(out.mask))
            assert unique_vals.issubset({0, 255})
            assert out.is_anomaly is True


class TestNSASynthesizer:
    def test_nsa_foreground_segmentation(self, clean_object_sample):
        synth = NSASynthesizer(seed=42)
        fg_mask = synth._extract_foreground_mask(clean_object_sample.image, "screw")
        assert fg_mask.shape == clean_object_sample.shape[:2]
        # Central pixel must be foreground (1), corner pixel must be background (0)
        assert fg_mask[64, 64] == 1
        assert fg_mask[2, 2] == 0

    def test_nsa_synthesis_object(self, clean_object_sample):
        synth = NSASynthesizer(
            width_ratio_range=(0.08, 0.18),
            height_ratio_range=(0.08, 0.18),
            seed=42
        )
        out = synth(clean_object_sample)

        assert out.shape == clean_object_sample.shape
        assert out.mask.dtype == np.uint8
        unique_vals = set(np.unique(out.mask))
        assert unique_vals.issubset({0, 255})
        assert 255 in unique_vals
        assert out.is_anomaly is True
        assert out.defect_type == "nsa_poisson"

    def test_nsa_synthesis_texture(self, clean_texture_sample):
        synth = NSASynthesizer(
            width_ratio_range=(0.08, 0.18),
            height_ratio_range=(0.08, 0.18),
            seed=42
        )
        out = synth(clean_texture_sample)
        assert out.shape == clean_texture_sample.shape
        assert 255 in set(np.unique(out.mask))


class TestYOLOSegExporterWithSynthesizers:
    def test_synthesized_masks_export_valid_polygons(self, clean_object_sample, clean_texture_sample):
        """
        Verify end-to-end integration:
        Synthesized samples -> YOLOSegExporter -> Valid normalized polygons [0, 1].
        """
        synth_cutpaste = CutPasteSynthesizer(mode="scar", seed=10)
        synth_draem = DRAEMSynthesizer(seed=20)
        synth_nsa = NSASynthesizer(seed=30)

        samples = [
            synth_cutpaste(clean_object_sample),
            synth_draem(clean_texture_sample),
            synth_nsa(clean_object_sample),
        ]

        tmp_out = tempfile.mkdtemp()
        try:
            exporter = YOLOSegExporter(output_dir=tmp_out, save_debug_masks=True)
            stats = exporter.export(samples, split="train")

            assert stats["total_exported"] == 3
            assert stats["anomalies"] == 3
            assert stats["defect_free"] == 0

            # Verify exported label polygon text files
            label_dir = os.path.join(tmp_out, "labels", "train")
            label_files = os.listdir(label_dir)
            assert len(label_files) == 3

            for lf in label_files:
                file_path = os.path.join(label_dir, lf)
                assert os.path.getsize(file_path) > 0, f"Label file {lf} should not be empty."

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]

                assert len(lines) >= 1
                for line in lines:
                    tokens = line.split()
                    class_id = int(tokens[0])
                    coords = [float(x) for x in tokens[1:]]
                    # Must be at least 3 points (6 coordinates)
                    assert len(coords) >= 6
                    assert len(coords) % 2 == 0
                    for c in coords:
                        assert 0.0 <= c <= 1.0, f"Polygon coordinate {c} outside [0, 1] range!"
        finally:
            shutil.rmtree(tmp_out, ignore_errors=True)

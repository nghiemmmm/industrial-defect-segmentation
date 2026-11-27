# Changelog

All notable milestones for **Frequency-Spatial Anomaly Synthesis for False-Alarm-Suppressed Industrial Surface Defect Segmentation** (FJCAI submission).

## [Unreleased] — 2026-11-27

### Added
- `MaterialAdaptiveRouter` in `data_engine/base.py` to route periodic textures (`grid`, `carpet`, `tile`) to 2D-FFT Notch / DRAEM Perlin and homogeneous objects (`screw`, `pill`, `bottle`) to 2D-DWT Boost / NSA Poisson.
- `tools/benchmark_table1_roundtrip.py` and verified full-dataset identity roundtrip results across all **2,292 unique MVTec AD RGB images** (`results/verification/table1_roundtrip_full.json` & `.md`).
- `tools/notion_experiment_sync.py` for automated experiment lifecycle & metric synchronization with Notion (`paper` DB).
- GPU `cuFFT` / Haar 2D-DWT micro-benchmark cell and per-experiment Drive auto-sync/resume in `experiments/colab_runner.ipynb`.

### Changed
- Streamlined `configs/experiments/` from 12 legacy YAMLs to the exact **9 standardized defect-free configs (`EXP-00`–`EXP-08`)** on `YOLOv11l-seg@640` (`defect_free: true`, `epochs: 100`, `batch: 16`, `seed: 42`), with MVTec-AD-C `robustness_benchmark: true` on `EXP-01` and `EXP-05`.
- Updated `experiments/run_experiment.py` to support `material_adaptive` synthesizer & frequency filters, strict train/eval pipeline separation (`T_freq` applied identically to test images without synthesis), and `evaluation.robustness_benchmark` parsing.
- Upgraded all 6 experimental tables (**Table I–VI**) in `paper/sections/experiments.tex` to unified IEEE/Q1 formatting (`booktabs`, directional arrows, units in headers, math-bold bests, self-contained footnotes) and verified clean compilation (`0 errors, 0 Overfull \hbox`).

### Fixed
- Eliminated dataset double-counting (`2,676` -> `2,292` unique RGB images) in Table I roundtrip benchmark.
- Fixed missing synthesizers in `EXP-00`, `EXP-04`, `EXP-05` and mismatched synthesizers in `EXP-06`, `EXP-07` under strict defect-free training.
- Fixed `evaluation.robustness_benchmark` flag being ignored in `experiments/run_experiment.py`.

# Table I Full-Dataset Unfiltered Identity Roundtrip Verification

- **Timestamp:** 2026-11-27T16:28:57.836204
- **Total Unique RGB Images:** 2,292 (`1,570` train/good + `722` test = `553` defect + `169` test/good)
- **Ground-Truth Masks:** 553 (Total PNG files: `2,845`)

## Overall Summary (Table I)

| Transform | MAE (0-255) | Mean PSNR (dB) | Global PSNR (dB) | SSIM | Mean CPU Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **2D-FFT** | `0.3980` | `52.65` | `51.58` | `0.9968` | `1581.40` |
| **2D-DWT (Haar)** | `0.6187` | `49.71` | `49.59` | `0.9963` | `372.12` |

## Per-Category Breakdown

| Category | Train Good | Test Good | Test Defect | Unique RGB | FFT MAE | FFT PSNR (dB) | FFT SSIM | DWT MAE | DWT PSNR (dB) | DWT SSIM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `grid` | 264 | 21 | 57 | 342 | 0.1609 | 57.02 | 0.9991 | 0.4761 | 51.36 | 0.9982 |
| `carpet` | 280 | 28 | 89 | 397 | 0.5086 | 50.52 | 0.9988 | 0.6807 | 48.76 | 0.9986 |
| `tile` | 230 | 33 | 84 | 347 | 0.5299 | 50.22 | 0.9967 | 0.6784 | 48.76 | 0.9962 |
| `screw` | 320 | 41 | 119 | 480 | 0.2178 | 56.29 | 0.9980 | 0.5378 | 50.83 | 0.9968 |
| `pill` | 267 | 26 | 141 | 434 | 0.5531 | 50.08 | 0.9926 | 0.6252 | 49.38 | 0.9922 |
| `bottle` | 209 | 20 | 63 | 292 | 0.4338 | 51.14 | 0.9958 | 0.7538 | 48.83 | 0.9964 |

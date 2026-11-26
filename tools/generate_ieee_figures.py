"""
Generate publication-grade high-resolution IEEE figures from real MVTec AD images
using the project's data_engine modules (pure NumPy + OpenCV, crisp white header bars
with black text, zero toy images, zero neon overlays).
"""

import sys
import random
from pathlib import Path
from typing import List, Tuple, Optional
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data_engine.sample import Sample
from data_engine.synthesizers.cutpaste_synthesizer import CutPasteSynthesizer
from data_engine.synthesizers.draem_synthesizer import DRAEMSynthesizer
from data_engine.synthesizers.nsa_synthesizer import NSASynthesizer
from data_engine.frequency.fft_filter import FFTPeriodicSuppressionFilter
from data_engine.frequency.dwt_filter import DWTSubbandFilter
from data_engine.corruptions.corruptions_engine import apply_defocus_blur

OUT_DIR = ROOT / "paper" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def load_rgb(path: Path) -> np.ndarray:
    img = cv2.imread(str(path))
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def draw_polygon_overlay(img_rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    out = img_rgb.copy()
    binary = (mask > 0).astype(np.uint8)
    red_layer = out.copy()
    red_layer[binary > 0] = (
        0.62 * out[binary > 0].astype(np.float32) + 0.38 * np.array([230, 40, 40])
    ).astype(np.uint8)
    contours, _ = cv2.findContours(binary * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(red_layer, contours, -1, (255, 215, 0), thickness=max(3, img_rgb.shape[0] // 180))
    return red_layer


def _load_pil_font(size: int):
    for name in ["timesbd.ttf", "times.ttf", "arialbd.ttf", "arial.ttf", "C:/Windows/Fonts/timesbd.ttf", "C:/Windows/Fonts/arialbd.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def make_labeled_tile(img: np.ndarray, title: str, tile_size: int = 420, header_h: int = 52) -> np.ndarray:
    """Creates a crisp RGB tile with a white header bar and centered black IEEE title."""
    if img.ndim == 2:
        rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        rgb = img.copy()

    resized = cv2.resize(rgb, (tile_size, tile_size), interpolation=cv2.INTER_AREA)
    # Thin light-gray border around image for clean separation on white paper
    cv2.rectangle(resized, (0, 0), (tile_size - 1, tile_size - 1), (200, 200, 200), 1)

    header = np.full((header_h, tile_size, 3), 255, dtype=np.uint8)
    if HAS_PIL:
        pil_hdr = Image.fromarray(header)
        draw = ImageDraw.Draw(pil_hdr)
        font = _load_pil_font(26)
        bbox = draw.textbbox((0, 0), title, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = max(4, (tile_size - tw) // 2)
        ty = max(2, (header_h - th) // 2 - 2)
        draw.text((tx, ty), title, fill=(15, 15, 15), font=font)
        header = np.array(pil_hdr)
    else:
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.72
        thickness = 2
        (tw, th), _ = cv2.getTextSize(title, font, scale, thickness)
        tx = max(4, (tile_size - tw) // 2)
        ty = (header_h + th) // 2
        cv2.putText(header, title, (tx, ty), font, scale, (15, 15, 15), thickness, cv2.LINE_AA)

    return np.vstack([header, resized])


def assemble_grid(rows: List[List[Tuple[np.ndarray, str]]], tile_size: int = 420, gap: int = 16, header_h: int = 52) -> np.ndarray:
    rendered_rows = []
    for row in rows:
        tiles = [make_labeled_tile(img, title, tile_size=tile_size, header_h=header_h) for img, title in row]
        h = tiles[0].shape[0]
        sep = np.full((h, gap, 3), 255, dtype=np.uint8)
        row_parts = []
        for idx, t in enumerate(tiles):
            if idx > 0:
                row_parts.append(sep)
            row_parts.append(t)
        rendered_rows.append(np.hstack(row_parts))

    w = rendered_rows[0].shape[1]
    row_sep = np.full((gap + 8, w, 3), 255, dtype=np.uint8)
    all_parts = []
    for idx, r in enumerate(rendered_rows):
        if idx > 0:
            all_parts.append(row_sep)
        all_parts.append(r)
    canvas = np.vstack(all_parts)
    # Clean outer white margin
    pad = 10
    return cv2.copyMakeBorder(canvas, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(255, 255, 255))


def save_rgb(path: Path, rgb: np.ndarray):
    cv2.imwrite(str(path), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    print(f"Saved: {path} ({rgb.shape[1]}x{rgb.shape[0]})")


def generate_fig1_interdomain_pipeline():
    """2x5 IEEE figure showing real train/good nominal -> Spatial Synth -> Freq -> Mask -> Overlay."""
    grid_img = load_rgb(ROOT / "mvtec_ad/grid/train/good/000.png")
    bottle_img = load_rgb(ROOT / "mvtec_ad/bottle/train/good/000.png")

    # Row 1: Grid (Periodic Texture) -> CutPaste-Scar -> 2D-FFT Notch
    random.seed(42)
    np.random.seed(42)
    s_grid = Sample(image=grid_img.copy(), category="grid", defect_type="good", is_anomaly=False)
    cp_scar = CutPasteSynthesizer(mode="scar", scar_width=(14, 28), scar_height=(90, 180), seed=42)
    s_grid_syn = cp_scar(s_grid)
    fft_filter = FFTPeriodicSuppressionFilter(tau=3.5, dc_radius_ratio=0.04, notch_sigma=5.0, use_luminance=True)
    s_grid_freq = fft_filter(s_grid_syn)
    grid_overlay = draw_polygon_overlay(s_grid_freq.image, s_grid_syn.mask)

    # Row 2: Bottle (Rigid Object) -> DRAEM Perlin -> 2D-DWT Boost
    random.seed(15)
    np.random.seed(15)
    s_bottle = Sample(image=bottle_img.copy(), category="bottle", defect_type="good", is_anomaly=False)
    draem = DRAEMSynthesizer(seed=15)
    s_bottle_syn = draem(s_bottle)
    dwt_filter = DWTSubbandFilter(alpha=0.6, gamma=1.4, wavelet="haar", use_luminance=True)
    s_bottle_freq = dwt_filter(s_bottle_syn)
    bottle_overlay = draw_polygon_overlay(s_bottle_freq.image, s_bottle_syn.mask)

    rows = [
        [
            (grid_img, "(a) Nominal (grid)"),
            (s_grid_syn.image, "(b) CutPaste-Scar"),
            (s_grid_freq.image, "(c) 2D-FFT Notch"),
            (s_grid_syn.mask, "(d) Binary Mask"),
            (grid_overlay, "(e) Polygon Overlay"),
        ],
        [
            (bottle_img, "(f) Nominal (bottle)"),
            (s_bottle_syn.image, "(g) DRAEM Perlin"),
            (s_bottle_freq.image, "(h) 2D-DWT Boost"),
            (s_bottle_syn.mask, "(i) Binary Mask"),
            (bottle_overlay, "(j) Polygon Overlay"),
        ],
    ]
    canvas = assemble_grid(rows, tile_size=380, gap=14, header_h=48)
    save_rgb(OUT_DIR / "fig1_interdomain_pipeline.png", canvas)


def generate_fig2_spatial_synthesis_bottle():
    """1x4 IEEE figure on 100% nominal bottle/train/good showing CutPaste, DRAEM Perlin, NSA Poisson."""
    bottle_img = load_rgb(ROOT / "mvtec_ad/bottle/train/good/001.png")

    random.seed(12)
    np.random.seed(12)
    s_cp = CutPasteSynthesizer(mode="normal", area_ratio=(0.03, 0.08), seed=12)(
        Sample(image=bottle_img.copy(), category="bottle", defect_type="good", is_anomaly=False)
    )

    random.seed(15)
    np.random.seed(15)
    s_draem = DRAEMSynthesizer(seed=15)(
        Sample(image=bottle_img.copy(), category="bottle", defect_type="good", is_anomaly=False)
    )

    random.seed(21)
    np.random.seed(21)
    s_nsa = NSASynthesizer(width_ratio_range=(0.14, 0.24), height_ratio_range=(0.14, 0.24), seed=21)(
        Sample(image=bottle_img.copy(), category="bottle", defect_type="good", is_anomaly=False)
    )

    rows = [[
        (bottle_img, "(a) Nominal Input"),
        (draw_polygon_overlay(s_cp.image, s_cp.mask), "(b) CutPaste"),
        (draw_polygon_overlay(s_draem.image, s_draem.mask), "(c) DRAEM Perlin"),
        (draw_polygon_overlay(s_nsa.image, s_nsa.mask), "(d) NSA Poisson"),
    ]]
    canvas = assemble_grid(rows, tile_size=400, gap=14, header_h=50)
    save_rgb(OUT_DIR / "fig2_spatial_synthesis_bottle.png", canvas)


def generate_fig3_grid_fft_notch():
    """1x4 IEEE figure on real defective grid/test/bent with clean black headers."""
    bent_dir = ROOT / "mvtec_ad/grid/test/bent"
    grid_path = sorted(bent_dir.glob("*.png"))[0]
    grid_img = load_rgb(grid_path)

    fft_filter = FFTPeriodicSuppressionFilter(tau=3.5, dc_radius_ratio=0.04, notch_sigma=5.0, use_luminance=True)
    s_out = fft_filter(Sample(image=grid_img.copy(), category="grid", defect_type="bent", is_anomaly=True))
    filtered = s_out.image

    gray = cv2.cvtColor(grid_img, cv2.COLOR_RGB2GRAY).astype(np.float32)
    fshift = np.fft.fftshift(np.fft.fft2(gray))
    mag = np.log1p(np.abs(fshift))
    mag_norm = (255.0 * (mag - mag.min()) / (mag.max() - mag.min() + 1e-8)).astype(np.uint8)

    diff = np.abs(grid_img.astype(np.float32) - filtered.astype(np.float32)).mean(axis=2)
    diff_norm = np.clip(diff * 4.0, 0, 255).astype(np.uint8)

    rows = [[
        (grid_img, "(a) Original (grid)"),
        (mag_norm, "(b) 2D-FFT Spectrum"),
        (filtered, "(c) Notch Filtered"),
        (diff_norm, "(d) Suppressed Lattice"),
    ]]
    canvas = assemble_grid(rows, tile_size=400, gap=14, header_h=50)
    save_rgb(OUT_DIR / "fig3_grid_fft_notch.png", canvas)


def generate_fig4_bottle_defocus_progression():
    """1x4 IEEE figure showing Clean, Sev 1, Sev 3, Sev 5 defocus blur on bottle."""
    defect_dir = ROOT / "mvtec_ad/bottle/test/broken_large"
    bottle_path = sorted(defect_dir.glob("*.png"))[0]
    bottle_img = load_rgb(bottle_path)

    rows = [[
        (bottle_img, "(a) Clean"),
        (apply_defocus_blur(bottle_img, severity=1), "(b) Severity 1"),
        (apply_defocus_blur(bottle_img, severity=3), "(c) Severity 3"),
        (apply_defocus_blur(bottle_img, severity=5), "(d) Severity 5"),
    ]]
    canvas = assemble_grid(rows, tile_size=400, gap=14, header_h=50)
    save_rgb(OUT_DIR / "fig4_bottle_defocus_progression.png", canvas)


if __name__ == "__main__":
    generate_fig1_interdomain_pipeline()
    generate_fig2_spatial_synthesis_bottle()
    generate_fig3_grid_fft_notch()
    generate_fig4_bottle_defocus_progression()
    print("All 4 IEEE figures generated successfully.")

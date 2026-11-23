"""
Synthetic Anomaly Generation Module (Research Group A).
Includes CutPaste (Normal & Scar), DRAEM (Perlin noise + texture blending),
and NSA (Natural Synthetic Anomalies with Poisson seamless cloning).
"""

from data_engine.synthesizers.base_synthesizer import BaseSynthesizer
from data_engine.synthesizers.cutpaste_synthesizer import CutPasteSynthesizer
from data_engine.synthesizers.draem_synthesizer import DRAEMSynthesizer
from data_engine.synthesizers.nsa_synthesizer import NSASynthesizer

__all__ = [
    "BaseSynthesizer",
    "CutPasteSynthesizer",
    "DRAEMSynthesizer",
    "NSASynthesizer",
]

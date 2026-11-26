# SECTION AUDIT & VALIDATION CHECKLIST

## 1. Zero-Hallucination & Code Grounding Audit
- [ ] Every numerical metric matches `results/` or `report/` without discrepancies.
- [ ] Every algorithmic parameter matches default values in source code YAML configs.
- [ ] Image dimensions, dataset counts, and class names match physical workspace files.

---

## 2. IEEE Manuscript Formatting Audit
- [ ] Equation width strictly within column limits (no Overfull hbox).
- [ ] Table uses `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) without vertical bars.
- [ ] Citations correctly resolved with 0 undefined warnings.
- [ ] Captions placed above tables and below figures.

---

## 3. Logical Flow & Tone Audit
- [ ] Strict formal academic English (no informal slang or colloquialisms).
- [ ] Aligned 100% with `paper/Mision.md` without topic drift.
- [ ] Transition sentences between paragraphs are coherent and persuasive.

<div align="center">

# Customer Growth Experimentation

### A/B testing with SRM controls, confidence intervals, practical significance and guardrails.

**Pretoria BI — Data · Intelligence · Performance**

</div>

---

## Management question

> **Did the treatment create a statistically credible, practically meaningful improvement without damaging guardrails?**

**All data and entities are synthetic. No client result or realised ROI is claimed.**

---

## What this repository proves

- Sample-ratio mismatch control
- Two-proportion z test
- 95% confidence interval
- Minimum practical effect
- Guardrail acceptance rule

The objective is not to inflate a portfolio with screenshots. The repository has an executable happy path and deliberately corrupted states that must be rejected.

## Evidence chain

```text
SIGNAL → CONTRACT → VALIDATION → ANALYSIS → DECISION RULE → ACTION OWNER → FOLLOW-UP
```

## Run locally

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -q
python -m growth_experiments.cli smoke
python -m growth_experiments.cli reverse-test
```

## Repository map

```text
customer-growth-experimentation/
├── .github/workflows/ci.yml
├── config/
├── docs/
├── sql/
├── src/growth_experiments/
├── tests/
├── Dockerfile
├── Makefile
├── pyproject.toml
└── README.md
```

## Proof boundary

Implemented evidence is separated from future production claims. See `docs/proof_matrix.md` and `docs/limitations.md`. Thresholds in this synthetic case are examples to demonstrate governance and must be calibrated before real deployment.

---

<div align="center">

**Pretoria BI**  
**Understand · Decide · Act · Measure**

</div>

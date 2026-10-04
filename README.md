<div align="center">

# Customer Growth Experimentation

### SRM · Confidence Intervals · MDE · Power · Guardrails · Segment Safety

**Python · Statistical Testing · Experiment Governance · CI**

**Pretoria BI — Data · Intelligence · Performance**

</div>

---

## Decision question

> **Should a treatment be rolled out once statistical significance, practical value, guardrails and segment-level risk are considered together?**

This project treats experimentation as a decision system rather than a p-value calculator.

## Experimental governance

```text
HYPOTHESIS + MDE
       ↓
SAMPLE-SIZE PLANNING
       ↓
RANDOMISATION / SRM CHECK
       ↓
EFFECT + CONFIDENCE INTERVAL
       ↓
PRACTICAL-SIGNIFICANCE GATE
       ↓
BUSINESS GUARDRAIL
       ↓
SEGMENT SAFETY REVIEW
       ↓
SHIP / HOLD / REJECT / INCONCLUSIVE
```

Implemented controls:

- sample-ratio mismatch detection;
- two-proportion z-test;
- unpooled 95% confidence interval;
- minimum practical effect;
- business guardrail;
- sample-size planning from baseline rate + MDE;
- segment-level decision review;
- rollout block when a material segment is significantly harmed.

## Why segment review matters

The included synthetic scenario deliberately creates a strong positive SMB effect and a negative Enterprise effect. A global improvement is therefore not sufficient by itself: the segment gate must surface the harm before rollout.

## Decision report

```bash
python -m growth_experiments.cli report
```

Produces `output/experiment_decision_report.html`.

## Run locally

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -q
python -m growth_experiments.cli smoke
python -m growth_experiments.cli report
python -m growth_experiments.cli reverse-test
```

All observations are synthetic. Statistical thresholds and guardrails must be pre-specified for a real experiment and interpreted in the context of the business decision.

---

**Pretoria BI — Understand · Decide · Act · Measure**

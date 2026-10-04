# Validation Matrix

| Claim | Executable evidence | Failure path | Status |
|---|---|---|---|
| Arm counts are internally valid | `core.validate_arm` | conversions/guardrails outside visitors | implemented |
| Randomisation balance is checked | SRM chi-square rule | imbalanced sample sizes | implemented |
| Effect estimate has uncertainty | z-test + 95% CI | boundary tests | implemented |
| Practical significance is explicit | minimum-effect gate | configurable MDE threshold | implemented |
| Guardrail harm blocks rollout | guardrail acceptance rule | elevated treatment guardrail | implemented |
| Sample size can be planned before launch | `planning.sample_size_per_arm` | invalid baseline/MDE inputs | implemented |
| Segment harm can override a global positive result | `analyse_segments` | synthetic Enterprise regression | implemented |
| Decision report is generated from governed rules | `reporting.experiment_report_html` | report-content test | implemented |
| CI validates invalid and harmful scenarios | GitHub Actions + reverse-test CLI | invalid counts, SRM, segment harm | implemented |
| Real growth uplift | no production evidence | not applicable | not claimed |

## Review principle

Statistical significance alone is insufficient. A rollout decision also requires acceptable randomisation, practical effect, business guardrails and segment safety.

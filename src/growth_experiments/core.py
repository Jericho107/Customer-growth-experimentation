from __future__ import annotations

import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ExperimentArm:
    name: str
    visitors: int
    conversions: int
    guardrail_events: int


@dataclass(frozen=True)
class ExperimentResult:
    control_rate: float
    treatment_rate: float
    absolute_lift: float
    relative_lift: float
    z_score: float
    p_value: float
    ci_low: float
    ci_high: float
    sample_ratio_mismatch: bool
    guardrail_ok: bool
    practically_meaningful: bool
    decision: str


def validate_arm(arm: ExperimentArm) -> None:
    if arm.visitors <= 0:
        raise ValueError("visitors must be positive")
    if not 0 <= arm.conversions <= arm.visitors:
        raise ValueError("conversion count outside valid range")
    if not 0 <= arm.guardrail_events <= arm.visitors:
        raise ValueError("guardrail count outside valid range")


def analyse(
    control: ExperimentArm,
    treatment: ExperimentArm,
    min_effect: float = 0.005,
) -> ExperimentResult:
    validate_arm(control)
    validate_arm(treatment)
    if min_effect < 0:
        raise ValueError("minimum practical effect must be non-negative")

    total = control.visitors + treatment.visitors
    expected = total / 2
    chi2 = (
        (control.visitors - expected) ** 2
        + (treatment.visitors - expected) ** 2
    ) / expected
    srm = chi2 > 6.635

    control_rate = control.conversions / control.visitors
    treatment_rate = treatment.conversions / treatment.visitors
    diff = treatment_rate - control_rate
    pooled = (control.conversions + treatment.conversions) / total
    null_se = math.sqrt(
        pooled
        * (1 - pooled)
        * (1 / control.visitors + 1 / treatment.visitors)
    )
    z_score = diff / null_se if null_se else 0.0
    p_value = math.erfc(abs(z_score) / math.sqrt(2))

    ci_se = math.sqrt(
        control_rate * (1 - control_rate) / control.visitors
        + treatment_rate * (1 - treatment_rate) / treatment.visitors
    )
    ci_low = diff - 1.96 * ci_se
    ci_high = diff + 1.96 * ci_se

    control_guardrail = control.guardrail_events / control.visitors
    treatment_guardrail = treatment.guardrail_events / treatment.visitors
    guardrail_ok = treatment_guardrail <= control_guardrail + 0.003
    practical = diff >= min_effect

    if srm:
        decision = "invalid-srm"
    elif not guardrail_ok:
        decision = "reject-guardrail"
    elif p_value < 0.05 and ci_low > 0 and practical:
        decision = "ship"
    elif p_value < 0.05 and diff < 0:
        decision = "reject-negative"
    else:
        decision = "inconclusive"

    return ExperimentResult(
        control_rate,
        treatment_rate,
        diff,
        diff / control_rate if control_rate else 0.0,
        z_score,
        p_value,
        ci_low,
        ci_high,
        srm,
        guardrail_ok,
        practical,
        decision,
    )


def sample() -> tuple[ExperimentArm, ExperimentArm]:
    return (
        ExperimentArm("control", 12000, 1200, 180),
        ExperimentArm("treatment", 12100, 1355, 190),
    )


def serialise_sample() -> dict[str, object]:
    control, treatment = sample()
    return asdict(analyse(control, treatment))

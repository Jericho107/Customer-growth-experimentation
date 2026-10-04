from __future__ import annotations

import math
from statistics import NormalDist

from .core import ExperimentArm, analyse


def sample_size_per_arm(
    baseline_rate: float,
    minimum_detectable_effect: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> int:
    if not 0 < baseline_rate < 1:
        raise ValueError("baseline rate must be in (0, 1)")
    if minimum_detectable_effect <= 0:
        raise ValueError("minimum detectable effect must be positive")
    treatment_rate = baseline_rate + minimum_detectable_effect
    if treatment_rate >= 1:
        raise ValueError("baseline plus effect must be below 1")
    if not 0 < alpha < 1 or not 0 < power < 1:
        raise ValueError("alpha and power must be in (0, 1)")

    pooled = (baseline_rate + treatment_rate) / 2
    z_alpha = NormalDist().inv_cdf(1 - alpha / 2)
    z_power = NormalDist().inv_cdf(power)
    numerator = (
        z_alpha * math.sqrt(2 * pooled * (1 - pooled))
        + z_power
        * math.sqrt(
            baseline_rate * (1 - baseline_rate)
            + treatment_rate * (1 - treatment_rate)
        )
    ) ** 2
    return math.ceil(numerator / (minimum_detectable_effect**2))


def analyse_segments(
    segments: dict[str, tuple[ExperimentArm, ExperimentArm]],
    min_effect: float = 0.005,
) -> dict[str, object]:
    results = {name: analyse(control, treatment, min_effect) for name, (control, treatment) in segments.items()}
    invalid = sorted(name for name, result in results.items() if result.decision == "invalid-srm")
    harmful = sorted(
        name
        for name, result in results.items()
        if result.decision in {"reject-negative", "reject-guardrail"}
    )
    if invalid:
        decision = "invalid-segment-srm"
    elif harmful:
        decision = "hold-segment-harm"
    elif results and all(result.decision == "ship" for result in results.values()):
        decision = "ship-all-segments"
    else:
        decision = "inconclusive-segments"
    return {
        "decision": decision,
        "invalid_segments": invalid,
        "harmful_segments": harmful,
        "segments": {name: result.__dict__ for name, result in results.items()},
    }


def sample_segments() -> dict[str, tuple[ExperimentArm, ExperimentArm]]:
    return {
        "SMB": (
            ExperimentArm("control", 10000, 900, 120),
            ExperimentArm("treatment", 10000, 1100, 125),
        ),
        "Enterprise": (
            ExperimentArm("control", 5000, 700, 70),
            ExperimentArm("treatment", 5000, 620, 72),
        ),
    }

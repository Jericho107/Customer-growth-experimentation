from __future__ import annotations

import json
import sys

from .core import ExperimentArm, analyse, serialise_sample
from .planning import analyse_segments, sample_segments, sample_size_per_arm
from .reporting import write_experiment_report


def smoke() -> int:
    payload = serialise_sample()
    payload["planned_sample_per_arm_for_1pp_mde"] = sample_size_per_arm(payload["control_rate"], 0.01)
    payload["segment_analysis"] = analyse_segments(sample_segments())
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def report() -> int:
    path = write_experiment_report("output/experiment_decision_report.html")
    print(path.as_posix())
    return 0


def reverse_test() -> int:
    cases: list[dict[str, str]] = []

    try:
        analyse(ExperimentArm("c", 10, 11, 0), ExperimentArm("t", 10, 1, 0))
    except ValueError as exc:
        cases.append({"case": "invalid-counts", "status": "PASS", "error": str(exc)})
    else:
        cases.append({"case": "invalid-counts", "status": "FAIL", "error": "corruption accepted"})

    srm = analyse(
        ExperimentArm("c", 1000, 100, 10),
        ExperimentArm("t", 2000, 250, 15),
    )
    cases.append(
        {
            "case": "sample-ratio-mismatch",
            "status": "PASS" if srm.decision == "invalid-srm" else "FAIL",
            "error": "SRM blocked" if srm.decision == "invalid-srm" else "SRM accepted",
        }
    )

    segmented = analyse_segments(sample_segments())
    cases.append(
        {
            "case": "segment-harm-guard",
            "status": "PASS" if segmented["decision"] == "hold-segment-harm" else "FAIL",
            "error": (
                "harmful segment blocks rollout"
                if segmented["decision"] == "hold-segment-harm"
                else "segment harm ignored"
            ),
        }
    )

    print(json.dumps(cases, indent=2, sort_keys=True))
    return 0 if all(case["status"] == "PASS" for case in cases) else 1


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    if command == "smoke":
        return smoke()
    if command == "report":
        return report()
    if command == "reverse-test":
        return reverse_test()
    print("usage: python -m growth_experiments.cli [smoke|report|reverse-test]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

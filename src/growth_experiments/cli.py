from __future__ import annotations

import json
import sys

from .core import ExperimentArm, analyse, sample, serialise_sample


def smoke() -> int:
    print(json.dumps(serialise_sample(), indent=2, sort_keys=True))
    return 0


def reverse_test() -> int:
    cases: list[dict[str, str]] = []

    try:
        analyse(
            ExperimentArm("c", 10, 11, 0),
            ExperimentArm("t", 10, 1, 0),
        )
    except ValueError as exc:
        cases.append(
            {"case": "invalid-counts", "status": "PASS", "error": str(exc)}
        )
    else:
        cases.append(
            {"case": "invalid-counts", "status": "FAIL", "error": "corruption accepted"}
        )

    try:
        control, treatment = sample()
        analyse(control, treatment, -0.1)
    except ValueError as exc:
        cases.append(
            {"case": "invalid-min-effect", "status": "PASS", "error": str(exc)}
        )
    else:
        cases.append(
            {"case": "invalid-min-effect", "status": "FAIL", "error": "corruption accepted"}
        )

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

    print(json.dumps(cases, indent=2, sort_keys=True))
    return 0 if all(case["status"] == "PASS" for case in cases) else 1


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    if command == "smoke":
        return smoke()
    if command == "reverse-test":
        return reverse_test()
    print(
        "usage: python -m growth_experiments.cli [smoke|reverse-test]",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import sys

from .core import ExperimentArm, analyse, sample, serialise_sample


def smoke() -> int:
    print(json.dumps(serialise_sample(), indent=2, sort_keys=True))
    return 0


def reverse_test() -> int:
    cases = []
    try:
        analyse(ExperimentArm('c',10,11,0), ExperimentArm('t',10,1,0))
    except ValueError as exc:
        cases.append({"case": "invalid-counts", "status": "PASS", "error": str(exc)})
    else:
        cases.append({"case": "invalid-counts", "status": "FAIL", "error": "corruption accepted"})
    try:
        c,t=sample(); analyse(c,t,-0.1)
    except ValueError as exc:
        cases.append({"case": "invalid-min-effect", "status": "PASS", "error": str(exc)})
    else:
        cases.append({"case": "invalid-min-effect", "status": "FAIL", "error": "corruption accepted"})
    print(json.dumps(cases, indent=2, sort_keys=True))
    return 0 if all(case["status"] == "PASS" for case in cases) else 1


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    if command == "smoke":
        return smoke()
    if command == "reverse-test":
        return reverse_test()
    print("usage: python -m PACKAGE.cli [smoke|reverse-test]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

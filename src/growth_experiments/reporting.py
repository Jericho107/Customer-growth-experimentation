from __future__ import annotations

from html import escape
from pathlib import Path

from .core import analyse, sample
from .planning import analyse_segments, sample_segments, sample_size_per_arm


def experiment_report_html() -> str:
    control, treatment = sample()
    overall = analyse(control, treatment)
    segments = analyse_segments(sample_segments())
    required = sample_size_per_arm(overall.control_rate, 0.01)
    rows = "".join(
        "<tr>"
        f"<td>{escape(name)}</td>"
        f"<td>{result['control_rate']:.2%}</td>"
        f"<td>{result['treatment_rate']:.2%}</td>"
        f"<td>{result['absolute_lift']:.2%}</td>"
        f"<td>{escape(result['decision'])}</td>"
        "</tr>"
        for name, result in segments["segments"].items()
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Customer Growth Experimentation</title></head>
<body>
<h1>Customer Growth Experimentation</h1>
<p><strong>Overall decision:</strong> {escape(overall.decision)}</p>
<p><strong>Segment decision:</strong> {escape(str(segments['decision']))}</p>
<p><strong>Illustrative sample size / arm for +1pp MDE:</strong> {required}</p>
<h2>Segment review</h2>
<table><thead><tr><th>Segment</th><th>Control</th><th>Treatment</th><th>Lift</th><th>Decision</th></tr></thead><tbody>{rows}</tbody></table>
<p><small>
Synthetic experiment data. Decisions depend on the pre-specified statistical and
business rules in the repository.
</small></p>
</body></html>"""


def write_experiment_report(path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(experiment_report_html(), encoding="utf-8")
    return output

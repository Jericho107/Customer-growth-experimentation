import pytest

from growth_experiments.planning import analyse_segments, sample_segments, sample_size_per_arm


def test_sample_size_increases_for_smaller_effect():
    one_point = sample_size_per_arm(0.10, 0.01)
    half_point = sample_size_per_arm(0.10, 0.005)
    assert half_point > one_point > 0


def test_invalid_planning_inputs_fail():
    with pytest.raises(ValueError):
        sample_size_per_arm(1.0, 0.01)


def test_segment_harm_blocks_global_rollout():
    result = analyse_segments(sample_segments())
    assert result["decision"] == "hold-segment-harm"
    assert result["harmful_segments"] == ["Enterprise"]

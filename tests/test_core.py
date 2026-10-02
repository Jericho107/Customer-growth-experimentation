import pytest
from growth_experiments.core import ExperimentArm, analyse, sample

def test_sample_is_valid_and_positive():
    c,t = sample()
    result = analyse(c,t)
    assert result.absolute_lift > 0
    assert result.sample_ratio_mismatch is False
    assert result.guardrail_ok is True

def test_srm_is_detected():
    result = analyse(ExperimentArm("c",1000,100,10),ExperimentArm("t",2000,250,15))
    assert result.sample_ratio_mismatch is True
    assert result.decision == "invalid-srm"

def test_invalid_counts_fail():
    with pytest.raises(ValueError, match="conversion"):
        analyse(ExperimentArm("c",10,11,0),ExperimentArm("t",10,1,0))

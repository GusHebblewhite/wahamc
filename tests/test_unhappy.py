import pytest
from agents import DiceNotRolledError, RerollingARerollError, HitRoll

def test_error_not_rolled():
    hit_roll = HitRoll(succeed_on=3)
    #Get value of unrolled dice
    with pytest.raises(DiceNotRolledError):
        print(hit_roll.is_success())

    #Try to reroll unrolle dice
    with pytest.raises(DiceNotRolledError):
        print(hit_roll.reroll())

def test_reroll_a_reroll():
    hit_roll = HitRoll(succeed_on=3)
    hit_roll.roll()
    hit_roll.reroll()
    with pytest.raises(RerollingARerollError):
        hit_roll.reroll()
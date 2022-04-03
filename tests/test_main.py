import pytest
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from agents import DiceNotRolledError, NormalRoll, HitRoll, WoundRoll, SaveRoll
from agents import FeelNoPainRoll, DamageRoll

# ----------------------------------------------------------------------------
## Happy Path

def test_roll():
    hit_roll = HitRoll(succeed_on=3)
    # Roll
    hit_roll.roll()
    assert hit_roll.roll_value in range(1, 7)
    assert(hit_roll.reroll_value) == None
    # Reroll
    hit_roll.reroll()
    assert hit_roll.roll_value in range(1, 7)
    assert hit_roll.reroll_value in range(1, 7)
    # Is success
    assert hit_roll.is_success() in [True, False]

def test_roll_with_modifiers():
    hit_roll = HitRoll(succeed_on=4)
    hit_roll.roll()
    hit_roll.modifier = -100
    #Rolls cannot be modified below 1
    assert hit_roll.get_active_roll() == 1
    #Check successful hit
    hit_roll.modifier = 100
    assert hit_roll.is_success() == True
    #Check modifier cap
    hit_roll.modifier = -100
    hit_roll.modifier_cap = 1
    assert hit_roll.get_active_modifier() == -1

# ----------------------------------------------------------------------------
# Unhappy Path

def test_error_not_rolled():
    hit_roll = HitRoll(succeed_on=3)
    with pytest.raises(DiceNotRolledError):
        print(hit_roll.is_success())

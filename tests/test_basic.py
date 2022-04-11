import pytest
import numpy as np
import sys
import os
np.warnings.filterwarnings('error', category=np.VisibleDeprecationWarning)

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from agents import HitRoll, Attack

def test_roll():
    hit_roll = HitRoll(succeed_on=3)
    # Roll
    hit_roll.roll()
    assert hit_roll.roll_value.item() in range(1, 7)
    assert hit_roll.reroll_value.item() == None
    # Reroll
    hit_roll.reroll()
    assert hit_roll.roll_value.item() in range(1, 7)
    assert hit_roll.reroll_value.item() in range(1, 7)
    # # # Is success
    print(hit_roll.is_success())
    # assert hit_roll.is_success() in [True, False]

def test_roll_with_modifiers():
    hit_roll = HitRoll(succeed_on=4)
    hit_roll.roll()
    hit_roll.modifier = -100
    #Check modifier cap
    hit_roll.modifier = -100
    assert hit_roll.get_active_modifier() == -1
    #Now remove modifier cap
    hit_roll.modifier_cap = None
    #Rolls cannot be modified below 1
    hit_roll.modifier = -100
    assert hit_roll.get_active_roll() == 1
    #Check successful hit
    hit_roll.modifier = 100
    assert hit_roll.is_success() == True

def test_attack_hit(monkeypatch):

    monkeypatch.setattr(HitRoll, 'roll_dice', lambda _ : np.array(1)) # Always roll a 1 to hit
    hit_on = 3
    wound_on = 4
    armour_pen = 1
    attack = Attack(hit_on=hit_on, wound_on=wound_on, armour_pen=armour_pen, 
        damage=[1,1])

    attack.do_hit_roll()
    # Force reroll
    attack.hit_roll.reroll()
    assert attack.hit_roll.roll_value.item() == 1
    assert attack.hit_roll.reroll_value.item() == 1
    assert attack.hit_roll.is_success() == False



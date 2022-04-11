import pytest
import numpy as np
from agents import HitRoll, Attack
from rules import HitRule

def test_reroll_X_to_hit(monkeypatch):

    monkeypatch.setattr(HitRoll, 'roll_dice', lambda _ : np.array(1)) # Always roll a 1 to hit
    hit_on = 3
    wound_on = 4
    armour_pen = 1
    attack = Attack(hit_on=hit_on, wound_on=wound_on, armour_pen=armour_pen, 
        damage=[1,1])

    attack.hit_rules.append(HitRule.reroll_X_to_hit(1))
    attack.do_hit_roll()
    assert attack.hit_roll.roll_value.item() == 1
    assert attack.hit_roll.reroll_value.item() == 1
    assert attack.hit_roll.is_success() == False

def test_reroll_X_to_hit_2():
    hit_on = 3
    wound_on = 4
    armour_pen = 1
    attack = Attack(hit_on=hit_on, wound_on=wound_on, armour_pen=armour_pen, 
        damage=[1,1])

    attack.hit_rules.append(HitRule.reroll_X_to_hit([1,2,3,4,5,6]))
    attack.do_hit_roll()
    assert attack.hit_roll.reroll_value.item() is not None
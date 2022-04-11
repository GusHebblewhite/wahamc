from agents import Attack
from typing import Union
import numpy as np
from enum import IntEnum

# Priority levels
class Priority(IntEnum):
    '''
    An enum the manage function priority. Some rules (e.g. rerolls) need to be
    applied before other rolls (e.g. counting additional hits) and so rerolls
    should have a higher priority
    '''
    HIGH = 1
    NORMAL = 0
    LOW = -1

def make_list(x):
    '''
    Converts ints to lists but leaves other types (i.e. lists) alone
    '''
    if isinstance(x, int):
        return [x]
    return x

class Rule:

    def __init__(self, function, priority=Priority.NORMAL):
        """_summary_

        Args:
            rule_function (func): The function to be applied to the attack object
            priority (Priority): The priority (higher get called first)
        """
        self.function = function
        self.priority = priority


class HitRule:

    def reroll_X_to_hit(X:Union[int, list]):
        return Rule(lambda obj: HitRule._reroll_X_to_hit(obj, X), Priority.HIGH)

    def _reroll_X_to_hit(obj:Attack, X:Union[int, list]):
        X = make_list(X)
        obj.hit_roll.validate_roll()
        if obj.hit_roll.roll_value in X:
            obj.hit_roll.reroll()

    def X_to_hit_Y_additional_hits(obj:Attack, X:Union[int, list], 
            Y:Union[int, list]):
            obj.hit_roll.get_active_roll



    
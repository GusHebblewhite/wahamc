import numpy as np
from abc import ABC, abstractmethod

#AttRules, DefRules, WepRules
class DiceNotRolledError(Exception):
    pass

class RerollingARerollError(Exception):
    pass

class Roll(ABC):

    @abstractmethod
    def __init__(self, n_dice=1, n_faces=6):
        self.n_dice = n_dice
        self.n_faces = n_faces
        self.roll_value = np.array(None)
        self.reroll_value = np.array(None)
        self.modifier = 0
        self.modifier_cap = None

        #Set default success criteria
        self.success_criteria = lambda on, roll : roll.item() >= on

    def roll_dice(self):
        return np.random.randint(1, self.n_faces+1, self.n_dice)

    def roll(self):
        self.roll_value = self.roll_dice()

    def reroll(self):
        if self.roll_value.item() == None:
            raise DiceNotRolledError
        if self.reroll_value.item() != None:
            raise RerollingARerollError
        self.reroll_value = self.roll_dice()

    def get_active_roll(self):
        # TODO make this return an np array
        '''
        Obtain the reroll if the dice was rerolled. Otherwise obtain the
        (initial) roll value. Also apply modifiers.
        '''
        if not self.validate_roll():
            return np.array(None)
        return np.array(
            np.max([1, (self.reroll_value.item() or self.roll_value.item()) + 
            self.get_active_modifier()])
            )

    def validate_roll(self):
        '''
        Make sure that a roll has occurred
        '''
        if (self.roll_value.item() == None):
            raise DiceNotRolledError
        return True

class NormalRoll(Roll):

    def __init__(self, succeed_on):
        '''
        By default a normal roll will succeed on a roll of "succeed on" or 
        better
        '''
        super().__init__()
        self.succeed_on = succeed_on
        self.n_dice = 1

    def get_active_modifier(self):
        '''
        Gets the final roll modifier after applying the modifier caps
        '''
        if self.modifier_cap == None:
            return self.modifier
        else:
            return np.clip(self.modifier, a_min=-self.modifier_cap, 
                a_max=self.modifier_cap)

    def is_success(self):
        '''
        Check if the dice roll is successful. If there is a reroll value 
        use that, otherwise use the roll value
        '''
        # Compare roll to succeed_on
        return self.success_criteria(self.succeed_on, 
            self.get_active_roll())


class HitRoll(NormalRoll):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modifier_cap = 1

class WoundRoll(NormalRoll):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modifier_cap = 1

class SaveRoll(NormalRoll):
    pass


class FeelNoPainRoll(NormalRoll):
    pass

class DamageRoll(Roll):

    def __init__(self, n_dice, n_faces):
        super().__init__(n_dice=n_dice, n_faces=n_faces)

    def get_active_modifier(self):
        '''
        Gets the final roll modifier after applying the modifier caps
        '''
        return self.modifier

class Attack:
    '''
    The attack object manages the rolls and tracks different conditions that
    might cause interactions (e.g. a certain value to wound leads to a better
    ap value for that attack).
    '''

    def __init__(self, hit_on, wound_on, armour_pen, damage=[1,1]):

        # Basic rolls
        self.hit_roll = HitRoll(hit_on)
        self.wound_roll = WoundRoll(wound_on)
        self.damage_roll = DamageRoll(*damage)
        self.armour_penetration = armour_pen
        # Special rules
        self.hit_rules = []

        # Additional "attacks"
        self.additional_hit_rolls = 0
        self.additional_wound_rolls = 0
        self.mortal_wounds = 0

    def do_hit_roll(self):
        '''Perform a hit roll and apply any additional rules'''
        self.hit_roll.roll()
        for rule in sorted(self.hit_rules, key=lambda r: r.priority, reverse=True):
            rule.function(self)

    def do_wound_roll(self):
        pass

    def roll(self):
        '''Roll each dice in order'''
        self.do_hit_roll()
        self.do_wound_roll.roll()

class Attacker():

    def __init__(self, name="", weapons=[]):
        self.name = name
        self.weapons = weapons

class Defender():
    def __init__(self, mode, toughness, save, invuln, rules, name=""):
        self.mode = mode
        self.toughness = toughness
        self.save = save
        self.invuln = invuln
        self.rules = rules
        self.name = name

class Weapon():

    def __init__(self, n_attacks, hit_on, strength, armour_pen, name="", 
                rules=[]):
        self.name = name
        self.n_attacks = n_attacks
        self.hit_on = hit_on
        self.strength = strength
        self.armour_pen = armour_pen
        self.rules = rules

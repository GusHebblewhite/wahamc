from webbrowser import get
import numpy as np
from abc import ABC, abstractmethod

#AttRules, DefRules, WepRules
class DiceNotRolledError(Exception):
    pass

class Roll(ABC):

    @abstractmethod
    def __init__(self, n_dice=1, n_faces=6):
        self.n_dice = n_dice
        self.n_faces = n_faces
        self.roll_value = None
        self.reroll_value = None
        self.modifier = 0
        self.modifier_cap = None

        #Set default success criteria
        self.success_criteria = lambda on, roll : roll >= on

    def roll(self):
        self.roll_value = np.random.randint(1, self.n_faces+1, self.n_dice)

    def reroll(self):
        self.reroll_value = np.random.randint(1, self.n_faces+1, self.n_dice)

    def get_active_roll(self):
        '''
        Obtain the reroll if the dice was rerolled. Otherwise obtain the
        (initial) roll value. Also apply modifiers.
        '''
        if not self.validate_roll():
            return None
        return np.max([1, (self.reroll_value or self.roll_value) + 
            self.get_active_modifier()])

    def validate_roll(self):
        '''
        Make sure that a roll has occurred
        '''
        if (self.roll_value is None):
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

    def roll(self):
        '''
        We only roll one dice per normal roll
        '''
        super().roll()
        self.roll_value = self.roll_value[0]

    def reroll(self):
        '''
        We only roll one dice per normal roll
        '''
        super().reroll()
        self.reroll_value = self.reroll_value[0]

    def get_active_modifier(self):
        '''
        Gets the final roll modifier after applying the modifier caps
        '''
        if self.modifier_cap is None:
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
        return self.success_criteria(self.succeed_on, self.get_active_roll())


class HitRoll(NormalRoll):
    pass

class WoundRoll(NormalRoll):
    pass

class SaveRoll(NormalRoll):
    
    def __init__(self, save, invuln_save, armour_pen):
        self.save = save
        self.invuln_save = invuln_save
        self.armour_pen = armour_pen

    def is_success(self):
        '''
        For a save, success means rolling above whatever is the better save
        out of the modified save or the invuln
        '''
        return self.success_criteria(
            min(self.save + self.armour_pen, self.invuln_save),
            self.get_active_roll()
        )


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

    def __init__(self, hit_on, would_on, armour_pen, save, 
        invuln_save):

        self.hit_roll = HitRoll(hit_on)
        self.would_roll = WoundRoll(would_on)
        self.armour_penetration = armour_pen
        self.save_roll = SaveRoll(save=save, invuln_save=invuln_save, 
            armour_pen=armour_pen)


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

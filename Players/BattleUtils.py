from random import randint

class BattleUtils:
    def __init__(self):
        pass

    def calculateDamage(self, playerMon, oppMon, move):
        # returns the calculated damage when the playerMon uses the given move
        # on the opponent mon

        ## addcording to GEN1 & ignoring critical hits & damage multiplier
        critical = 1
        t1 = (((((2 * playerMon.level * critical) / 5) + 2) * move.base_power * (playerMon.base_stats['atk'] / oppMon.base_stats['def'])) / 50) + 2
        stab = 1
        if((move.type == playerMon.type_1) or (move.type == playerMon.type_1)):
            stab = 1.5
        type_1 = 1
        type_2 = 1
        rand = randint(217, 255)

        return t1 * stab * type_1 * type_2 * rand

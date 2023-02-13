from random import randint

class BattleUtils:
    def __init__(self):
        pass

    def calculateDamage(self, playerMon, oppMon, move):
        # returns the calculated damage when the playerMon uses the given move
        # on the opponent mon

        # grab the poke-env pokemon objects
        player_mon = playerMon.pokemon_obj
        opp_mon = oppMon.pokemon_obj
    
        ## according to GEN5 & ignoring critical hits & status effects
        if(move.category == 1): # Then physical 
            attk = player_mon.base_stats['atk']
            defense = opp_mon.base_stats['def']
        elif(move.category == 2): # Then Special
            attk = player_mon.base_stats['spa']
            defense = opp_mon.base_stats['spd']
        else:
            attk = 0
            defense = 1

        targets = 1 # 0.75 if more than one target
        pb = 1 ## 0.25 if second strike of parental bond
        weather = 1 ## based on current weather condition of the battle
        gr = 1 ## glaive rush
        critical = 1
        rand = randint(217, 255)
        ## calculate stab
        if((move.type == playerMon.type_1) or (move.type == playerMon.type_1)):
            stab = 1.5
        
        # Type multiplier
        type_multiplier = opp_mon.damage_multiplier(move)

        burn = 1 ## if burn is active

        other = 1 ## multiplier for held items, special scenarios


        t1 = (((((2 * playerMon.level * critical) / 5) + 2) * move.base_power * (attk / defense)) / 50) + 2
        stab = 1

        return t1 * targets * pb * weather * gr * critical * rand  * stab * type_multiplier * burn * other

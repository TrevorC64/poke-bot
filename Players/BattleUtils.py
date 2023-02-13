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

        critical = 1 ## For GEN5 crits deal x2 dmg
        crit_ratio = move.crit_ratio
        
        match crit_ratio:
            case 0:
                crit_chance = 6.25
            case 1:
                crit_chance = 6.25
            case 2:
                crit_chance = 12.5
            case 3:
                crit_chance = 25
            case 4:
                crit_chance = 33.3
            case 5:
                crit_chance = 50
            case 6:
                crit_chance = 100
                critial = 2
        
        crit_rand = randint(0,100)
        if(crit_rand >= crit_chance):
            critial = 2

        rand = randint(217, 255)
        stab = 1
        ## calculate stab
        if((move.type == playerMon.type_1) or (move.type == playerMon.type_2)):
            stab = 1.5
        
        # Type multiplier
        type_multiplier = opp_mon.damage_multiplier(move)

        burn = 1 ## if burn is active

        other = 1 ## multiplier for held items, special scenarios


        t1 = (((((2 * playerMon.level * critical) / 5) + 2) * move.base_power * (attk / defense)) / 50) + 2


        return t1 * targets * pb * weather * gr * critical * rand  * stab * type_multiplier * burn * other

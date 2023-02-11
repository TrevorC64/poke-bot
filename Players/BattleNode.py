from BattleUtils import BattleUtils

class PokemonSim:
    def __init__(self, pokemon_obj):
        ## Basic variables needed only, so we can manipluate as we simulate
        self.current_hp = pokemon_obj.current_hp
        self.base_stats = pokemon_obj.base_stats
        self.fainted = pokemon_obj.fainted
        self.level = pokemon_obj.level
        self.moves = pokemon_obj.moves
        self.type_1 = pokemon_obj.type_1
    
    def takeDamage(self, dmg):
        ## add handling for fainting
        self.current_hp -= dmg
    
class BattleTree:
    def __init__(self, activePokemon=None,
                       team =[],
                       opponent_active_pokemon=None,
                       opponent_team=[],
                       last_move=None):
        self.active_pokemon = activePokemon
        self.team = team
        self.opponent_active_pokemon = opponent_active_pokemon
        self.opponent_team = opponent_team
        self.last_move = last_move
        self.subnodes = []

    def populateFromBattleState(self, battleState):
        self.active_pokemon = PokemonSim(battleState.active_pokemon)
        for key in battleState.team:
            self.team.append(PokemonSim(battleState.team[key]))
        self.opponent_active_pokemon = PokemonSim(battleState.opponent_active_pokemon)
        for key in battleState.opponent_team:
            self.opponent_team.append(PokemonSim(battleState.opponent_team[key]))

    def staticEval(self):
        player_total_hp = self.active_pokemon.current_hp
        for mon in self.team:
            player_total_hp += 0 if (mon.current_hp == None) else mon.current_hp

        opp_total_hp = self.opponent_active_pokemon.current_hp
        for mon in self.opponent_team:
            opp_total_hp += 0 if (mon.current_hp == None) else mon.current_hp
        
        return player_total_hp - opp_total_hp
    
    ## generate subnodes
    def generate(self, depth, playerTurn):
        if depth != 0:
            if playerTurn:
                for move_key in self.active_pokemon.moves:
                    move = self.active_pokemon.moves.get(move_key)
                    ## we need to simulate the move from self.activePokemon -> opponent_active_pokemon
                    damage = BattleUtils().calculateDamage(self.active_pokemon, self.opponent_active_pokemon, move)
                    if (damage >= self.opponent_active_pokemon.current_hp):
                        ## then we do the "damage" and KO and switch opp mon
                        bt = BattleTree(activePokemon=self.active_pokemon,
                                        team=self.team,
                                        opponent_active_pokemon=self.opponent_team[0],
                                        opponent_team=self.opponent_team[1:], ## NEED TO ADJUST FOR FAINTED MON
                                        last_move=move)
                    else:
                        ## then we do the "damage" and no switch
                        self.opponent_active_pokemon.takeDamage(damage)
                        bt = BattleTree(activePokemon=self.active_pokemon,
                                        team=self.team,
                                        opponent_active_pokemon=self.opponent_active_pokemon,
                                        opponent_team=self.opponent_team,
                                        last_move=move)
                        
                    bt.generate(depth-1, False)
                    self.subnodes.append(bt)

            if not playerTurn:
                for move_key in self.opponent_active_pokemon.moves:
                    move = self.opponent_active_pokemon.moves.get(move_key)
                    ## we need to simulate the move from opponent_active_pokemon -> self.activePokemon 
                    damage = BattleUtils().calculateDamage(self.opponent_active_pokemon, self.active_pokemon, move)
                    if (damage >= self.active_pokemon.current_hp):
                        ## then we do the "damage" and KO and switch opp mon
                        bt = BattleTree(activePokemon=self.team[0],
                                        team=self.team[1:],  ## NEED TO ADJUST FOR FAINTED MON
                                        opponent_active_pokemon=self.opponent_active_pokemon,
                                        opponent_team=self.opponent_team,
                                        last_move=move)
                    else:
                        ## then we do the "damage" and no switch
                        self.active_pokemon.takeDamage(damage)
                        bt = BattleTree(activePokemon=self.active_pokemon,
                                        team=self.team,
                                        opponent_active_pokemon=self.opponent_active_pokemon,
                                        opponent_team=self.opponent_team,
                                        last_move=move)

                    bt.generate(depth-1, True)
                    self.subnodes.append(bt)
                



        



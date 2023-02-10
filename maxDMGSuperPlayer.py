import time
import asyncio

from poke_env.player import Player, RandomPlayer

## Player object that always chooses a super effective move, if none exist choose max damage move

class MaxDamageSEPlayer(Player):
    def choose_move(self, battle):
        # Battle describes the current battle state, has attributes like: active_pokemon, available_moves, available_switches, opponent_active_pokemon, opponent_team and team
        opponent_active_mon = battle.opponent_active_pokemon
        
        # if the player can attack, it will
        if battle.available_moves: 
            best_move = None
            super_effective_moves = []
            # look at each move that is available
            for move in battle.available_moves:
                # if the move is super effective against the current mon
                if(opponent_active_mon.damage_multiplier(move) > 1.0):
                    # add to our list of super effective moves 
                    super_effective_moves + [move]
                # if no best_move has been set, or the current move is more powerful, make the move our best_move
                if((best_move == None) or (move.base_power > best_move.base_power)):
                    best_move = move             
            # if there are some moves that are super effective
            if len(super_effective_moves) != 0:
                # choose the one that has the highest base power
                best_move = max(super_effective_moves, key=lambda move: move.base_power)
            
            return self.create_order(best_move)
        # otherwise make a random swtich
        else:
            return self.choose_random_move(battle)
        

async def main():
    start = time.time()

    # Create two players
    random_player = RandomPlayer(
        battle_format = "gen8randombattle",
    )

    max_damage_player = MaxDamageSEPlayer(
        battle_format="gen8randombattle",
    )

    # Now let the two players battle 100 times
    await max_damage_player.battle_against(random_player, n_battles=100)

    print(
        "Max Damage Super Effective player won %d / 100 battles [this took %f seconds]"
        % (
            max_damage_player.n_won_battles, time.time() - start
        )
    )

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())



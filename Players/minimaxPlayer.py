import time
import asyncio
from poke_env.player import Player, RandomPlayer
from BattleNode import BattleTree 

## Player object that utilizes a minimax algorithm to attack

class MinimaxPlayer(Player):
    DEPTH = 3
    
    def choose_move(self, battle):
        bt = BattleTree()
        bt.populateFromBattleState(battle)
        bt.generate(4, True)
        print("begin minimax")
        if battle.available_moves: 
            # Finds move from avaliable moves with highest base power
            best_eval, best_move = self.minimax(bt, True)

            # check if best_move is in available_moves
            if(best_move in battle.available_moves):
                return self.create_order(best_move)
        
        # if no attack can be made, make a random switch
        return self.choose_random_move(battle)


    #standard minimax algorithm to be used in choose_move
    def minimax(self, node, maximizingPlayer):
        if(node.subnodes == []):
            return node.staticEval(), node.last_move
        
        if(maximizingPlayer):
            maxEval = float('-inf')
            maxMove = None
            for child in node.subnodes:
                currEval, currMove = self.minimax(child, False)
                if (currEval >= maxEval):
                    maxEval = currEval
                    maxMove = currMove
            return maxEval, maxMove
        
        if(not maximizingPlayer):
            minEval = float('inf')
            minMove = None
            for child in node.subnodes:
                currEval, currMove = self.minimax(child, True)
                if (currEval <= minEval):
                    minEval = currEval
                    minMove = currMove
            return minEval, minMove


async def main():
    start = time.time()

    random_player = RandomPlayer(
        battle_format = "gen8randombattle"
    )

    minimax_player = MinimaxPlayer(
        battle_format = "gen8randombattle"
    )

    await minimax_player.battle_against(random_player, n_battles=100)

    print(
        "Minimax player won %d / 100 battles [this took %f seconds]"
        % (
            minimax_player.n_won_battles, time.time() - start
        )
    )


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
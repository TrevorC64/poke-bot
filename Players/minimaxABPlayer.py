import time
import asyncio
from poke_env.player import Player, RandomPlayer
from BattleNode import BattleTree 

## Player object that utilizes a minimax algorithm + alpha beta pruning to attack

class MinimaxABPlayer(Player):
    DEPTH = 3
    
    def choose_move(self, battle):
        bt = BattleTree()
        bt.populateFromBattleState(battle)
        bt.generate(4, True)
        
        if battle.available_moves: 
            # Finds move from avaliable moves with highest base power
            _, best_move = self.minimax(bt, float('-inf'), float('inf'), True)

            # check if best_move is in available_moves
            if(best_move in battle.available_moves):
                return self.create_order(best_move)
        
        # if no attack can be made, make a random switch
        return self.choose_random_move(battle)


    #standard minimax algorithm to be used in choose_move
    def minimax(self, node, alpha, beta, maximizingPlayer):
        if(node.subnodes == []):
            return node.staticEval(), node.last_move
        
        if(maximizingPlayer):
            maxEval = float('-inf')
            maxMove = None
            for child in node.subnodes:
                currEval, currMove = self.minimax(child, alpha, beta, False)
                if (currEval >= maxEval):
                    maxEval = currEval
                    maxMove = currMove
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break
            return maxEval, maxMove
        
        if(not maximizingPlayer):
            minEval = float('inf')
            minMove = None
            for child in node.subnodes:
                currEval, currMove = self.minimax(child, alpha, beta, True)
                if (currEval <= minEval):
                    minEval = currEval
                    minMove = currMove
                beta = min(beta, minEval)
                if beta <= alpha:
                    break
            return minEval, minMove


async def main():
    start = time.time()

    random_player = RandomPlayer(
        battle_format = "gen8randombattle"
    )

    minimax_ab_player = MinimaxABPlayer(
        battle_format = "gen8randombattle"
    )

    await minimax_ab_player.battle_against(random_player, n_battles=100)

    print(
        "Minimax Alpha-Beta player won %d / 100 battles [this took %f seconds]"
        % (
            minimax_ab_player.n_won_battles, time.time() - start
        )
    )


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
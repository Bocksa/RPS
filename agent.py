import torch
import time
from game import RPSGame_AI
from collections import deque
import numpy as np
import random
from model import Linear_QNet, QTrainer
from helper import plot
from helper import bar

MAX_MEMORY = 100_000
BATCH_SIZE = 3
LR = 0.001

START_TIME = time.time()

class Agent:

    def __init__(self):
        self.n_games = 0 # Number of games
        self.epsilon = 0 # Randomness
        self.gamma = 0.9 # Discount rate 0 < x < 1
        self.memory = deque(maxlen = MAX_MEMORY) # popleft()
        self.model = Linear_QNet(2, 256, 3).cuda()
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game=RPSGame_AI):
        state = [
            game.AILastMove,
            game.PlayerLastMove
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # if it exceeds MAX_MEMORY it pops the left entry

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = 0
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0,2)
            final_move = move
        else:
            state0 = torch.tensor(state, dtype=torch.float).cuda()
            prediction = self.model(state0)

            move = torch.argmax(prediction).item()
            final_move = move

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    plot_win_percentage = []
    plot_mean_win_percentage = []
    total_score = 0
    total_win_percentage = 0
    record = 0
    agent = Agent()
    game = RPSGame_AI()
    print("Choose a strategy 1-4: ")
    game.strategy = int(input())
    
    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        win_percentage = 0

        if game.AI_Wins < 1:
            win_percentage = 0
        else:
            win_percentage = (game.AI_Wins / (game.AI_Wins + game.Player_Wins)) * 100

        if done:
            # train long memory
            if (game.AI_Wins == 0 and game.Player_Wins == 0):
                print(f"Agent Wins: {game.AI_Wins} | Player Wins: {game.Player_Wins} | Ties: {game.Ties} | Win Percentage: Mysterious fucking edge case where it managed to tie {game.Tie_Condition} games in a row with no wins. | Player Strategy: {game.strategy}")
            else:
                print(f"Agent Wins: {game.AI_Wins} | Player Wins: {game.Player_Wins} | Ties: {game.Ties} | Win Percentage: {(game.AI_Wins / (game.AI_Wins + game.Player_Wins)) * 100} | Player Strategy: {game.strategy} | Moves: {game.played_moves}")
            bar(game.played_moves, START_TIME)
            game.reset()
            agent.n_games = agent.n_games + 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print(f"Match: {agent.n_games} Score: {score} Record: {record}")

            plot_scores.append(round(score, 2))
            plot_win_percentage.append(round(win_percentage, 2))
            total_score = total_score + score
            total_win_percentage = total_win_percentage + win_percentage
            mean_score = total_score / agent.n_games
            mean_win_percentage = total_win_percentage / agent.n_games
            plot_mean_scores.append(mean_score)
            plot_mean_win_percentage.append(mean_win_percentage)

            plot(plot_win_percentage, plot_mean_win_percentage, START_TIME)
            
if __name__ == '__main__':
    train()
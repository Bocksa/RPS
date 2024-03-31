# Reset

from enum import Enum

class RPSGame_AI:
    PlayerLastMove = 0
    AILastMove = 0

    AI_Wins = 0
    Player_Wins = 0
    Ties = 0
    Rounds = 0
    Win_Condition = 4

    moves = ["rock", "paper", "scissors"]

    Score = 0

    def __init__(self):
        self.PlayerLastMove = 0
        self.AILastMove = 0
    
    def play_step(self, action):
        return self._play_round(self._getPlayerMove(strategy=1), action)

    def _play_round(self, player_action, ai_action):
        self.Rounds = self.Rounds + 1
        self.AILastMove = ai_action
        self.PlayerLastMove = player_action

        if (self.moves[ai_action] == "rock" and self.moves[player_action] == "scissors") or (self.moves[ai_action] == "paper" and self.moves[player_action] == "rock") or (self.moves[ai_action] == "scissors" and self.moves[player_action] == "paper"):
            self.AI_Wins = self.AI_Wins + 1
            self.Score = self.Score + 1
            return 1, (self.AI_Wins == self.Win_Condition or self.Player_Wins == self.Win_Condition), self.Score # AI Wins
        elif (self.moves[ai_action] == "rock" and self.moves[player_action] == "paper") or (self.moves[ai_action] == "paper" and self.moves[player_action] == "scissors") or (self.moves[ai_action] == "scissors" and self.moves[player_action] == "rock"):
            self.Player_Wins = self.Player_Wins + 1
            self.Score = self.Score - 1
            return -1, (self.AI_Wins == self.Win_Condition or self.Player_Wins == self.Win_Condition), self.Score # Player Wins
        else:
            self.Ties = self.Ties + 1
            return 0, (self.AI_Wins == self.Win_Condition or self.Player_Wins == self.Win_Condition), self.Score # Tie
        
    def _getPlayerMove(self, strategy):

        if strategy == 1:
            if self.Rounds == 0:
                return 2
            
            if self.AILastMove == 0:
                return 2
            elif self.AILastMove == 1:
                return 0
            elif self.AILastMove == 2:
                return 1
        
    def reset(self):
        self.PlayerLastMove = 0
        self.AILastMove = 0
        self.AI_Wins = 0
        self.Player_Wins = 0
        self.Rounds = 0

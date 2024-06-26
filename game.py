import random

class RPSGame_AI:
    PlayerLastMove = 3
    AILastMove = 3

    AI_Wins = 0
    Player_Wins = 0
    Ties = 0
    Rounds = 0
    Win_Condition = 250
    Tie_Condition = 50_000

    LastWinner = None

    strategy = 2

    moves = ["rock", "paper", "scissors"]

    played_moves = dict(rock = 0, paper = 0, scissors = 0)

    move_probabilities = dict(rock = 0.5, paper = 0.3, scissors = 0.2)

    Score = 0

    def __init__(self):
        self.PlayerLastMove = 0
        self.AILastMove = 0
        self.LastWinner = None

    def _checkScoreValidity(self):
        return self.Score
    
    def play_step(self, action):
        return self._play_round(self._getPlayerMove(strategy=self.strategy), action)

    def _play_round(self, player_action, ai_action):
        self.Rounds = self.Rounds + 1
        self.AILastMove = ai_action
        self.PlayerLastMove = player_action

        reward = 0

        if self.AILastMove == ai_action:
            reward = reward - 0

        self.played_moves[self.moves[ai_action]] += 1

        if (self.moves[ai_action] == "rock" and self.moves[player_action] == "scissors") or (self.moves[ai_action] == "paper" and self.moves[player_action] == "rock") or (self.moves[ai_action] == "scissors" and self.moves[player_action] == "paper"):
            self.AI_Wins = self.AI_Wins + 1
            reward = reward + 1
            self.Score = self.Score + reward
            self.LastWinner = "AI"
            return reward, (self.AI_Wins == self.Win_Condition or self.Player_Wins == self.Win_Condition or self.Ties > self.Tie_Condition), self.Score # AI Wins
        elif (self.moves[ai_action] == "rock" and self.moves[player_action] == "paper") or (self.moves[ai_action] == "paper" and self.moves[player_action] == "scissors") or (self.moves[ai_action] == "scissors" and self.moves[player_action] == "rock"):
            self.Player_Wins = self.Player_Wins + 1
            reward = reward - 1
            self.Score = self.Score + reward
            self.LastWinner = "Player"
            return reward, (self.AI_Wins == self.Win_Condition or self.Player_Wins == self.Win_Condition or self.Ties > self.Tie_Condition), self.Score # Player Wins
        else:
            self.Ties = self.Ties + 1
            self.LastWinner = "Tie"
            self.Score = self.Score + reward
            return reward, (self.AI_Wins == self.Win_Condition or self.Player_Wins == self.Win_Condition or self.Ties > self.Tie_Condition), self.Score # Tie
        
    def _getPlayerMove(self, strategy):
        self.strategy = strategy
        if self.strategy == 1:
            if self.LastWinner == None:
                return 2
            
            if self.AILastMove == 0:
                return 2
            elif self.AILastMove == 1:
                return 0
            elif self.AILastMove == 2:
                return 1
            
        if strategy == 2:
            if self.LastWinner == None:
                return 0
            if self.AILastMove == 0:
                return 1
            elif self.AILastMove == 1:
                return 2
            elif self.AILastMove == 2:
                return 0
            
        if strategy == 3:
            if self.LastWinner == None:
                return 0
            else:
                return self.AILastMove
            
        if strategy == 4:
            if self.LastWinner == None:
                return random.choice([0,2])
            elif self.LastWinner == "AI":
                match self.AILastMove:
                    case 0:
                        return 1
                    case 1:
                        return 2
                    case 2:
                        return 0
            elif self.LastWinner == "Player":
                return self.PlayerLastMove
            else:
                match self.AILastMove:
                    case 0:
                        return 1
                    case 1:
                        return 2
                    case 2:
                        return 0

        

        
    def reset(self):
        self.PlayerLastMove = 3
        self.AILastMove = 3
        #self.strategy = 2 #random.randint(1,4)

        self.AI_Wins = 0
        self.Player_Wins = 0
        self.Ties = 0
        self.Rounds = 0

        self.LastWinner = None
        self.played_moves = dict(rock = 0, paper = 0, scissors = 0)
        self.move_probabilities = dict(rock = 0.5, paper = 0.3, scissors = 0.2)


import random

class RPSGame_AI:
    PlayerLastMove = 0
    AILastMove = 0

    AI_Wins = 0
    Player_Wins = 0
    Ties = 0
    Rounds = 0
    Win_Condition = 250
    Tie_Condition = 50_000

    LastWinner = None

    moves = ["rock", "paper", "scissors"]

    Score = 0

    def __init__(self):
        self.PlayerLastMove = None
        self.AILastMove = None
        self.strategy = 4 #random.randint(1,4)
    
    def play_step(self, action):
        return self._play_round(self._getPlayerMove(strategy=self.strategy), action)

    def _play_round(self, player_action, ai_action):
        self.Rounds = self.Rounds + 1
        self.AILastMove = ai_action
        self.PlayerLastMove = player_action

        if (self.moves[ai_action] == "rock" and self.moves[player_action] == "scissors") or (self.moves[ai_action] == "paper" and self.moves[player_action] == "rock") or (self.moves[ai_action] == "scissors" and self.moves[player_action] == "paper"):
            self.AI_Wins = self.AI_Wins + 1
            self.Score = self.Score + 1
            self.LastWinner = "AI"
            return 1, (self.AI_Wins == self.Win_Condition or self.Player_Wins == self.Win_Condition or self.Ties > self.Tie_Condition), self.Score # AI Wins
        elif (self.moves[ai_action] == "rock" and self.moves[player_action] == "paper") or (self.moves[ai_action] == "paper" and self.moves[player_action] == "scissors") or (self.moves[ai_action] == "scissors" and self.moves[player_action] == "rock"):
            self.Player_Wins = self.Player_Wins + 1
            self.Score = self.Score - 1
            self.LastWinner = "Player"
            return -0.95, (self.AI_Wins == self.Win_Condition or self.Player_Wins == self.Win_Condition or self.Ties > self.Tie_Condition), self.Score # Player Wins
        else:
            self.Ties = self.Ties + 1
            self.LastWinner = None
            return -0.05, (self.AI_Wins == self.Win_Condition or self.Player_Wins == self.Win_Condition or self.Ties > self.Tie_Condition), self.Score # Tie
        
    def _getPlayerMove(self, strategy):
        self.strategy = strategy

        if strategy == 1:
            if self.AILastMove == None:
                return 2
            
            if self.AILastMove == 0:
                return 2
            elif self.AILastMove == 1:
                return 0
            elif self.AILastMove == 2:
                return 1
            
        if strategy == 2:
            if self.AILastMove == None:
                return 0
            if self.AILastMove == 0:
                return 1
            elif self.AILastMove == 1:
                return 2
            elif self.AILastMove == 2:
                return 0
            
        if strategy == 3:
            if self.AILastMove == None:
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
        

        
    def reset(self):
        self.PlayerLastMove = None
        self.AILastMove = None
        self.strategy = 4 #random.randint(1,4)

        self.AI_Wins = 0
        self.Player_Wins = 0
        self.Ties = 0
        self.Rounds = 0

        self.LastWinner = None


# coding: utf-8

# 7 x 6 board
# 0-41 list

# Goal: use neural networks and monte carlo tree search to train a connect four AI from scratch
# 
# Actors: Each actor should be its own class that will recieve board data and then submit an action
# Neural
# Human
# Random
# Search
# 
# The Game class will control the board state, update and save it, as well as saving the move made, and the win condition
# 
# 

# rough percentages for random play:
# tie: 0.15%  player1: 55.567%  player2: 44.283%

# In[101]:


import numpy as np
from connect4_win_cond import win_cond
win_cond = np.array(win_cond)[::-1]


# In[129]:


class Game():
    def __init__(self, board = np.zeros((7,6), dtype=int), winner = None): 
        # board is sideways so that begining of each array is the bottom
        self.board = np.array(board)
        #need to save moves and board states for latter AI training        
        self.states = []
        self.actions = []
        self.winner = winner
        
    def update(self, action, player_id, retries = 0, saving = True):
        if retries == 0 and saving: self.save_board()
        if self.place(action, player_id) == "full": return "full" # checks to see if column is filled
        if saving: self.save_action(action)
        if self.end(player_id): return self.winner
       
    def place(self, action, player_id):
        if 0 not in self.board[action]: return "full"
        for i in range(6): 
            if self.board[action][i] == 0:
                self.board[action][i] = player_id
                return

    def end(self, player_id): 
        if 0 not in self.board:
            self.winner = 0
            return True
        temp = self.board.transpose().flatten()
        for win_con in win_cond: 
            if set(temp[win_con]) == {player_id}: # for enhancing speed
                self.winner = player_id
                return True
            
    def save_board(self):
        # all board states will be put in to the list; states
        self.states.append(np.array(self.board))
        
    def save_action(self, action): # all odd elements in the list belong to player 1, all even elements belong to player 2
        # all actions will be put in to the list; actions
        self.actions.append(action)


# In[128]:


class Gameroom():
    # Where multiple games are played. Where everything is brought together
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score = {0:0 , 1:0 , 2:0}  
        self.data_store = {"winners": [], "actions": [], "states": []}
        
    def match(self, board = np.zeros(1), saving = True, seeing = False): # structure for a single match
        game = Game()
        if board.shape == (7,6): game.board = board
        previous_action = 0
        for count, player in enumerate([self.player1, self.player2] * 22):
            if seeing: self.show(game)      
            retries = 0
            player_id = count % 2 + 1  # even --> player 1
            while True:
                action = player.choice(game.board, retries = retries, player_id = player_id,
                                      counter = count // 2, away = previous_action)
                update_note = game.update(action, retries = retries, player_id = player_id, 
                                          saving = saving) #full column?
                if update_note == "full":
                    retries += 1
                elif isinstance(update_note, int):
                    if seeing: self.show(game)  
                    return game
                if not update_note:
                    previous_action = action
                    break
                        
    def tournament(self, rounds, reset_data = True, seeing = False): # structure for series of matches
        self.reset(reset_score = True, reset_data = reset_data)
        for i in range(rounds):
            results = self.match(seeing = seeing)
            self.data_store["states"].append(results.states)
            self.data_store["actions"].append(results.actions)
            self.data_store["winners"].append(results.winner)
            self.win_counter(results.winner)
        if seeing: self.show_score()
            
    def win_counter(self, winner):
        self.score[winner] += 1
        
    def show_score(self):
        print("tie: {0}   player1 wins: {1}   player2 wins: {2}".format(self.score[0], self.score[1], self.score[2]))
        
    def reset(self, reset_score = True, reset_data = False):
        if reset_score: self.score = {0:0 , 1:0 , 2:0}
        if reset_data:
            self.data_store = {"winners": [], "actions": [], "states": []}
            
    def show(self, game, symbols = ["X","O","-"," "]):
        interface = np.array(game.board.transpose()[::-1])
        print("1 2 3 4 5 6 7")
        for row in interface:
            row = list(row)
            for i,e in enumerate(row):
                if e == 1:
                    row[i] = symbols[0]                    
                if e == 2:
                    row[i] = symbols[1]
                if e == 0:
                    row[i] = symbols[2]
            print(symbols[3].join(row))
        print("..............\n")


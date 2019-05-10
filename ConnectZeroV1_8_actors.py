
# coding: utf-8

# This Code establishes five different players as well as their dependencies
# 1. Human
# 2. Random
# 3. Dolphin - Random unless sees oppertunity to win immidiately
# 4. Search - uses MCTS or MCTS + Neural
# 5. Neural
# 
# 
# TensorFlow Backend

# In[230]:


import pprint as pp
from keras.layers import *
from keras.models import Sequential , Model, Input
import numpy as np
from connect4_win_cond import win_cond
win_cond = np.array(win_cond)[::-1]
from ConnectZeroV1_8_game import *


# In[189]:


class Random():
    def __init__(*args, **kwargs):
        pass
    
    def choice(self, *args, **kwargs):
        action = np.random.randint(0,7)
        return action


# In[190]:


class Human():
    def choice(self, *args, **kwargs):
        action = int(input("pick column 1-7:  " )) - 1
        return action


# In[14]:


## general functions list

def preprocess_data(data_store):
    # victory history of players
    inputs1, targets1 = sifting_winners(data_store, winning_player = 1, turn_of_winner = 0) 
    inputs2, targets2 = sifting_winners(data_store, winning_player = 2, turn_of_winner = 1) 
    return inputs1, targets1, inputs2, targets2

def sifting_winners(data_store, winning_player, turn_of_winner):
    inputs, targets = [], []
    for index, winner_value in enumerate(data_store["winners"]):
        if winner_value == winning_player:
            for state in data_store["states"][index][turn_of_winner::2]:
                inputs.append(onehot_encoder(state, winning_player))
            for move in data_store["actions"][index][turn_of_winner::2]:
                targets.append(np.array([move])) #policy, value                
    return np.array(inputs), np.array(targets)

def onehot_encoder(board, player_id, a = 1, b = 2, ):
    flat_board = board.transpose().flatten()
    whos_playing = np.array([player_id for i in range(7)])
    flat_board = np.append(flat_board, whos_playing)
    ind1, ind2 = np.where(flat_board==a)[0], np.where(flat_board==b)[0]
    onehot_board = np.zeros((len(flat_board),2), dtype=int)
    onehot_board[ind1] = [1,0]
    onehot_board[ind2] = [0,1]
    return onehot_board.reshape(7,7,2)
    
def train(model, data_store, epochs = 1, verbose = 0):
    inputs1, targets1, inputs2, targets2 = preprocess_data(data_store)
    if len(targets1) > 0 and len(targets2) > 0:
        targets = np.concatenate((targets2, targets1))
        inputs = np.concatenate((inputs2, inputs1))
    elif len(targets1) > 0:
        targets = targets1
        inputs = inputs1 
    elif len(targets2) > 0:
        targets = targets2
        inputs = inputs2
    print(targets.shape)
    if len(targets) > 0: model.fit(inputs, targets, epochs = epochs, verbose = verbose)
        
def swap_board(board, a = 1, b = 2, c = 3):
    board = np.array(board)
    board[board == a] = c
    board[board == b] = a
    board[board == c] = b
    return board

def place_general(action, player_id, board):
    board = np.array(board)
    if 0 not in board[action]: return "full"
    for i in range(6): 
        if board[action][i] == 0:
            board[action][i] = player_id
            return board


# In[76]:


class Branch():
    def __init__(self, branch_id, player_id, board, q = 0, n = 0, policy_weight = 0, initial = False):
        self.branch_id = branch_id
        self.player_id = player_id
        if initial: self.board = np.array(board)
        else: self.board = place_general(branch_id, player_id, board)
        self.q = q
        self.n = n
        self.p = policy_weight
        self.children = {}
        self.end = False
        
    def child(self, branch_id):
        if branch_id not in self.children:
            new_player_id = int(not(self.player_id - 1)) + 1
            self.children[branch_id] = Branch(branch_id, new_player_id, self.board, 0, 0)
        return self.children[branch_id]
        
    def stats(self):
        return (self.n, self.q, self.p, self.branch_id)


# In[72]:


class MCTS():
    def __init__(self, player_id, board, rollout_player = Random(), neuralnet = None, parent = None, 
                 search_length = 1000, width = 7):
        self.width = width
        self.search_length = search_length
        self.rollout_player = rollout_player
        self.neuralnet = neuralnet
        if parent == None: self.parent = Branch(branch_id = -1, player_id = player_id, board = board, initial = True)
        else: self.parent = parent

    def uct(self, v_i, v, c = 1.2):
        # Q(v_i)/N(v_i) + c * sqrt(log(N(v))/N(v_i))
        return v_i.q/(v_i.n) + np.sqrt(np.log(v.n)/(v_i.n)) + v_i.p * c

    def best_uct(self, node):
        # only node.childs with boards can be counted. full childs also have n == 0
        orig = [-100, 0]
        for i in range(self.width):
            if type(node.child(i).board) != str:
                chal = [self.uct(node.child(i), node), i]
                if chal[0] > orig[0]:
                    orig = chal
        return node.child(orig[1]) 

    def unpicked(self, node):
        k = np.arange(self.width)
        np.random.shuffle(k)
        for i in k:
            if node.child(i).n == 0 and type(node.child(i).board) != str:
                return node.child(i)

    def fully_expanded(self, node):
        return all([node.child(i).n != 0 or type(node.child(i).board) == str for i in range(self.width)]) 
    
    def update_policy(self, node): # we look at the board from the perspective of the player who has not yet gone
        #node.board has already been played by node.player, her opponent must now look at the board
        distribution = self.neuralnet.choice(node.board, player_id = node.child(0).player_id, return_all = True)
        for i in range(self.width):
            node.child(i).p += distribution[i]                    

    def selection(self, node):
        if self.fully_expanded(node):
            if node.child(0).p == 0 and self.neuralnet:
                self.update_policy(node)
            return self.best_uct(node) # apply uct to each child node and choose the highest value child
        else:
            return self.unpicked(node) # choose unpicked child node

    def network(self):
        for i in range(self.search_length):
            history = []
            again = True
            node = self.parent
            while again:
                node = self.selection(node)
                history.append(node.branch_id) # produces list of children path
                a_game = Game(node.board)
                if a_game.end(node.player_id):
                    reward = self.end_reward(node, a_game)
                    self.back_propogate(history, reward, node.player_id)
                    again = False
                elif node.n == 0:
                    self.simulate(node, history)
                    again = False
        return self.parent
    
    
    def end_reward(self, node, temp_game):
        if temp_game.winner == node.player_id: return 1
        elif temp_game.winner == 0: return 0
        else: 
            print(temp_game.winner, -1)
            return -1  # don't think this is possible, because for an inspected node that just moved 
                        # it can only win or tie on its turn

            
    def simulate(self, node, history):
        reward = self.run_simulation(node)
        self.back_propogate(history, reward, node.player_id)

    def back_propogate(self, history, reward, final_node_id):
        node = self.parent
        node.n += 1
        for i in history: # evaluates children path, last value is value of simulated node
            node = node.child(i)
            node.n += 1
            if node.player_id == final_node_id: #parent.player_id is opponent
                node.q += reward
            else: 
                node.q -= reward
                
    # when accessing the node board it assumes the player has already played
    # first player should take on position as second player so that they don't play immidiately
    # second player must wait so they can remain as second player
    # thus desired return  for node.player is always for the 2nd player to win
    def run_simulation(self, node): 
        if node.player_id == 1: 
            board = swap_board(node.board) # player1 is now in position of second player
        else: board = np.array(node.board) # player2 already must wait their turn
        simulator = Gameroom(self.rollout_player, self.rollout_player)
        result = simulator.match(board, saving = False)

        if result.winner == 2:
            return 1
        elif result.winner == 1:
            return -1
        else:
            return 0
            
    def evaluate(self):
        result = self.network()
        return np.argmax([result.child(i).n for i in range(self.width)])


# In[75]:


class Search(): 
    def __init__(self, neuralnet = None, search_length = 50, rollout_player = Random()):
        self.search_length = search_length
        self.rollout_player = rollout_player
        self.neuralnet = neuralnet
        
    def choice(self, board, retries, player_id, counter = 0, away = 0):
        # parent id is id of opponent, Search plays using id of first children it wants the first children to be successful
        # int(not...) flips id 1 <--> 2
        if counter: 
            self.parent = self.parent.child(self.home).child(away)
        else:
            self.parent = None
        mcts = MCTS(player_id = int(not(player_id - 1)) + 1, board = board, neuralnet = self.neuralnet,
                      search_length = self.search_length, rollout_player = self.rollout_player, parent = self.parent)
        if counter == 0: self.parent = mcts.parent
        action = mcts.evaluate()
        self.home = action
        return action
    
    def guess_value(self, board, player_id):
        # parent id is id of opponent, MCTS plays using id of first children it wants the first children to be successful
        # int(not...) flips id 1 <--> 2
        mcts = MCTS(player_id = int(not(player_id - 1)) + 1, board = board, neuralnet = self.neuralnet,
                      search_length = self.search_length, rollout_player = self.rollout_player)
        mcts.evaluate()
        total_q = sum([mcts.parent.child(i).q for i in range(7)]) 
        total_n = sum([mcts.parent.child(i).n for i in range(7)])
        return total_q/total_n


# In[74]:


class Neural():
    def __init__(self, model = None, random_scale = 0.5):
        if model == None:
            self.model = self.setup_model()
        else: self.model = model
        self.random_scale = random_scale
        
    def choice(self, board, player_id, retries = 0, return_all = False, *args, **kwargs):
        onehot_board = onehot_encoder(board, player_id)
        prediction_dist = self.model.predict(onehot_board.reshape(1,7,7,2))[0] # [0] bcuz shape (1,7) --> (7)  
        random_dist = np.random.dirichlet(np.ones(7),size=1)[0]  # [0] bcuz shape (1,7) --> (7)
        if retries == 0: choice_dist = prediction_dist + random_dist * self.random_scale
        else: choice_dist = prediction_dist + random_dist * retries # thus always added by a random dist of 1
        if return_all: return choice_dist
        
        choices = choice_dist.argsort()[::-1] # best move to worst move
        action = choices[0]
        return action
    
    
    def setup_model(self, drop = 0.7):
        main_input = Input(shape=(7,7,2), name = "main_input") # change to shape = (49,2) later
        temp = Conv2D(filters = 2**8, kernel_size= (1,4), data_format="channels_last")(main_input)
        temp = Dropout(drop)(temp)
        temp = Conv2D(filters = 2**7, kernel_size= (3,1), data_format="channels_last")(temp)
        temp = Dropout(drop)(temp)
        temp = Conv2D(filters = 2**7, kernel_size= (2,1), data_format="channels_last")(temp)
        temp = Dropout(drop)(temp)
        temp = Conv2D(filters = 2**7, kernel_size= (2,3), data_format="channels_last")(temp)
        temp = Flatten()(temp)
        temp = BatchNormalization()(temp)
        
        out = Dense(216, activation='elu', name = "out_dense1")(temp)
        out = BatchNormalization()(out)
        out = Dense(56, activation='elu', name = "out_dense2")(out)
        out = BatchNormalization()(out)
        out = Dense(7, activation='softmax', name = "policy")(out)
        
        model = Model(inputs=main_input, outputs=out)
        model.compile(optimizer = "adam", loss='sparse_categorical_crossentropy')
        return model


# In[188]:


class Dolphin():
    def __init__(*args, **kwargs):
        pass
    
    def choice(self, board, *args, **kwargs):
        # finds 3 of the same value and an open space then places in the open space either securing a win or preventing a loss
        temp = board.transpose().flatten()
        oppertunity_index = np.array([0,2,3])
        for i in np.arange(69): 
            if (temp[win_cond[i]]).astype(bool).sum() == 3:
                check_oppertunity = np.concatenate(np.unique(temp[win_cond[i]], return_counts= True))
                if len(check_oppertunity) == 4 and (check_oppertunity[oppertunity_index ] == [0,1,3]).all():
                    for index, value in enumerate(win_cond[i]):
                        if temp[value] == 0 and (value - 7 < 0 or temp[value-7] != 0):
                            action = value % 7
                            return action
            
        action = np.random.randint(0,7)
        return action    


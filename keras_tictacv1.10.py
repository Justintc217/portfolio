
# coding: utf-8

# In[1]:


from tictac_extra import *


# In[2]:


from keras.layers import Dense, Flatten , Conv1D
from keras.models import Input, Model

from tcn import TCN


# In[3]:


class Neural():
    def __init__(self , models):
        self.models = models

    def cho(self , board , edit_choice = 0 , who = 0):
        board = list(board)
        board = np.array(board_mod(board))
        board = np.array([board[j] for j in win_cond])
        model = self.models
        #print(np.shape(board))
        pred = model.predict(np.array([board]))
        choices = pred[0].argsort()[::-1]  #highest to lowest
        #print(choices)
        pos = choices[edit_choice]
        return pos


# In[4]:


def setup_model():
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(12, activation=tf.nn.relu),
      tf.keras.layers.Dense(12, activation=tf.nn.relu),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(9, activation=tf.nn.softmax)
    ])

    model.compile(optimizer='adam', lr = 0.001,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


# In[5]:


def setup_cnn():   
    model = tf.keras.models.Sequential([
      tf.keras.layers.Conv2D(10 , (3,2) , activation = "relu" , input_shape = (8 , 3 , 2) , strides = (3,2)),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Flatten(),  
      tf.keras.layers.Dense(12, activation=tf.nn.relu),
      tf.keras.layers.Dropout(0.2),  
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(9, activation=tf.nn.softmax)
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


# In[6]:


def match(rounds, actor_list , model_list = [None,None], show = False , see_score = True):
    reset_score(score)
    for r in range(rounds):
        board = reset()
        winner = play(board , actor_list , show)
        loser = switch(winner , 1 ,2)
        update_score(winner)
        if winner == 0:
            update_neural(1 , 2 , model_list[0]) # player 1 and model 0 corrects
            update_neural(2 , 1 , model_list[1]) # player 2 and model 1 corrects (tie is good for p2)
        #update_byneural(winner)
        else:
            update_neural(winner , 1 , model_list[winner - 1]) #-1 track index if winner is 2 then model is 1;second in the list
            update_neural(loser , 2 , model_list[loser - 1])
        if show:
            festive(winner)
    if see_score == True:
        show_score(score)
    
def play(board, actor_list , show = False):
    for t in who_play:
        if action(board , actor_list[t - 1] , t , show):
            return t
    return 0

def action(board, actor , who , show = False):
    board , pos , run = place(board , actor , who)
    save(board , pos , run) # remember this is post move board make sure to redact the change from the post move board
    if show:
        show_board(board)
    return end(board , win_cond)
    
def place(board , actor , who , edit_choice = 0):
    while True:
        pos = actor(board , edit_choice , who)
        if board[pos] == 0:
            if edit_choice < 8:
                run = actor(board , edit_choice + 1 , who)
            else:
                run = np.random.randint(9)
            board[pos] = who
            return board , pos , run
        else:
            edit_choice += 1
            
def save(board , pos , run):
    global data
    board = list(board)
    board[pos] = 0
    board_mod(board)
    data.append([board , pos , run])
    
def reset():  # to update every round or not to update every round that is the question
    global data
    data = []
    return [0] * 9

def update_score(winner):
    global score
    score[winner] += 1
    
def update_neural(winner ,reward , model = None): #regular = 1 is actual moves, regular = 2 is runner up moves
    if model != None:
        actor = winner -1
        global data
        global pos_mat
        win_data = np.array(data[actor::2])   #winner is 1st or 2nd player subtract by 1 to get states and actions of player
        
        board_data = np.array([win_data.item(x,0) for x in range(len(win_data))])
        sym_board_data = np.array([board_sym(boards) for boards in board_data])
        sym_board_data = np.concatenate(sym_board_data , axis = 0)
        # bringing from 4D (whole list, sets of symmetries , board , one hots) to 3D without sets of symmetries
        
        move_data = np.array([win_data.item(x,reward) for x in range(len(win_data))])
        sym_move_data = np.array([pos_mat[moves] for moves in move_data])
        sym_move_data = np.concatenate(sym_move_data , axis = 0)
        sym_board_data = np.array([[i[j] for j in win_cond] for i in sym_board_data])
        model.fit(sym_board_data , sym_move_data , epochs = 1 , verbose = 0)


# In[7]:


def strat(board , edit_choice , who):
    board = list(board)
    other = switch(who , 1 , 2)
    first =  testplace(board , who , init = True) 
    if isinstance(first, int):
        return first
    pos_list = {first[0][x]:0 for x in range(len(first[0]))}
    for pos,board in zip(pos_list , first[1]):
        recu(pos , board , who , other , pos_list)
    
    max_value = max(pos_list.values())
    max_keys = [k for k, v in pos_list.items() if v == max_value]
    return max_keys[0]
    

def recu(pos , b , who , other ,  pos_list , recursion = 0, params = (5 , 1)):
    second = testplace(b , other)
    if isinstance(second, int):
        pos_list[pos] = pos_list[pos] - 1 * params[0] ** (-1* params[1] * turn(b))
    else:
        for j in second:
            third = testplace(j , who) 
            if isinstance(third, int):
                pos_list[pos] = pos_list[pos] + 1 * params[0] ** (-1* params[1] * turn(j))
            elif turn(j) < 8 and recursion < 2:
                recursion += 1
                for k in third:
                    recu(pos , k , who , other , pos_list)


# In[55]:


modelx , modelo = setup_model() , setup_model()


# In[56]:


models = [modelx , modelo]
nu1 = Neural(modelx)
nu2 = Neural(modelo)


# In[59]:


#match(10000 , [ra , ra] , [modelx , modelo])
#match(100 , [strat , ra] , [modelx , N])
#match(100 , [ra , strat] , [N , modelo])

for i in range(10):
    match(100 , [nu1.cho , ra] ,  [modelx , N] , show = F)
    match(100 , [ra , nu2.cho] , [N , modelo])
    match(10 , [nu1.cho, nu2.cho] , [modelx , modelo])
    print("-------------------------------")


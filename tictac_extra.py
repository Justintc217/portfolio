import numpy as np
import tensorflow as tf

win_cond = [[0, 1, 2],
 [3, 4, 5],
 [6, 7, 8],
 [0, 3, 6],
 [1, 4, 7],
 [2, 5, 8],
 [0, 4, 8],
 [2, 4, 6]]

who_play = [1, 2, 1, 2, 1, 2, 1, 2, 1]

data = []

score = {0: 0, 1: 0, 2: 0}

F = False
T = True
N = None

def show_score(score):
    print("tie: {0} || p1win: {1} || p2win: {2}".format(score[0] , score[1] , score[2]))
    
def show_board(board):
    board = list(board)
    for i,x in enumerate(board):
        if x == 0:
            board[i] = "□"
        if x == 1:
            board[i] = "X"
        if x == 2:
            board[i] = "O"
    for i in [0,3,6]:
        print(board[i] + board[i+1] + board[i+2])
    print("____")
    print("")
    
def festive(winner):
    corr = {0: "Nobody" , 1: "X" , 2: "O"}
    print("{0} wins!".format(corr[winner]))
    print("=============================")
    print("")
    
def board_mod(board):
    for i,x in enumerate(board):
        if x == 0:
            board[i] = [0,0]
        if x == 1:
            board[i] = [1,0]
        if x == 2:
            board[i] = [0,1]
    return board

def data_to_board(temp_data):   #inverse board_mod
    ndata = np.array(temp_data)
    for boardplus in ndata:
        for board in boardplus:
            if type(board) == list:
                for mark in range(len(board)):
                    if board[mark] == [0,0]:
                        board[mark] = 0
                    elif board[mark] == [1,0]:
                        board[mark] = 1
                    elif board[mark] == [0,1]:
                        board[mark] = 2
                print(board[0:3])
                print(board[3:6])
                print(board[6:9])
                print("-------------------")
            else:
                print(board)
                print("-------------------")
    
def rboard():
    return list(np.random.randint(0,3,9))

def turn(board):
    return sum([1 for x in board if x > 0])

def board_sym(board): # CC rotation
    board = list(board)
    I = np.array(board)
    D1 = Trans(board)
    H = Hflip(board)
    R1 = Hflip(D1)
    V = Trans(R1)
    R3 = Trans(H)
    D2 = Hflip(R3)
    R2 = Hflip(V)
    return [I , R1 , R2 , R3 , H , V , D1 , D2]

def Trans(board): #ttansposes , assumes onehot fotm
    t = list(board)
    t = np.reshape(t , (3,3,2))
    t = np.transpose(t , (1,0,2))
    t = np.reshape(t , (9 , 2))
    return t

def Hflip(board):
    board = list(board)
    h = board[6:9]+board[3:6]+board[0:3]
    return np.array(h)

def eboard(pos):
    pos_board = np.array([[0,0]] * 9)
    pos_board[pos] = [1,1]
    return pos_board

def posfinder(pos):
    global pos_sym
    pos_transforms = np.array([])
    for transform in pos_sym:
        pos_transforms = np.append(pos_transforms , transform[pos][0])
    return pos_transforms

temp = [[x,0] for x in range(9)]
pos_sym = board_sym(temp)
pos_mat = [posfinder(x) for x in range(9)]
pos_mat

def switch(initial , num1 , num2):
    if initial == num1:
        return num2
    if initial == num2:
        return num1
    else:
        return initial

def reset_score(score):
    score[0] , score[1] , score[2] = 0,0,0

def end(board , LIST):
    return any([set([board[x] for x in y])  in [{1},{2}] for y in LIST])

def setup_model_standard():
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(12, activation=tf.nn.relu),
      tf.keras.layers.Dense(12, activation=tf.nn.relu),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(9, activation=tf.nn.softmax)
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def human(board , edit_choice = 0 , who = 0):
    if edit_choice > 0:
        return np.random.randint(9)
    pos = int(input("1-9 based on numpad:"))
    if pos >= 7:
        pos = pos - 6
    elif pos <= 3:
        pos = pos + 6
    pos -= 1 # because of list indexing
    return pos

def rando(board , edit_choice = 0 , who = 0):
    pos = np.random.randint(0,9)
    return pos
                

def testplace(board =[] , who = 1  , board_list = [], init = False , pos_list = []):
    board_list = []
    pos_list = []
    board = list(board)
    for i in range(9):
        if board[i] == 0:
            board[i] = who
            temp_board = list(board)
            board_list.append(temp_board)
            if init:
                pos_list.append(i)
            if end(board , win_cond):
                return i
            else:
                board[i] = 0
    if init == False:
        return board_list
    else:
        return [pos_list , board_list]
    
       
ra = rando
hu = human
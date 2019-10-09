
# coding: utf-8

# In[1]:


import numpy as np
from numpy import linalg as LA


# In[2]:


def weights(i, save = False):
    n = 9
    if i == "input":
        weight = np.random.rand(9,n)
        return weight
    if i == "mid":
        weight = np.random.rand(n,n)
        return weight
    if i == "output":
        weight = np.random.rand(n,9)
        return weight
    if i == "pred_output":
        weight = np.random.rand(n,1)
        return weight

    


# In[3]:


def null(x, y=2):
    x = x


# In[4]:


# neural (player) = 1 , X's : RNG = 0 or 2, O's
# thinker1 tied to index = 1

class Game():
    def __init__(self , board = "000000000" , player_win_count = 0 , computer_win_count = 0 , tie_count = 0 , end = False, thinker1 = None , 
                 thinker2 = None , over = False , reinforce = 0.5):
        self.board = board
        self.player_win_count = player_win_count
        self.computer_win_count = computer_win_count
        self.tie_count = tie_count
        self.end = end
        self.thinker1 = thinker1
        self.thinker2 = thinker2 
        self.over = over
        self.reinforce1 = reinforce
        self.reinforce2 = reinforce

    def reset(self):
        self.player_win_count = 0
        self.computer_win_count = 0
        self.tie_count = 0
        
    def place(self , obj, pos):
        self.board = self.board[:pos] + obj + self.board[pos+1:]
        
    def evaluator(self , index):
        win = index * 3
        diag_ru = self.board[0] + self.board[4] + self.board[8] 
        diag_ld = self.board[2] + self.board[4] + self.board[6]
        if diag_ld == win or diag_ru == win:
            self.winning(index)
            return
        for i in range(3):
            row = self.board[3*i:3*i+3] 
            col = self.board[i] + self.board[i + 3] + self.board[i+6]
            if row == win or col == win:
                self.winning(index)
                return
        
    def winning(self , index):
        if index == "1":
            self.player_win_count += 1
            #print("PLAYER WINS!" , self.player_win_count)
            self.reinforce1 = 1
            self.reinforce2 = 0
        if index == "2":
            self.computer_win_count += 1
            #print("COMPUTER WINS!" , self.computer_win_count)
            self.reinforce1 = 0
            self.reinforce2 = 1
        self.end = True
    
    def play(self , index , show):
        for count in range(1,10):
            if index == 3:
                index = 1
            self.turn(index = index , count = count)
            self.show_board(show)
            index += 1
            if self.end == True:
                self.end = False
                break
            if count == 9:
                self.tie_count += 1
                #print("THATS A TIE!" , self.tie_count)
                self.reinforce1 = 1
                self.reinforce2 = 0
                break
            
    def turn(self , index , count):
        pos = self.decision(index)
        index = str(index)
        self.place(index, pos)
        if count  > 4:   # don't bother evaluating for first 4 moves
            self.evaluator(index)
            
    def show_board(self , show = False):
        if self.thinker1 ==  self.inputter or self.thinker2 ==  self.inputter or show == True:
            show = "░" * 9
            for i in range(9):
                if self.board[i] == "1":
                    show = show[:i] + "X" + show[i + 1:]
                if self.board[i] == "2":
                    show = show[:i] + "O" + show[i + 1:]
            show = show[:3]  + "\n" + show[3:6] + "\n" + show[6:9] 
            print(show)
            print(self.board)
            print("--------------------------------------------------")
            print()
    
    def decision(self , index):
        if index == 1:
            pos = self.thinker1()

            return pos
        if index == 2:
            pos = self.thinker2()
            return pos
        
    def rng(self , r = -6):
        if r == -6:
            while True:
                pos = np.random.randint(0,9)
                if self.board[pos] == "0":
                    return pos
            
    def programmed_1(self):
        for i in range(9):
            pos = i
            if self.board[pos] == "0":
                return pos
            
    def programmed_2(self):
        for i in [4,0,8,2,6,1,3,5,7,9]:
            pos = i
            if self.board[pos] == "0":
                return pos
            
    def inputter(self , r = -6):
        if r == -6:
            pos = int(raw_input("pick a number 1 - 9: ")) - 1
            return pos
            
    def play_again(self , j , thinker1 , thinker2, index = 1 , automate = False , show = False):  # index can be one or two
        self.thinker1 = thinker1
        self.thinker2 = thinker2
        for i in range(j):
            if i > 0:
                self.over = True
                self.thinker1(self.reinforce1)
                self.thinker2(self.reinforce2)
                self.over = False
            if automate == False:
                another = input("play again? [y/n]: ")
            else:
                another = "y"
            if another == "y":
                self.board = "0" * 9
                self.play(index , show)
                if show == True:
                    print("------------------")
            else:
                break
                
        temp = (self.player_win_count , self.computer_win_count , self.tie_count)
        print(temp[0] , temp[1] , temp[2])
        self.reset()
        return temp

            
    


# In[116]:


# must recieve data about board, and back_propogation
# must send data about position chosen


class Neural(Game):
    def __init__ (self , G = Game , save_data = [] , weight_input = weights("input") , weight_mid = weights("mid") , weight_output = weights("output")):
        self.save_data = save_data
        self.weight_input = weight_input
        self.weight_mid = weight_mid
        self.weight_output = weight_output
        self.G = G
    
    def neural_1(self , reinforce = 0):
        if self.G.over == True:
            self.setup_BP(self.save_data , reinforce)
            self.save_neural_choices_reset()
            #self.show_weight()
            #self.normalize()
        else:
            bias = 0.1
            N0 = self.neural_row1(self.G.board)
            print(N0)
            N1 = N0.dot(self.weight_input)  # 1 X 9 times 9 X 12 --> 1 X 12
            M1 = self.sigmoid(N1)
            N2 = M1.dot(self.weight_mid)  # 1 X 12 times 12 X 12 --> 1 X 12
            M2 = self.sigmoid(N2)
            N3 = M2.dot(self.weight_output)  # 1 X 12 times 12 X 9 --> 1 X 9
            print(N3)
            
            choices = list(enumerate(N3[0]))
            #print(choices)
            #print("------------")
            while True:
                choice = max(choices , key = lambda x: x[1])
                pos = choice[0]
                if self.G.board[pos] == "0":
                    self.save_neural_choices(N0, N1 , N2 , N3 , pos)
                    """print(N0)
                    print(N1)
                    print(N2)
                    print(N3)
                    print(pos)"""
                    return pos
                else:
                    choices.remove(choice)
        
    def neural_row1(self , board):    
        input_data = np.array([list(map(float , list(board)))])   # makes the board as a string into number
        input_data = input_data.astype(float)
        #print("input data" , input_data)
        np.place(input_data , input_data==0 , 3)   # empty space is regular value
        np.place(input_data , input_data==1 , 5)
        np.place(input_data , input_data==2 , 1)   # opponent is viewed as low value
        #print("input data refined" , input_data)
        return input_data
    
    def save_neural_choices(self , input_data , layer2_data , layer3_data , output_data , pos):
        self.save_data.append([input_data[0] , layer2_data[0] , layer3_data[0] , output_data[0] , pos])  # since node lists in matrix form only take [0] element
        
    def save_neural_choices_reset(self):
        self.save_data = []
        
    def setup_BP(self, data , reinforce):
        moves = len(data)
        for t in range(len(data)):
            self.BP(data[t] , reinforce , t , moves)
    
    def BP(self , data , reinforce , t , moves):
        N0 = data[0]
        N1 = data[1]
        N2 = data[2]
        N3 = data[3]
        pos = data[4]
        N3_pos = N3[pos]
        E2 = 0.5 * (N3_pos - reinforce) ** 2
        E = N3_pos - reinforce
        i3 = pos
        gamma = 0.005 #*  (t + 1)**2 / moves**2
        
        #print(self.weight_output)
        # input weights
        sum_i2 = self.sigma(self.weight_output , i3 , N2)   # establishes Pi multiplication series summed together over iteration i2, this value doesn't change; for weight_input
        for i0 in range(len(self.weight_input)):
            for i1 in range(len(self.weight_mid)):
                end_weight = 0
                for i2 in range(len(self.weight_output)):
                    end_weight += self.weight_mid[i1][i2]   # establishes sigma iteration over i2 for end weight which is weight at the end of dE/dw equation; for weight_input
                    
                    
                    #mid weight adjustment
                    if i0 == 0:   # only iterates over i1 and i2
                        dEdw_mid = E * self.weight_output[i2][i3] * self.sigprime(N2[i2]) * self.sigmoid(N1[i1]) 
                        self.weight_mid[i1][i2] += -gamma * dEdw_mid
                        
                        
                        #output weight adjustment
                        if i1 == 0:   # only iterates over i2 and i3**
                            dEdw_output = E * self.sigmoid(N2[i2]) 
                            self.weight_output[i2][i3] += -gamma * dEdw_output
                        
                 #input weight adjustment
                dEdw_input = E * sum_i2 * end_weight * self.sigprime(N1[i1]) * N0[i0]
                self.weight_input[i0][i1] += -gamma * dEdw_input
        #print(self.weight_output)
        #print("--")
                
                
    def normalize(self):
        for w in [self.weight_input, self.weight_mid, self.weight_output]:
            w = w/np.max(w)
        
    def sigma(self , weight , j , node_prev):
        result = 0
        for i in range(len(weight)):
            result += weight[i][j] * self.sigprime(node_prev[i])
        return result            
                
    def sigmoid(self , x):
        y = 1/(1 + np.exp(-x))
        return y
    
    def sigprime(self , x):
        s = self.sigmoid(x) 
        y = s * (1 - s)
        return y
    
    def show_weight(self):
        print("+++++++++++++++++++++++++++++++++++++++++++")
        print("")
        print("input weights:: " , self.weight_input)
        print("")
        print("------------------------------------------------------------------------")
        print("")
        print("mid weights::" , self.weight_mid)
        print("")
        print("------------------------------------------------------------------------")
        print("output weights:: " , self.weight_output)


# In[117]:


g = Game()
g.board


# In[118]:


n1 = Neural(g)
n2 = Neural(g)


# In[119]:


p = g.play_again(1 , n2.neural_1 , g.rng , index = 1 , automate = True , show = True)





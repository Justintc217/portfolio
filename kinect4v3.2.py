
# coding: utf-8

# In[1]:

import string
import numpy as np
trial = string.digits + string.ascii_lowercase + "!@#$%^" 


# In[2]:

trial
trial2 = "0" * 42


# In[3]:

trial2 = "X00000000000000000000000000000000000000000"


# In[ ]:




# In[11]:

# board has upward gravity, board is flipped by show_board function
# 1 = player , 2 = computer


class Game():
    def __init__(self, board = "0"*42):
        self.board = board
        self.player = "#"
        self.comp = "X"
        self.null = "0"
    
        
    def show_board(self , board):   # Interface, first part of board string is printed on the bottom
        for i in range(6):
            i = 5 - i
            row = board[7*i:7*i+7]
            print(row)
            
            
    def place(self,actor,board,place,cond = "null",can_go = False):   
        # changes board based on placing
        # Counts from 1 to 7 and so that actor can replace the index value and not insert between
        if board == "fail":
            return "fail"
        while can_go == False:
            if place > 42:
                return "fail"
            if board[place-1] != self.null:
                place += 7
                
            else:
                can_go = True
        board = board[0:place-1] + actor + board[place::]
        if cond == "real":
            self.board = board
        return board
        
    def play(self):
        while True:
            decision = self.decision_v1()
            self.place(self.player,self.board,decision,"real")
            self.show_board(self.board)
            if self.evaluate(self.board , self.player) == 1:
                print("player wiinnning")
            decision = self.decision_v2()
            self.place(self.comp,self.board,decision,"real")
            self.show_board(self.board)
            if self.evaluate(self.board , self.comp) == 1:
                print("comp wiinnning")
        
        
    def evaluate(self,board,obj = "X"):   # check to make sure same as self.comp
        if board != "fail":
            diag_right_start = [14,7,0,1,2,3]     # diag start is where the diag starts
            diag_left_start = [20,13,6,5,4,3]
            diag_run = [4,5,6,6,5,4]        # diag run is how long the diag is
            for i in range(7):
                a = 0
                diag_right, diag_left = "" , ""
                if obj * 4 in board[i] + board[i + 7] + board[i + 14] + board[i + 21] + board[i + 28] + board[i + 35]:
                    return 0.3

                if i < 6:
                    if obj * 4 in board[7*i:7*i+7]:
                        return 1
                    m = diag_right_start[i]
                    j = diag_left_start[i]
                    for k in range(diag_run[i]):    # sets condition for analyzing until diagonal is out of bounds
                        diag_right += board[m + 8*a]
                        diag_left += board[j + 6*a]
                        a += 1
                    if obj * 4 in diag_right or obj * 4 in diag_left:
                        return 1
        return 0

    def decision_v1(self):
        decision = int(raw_input())
        return decision
    
    def analyzer_v2(self,selector):
        no_info = True
        maxim = -1000000
        stats = [100000000 , -1000000 , 7**4 , -7**3 , 7**2 , -7 , 1]
        print(selector)
        for i in range(1,8):
            var = 0
            for j in range(len(stats)):
                var += selector[i][j] * stats[j]
            print(var)
            if var > maxim:
                maxim = var
                choice = i
            if var != 0:
                no_info = False
        if no_info == True:
            print("path of random")
            return np.random.randint(1,8)
        else:
            return choice
    
    def decision_v2(self):
        selector = {1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
        
        for i1 in range(1,8):
            count_1 , count_2 , count_3 , count_4 , count_5 , count_6 , count_7 = 0,0,0,0,0,0,0
            board_1 = self.place(self.comp,self.board,i1)
            add_1 = self.evaluate(board_1,self.comp)
            count_1 += add_1
            if add_1 == 0:
                for i2 in range(1,8):
                    board_2 = self.place(self.player,board_1,i2)
                    add_2 = self.evaluate(board_2,self.player)
                    count_2 += add_2
                    if add_2 == 0:
                        for i3 in range(1,8):
                            board_3 = self.place(self.comp,board_2,i3)
                            add_3 = self.evaluate(board_3,self.comp)
                            count_3 += add_3
                            if add_3 == 0:
                                for i4 in range(1,8):
                                    board_4 = self.place(self.player,board_3,i4)
                                    add_4 = self.evaluate(board_4,self.player)
                                    count_4 += add_4
                                    if add_4 == 0:
                                        for i5 in range(1,8):
                                            board_5 = self.place(self.comp,board_4,i5)
                                            add_5 = self.evaluate(board_5,self.comp)
                                            count_5 += add_5
                                            if add_5 == 0:
                                                for i6 in range(1,8):
                                                    board_6 = self.place(self.player,board_5,i6)
                                                    add_6 = self.evaluate(board_6,self.player)
                                                    count_6 += add_6
                                                    if add_6 == 0:
                                                        for i7 in range(1,8):
                                                            board_7 = self.place(self.comp,board_6,i7)
                                                            add_7 = self.evaluate(board_7,self.comp)
                                                            count_7 += add_7
             
            selector[i1] = [count_1 , count_2 , count_3 , count_4 , count_5 , count_6 , count_7]   
            
        x = self.analyzer_v2(selector)    
        return x
        # evaluates board centered around place 

        
    


# In[12]:

a = Game()
a.play()


# In[ ]:




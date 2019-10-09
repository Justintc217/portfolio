
# coding: utf-8

# In[5]:

#49 digits decide the state of the game
#0 = blank , 1 = red , 2 = black
#string begins in left bottom corner of the board



# In[6]:

def maxfinder(listing):
    full = []
    if listing != []:
        maxer = -100000
        indexer = 0
        for i in range(len(listing)):
            test = listing[i][1]
            if test > maxer:
                maxer = test
                indexer = listing[i][0]
        for i in range(len(listing)):
            test = listing[i][1]
            if test == maxer:
                full.append(listing[i][0])   # this tests if there are multiple max results
        return [indexer,maxer,full]
    else:
        return[0,0,full]


# In[7]:

maxfinder([[2,3],[1,7],[3,4],[5,7]])


# In[8]:

import numpy as np
import math


# In[9]:

def kinect_rng():
    selector = [0,1,1,2,2,2,3,3,3,3,4,4,4,5,5,6]
    selected = np.random.randint(0,len(selector))
    selection = selector[selected]
    return selection


# In[10]:

def set_rng(selector):
    if len(selector) == 0:
        selected = np.random.randint(0,7)
    else:
        selected = np.random.randint(0,len(selector))
    selection = selector[selected]
    return selection


# In[18]:

class Game():
    def __init__(self , height = 6 , length = 7 ,
                 objects = ["X " , "# "],
                 space = "O ", end_cond = False , var = 0, count = 0):
        self.height = height
        self.length = length
        self.space = space
        self.end_cond = end_cond
        self.objects = objects
        self.var = var
        self.count = count
        self.board = [[space] * self.length for i in range(self.height)]
        self.empty = [[space] * self.length for i in range(self.height)]
        
        
    
    
    def place(self,obj,value,testing = False):
        where = int(value)
        col = [self.board[x][where] for x in range(6)]
        col = col[::-1]
        if self.space in col:
            for i in range(6):
                if col[i] == self.space:
                    self.board[5-i][where] = obj
                    break   
            else: 
                print("failure")
                return "failure"
        
        
    
    def show_board(self):
        for row in self.board:
            print(''.join(row))
            
    def win_con(self):
        P = self.objects
        case = [[P[0]]*4,[P[1]]*4]
        for y in range(6):
            for x in range(7):
                if y < 3:
                    upward = [self.board[y][x]] + [self.board[y+1][x]] + [self.board[y+2][x]] + [self.board[y+3][x]]
                if x < 4 and y < 3:
                    diag_upright = [self.board[y][x]] + [self.board[y+1][x+1]] + [self.board[y+2][x+2]] + [self.board[y+3][x+3]]
                if x < 4 and y < 3:
                    diag_downleft = [self.board[y][x+3]] + [self.board[y+1][x+2]] + [self.board[y+2][x+1]] + [self.board[y+3][x]]
                if x < 4 and self.board[y][x:x+4] in case:
                    #print("hey!! listen")
                    self.end_cond = True
                elif y < 3 and upward in case:
                    #print("hey!! listen")
                    self.end_cond = True
                elif x < 4 and y < 3 and diag_upright in case:
                    #print("hey!! listen")
                    self.end_cond = True
                elif x < 4 and y < 3 and diag_downleft in case:
                    #print("hey!! listen")
                    self.end_cond = True
                    
    
    
    def testplace(self,mv,obj,board):
        if board == "failure":
            return "failure"
        dumboard = [list(board[t]) for t in range(6)]
        mv = int(mv)
        col = [dumboard[x][mv] for x in range(6)]
        col = col[::-1]
        if self.space in col:
            for i in range(6):
                if col[i] == self.space:
                    dumboard[5-i][mv] = obj
                    return dumboard
                    break     
        else: 
            return "failure"
    
    def selector_analyzer(self,selector):
        which_move = [0,1,2,3,4,5,6]    # which_move options are removed if they produce a "failure" board
        while which_move != []:
            A = 12
            B = 7
            C = 1
            print("selector:" , selector)
            third = []
            fifth = []
            calcu = []
            for i in which_move:
                move = i
                if selector[i][0] > 0:
                    return move
                if selector[i][1] == 0:
                    calcu.append([i,round(selector[i][2] * A - B * selector[i][3] + C * selector[i][4],1)])
                    third.append([i,selector[i][2]])
                    if selector[i][3] == 0:
                        fifth.append([i,selector[i][4] - 4 * selector[i][3]])

            move = maxfinder(calcu)[0]
            #print("path of calcu", calcu)
            if self.testplace(move, self.objects[0], self.board) != "failure":
                return move
            else:
                which_move.remove(move)
                
        # in case of no good moves
        for run in range(100):
            move = set_rng([0,1,2,3,4,5,6])
        if self.testplace(move, self.objects[0], self.board) != "failure":
            return move
        
                
    def evaluate(self, board):   # evaluates the board and checks for winning scenerios, awards points to team with a win. 
                                 # Used for testplacing
        if board == "failure":
            return [0,0,0,0]
        player_win = 0
        comp_win = 0
        player_pt = 0
        comp_pt = 0
        n = 0.3
        P = self.objects
        case = [[P[0]]*4,[P[1]]*4]
        alt_casec = [[P[0]] * 3 + [self.space] , [self.space] + [P[0]] * 3 , [P[0]] + [self.space] + [P[0]] * 2, [P[0]] * 2 + [self.space] + [P[0]]]
        alt_casep = [[P[1]] * 3 + [self.space] , [self.space] + [P[1]] * 3 , [P[1]] + [self.space] + [P[1]] * 2, [P[1]] * 2 + [self.space] + [P[1]]]
        for y in range(6):
            for x in range(7):
                if y < 3:
                    upward = [board[y][x]] + [board[y+1][x]] + [board[y+2][x]] + [board[y+3][x]]
                if x < 4 and y < 3:
                    diag_upright = [board[y][x]] + [board[y+1][x+1]] + [board[y+2][x+2]] + [board[y+3][x+3]]
                if x < 4 and y < 3:
                    diag_downleft = [board[y][x+3]] + [board[y+1][x+2]] + [board[y+2][x+1]] + [board[y+3][x]]
                    
                if x < 4 and board[y][x:x+4] == case[1]:
                    player_win += 1
                if x < 4 and board[y][x:x+4] in alt_casep:
                    player_pt += n
                    
                if x < 4 and board[y][x:x+4] == case[0]:
                    comp_win += 1
                if x < 4 and board[y][x:x+4] in alt_casec:
                    comp_pt += n 
                    
                if y < 3 and upward == case[1]:
                    player_win += 1
                if y < 3 and upward in alt_casep:
                    player_pt += n
                    
                if y < 3 and upward == case[0]:
                    comp_win += 1
                if y < 3 and upward in alt_casec:
                    comp_pt += n
                    
                if x < 4 and y < 3 and diag_upright == case[1]:
                    player_win += 1
                if x < 4 and y < 3 and diag_upright in alt_casep:
                    player_pt += n
                    
                if x < 4 and y < 3 and diag_upright == case[0]:
                    comp_win += 1
                if x < 4 and y < 3 and diag_upright in alt_casec:
                    comp_pt += n
                    
                if x < 4 and y < 3 and diag_downleft == case[1]:
                    player_win += 1
                if x < 4 and y < 3 and diag_downleft in alt_casep:
                    player_pt += n
                    
                if x < 4 and y < 3 and diag_downleft == case[0]:
                    comp_win += 1
                if x < 4 and y < 3 and diag_downleft in alt_casec:
                    comp_pt += n
        final = [comp_win, player_win, comp_pt, player_pt]
        return final
    
                
    def decision_v4(self):
        selector = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}
        
        for i1 in range(7):
            first_counter = 0
            second_counter = 0
            third_counter = 0
            fourth_counter = 0
            fifth_counter = 0
            first_board = self.testplace(i1,self.objects[0],self.board)
            first_points = self.evaluate(first_board)
            first_counter += first_points[0]
            for i2 in range(7):
                second_board = self.testplace(i2,self.objects[1],first_board)
                second_points = self.evaluate(second_board)
                second_counter += second_points[1]
                for i3 in range(7):
                    third_board = self.testplace(i3,self.objects[0],second_board)
                    third_points = self.evaluate(third_board)
                    third_counter = round(third_counter + third_points[0] + third_points[2] ,2)
                    for i4 in range(7): 
                        fourth_board = self.testplace(i4,self.objects[1],third_board)
                        fourth_points = self.evaluate(fourth_board)
                        fourth_counter = round(fourth_counter + fourth_points[1] + fourth_points[3],2)
                        for i5 in range(7):
                            fifth_board = self.testplace(i5,self.objects[0],fourth_board)
                            fifth_points = self.evaluate(fifth_board)
                            fifth_counter = round(fifth_counter + fifth_points[0] + fifth_points[2],2)
            selector[i1] += [first_counter, second_counter, third_counter, fourth_counter, fifth_counter]
        
        move = self.selector_analyzer(selector)
        
        return move                

                    
    def play(self):

        playing = True
        player_first = int(input("press 1 to go first; 0 to go second:"))  ##### set to 1 to make player go first
        print_on = True
        turn = 0
        while playing == True:
            turn += 1
            if player_first == 0:
                #computer
                comp_num = self.decision_v4()
                if turn == 1:
                    comp_num = kinect_rng()
                self.place(self.objects[0], comp_num)
                if print_on == True:
                    self.show_board()
                    print("_____________")
                self.win_con()
                if self.end_cond == True:
                    print("comp wins!")
                    self.count += 1
                    
                #player
                play_num = self.decision()
                self.place(self.objects[1] , play_num)
                if print_on == True:
                    self.show_board()
                    print("_____________")
                self.win_con()
                if self.end_cond == True:
                    print("player wins!")
                    break
            
            else:
                play_num = self.decision()
                self.place(self.objects[1] , play_num)
                if print_on == True:
                    self.show_board()
                    print("_____________")
                self.win_con()
                if self.end_cond == True:
                    print("player wins!")
                    break
                
                #computer
                comp_num = self.decision_v4()
                self.place(self.objects[0], comp_num)
                if print_on == True:
                    self.show_board()
                    print("_____________")
                self.win_con()
                if self.end_cond == True:
                    print("YOUVE BEEN BAMBOOZLED!")
                    self.count += 1
                    break
                    
    def decision(self):
        while True:
            player_mov = str(input())
            
            if player_mov in ["1","2","3","4","5","6","7"]:
                move = int(player_mov) - 1
                
                if self.testplace(move,self.objects[1],self.board) != "failure":
                
                    return move
            elif player_mov == "end":
                self.end_cond = True
                return 1
            print("okay, there was an error, lets try again")
        
        
        

                    

            
            


# In[ ]:




# In[19]:

wins = 0
for i in range(1):
    x = Game()
    x.play()
    if x.count == 1:
        wins += 1
print(wins)


# In[ ]:




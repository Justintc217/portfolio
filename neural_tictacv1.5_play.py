
# coding: utf-8

# In[349]:


import numpy as np


weight1 = np.array([[ 0.20515033,  0.33485252,  0.30895811,  0.05201501,  0.15739759,
          0.27736616,  0.32164945,  0.20206639,  0.48640573,  0.15056051,
          0.18573921,  0.30139343],
        [ 0.33432435,  0.57594894,  0.48405146,  0.28629315,  0.28467867,
          0.52084361,  0.49141526,  0.34099983,  0.74558442,  0.31294252,
          0.53154587,  0.41497943],
        [ 0.2631565 ,  0.49482227,  0.4464021 ,  0.30419326,  0.31966052,
          0.48001984,  0.44089521,  0.4216827 ,  0.66248609,  0.25389322,
          0.43888045,  0.41868083],
        [-0.04425561, -0.02405354,  0.07377362, -0.0425024 ,  0.09994408,
          0.04235539,  0.11171297, -0.03052045,  0.29460494, -0.00995116,
          0.00797904,  0.19291826],
        [ 1.34747624,  1.48732862,  1.52222079,  1.34330968,  1.41517235,
          1.45567884,  1.48363685,  1.40340345,  1.682582  ,  1.30056924,
          1.44314226,  1.55001263],
        [ 0.31014261,  0.23666726,  0.37148804,  0.36434999,  0.53887238,
          0.23488071,  0.80781552,  0.62106675,  0.53251654,  0.38962217,
          0.38226082,  0.61679634],
        [ 0.32732343,  0.42538307,  0.49454646,  0.25832967,  0.34451707,
          0.4561452 ,  0.54242868,  0.39660953,  0.66371954,  0.27767091,
          0.4257498 ,  0.47461133],
        [ 0.09425456,  0.26395123,  0.35237964,  0.20325162,  0.11146274,
          0.03881566,  0.09492509,  0.06924304,  0.32848329, -0.14594621,
          0.30063932,  0.33987054],
        [ 0.8533017 ,  0.98240503,  0.9135388 ,  0.64155512,  0.71840374,
          0.88569653,  0.99720835,  0.92794752,  1.09484671,  0.74718539,
          0.78028807,  0.86404034]])
weight2 = np.array([[-0.79249694, -0.62728035, -0.4273461 , -0.89721011, -0.62290712,
         -0.84320843, -0.27363323, -0.57863221, -0.39435551, -0.6028725 ,
         -0.05155123, -0.64077333],
        [-0.43456008, -0.31386687, -0.43154254, -0.07180775, -0.65001311,
         -0.61065205, -0.89199996, -0.48840872, -0.65974756, -0.9210304 ,
         -0.51970767, -0.38778815],
        [-0.91280195, -0.39615051, -0.4038613 , -0.85247116, -0.60584349,
         -0.39573216, -0.49848265, -0.75567349, -0.65986581, -0.5191928 ,
         -0.16390776, -0.28661503],
        [-0.76320767, -0.47852757,  0.00944089, -0.7919585 ,  0.05848982,
         -0.02158309, -0.79513748, -0.0653604 , -0.47521126, -0.1390897 ,
         -0.53045091, -0.36580756],
        [-0.29229787, -0.2433211 , -0.92451215, -0.38022743, -0.81557688,
         -0.70177307, -0.6082455 , -0.60679929, -0.58463984, -0.95080403,
         -0.88140914, -0.85928596],
        [-0.4751612 , -0.09529711, -0.86467188, -0.05114437, -0.29922933,
         -0.43636032, -0.33962314, -0.28252295, -0.83136056, -0.58671052,
         -0.36231706, -0.32406492],
        [ 0.09856728, -0.75081514, -0.07453461, -0.24647924, -0.42940173,
         -0.51187178, -0.14575943,  0.00672682, -0.23027014, -0.04411455,
         -0.43544286, -0.59539996],
        [-0.7185811 , -0.82698035, -0.43988713, -0.49012384, -0.14988941,
         -0.17091666, -0.75999337, -0.71378359, -0.50609081, -0.37678681,
         -0.74757004, -0.61044302],
        [-0.0107538 , -0.25548415, -0.81218532, -0.59821704, -0.68590827,
         -0.29863655, -0.477402  , -0.98552747, -0.21338638, -0.70332689,
         -0.8099486 , -0.5425699 ],
        [-0.34714898, -0.58725349, -0.63026027, -0.4911045 , -0.89337635,
         -0.19079167, -0.69828912, -0.94225593, -0.18385155, -0.2000088 ,
         -0.13285998, -0.31280977],
        [-0.58752011, -0.1605337 , -0.13726867, -0.59767922,  0.01533571,
         -0.81684927,  0.14581609, -0.10101706, -0.10310121, -0.0036701 ,
         -0.18454138, -0.57305541],
        [-0.42796695, -0.88516518, -0.511121  , -0.1752907 , -0.55419687,
         -0.65197657, -0.3057216 , -0.14427524, -0.81265203, -0.61002337,
         -0.80848905, -0.14407774]])
weight3 = np.array([[-0.38069208,  0.15413592, -0.08947337, -0.29128059,  0.37990037,
         -0.43235645, -0.05364798, -0.50228261, -0.02507877],
        [-0.00091372, -0.21982036, -0.25553966, -0.12455473,  0.10429544,
          0.29745761, -0.00133466,  0.06722994, -0.31432363],
        [-0.20339235, -0.3664327 , -0.13028251, -0.2611283 , -0.04210269,
          0.10044027,  0.43866041, -0.32072487,  0.1340999 ],
        [ 0.31840051,  0.03457664, -0.12940868, -0.2336797 , -0.52226343,
         -0.15698492,  0.23032151, -0.47816617, -0.29493239],
        [ 0.21551998,  0.24433329,  0.06808388,  0.2069551 , -0.17855219,
         -0.31892924, -0.13308881,  0.06445847,  0.43787164],
        [-0.43284212, -0.03493632, -0.05911659,  0.01711952, -0.54055438,
         -0.16629683,  0.27747459,  0.03438423, -0.05763401],
        [-0.20387049, -0.22956083, -0.00082933,  0.33700956,  0.40406394,
         -0.03162033, -0.11625661,  0.32181688, -0.08825395],
        [ 0.04228871, -0.32405451,  0.33856837,  0.03100672,  0.23962457,
          0.29077743, -0.34396056,  0.19047516,  0.27875443],
        [-0.13502406, -0.33935297, -0.36950505, -0.0329453 , -0.20356534,
          0.1013236 , -0.30006358,  0.34321526, -0.24380982],
        [-0.27429027, -0.06645693,  0.10021225, -0.28177166, -0.29368295,
         -0.3188515 ,  0.1678608 ,  0.24835218, -0.04933375],
        [ 0.20704607,  0.19097493, -0.2502367 ,  0.46554487,  0.25676757,
         -0.28064983, -0.34691527, -0.39872695, -0.37182191],
        [ 0.26430939, -0.0391639 ,  0.41065204,  0.25963948,  0.04775998,
          0.24308495, -0.46514285, -0.20786891,  0.1279872 ]])





# In[350]:


def weights(i, save = False):
    if i == "input":
        weight_input = np.random.rand(9,12)
        return weight_input
    if i == "mid":
        weight_mid = np.random.rand(12,12)
        return weight_mid
    if i == "output":
        weight_output = np.random.rand(12,9)
        return weight_output
    


# In[351]:


def cons_randomizer(j):
    m = np.empty
    for i in range(j):
        m = np.append(m , np.random.randint(1,9))
    
    return np.random.randint(1,9)


# In[352]:


# neural (player) = 1 , X's : RNG = 0 or 2, O's

class Game():
    def __init__(self , board = "000000000" , player_win_count = 0 , computer_win_count = 0 , tie_count = 0 , end = False, save_data = [], thinker1 = None , 
                 thinker2 = None, weight_input = weight1 , weight_mid = weight2 , weight_output = weight3):
        self.board = board
        self.player_win_count = player_win_count
        self.computer_win_count = computer_win_count
        self.tie_count = tie_count
        self.end = end
        self.thinker1 = thinker1
        self.thinker2 = thinker2
        
        #neural stuff
        self.save_data = save_data
        self.weight_input = weight_input
        self.weight_mid = weight_mid
        self.weight_output = weight_output
        
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
            self.back_propogate(1)
        if index == "2":
            self.computer_win_count += 1
            #print("COMPUTER WINS!" , self.computer_win_count)
            self.back_propogate(0)
        self.end = True
    
    def play(self , index , show):
        for count in range(1,10):
            if index == 3:
                index = 1
            self.turn(index = index , count = count)
            self.show_board(show)
            index += 1
            
            if self.end == True:
                self.save_neural_choices_reset()
                self.end = False
                break
            if count == 9:
                self.save_neural_choices_reset()
                self.tie_count += 1
                #print("THATS A TIE!" , self.tie_count)
                self.back_propogate(0.5)
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
        
    def rng(self):
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
            
    def inputter(self):
        pos = int(input("pick a number 1 - 9: ")) - 1
        return pos
            
    def play_again(self , j , thinker1 , thinker2, automate = False , show = False):
        self.thinker1 = thinker1
        self.thinker2 = thinker2
        for i in range(j):
            if automate == False:
                another = input("play again? [y/n]: ")
            else:
                another = "y"
            if another == "y":
                self.board = "0" * 9
                self.play(1 , show)
                #print("------------------")
            else:
                break
        print(self.player_win_count , self.computer_win_count , self.tie_count )
        self.reset()
        weight_list = [self.weight_input , self.weight_mid , self.weight_output]
        return weight_list
        
        
                
    #neural functions
                
    def neural_1(self):

        input_data = self.neural_row1()
        layer2_data = self.sigmoid(input_data.dot(self.weight_input))  # 1 X 9 times 9 X 12 --> 1 X 12
        layer3_data = self.sigmoid(layer2_data.dot(self.weight_mid))  # 1 X 12 times 12 X 12 --> 1 X 12
        output_data = self.sigmoid(layer3_data.dot(self.weight_output))  # 1 X 12 times 12 X 9 --> 1 X 9
        choices = list(enumerate(output_data[0]))
        """print("input: ", input_data)
        print("layer2: ",  layer2_data)
        print("layer3: ", layer3_data)
        print("output: ", output_data)"""
        #print(choices)
        while True:
            choice = max(choices , key = lambda x: x[1])
            pos = choice[0]
            if self.board[pos] == "0":
                self.save_neural_choices(input_data , layer2_data , layer3_data , output_data , pos)
                #print(pos)
                return pos
            else:
                choices.remove(choice)
        
        
    def neural_row1(self):    
        input_data = np.array([list(map(float , list(self.board)))])   # makes the board as a string into number
        input_data = input_data.astype(float)
        np.place(input_data , input_data==2 , -1)   # opponent is viewed as low value
        np.place(input_data , input_data==0 , 0)   # empty space is regular value
        np.place(input_data , input_data==1 , 1)
        return input_data
    
    def save_neural_choices(self , input_data , layer2_data , layer3_data , output_data , pos):
        self.save_data.append([input_data[0] , layer2_data[0] , layer3_data[0] , [output_data[0][pos]] , pos])  # since node lists in matrix form only take [0] element
        
    def save_neural_choices_reset(self):
        self.save_data = []
    
    def back_propogate(self , reinforcement):
        weight_list = [self.weight_input , self.weight_mid , self.weight_output]
        for moves in range(len(self.save_data)):
            for i in range(0,3):
                self.enforce(self.save_data[moves][i] , self.save_data[moves][i+1], weight_list[i],  self.save_data[moves][4] , reinforcement)
                
    def enforce(self , early_nodes , late_nodes, weight , pos , reinforcement):
        avg = np.average(weight)
        for early_node in range(len(early_nodes)):
            for late_node in range(len(late_nodes)):
                correct = self.sigprime(early_nodes[early_node])  * early_nodes[early_node] * (reinforcement - late_nodes[late_node])
                if len(late_nodes) == 1:
                    weight[early_node][pos] = weight[early_node][pos] + correct
                else:
                    weight[early_node][late_node] = weight[early_node][late_node] + correct
                #w1+sigmoid_prime(a1)(answer - output)a1
                
                
                #late_nodes is a list of numbers
                # late node must be an index of corresponding values
                # for output analysis late_nodes is a single value, information about its position in the list is lost
                
                
    def sigmoid(self , x):
        y = 1/(1 + np.exp(-x))
        return y
    
    def sigprime(self , x):
        s = self.sigmoid(x) 
        y = s * (1 - s)
        return y
        
            
    


# In[355]:


"hi"


# In[356]:


x = Game()
y = Game()
z = Game()



# In[360]:


x.play_again(10 , x.neural_1 , x.inputter , automate = True , show = True)


# In[354]:



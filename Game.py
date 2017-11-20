
# coding: utf-8

# In[1]:

import numpy
import random

def rand(a , b):
    return random.randint(a , b)


# In[2]:

class Resource():
    def __init__(self , stock_berry = 0 , stock_burger = 0):
        self.stock_berry = stock_berry
        self.stock_burger = stock_burger
    
    


# In[3]:

class Brah():
    def __init__(self , health = 0 , attack = 0, crop = 0):
        self.health = health
        self.attack = attack
        self.crop = crop
        self.stock_opt = {"Qburger":0 , "Qberry":0 , "Qcarrot":0}
    
    def eat(self , food):
        what_eat = {"burger":20 , "berry":5 , "carrot":7}
        if food in what_eat: 
            self.health += what_eat[food]
    
    
        
            
    def var_health(self , amt):
        self.health += amt
    
    def boost_attack(self , amt):
        self.attack += amt
    
    def attacked(self , amt):
        self.health -= amt
        
    
    def stock_change(self , stock , amt):
        if stock in self.stock_opt:
            self.stock_opt[stock] += amt
    
    def plant(self):
        x = rand(0 , 3)
        self.stock_change("Qcarrot" , x)
        print("you planted {0} crops!".format(x))
    
    def forage(self):
        x = rand(0 , 6)
        self.stock_change("Qberry" , x)
        print("you foraged {0} berries".format(x))
    
    def hunt(self):
        x = rand(0 , 9)
        y = rand(2 , 7)
        if x > 5:
            self.stock_change("Qburger" , y)
            print("you killed a grayson, recieve {0} burgers".format(y))
        else:
            print("you didn\'t kill grayson :( , better luck next time!")
    
    
    
    
    
    
        


# In[4]:

MU = Brah(health = 100 , attack = 50)


def MU_stats():
    print("health: " , MU.health , " attack: ", MU.attack , " Burgers: " , MU.stock_opt["Qburger"]
         , " Berries: " , MU.stock_opt["Qberry"] , " carrots: " , MU.stock_opt["Qcarrot"])

def type_again(choice , action):
    if action not in choice:
        print("I\'m sorry but you must choose from the following {0}".format(choice))


# In[7]:

MU_stats()
playing = True
while playing == True:
    choices = ["eat" , "sleep", "plant" , "hunt" , "forage" ,"craft" , "quit"]
    action = input()
    type_again(choices , action)
    
    if action == "eat":
        food_choice = ["burger" , "berry" , "carrot"]
        eat_action = input("eat what?:" )
        type_again(food_choice , eat_action)
        if eat_action == "carrot":
            MU.eat("carrot")
            MU.stock_change("Qcarrot" , -1)
            MU_stats()
        
        if eat_action == "berry":
            MU.eat("berry")
            MU.stock_change(stock = "Qberry" ,amt = -1)
            MU_stats()
        
        if eat_action == "burger":
            MU.eat("burger")
            MU.stock_change("Qburger" , 5)
            MU_stats()
            
            
    if action == "plant":
        MU.plant()
        MU_stats()
    
    if action == "forage":
        MU.forage()
        MU_stats()
    
    if action == "hunt":
        MU.hunt()
        x = rand(0 , 1)
        if x == 1:
            hurt = 5*[5] + 3*[10] + 2*[20] + [40]
            y = rand(0 , 10)
            MU.health -= hurt[y]
        MU_stats
    
    
        
    if action == "quit":
        playing = False
        
    
    if action in choices:
        print("""your dieing... don\'t worry... whose to say death is bad... why do you fear something 
              you cannot even state the consequence of""")
        MU.health -= 5
        MU_stats()
    
    
    


# In[ ]:




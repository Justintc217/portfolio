
# coding: utf-8

# In[13]:


from ConnectZeroV1_8_actors import *


# In[ ]:


home = Neural(model = None)
away = Neural(model = None)
demo = []

p2help = 60
p1help = 60
for i in range(1,200):
    print("training period %d" % i)
    home = Neural(model = home.model, random_scale= np.sqrt(1/i))
    away = Neural(model = away.model, random_scale= np.sqrt(1/i))
    
    print("CNN self training phase")
    games = Gameroom(player1 = home, player2 = Dolphin())
    games.tournament(9, reset_data = True)
    print("score for player1 is CNN: ", games.score)
    train(home.model, games.data_store, epochs = 3)
    print("player1 is CNN")
    games.tournament(1, reset_data = True, seeing = True)
    demo.append(games.data_store)
    print("...")

    games = Gameroom(player1 = Dolphin(), player2 = home)
    games.tournament(9, reset_data = True)
    print("score for player2 is CNN: ", games.score)
    train(home.model, games.data_store, epochs = 3)
    print("player2 is CNN")
    games.tournament(1, reset_data = True, seeing = True)
    demo.append(games.data_store)

    games = Gameroom(player1 = home, player2 = home)
    games.tournament(9, reset_data = True)
    print("score for both players are CNN: ", games.score)
    train(home.model, games.data_store, epochs = 3)
    print("both players are CNN")
    games.tournament(1, reset_data = True, seeing = True)
    demo.append(games.data_store)


    ## advanced phase
    print("MCTS + CNN self training phase")
    games = Gameroom(player1 = Search(search_length = p1help, neuralnet = home, rollout_player = Dolphin()),
                 player2 = Search(search_length = p2help, neuralnet = home, rollout_player = Dolphin()))
    games.tournament(9, reset_data = True)
    if games.score[2] < games.score[1] - 1:
        p2help += 8
    elif games.score[1] < games.score[2] - 1:
        p1help += 8
    print("score: ", games.score)
    train(home.model, games.data_store, epochs = 10)
    
    # challenge previous phase
    challenge_games = Gameroom(player1 = Search(search_length = p1help, neuralnet = home, rollout_player = Dolphin()), 
                               player2 = Search(search_length = p2help, neuralnet = away, rollout_player = Dolphin()))
    challenge_games.tournament(3, reset_data = False)
    print("p1 = home  p2 = away games", challenge_games.score)
    next_challenge_games = Gameroom(player1 = Search(search_length = p1help, neuralnet = away, rollout_player = Dolphin()), 
                                    player2 = Search(search_length = p2help, neuralnet = home, rollout_player = Dolphin()))
    next_challenge_games.tournament(3, reset_data = False)
    print("p1 = away  p2 = home games", next_challenge_games.score)
    
    #demo
    print("challenge demo")
    game1 = Gameroom(player1 = home, player2 = away)
    game1.tournament(1, seeing= True)
    game2 = Gameroom(player1 = away, player2 = home)
    game2.tournament(1, seeing = True)
    demo.append(game1.data_store)
    demo.append(game2.data_store)
    
    
    homescore = challenge_games.score[1] + next_challenge_games.score[2]
    awayscore = challenge_games.score[2] + next_challenge_games.score[1]
    print("home = {0}  away = {1}".format(homescore, awayscore))
    if homescore > awayscore:
        away.model.set_weights(home.model.get_weights())
    elif homescore < awayscore:
        home.model.set_weights(away.model.get_weights())
        
    train(home.model, challenge_games.data_store, epochs = 1)
    train(home.model, next_challenge_games.data_store, epochs = 1)
    print("help is", p1help, p2help)
	
np.save("demo.npy", demo)
home.model.save_weights("trained.h5")


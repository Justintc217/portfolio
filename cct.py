# comp training

act = ['split' , 'use left hit left' , 'use left hit right' , 'use right hit left' , 'use right hit right']

# Intial conditions
cwisechoice = []
pwisechoice = []
playerwin = 0
compwin = 0
game = 1
end = 500
y = 10
while True:
    # temporary in game starting conditions
    plh = 1
    prh = 1
    clh = 1
    crh = 1
    cgoodmove = []
    pgoodmove = []
    turn = 0
    psave = [1 , 1 , 1 , 1]
    comp = 'non'

    game = game + 1
    whofirst = game % 2
    
    # entering gameplay
    while True:
        if whofirst == 0 or turn > 0:
            turn = turn + 1
            g = 1
            while g == 1:
                if clh + crh == 0:
                    break
                choice = []
                
                # player random choice generator
                det = int(y**2 - 2 * y + y ** (1.3))
                result = det % 5
                player = act[result]
                choice.append(player)

                
                # computer strat
                for var in range(0 , len(pwisechoice) , 1):
                    
                    if pwisechoice[var] == [plh , prh , clh , crh]:
                        choice.append(pwisechoice[var + 1])
                        
                chosen = (4 * y - y **2) % (len(choice))
                player = choice[chosen]

                if player == act[0]:
                    if plh == 0 or prh == 0:
                        if plh == 2 or prh == 2:
                            plh = 1
                            prh = 1
                            g = 0
                        if plh == 4 or prh == 4:
                            plh = 2
                            prh = 2
                            g = 0
                if player == act[1]:
                    clh = clh + plh
                if player == act[2]:
                    crh = crh + plh
                if player == act[3]:
                    clh = clh + prh
                if player == act[4]:
                    crh = crh + prh
                if (plh != 0 and player in act[1:3]) or (prh != 0 and player in act[3:5]):
                    g = 0
                y = y + 1

            # comp hand death condition
            if clh > 4:
                clh = 0
            if crh > 4:
                crh = 0

            # upload player situation and action
            cgoodmove.append(psave)
            cgoodmove.append(player)
            csave = [clh , crh , plh , prh]
            '''print('player status:' , psave , player)
            print('')'''
                

            # Victory conditions 
            if clh + crh == 0:
                # adding player successes to computer database
                for x in range(0 , len(cgoodmove) , 1):
                    cwisechoice.append(cgoodmove[x])
                playerwin = playerwin + 1
                '''print('YOU WON!! :D')
                print('game:' , game)
                print('playerwin:' , playerwin)
                print('computer database:' , cwisechoice)'''
                break

        # relay game status
        """print('player\'s left hand:' , plh , 'player\'s right hand:' , prh)
        print('computer\'s left hand:' , clh , 'computer\'s right hand:' , crh)
        print('')"""

        # BEGIN COMPUTER TURN     
            
        if whofirst == 1 or turn > 0:
            
            turn = turn + 1
            cg = 1
            while cg == 1:
                choice = []
                if plh + prh == 0:
                    break
                
                # random choice generator
                det = int(y + y ** (2.3) - y ** 1.6)
                result = det % 5
                comp = act[result]
                choice.append(comp)

                # assembling choice options
                for var in range(0 , len(cwisechoice) , 1):
                    if cwisechoice[var] == [plh , prh , clh , crh]:
                        choice.append(cwisechoice[var + 1])

                chosen = (3 * y - y **2) % (len(choice))        
                comp = choice[chosen]

                # choice becoming action

                if comp == act[0]:                          
                    if clh == 0 or crh == 0:
                        if clh == 2 or crh == 2:
                            clh = 1
                            crh = 1
                            cg = 0
                        if clh == 4 or crh == 4:
                            clh = 2
                            crh = 2
                            cg = 0
                if comp == act[1]:
                    plh = plh + clh
                if comp == act[2]:
                    prh = prh + clh
                if comp == act[3]:
                    plh = plh + crh
                if comp == act[4]:
                    prh = prh + crh
                if (clh != 0 and comp in act[1:3]) or (crh != 0 and comp in act[3:5]):
                    cg = 0
                y = y + 1

            # player hand death condition
            if plh > 4:
                plh = 0
            if prh > 4:
                prh = 0
            
            # upload situation and action of computer
            pgoodmove.append(csave)
            pgoodmove.append(comp)
            psave = [clh , crh , plh , prh]
            '''print('computer status:' , csave , comp)
            print('')'''

            # victory and special conditions
            
            if plh + prh == 0:
                for x in range(0 , len(pgoodmove) , 1):
                    pwisechoice.append(pgoodmove[x])

                compwin = compwin + 1
                '''print('YOU LOSE :(')
                print('game:' , game)
                print('compwin:' , compwin)
                print('player database:' , pwisechoice)'''
                break

        # relay game status
        '''print('player\'s left hand:' , plh , 'player\'s right hand:' , prh)
        print('computer\'s left hand:' , clh , 'computer\'s right hand:' , crh)
        print('')'''


        # End training condition
        if game > end:
            print('SUCCESS!!' , compwin , playerwin)
            break
    if game > end:
        break

print('FINISH')
          







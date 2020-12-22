# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:03:33 2020

CC07 Group 5 Blackjack

Ankita (Initialisation)
Elliot (Decision & Wincombo)
Carmen (Score & Points)
Fatima (End of Round)
Ke Wei (Displayconsole & Integration of whole programme)
"""
import random
import time

'''
Initialisation Functions
'''
def Welcome(): #Prints opening statements
    print('Welcome to Blackjack!')
    print('Rules: Each player attempts to beat the dealer by getting a count as close to 21 as possible,\nwithout going over 21.')

def newdict(): #Creates new dictionary (dd), returns dd
    playerdict =  {0: {'hand':[],'money':0, 'bet':0 ,'played': True,'stillplaying': False, 'wincombo': False, 'deck': [] },
                    1: {'hand':[],'money':0, 'bet':0 ,'played': False,'stillplaying': False, 'wincombo': False},
                    2: {'hand':[],'money':0, 'bet':0 ,'played': False,'stillplaying': False, 'wincombo': False},
                    3: {'hand':[],'money':0, 'bet':0 ,'played': False,'stillplaying': False, 'wincombo': False},
                    4: {'hand':[],'money':0, 'bet':0 ,'played': False,'stillplaying': False, 'wincombo': False}
                    }
    playerdict[0]['deck'] = newdeck()
    return playerdict

def newdeck(): #returns a new shuffled-deck list
    deck=[2,3,4,5,6,7,8,9,10,11,12,13,14]*4
    random.shuffle(deck)
    return deck

def draw(i,dd): #Takes int (player index) and dd, returns updated dd and deck
    value = str(dd[0]['deck'].pop())
    if value == '11':
        value = "J"
    elif value == '12':
        value = "Q"
    elif value == '13':
        value = "K"
    elif value == '14':
        value = "A"
    dd[i]['hand'].append(value)
    return dd

def deal(playdd): #Takes dd, loops through to draw card from player 1 to dealer (2 times). Returns udpated dd
    newdd = {}
    for i in range(2):
        for n in range(1,len(playdd)+1):
            if n == 5:
                newdd = draw(0,playdd)
            elif playdd[n]['stillplaying']:
                newdd = draw(n,playdd)
    print("\nDeal!")
    return newdd

def playerbet(dd): #Takes dd, Asks each playing player for bet, returns updated dd with new bet amount with deduction from money
    
    for i in range(1,len(dd)):
        inputcheck=True
        if (dd[i]['stillplaying']==True):
            money = dd[i]['money']
            while(inputcheck):
                string = "Player "+str(i)+" Please make a bet between $0-{}".format(str(money))
                try:
                    bet_amount=int(input(string+": "))
                    if bet_amount >0 and bet_amount < money+1:
                        dd[i]['bet']=bet_amount
                        dd[i]['money'] = dd[i]['money']-bet_amount
                        inputcheck= False
                    else:
                        print("Error! Please input within range!")
                except ValueError:
                    print("Error! Please input an integer.")
    return dd

def setPlayersnRounds(dd): #Takes dd, returns updated dd, possiblerounds and players (int) to play
    inputcheck = True
    while (inputcheck):
        try:
            number_players=int(input("How many players are there? (choose between 1 to 4): "))
            if(number_players>4 or number_players<1):
                print("Please choose the number between 1 to 4 again")
            else:
                inputcheck = False
                for i in range(0,number_players+1):
                    dd[i]["stillplaying"]= True
                    dd[i]["played"]= True
                    dd[i]['money']=1000
        except ValueError:
            print("Error! Please input an integer.")
    inputcheck= True
    while(inputcheck):  
        try:
            possible_rounds=int(input("How many rounds do you want to play?(1/5/10): "))
            if(possible_rounds==1 or possible_rounds==5 or possible_rounds==10):
                inputcheck= False
            else:
                print("Error! Try again!")
        except ValueError:
            print("Error! Please input an integer.")
    return dd, possible_rounds

def continueplaying(): #Asks if they want to start a new game, returns True/False
    inputcheck= True
    while(inputcheck):       
        userinput =input("Start another New Game? (Y/N): ").lower()
        if userinput == 'y':
            userinput = True
            inputcheck= False
        elif userinput == 'n':
            userinput = False
            inputcheck= False
        else:
            print("Error, Please try again!")
    return userinput

'''
Player/Dealer Decision & Handle Immediate Win-Combo Funtions
'''

def dealer(playerdict,roundcount): #Dealer's action Algorithm to draw/pass. Takes dd and current_round to displayconsole, returns updated dd
    print("Dealer's Turn...")
    time.sleep(3)
    dealerpoints = calculatescore(0, playerdict)
    cards_in_hand = playerdict[0]["hand"]
    
    while dealerpoints <= 16 and len(cards_in_hand) < 5:
            playerdict = draw(0,playerdict)
            cards_in_hand = playerdict[0]["hand"]
            dealerpoints = calculatescore(0, playerdict)

    displaycardsConsole(playerdict, roundcount)
    return playerdict

def player_decision(playerdict,currentrounds): #loops through players still playing, asks each player if they want to draw or pass. Then dealer will run its own algorithm of draw/passing
        
    for i in range(1, len(playerdict)+1):
        if i == 5: #Call dealer card draw algorithm
            playerdict = dealer(playerdict, currentrounds)   
        else: #do Deal/Pass query for Human Players
            cards_in_hand = playerdict[i]["hand"]
            played = playerdict[i]['played']
            stillplaying = playerdict[i]['stillplaying']
            if stillplaying and played:
                handamount = len(cards_in_hand)
                inputcheck = True
                while(inputcheck):
                    if handamount < 5:
                        option = 0
                        option = input('Player '+ str(i) +"\n(1) Draw more cards | (2) Pass : ")
                        if option == '1':
                            playerdict = draw(i,playerdict)
                            cards_in_hand = playerdict[i]['hand']
                            handamount = len(cards_in_hand)
                            displaycardsConsole(playerdict,currentrounds)
                        elif option == '2':
                            print('Player '+ str(i) +' Passed')
                            inputcheck = False
                        else:
                            print('Error. Please select your option again.')
                    else:
                        print('\nPlayer '+ str(i) + ' have reached the max cards in hand!')
                        inputcheck = False
            else:
                # print('Player '+ str(i) +" is not playing")
                pass

    return playerdict

def updateWincombo(playerdict): #Takes dd, checks for wincombo, return updated dd and ranking dict
    
    player_score = {0 : -1, 1 : -1, 2 : -1, 3: -1, 4 : -1} #-1 refers to not playing, 0 means no winningcombo, 1 means A10, 2 means AA
    winning_combo_1 = ["A", "A"]
    winning_combo_2 = ["A", '10']
    winning_combo_3 = ["A", "J"]
    winning_combo_4 = ["A", "Q"]
    winning_combo_5 = ["A", "K"]
    
    for players in playerdict: #Checks if they have winning combo and assigns ranking

        playerhand = playerdict[players]['hand']
        if players != 0:
            playerstring = "Player "+ str(players)
        else:
            playerstring = "Dealer"
            
        if playerhand == winning_combo_1:
            playerdict[players]['wincombo'] = True
            player_score[players] = 2
            print("{} has {}{} combo.".format(playerstring, 'A', 'A'))
        elif playerhand == winning_combo_2 or playerhand == winning_combo_2[::-1]:
            playerdict[players]['wincombo'] = True
            player_score[players] = 1
            print("{} has {}{} combo.".format(playerstring, 'A', winning_combo_2[1]))
        elif playerhand == winning_combo_3 or playerhand == winning_combo_3[::-1]:
            playerdict[players]['wincombo'] = True
            player_score[players] = 1
            print("{} has {}{} combo.".format(playerstring, 'A', winning_combo_3[1]))
        elif playerhand == winning_combo_4 or playerhand == winning_combo_4[::-1]:
            playerdict[players]['wincombo'] = True
            player_score[players] = 1
            print("{} has {}{} combo.".format(playerstring, 'A', winning_combo_4[1]))
        elif playerhand == winning_combo_5 or playerhand == winning_combo_5[::-1]:
            playerdict[players]['wincombo'] = True
            player_score[players] = 1
            print("{} has {}{} combo.".format(playerstring, 'A', winning_combo_5[1]))
        elif playerdict[players]['stillplaying']:
            player_score[players] = 0
            
    return playerdict,player_score

def checkdealerWincombo(playerdict,rankingdd): #Takes dd and ranking list, returns updated money for all players if dealer/player has wincombo. Those who can match dealer runs, if not lose 
    if rankingdd[0] == 2:
        print('Dealer has AA combo!\n')
        for i in range(1,len(rankingdd)):
            if not(rankingdd[i] == -1):
                bet = playerdict[i]['bet']
                if rankingdd[0]>rankingdd[i]: #player gets lower than AA, loses 3x of bet
                    loss = bet*3
                    playerdict[i]['money'] -= bet*2 #2 because 1x amount is already taken out of 'money'
                    print("Player {} loses triple (${}) :c".format(i,loss))
                else: #player gets same as dealer, no payout
                    playerdict[i]['money'] += bet
                    print("Player {0} has the same combo as Dealer! Player {0} Runs!".format(i))
                 
    elif rankingdd[0] == 1:
        print('Dealer has A10-type combo!\n')
        for i in range(1,len(rankingdd)):
            if not(rankingdd[i] == -1):
                bet = playerdict[i]['bet']
                if rankingdd[0]>rankingdd[i]: #Dealer's A10 larger than player, loses 2x bet
                    loss =  bet*2
                    playerdict[i]['money'] -= bet
                    print("Player {} loses double (${}) :c".format(i,loss))
                elif rankingdd[0]==rankingdd[i]: #player gets same as dealer, no payout
                    playerdict[i]['money'] += bet
                    print("Player {0} has the same combo as Dealer! Player {0} Runs!".format(i))
                else: #player gets AA, 3 times payout from bet amount
                    winnings = bet*3
                    playerdict[i]['money'] += bet*4 #4x because inclusive of bet amount
                    print("Player {} congratz! You win triple (${}) c:".format(i,winnings))
    else:
        for i in range(1,len(rankingdd)):
            if not(rankingdd[i] == -1):
                bet = playerdict[i]['bet']
                if rankingdd[i]==2: #Player has AA, wins 3x of bet
                    winnings = bet*3
                    playerdict[i]['money'] += bet*4 #4x because inclusive of bet amount
                    print("Player {} congratz! You win triple (${}) c:".format(i,winnings))
                elif rankingdd[i]==1: #Player has A10, wins 2x of bet
                    winnings = bet*2
                    playerdict[i]['money'] += bet*3
                    print("Player {} congratz! You win double (${}) c:".format(i,winnings))
    return playerdict

'''
Check and Update Scores Function
'''
def calculatescore(i,dd):
    player_list = []
    for card in (dd[i]['hand']):
        if (card == 'J') or (card == 'Q') or (card == 'K'):
            card = 10
            player_list.append(int(card))
        elif (card == 'A'):
            card = 14
            player_list.append(int(card))
        else:
            player_list.append(int(card))
    number_of_aces = 0
    for card in player_list:
        current_points = 0
        if card == 14:
            number_of_aces += 1
        if len(player_list) == 2: #case when 2 cards, Ace takes 11/10 ,no need to consider instant wins 
            if number_of_aces == 1: 
                current_points =player_list[0] + player_list[1] - 3
            elif number_of_aces == 0:
                current_points = player_list[0] +player_list[1] 
        elif len(player_list) == 3:#case when 3 cards Ace takes 10/1   
            if number_of_aces == 2:
                current_points = player_list[0] + player_list[1] + player_list[2] - 8
            elif number_of_aces == 1: 
                current_points = player_list[0] + player_list[1] + player_list[2] - 4             
                if current_points > 21:
                    current_points = current_points - 9  
            elif number_of_aces == 0:
                current_points = player_list[0] +player_list[1] +player_list[2]               
        elif len(player_list) == 4:#case when 4 cards,ace takes value 1 only 
            if number_of_aces == 4:
                current_points = 4                
            elif number_of_aces == 3:
                current_points = player_list[0] + player_list[1] +  player_list[2] + player_list[3] - (13*3)                
            elif number_of_aces == 2:
                current_points = player_list[0] + player_list[1] + player_list[2] +  player_list[3] - (13*2)                
            elif number_of_aces == 1:
                current_points =  player_list[0] + player_list[1] + player_list[2] +  player_list[3] - 13                
            else:
                current_points =  player_list[0] +player_list[1] + player_list[2] +player_list[3]               
        elif len(player_list) == 5:#case when 5 cards, ace takes value of 1 only
            if number_of_aces == 4:
                current_points =  player_list[0] + player_list[1] + player_list[2] + player_list[3] +player_list[4] - (13*4)                
            elif number_of_aces == 3:
                current_points =  player_list[0] +player_list[1] + player_list[2] +player_list[3] + player_list[4] - (13*3)                
            elif number_of_aces == 2: 
                current_points =  player_list[0] + player_list[1] + player_list[2] +player_list[3] + player_list[4] - (13*2)                
            elif number_of_aces == 1:
                current_points = player_list[0] + player_list[1] + player_list[2] + player_list[3] + player_list[4] - 13
            else:
                current_points =  player_list[0] + player_list[1] + player_list[2] + player_list[3] + player_list[4]                                   
    return current_points    

def calculatefinalscore(dd):#convert to points as integer values 
    for i in range(5):
        if dd[i]['stillplaying'] == False:
            pass
        elif dd[i]['stillplaying'] == True:
             dd[i]['points'] = calculatescore(i,dd) 
    return dd

def compare_playerpoints_with_bankerpoints(dd):#function that updates the current points into the playerdict
    dd = calculatefinalscore(dd)
    banker_points = dd[0]['points']       #for loop to update the points in the dictionary 

    for i in range(1,5):
        if dd[i]['stillplaying'] == False :
            pass
        elif dd[i]['stillplaying'] == True:
            if dd[i]['wincombo'] == True:
                continue    
            elif dd[i]['wincombo'] == False:
                player_points = dd[i]['points']
                player_bet = dd[i]['bet']
                loss = 0
                winning = 0
                if len(dd[i]['hand']) == 5:#it will check whether the 5card hand win or lose
                    if player_points > 21:
                        loss = 2*player_bet
                        print('Player {}, you busted with max cards! You lose double (${}) :c'.format(i,loss))
                        dd[i]['money'] -= player_bet
                    elif player_points <= 21:
                        winning = 2*player_bet
                        print('Player {} congratz! You win double (${}) c:'.format(i,winning))
                        dd[i]['money'] += 3*player_bet
                
                elif len(dd[i]['hand'])<5:
                    
                    if player_points < 16: #under limit
                        loss = 2*player_bet
                        print('Player {}, you did not take enough cards! You lose double (${}) :c '.format(i,loss))
                        dd[i]['money'] -= player_bet
                    elif player_points > 21: #over limit           
                        if banker_points > 21:
                            print('Player {}, you and the Dealer busted! No win, no lose c:'.format(i))
                            dd[i]['money'] += player_bet
                        elif banker_points <= 21: #under limit
                            loss = player_bet
                            print('Player {}, you busted! You lose (${}) :c'.format(i,loss))
                    elif player_points >= 16 and player_points <= 21: #within limits
                        if banker_points > 21:#dealer bust
                            winning = player_bet
                            print('The Dealer busted! Player {}, you win (${}) c:'.format(i,winning))
                            dd[i]['money'] += 2*player_bet
                        elif banker_points >= 16 and banker_points <= 21:
                            if player_points > banker_points: #if player > dealer
                                winning = player_bet
                                print('Player {}, you beat the Dealer! you win (${}) c:'.format(i,winning))
                                dd[i]['money'] += 2*player_bet
                            elif player_points == banker_points: #runs
                                print('Player {}, you and the Dealer run! No win, no lose c:'.format(i))
                                dd[i]['money'] += player_bet
                            elif player_points < banker_points: #if player < dealer
                                loss = player_bet
                                print('Player {}, the Dealer beat you! You lose (${}) :c'.format(i,loss))
    return dd

'''
End of Round Functions
'''

def resetnewrd_player(dd): #Takes and resets bet, points, hand and wincombo
    for player in dd:
        dd[player]['bet'] = 0 
        dd[player]['points'] = 0
        dd[player]['hand'] = [] 
        dd[player]['wincombo'] = False
    dd[0]['deck']=newdeck() #resets deck
    return dd

def nomoneynoplay(dd):# Takes dd, updates boolean for player with money <= 0
    for i in range(1,len(dd)):
        if dd[i]['money'] <= 0:
            dd[i]['stillplaying'] = False
    return dd
            
def decision_to_continue(dd,currentrounds):#Asks players if they want to gamble more?
    continued = True
    dd = nomoneynoplay(dd)
    if checkplayersleft(dd)>0:
        showHighscore(dd,currentrounds,continued)
        for i in range(1,len(dd)):
            if dd[i]['stillplaying'] == True:
                while True:
                    string = "Player "+ str(i) +" - Do you wish to gamble more? (Y/N) : "
                    decision = input(string).lower()
                    if decision == "n":
                        dd[i]['stillplaying'] = False
                        if checkplayersleft(dd) == 0:
                            continued = False
                        break
                    elif decision == "y":
                        break
                    else:
                        print("Error! Please try again")
                        continue
    else:
        continued = False
        print("There are no more active players!")
        showHighscore(dd,currentrounds,continued)
    return dd, continued

def checkplayersleft(dd): #Checks dd and returns amount of players still playing excludes dealer
    count = 0
    for i in range(1,len(dd)):
        if dd[i]['stillplaying'] == True:
            count+=1
    return count

'''
Display Console Functions
'''

def findplayersPlaying(dd): #Takes dictionary, Returns updated dictionary with those still playing
    playingdd={}
    for i in range(len(dd)): #loops through each element in dd
        if dd[i]["stillplaying"]: #True
            playingdd[i]=dd[i]
    # print(playingdd) #Checks if working
    return playingdd

def pharseHands(pdd): #Takes dd, returns the cardslist [strs] & playerlist [player key] of current players

    cardslist=[] #stores hand list in respective order
    playerlist=[] #stores player key
    for i,playerdd in pdd.items(): #loops through current player dictionary
        templist=[]
        cards=""
        playerhands = playerdd["hand"] #Readable variable to point to 'hand' key
        for n in range(5): #loop through 5 times for each potential hand
            if len(playerhands) < n+1:
                templist.append("░░")
            else: #for 2 digit chars, only 10 in this case
                if playerhands[n]== '10':
                    templist.append(playerhands[n])
                else: #for 1 digit chars
                    templist.append("░"+playerhands[n])
        #Format and concatenate the list of formatted 'hand' strings from templist
        cards = f'│{templist[0]}░││{templist[1]}░││{templist[2]}░││{templist[3]}░││{templist[4]}░│'
        cardslist.append(cards)
        playerlist.append(i)
        
    if len(pdd) <5: #adds empty card sets for end of list to display for players not playing
        for i in range(5-len(pdd)):
            cardslist.append('│░░░││░░░││░░░││░░░││░░░│')
            
    return cardslist,playerlist
    
def displaycardsConsole(playerdict,roundcount): #Takes dd, Displays console (main display function)
        
    cards, players = pharseHands(findplayersPlaying(playerdict))

    
    topbracket = "┌───┐┌───┐┌───┐┌───┐┌───┐"
    botbracket = "└───┘└───┘└───┘└───┘└───┘"
    
    #print current round
    r0 = 52
    roundstr = "[ROUND  "+ str(roundcount)+"]"
    print(f'{roundstr:>{r0}}')

    #Used to normalise the positions of each line
    l0 = 50
    l0Offset= 10
    l1 = 27
    l1Offset = 8
    l2 = 50
    
    print(f'{"DEALER":>{l0}}')
    print(f'{topbracket:>{l0+l0Offset}}')
    print(f'{cards[0]:>{l0+l0Offset}}')
    print(f'{botbracket:>{l0+l0Offset}}')
    
    l2Name = l3Name = l4Name = "No Player"
    l1Name = "Player " + str(players[1])
    
    if len(players) == 3:
        l2Name = "Player " + str(players[2])
    elif len(players) == 4:
        l2Name = "Player " + str(players[2])
        l3Name = "Player " + str(players[3])
    elif len(players) == 5:
        l2Name = "Player " + str(players[2])
        l3Name = "Player " + str(players[3])
        l4Name = "Player " + str(players[4])
        
    
    l1NameHolder = f'{l1Name:>{l1}}'
    l2NameHolder = f'{l2Name:>{l2}}'
    l1TopBracket = f'{topbracket:>{l1+l1Offset}}'
    l2TopBracket = f'{topbracket:>{l2}}'
    l1CardHolder = f'{cards[1]:>{l1+l1Offset}}'
    l2CardHolder = f'{cards[2]:>{l2}}'
    l1BotBracket = f'{botbracket:>{l1+l1Offset}}'
    l2BotBracket = f'{botbracket:>{l2}}'
    print(l1NameHolder+l2NameHolder)
    print(l1TopBracket+l2TopBracket)
    print(l1CardHolder+l2CardHolder)
    print(l1BotBracket+l2BotBracket)
    
    l3NameHolder = f'{l3Name:>{l1}}'
    l4NameHolder = f'{l4Name:>{l2}}'
    l3TopBracket = f'{topbracket:>{l1+l1Offset}}'
    l4TopBracket = f'{topbracket:>{l2}}'
    l3CardHolder = f'{cards[3]:>{l1+l1Offset}}'
    l4CardHolder = f'{cards[4]:>{l2}}'
    l3BotBracket = f'{botbracket:>{l1+l1Offset}}'
    l4BotBracket = f'{botbracket:>{l2}}'
    print(l3NameHolder+l4NameHolder)
    print(l3TopBracket+l4TopBracket)
    print(l3CardHolder+l4CardHolder)
    print(l3BotBracket+l4BotBracket)

def displayemptycardConsole(): #Takes dd, Displays Empty Hands and Empty Players on Console (use when new game)
        
    topbracket = "┌───┐┌───┐┌───┐┌───┐┌───┐"
    midContents= '│░░░││░░░││░░░││░░░││░░░│'
    botbracket = "└───┘└───┘└───┘└───┘└───┘"
    
    #Used to normalise the positions of each line
    l0 = 50
    l0Offset= 10
    l1 = 27
    l1Offset = 8
    l2 = 50
    
    print(f'{"DEALER":>{l0}}')
    print(f'{topbracket:>{l0+l0Offset}}')
    print(f'{midContents:>{l0+l0Offset}}')
    print(f'{botbracket:>{l0+l0Offset}}')
    
    l1Name = l2Name = "No Player"
    
    for i in range(2):
        l1NameHolder = f'{l1Name:>{l1}}'
        l2NameHolder = f'{l2Name:>{l2}}'
        l1TopBracket = f'{topbracket:>{l1+l1Offset}}'
        l2TopBracket = f'{topbracket:>{l2}}'
        l1CardHolder = f'{midContents:>{l1+l1Offset}}'
        l2CardHolder = f'{midContents:>{l2}}'
        l1BotBracket = f'{botbracket:>{l1+l1Offset}}'
        l2BotBracket = f'{botbracket:>{l2}}'
        print(l1NameHolder+l2NameHolder)
        print(l1TopBracket+l2TopBracket)
        print(l1CardHolder+l2CardHolder)
        print(l1BotBracket+l2BotBracket)
   
def showHighscore(playerdict,roundcount,continued): #Takes dd, current roundcount and bool ended, Sorts order of player & scores in descending order
    scorelist = []
    namelist = [] 
    
    for i,dd in playerdict.items():
        if i == 0 or not(dd['played']): #checks if the player has played at the start of game, if not player is skipped
            pass
        else:
            scorelist.append(dd['money'])
            namelist.append(i)
    
    #bubblesort algorithm taken from https://runestone.academy/runestone/books/published/pythonds/SortSearch/TheBubbleSort.html
    for passnum in range(len(scorelist)-1,0,-1):
        for i in range(passnum):
            if scorelist[i]<scorelist[i+1]:
                temp = scorelist[i] #holds old value
                ntemp = namelist[i] 
                scorelist[i] = scorelist[i+1] #updates old with new
                namelist[i] = namelist[i+1]
                scorelist[i+1] = temp #reassign new with old value
                namelist[i+1] = ntemp
    # print(namelist)
    # print(scorelist)
    
    #If Else to change title of score display (Round/Highscore)
    if continued:
        if roundcount == 10:
            l0 = 52
            l0Offset = 7
        else:
            l0 = 51
            l0Offset= 8
        stringtitle = "Round "+str(roundcount)
       
    else:
        stringtitle = "HIGHSCORE"
        l0 = 53
        l0Offset= 6

    
    #Used to normalise the positions of each line

    l1 = 50
    l1Offset = 8
    topbracket = "───────────────────────"
    print(f'{stringtitle:>{l0}}')
    print(f'{topbracket:>{l0+l0Offset}}')
    for i,value in enumerate(namelist):
        midContents = str(i+1) + ". Player " + str(value)+" : "+ \
                        f'{str(scorelist[i]):>7}'#Justify score portion to right
        print(f'{midContents:>{l1+l1Offset}}')

'''
Game function!
'''
def blackjack():
    Welcome()
    playing = True
    while (playing):
        
        displayemptycardConsole()
        #Initial variables
        playerdict = newdict()
        current_round = 1
        playerdict, possible_rounds = setPlayersnRounds(playerdict)
        continued = True
        while (continued):
            #Round initialisation
            
            playerdict = playerbet(playerdict) #Asks players to place bets
            playerdict = deal(playerdict) #Deal 2 cards and update dd
            displaycardsConsole(playerdict, current_round)#Display cards after Deal
            
            #Action Phase
            playerdict = player_decision(playerdict,current_round)
            
            #Compare winning-combos if any
            playerdict,rankingdd = updateWincombo(playerdict)
            playerdict = checkdealerWincombo(playerdict, rankingdd)
            
            #Compare hands to Dealer (non-winning combo) and calculate winnings/loss
            playerdict = compare_playerpoints_with_bankerpoints(playerdict)
            
            
            if current_round < possible_rounds: #Checks if current round has reached the last round
                playerdict, continued = decision_to_continue(playerdict,current_round)
                playerdict = resetnewrd_player(playerdict)
            else:
                continued = False
                showHighscore(playerdict,current_round,continued)
            
            current_round +=1
        
        playing = continueplaying()
        if not(playing):
            print("Thank you for playing our Blackjack game! :)")

if __name__ == "__main__":
    blackjack()
        
            
        
    
    
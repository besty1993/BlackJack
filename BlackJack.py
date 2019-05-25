import random

def Score(hand) :
    score = 0
    aces = 0
    for card in hand :
        if card in [2,3,4,5,6,7,8,9] :
            score += card
        elif card in [10,11,12,13] :
            score += 10
        else :
            aces += 1
    if score+aces*11 > 21 :
        return score+aces
    else :
        return score+aces*11

class BlackJack () :
    def __init__ (self) :        
        self.deck = [2,3,4,5,6,7,8,9,10,11,12,13,1] *4
        random.shuffle(self.deck)
        
        self.playerHand = []
        self.dealerHand = []
        
        
        self.usedCards = []
        self.game_result = []
        self.preparation()

        self.done = False
        self.reward = 0
    
    def play(self, n, strategy) :
        for i in range(n) :
            if self.playerHand == [] :
                self.preparation()
            self.player_play(strategy)
            self.turn_end_and_dealer_play()
            self.finish(i)
            print(sum(self.game_result)/len(self.game_result))
        print("Win Rate : {}".format(sum(self.game_result)/len(self.game_result)))
        return self.state, self.reward, self.done

    def Result(self) :
        return self.game_result

    def Step(self, action) :
        if self.Done() :
            self.preparation()
        if action and Score(self.playerHand) < 21 :
            self.hit(self.playerHand)  
        if Score(self.playerHand) == 21 :
            self.finish(1)
        elif Score(self.playerHand) > 21:
            self.finish(1)
        else :
            self.turn_end_and_dealer_play()
            self.finish(1)
        print(Score(self.playerHand))
        print(self.playerHand)
            
        return self.State(), self.Reward(), self.Done()

    def State(self) :
        # p = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        # d = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        # u = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        # for hand in self.playerHand :
        #     p[hand-1] += 1
        # for hand in [self.dealerHand[0]] :
        #     d[hand-1] += 1
        # for hand in self.usedCards :
        #     u[hand-1] += 1
        # return p+d+u
        return [Score(self.playerHand)/21, Score([self.dealerHand[0]])/21]

    def Reward(self) :
        return self.reward

    def Done(self) :
        return self.done
    
    def preparation(self) :
        self.usedCards = self.usedCards + self.playerHand + self.dealerHand
        temp = self.usedCards
        self.playerHand = []
        self.dealerHand = []
        self.hit(self.playerHand)
        self.hit(self.playerHand)
        self.hit(self.dealerHand)
        self.hit(self.dealerHand)
        self.reward = 0
        self.done = False
        return
        
    def reshuffle(self) :
        if not len(self.deck) ==  0 : return
        else :
            self.deck = self.usedCards
            self.usedCards = []
            random.shuffle(self.deck)
#             print("Reshuffled")
            return
        
    def hit(self,hand) :
        if len(self.deck) == 0 :
            self.reshuffle()
        card = self.deck.pop()
#         print(str(hand) +" hit! "+ str(card))
        hand.append(card)
        return hand
    
    def turn_end_and_dealer_play(self) :
        while Score(self.dealerHand) < 17 :
            self.hit(self.dealerHand)
        return self
    
    def player_play(self, strategy) :
        while True :
            player = self.playerHand
            dealer = self.dealerHand
            used = self.usedCards
            if strategy(player, dealer, used) and Score(player) < 21 :
                self.hit(self.playerHand)
            else :
                return
    
    def finish(self, gameNum) :
        self.done = True
        playerScore = Score(self.playerHand)
        dealerScore = Score(self.dealerHand)
#         print("GAME"+str(gameNum)+", Player : " + str(playerScore) + ", Dealer : " + str(dealerScore), end=', ')
        log = "GAME {}: Player {}, Dealer {} ".format(gameNum+1, playerScore, dealerScore)
        if playerScore > 21:
            log = log + "Dealer Win"
            self.reward = -1
            self.game_result.append(False)
        elif playerScore == 21 or playerScore > dealerScore or dealerScore >21 :
            log = log + "Player Win"
            self.reward = 1
            self.game_result.append(True)
        elif playerScore == dealerScore :
            log = log + "Draw"
            self.reward = 0
            self.game_result.append(True)
        else :
            log = log + "Dealer Win"
            self.reward = -1
            self.game_result.append(False)
        # print(log)

if __name__ =='__main__' :
    def strategy (player, dealer, used) :
        return Score(player) < 14

    blackjack = BlackJack()
    A = blackjack.play(1000, strategy)
    # print(sum(A.game_result)/len(A.game_result))
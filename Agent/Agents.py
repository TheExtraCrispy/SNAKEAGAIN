import random
import keyboard
import time
class Agent():
    def __init__(self, parameters) -> None:
        self.params = parameters
        self.fitness = 0
    
    #Chooses the best of 3 moves, represented as floats of probability that that move is best. 
    #eg:(0.5, 0.4, 0.1) ordered as Left, Straight, Right
    
    #using softmax maybe?

    #Choose move, make move, evaluate score of move.
    def MakeMove(self, g):
        distToFood = g.GetDistance(g.snake.head, g.food)        
        move = self.ChooseMove()
        ateFood = g.snake.MakeMove(move)

        newDistToFood = g.GetDistance(g.snake.head, g.food)

        change = distToFood-newDistToFood

        #Points for eating food
        if(ateFood):
            self.fitness += self.params["ateFoodScore"]
        #Moved towards or away from food
        elif(change>0):
            self.fitness += self.params["towardsFoodScore"]
        else:
            self.fitness += self.params["awayFoodScore"]

        



    def ChooseMove(self):
        #Implemented by agent
        raise NotImplementedError

class RandomAgent(Agent):
    def ChooseMove(self):
        options = ["left", "straight", "right"]
        picked = random.choice(options)
        return picked 

class HumanPlayer(Agent): #Controls are inverted because i flipped something somewhere, it works though
    def ChooseMove(self):
        if keyboard.is_pressed("left"):
           return "right"
        elif keyboard.is_pressed("right"):
            return "left"
        else:
            return "straight"
        
        
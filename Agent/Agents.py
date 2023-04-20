import random
import keyboard
import time
import tensorflow
import numpy as np
from Game.Grid import Direction


class Agent():
    def __init__(self) -> None:
        self.steps = 0
        self.movement = 0.0
        self.foodEaten = 0
        self.died = False
    

    def reset(self):
        self.steps = 0
        self.movement = 0.0
        self.foodEaten = 0
        self.died = False
    #Chooses the best of 3 moves, represented as floats of probability that that move is best. 
    #eg:(0.5, 0.4, 0.1) ordered as Left, Straight, Right
    
    #using softmax maybe?

    #Choose move, make move, evaluate score of move.
    def MakeMove(self, g):
        distToFood = g.GetDistance(g.snake.head, g.food)        
        move = self.ChooseMove()
        state = g.snake.MakeMove(move)

        newDistToFood = g.GetDistance(g.snake.head, g.food)

        change = distToFood-newDistToFood
        
        #Points for eating food
        if(state==1):
            self.foodEaten += 1
        #Moved towards or away from food
        elif(change>0):
            self.movement += 1.0
        else:
            self.movement += -1.5

        if(state==-1):
            self.died = True
        self.steps += 1



    def ChooseMove(self):
        #Implemented by agent
        raise NotImplementedError

class RandomAgent(Agent):
    def ChooseMove(self):
        picked = random.randint(0,2)
        return picked 

class HumanPlayer(Agent): #Controls are inverted because i flipped something somewhere, it works though
    def ChooseMove(self):
        if keyboard.is_pressed("left"):
           return 2
        elif keyboard.is_pressed("right"):
            return 0
        else:
            return 1
        

class AIAgent(Agent):
        def __init__(self, model):
            super().__init__()
            self.model = model
            self.energyMax = 100
            self.energy = self.energyMax

        def setModel(self, model):
            self.model = model
            self.energy = self.energyMax

        def getInput(self, g):
            input = []
            
            heading = g.snake.heading
            #Gets the current position and direction of it's head
            input += g.snake.head.GetPosition()
            input += [heading.value]

            #Looks at what points are left, forward, and right, and how far away they are
            input += g.snake.Look(Direction.rotateCW(heading))
            input += g.snake.Look(heading)
            input += g.snake.Look(Direction.rotateCCW(heading))

            #Gets the size of the snake and the size of the board
            input += [g.snake.bodySize]
            input += [g.colNum]
            input += [g.rowNum]

            #Gets the position and manhattan distance from head to food
            input += g.food.GetPosition()
            input += [g.GetDistance(g.snake.head, g.food)]
            
            return np.array(input, dtype=np.float32)
            

        def MakeMove(self, g):
            distToFood = g.GetDistance(g.snake.head, g.food)

            input = self.getInput(g)
            move = self.ChooseMove(input)
            state = g.snake.MakeMove(move)

            newDistToFood = g.GetDistance(g.snake.head, g.food)

            change = distToFood-newDistToFood
            self.energy -= 1
            #Points for eating food
            if(state==1):
                self.foodEaten += 1
                self.energy = self.energyMax
            #Moved towards or away from food
            elif(change>0):
                self.movement += 1
            else:
                self.movement += -1

            if(state==-1):
                self.died = True
            self.steps += 1
            if(self.energy <= 0):
                g.GameOver()
                self.died = True


        def ChooseMove(self, input):
            input = tensorflow.expand_dims(input, axis=0)
            choices = self.model(input)
            bestChoice = np.argmax(choices)
            return bestChoice

            
from Agent.Agents import AIAgent
from Game.Grid import Grid
from Game.GUI import GUI
import tensorflow
import pygad.kerasga
import numpy as np

class Population():
    def __init__(self, config, model=None):
        self.config = config
        if(model != None):
            print("loading model")
        self.model = model
        
            
        self.agent = AIAgent(self.model)
        self.grid = Grid(config["gridHeight"],config["gridWidth"], self.agent)
        self.grid.Setup()

    def run(self, populationSize, generations, parents, modelName):
        self.gencount = 0
        self.gentarget = generations
        self.modelName = modelName
        modelGA = pygad.kerasga.KerasGA(model=self.model, num_solutions=populationSize)
        initialPopulation = modelGA.population_weights

        GA = pygad.GA(num_generations=generations,
                      num_parents_mating=parents,
                      initial_population=initialPopulation,
                      fitness_func=self.fitness,
                      on_generation=self.genCallback,
                      parallel_processing=10)
        GA.run()

        solution = GA.best_solution()[0]
        bestWeights = pygad.kerasga.model_weights_as_matrix(model=self.model, weights_vector=solution)

        GA.plot_fitness(title=modelName, linewidth=4)
        self.model.set_weights(bestWeights)
        self.saveModel("Agent\\Models\\"+modelName)
    
   
    def fitness(self, inst, solution, sol_idx):
        modelWeights = pygad.kerasga.model_weights_as_matrix(model=self.model, weights_vector=solution)
        self.model.set_weights(weights=modelWeights)
        
        self.agent.setModel(self.model)
        self.agent.reset()
        self.grid.reset()

        #gui = GUI(self.config, self.grid)
        #gui.startGameLoop()

        self.grid.startLoopNoGUI()

        score = 0
        score += self.agent.foodEaten*50
        score += self.agent.movement
        score += self.agent.died*-50

        #print("Model", sol_idx, "Done!")
        #print("Fitness:", score)
        #print("Steps:", self.agent.steps)
        #print()
        return score

    def genCallback(self, ga):
        self.gencount += 1
        print("Generation", self.gencount, "of", self.gentarget, "finished!")
        print()
        if(self.gencount%50==0):
            self.saveModel("Agent\\Models\\"+self.modelName)

    
        

    #-------------------Model Functions------------------
     #layers is a list of tuples, with an integer count and a string activation function
    #It does NOT include the input or output layers
    
    def buildModel(self, layers):
        model = tensorflow.keras.Sequential()
        #15
        model.add(tensorflow.keras.layers.Dense(layers[0], activation=tensorflow.nn.relu, input_shape=[15,]))
        for size in layers[1:]:
            print("Adding layer with size", size)
            model.add(tensorflow.keras.layers.Dense(size, activation=tensorflow.nn.relu))
        
        model.add(tensorflow.keras.layers.Dense(3, activation=tensorflow.nn.softmax))

        #adam = tensorflow.keras.optimizers.Adam()
        #model.compile(loss='mse', optimizer=adam)
        #if(weights):
        #    model.load_weights(weights)
        return model

    def loadModel(path):
        model = tensorflow.keras.models.load_model(path)
        return model
    
    def saveModel(self, path):
        self.model.save(path)

    def setModel(self, model):
        self.model = model
    
    def getModel(self):
        return self.model
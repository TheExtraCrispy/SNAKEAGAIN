from Agent.Agents import AIAgent
from Game.Grid import Grid
from Game.GUI import GUI
import tensorflow
import pygad.kerasga
import numpy as np

class Population():
    def __init__(self, config, model=None):
        self.config = config
        self.model = self.buildModel()
        self.agent = AIAgent(self.model)
        self.grid = Grid(config["gridHeight"],config["gridWidth"], self.agent)

    def run():
        return

        
   
    def fitness(self, inst, solution, sol_idx):
        modelWeights = pygad.kerasga.model_weights_as_matrix(model=self.model, weights_vector=solution)
        self.model.set_weights(weights=modelWeights)
        
        self.agent.setModel(self.model)
        self.agent.reset()
        self.grid.Setup()
        #gui = GUI(self.config, grid)
        #gui.startGameLoop()

        self.grid.startLoopNoGUI()
        score = 0
        score += self.agent.foodEaten*50
        score += self.agent.movement
        score += self.agent.died*-50

        print("Model", sol_idx, "Done!")
        print("Fitness:", score)
        print("Steps:", self.agent.steps)
        print()
        return score

    def genCallback(self, ga):
        print("Generation finished!")
        print()

    def test(self):
        modelGA = pygad.kerasga.KerasGA(model=self.model, num_solutions=10)
        initialPopulation = modelGA.population_weights

        GA = pygad.GA(num_generations=10,
                      num_parents_mating=2,
                      initial_population=initialPopulation,
                      fitness_func=self.fitness,
                      on_generation=self.genCallback)
        GA.run()
        #GA.plot_fitness(title="OHMAN", linewidth=4)

    #-------------------Model Functions------------------
     #layers is a list of tuples, with an integer count and a string activation function
    #It does NOT include the input or output layers
    
    def buildModel(self):
        model = tensorflow.keras.Sequential()
        #15
        model.add(tensorflow.keras.layers.Dense(32, activation=tensorflow.nn.relu, input_shape=[15,]))
        model.add(tensorflow.keras.layers.Dense(32, activation=tensorflow.nn.relu))
        model.add(tensorflow.keras.layers.Dense(3, activation=tensorflow.nn.softmax))

        #adam = tensorflow.keras.optimizers.Adam()
        #model.compile(loss='mse', optimizer=adam)
        #if(weights):
        #    model.load_weights(weights)
        return model

    def loadModel(path):
        model = tensorflow.keras.models.load_model(path)
        return model
    
    def saveModel(model, path):
        model.save(path)

    def setModel(self, model):
        self.model = model
    
    def getModel(self):
        return self.model
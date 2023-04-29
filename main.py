from Game.Grid import Grid
from Game.GUI import GUI
from Game.Point import PointType
from Agent.Agents import *
from Agent.Training import Population
import tensorflow

tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)

conf = {
    "gridHeight": 30,
    "gridWidth": 30,
    "canvasSize": 800,
    "updateRate": 100,
    "colorPalette": {
        PointType.EMPTY: '#2a2a2b',
        PointType.WALL: '#141414',
        PointType.FOOD: '#8bf739',
        PointType.HEAD: '#2450f0',
        PointType.BODY: '#18328f'},
}

#Sets up a grid instance, with a specified agent player
def setupGrid(agent):
    cols = conf["gridHeight"]
    rows = conf["gridWidth"]
    grid = Grid(cols, rows, agent)
    grid.Setup()
    return grid

#Creates an runs a game with the given agent, displays game on screen
def runGameGUI(agent):
    grid = setupGrid(agent)
    gui = GUI(conf, grid)
    gui.startGameLoop()

#Creates and runs a game without displaying on screen, runs much faster
def runGameNoGUI(agent):
    grid = setupGrid(agent)
    grid.startLoopNoGUI(throttle=0)


#Loads a model by name, and runs a game on screen using that model
def RunAI(modelName):
    model = tensorflow.keras.models.load_model("Agent\\Models\\"+modelName)
    #print(model.layers)
    agent = AIAgent(model)
    runGameGUI(agent)

#Creates a new model of a given name, with the given architecture
#Trains the model according to the given parameters, saves it under given name
def MakeModel(modelName, layers, populationSize, generations, parents):
    pop = Population(conf)
    pop.buildModel(layers, modelName)
    pop.run(populationSize, generations, parents, modelName)

#Trains an existing model by creating a 1 parent population based on it,
#and running the GA according to the given parameters. New resulting model
#will overwrite previous model.
def TrainModel(modelName, populationSize, generations, parents):
    pop = Population(conf, modelName=modelName)
    pop.run(populationSize, generations, parents, modelName)

#Displays a plot of the average and peak fitness of the most recent GA run.
def plotStats():
    import matplotlib.pyplot as plt

    with open("avg.csv", 'r') as file:
        avg = [round(float(line.strip()), 3) for line in file.readlines()]
        
    with open("peak.csv", 'r') as file:
        peak = [round(float(line.strip()), 3) for line in file.readlines()]
    fig, axs = plt.subplots(1,2, figsize=(10,5))

    axs[0].plot(avg)
    axs[0].set_title("Average Fitness")
    axs[0].set_xlabel("Generations")
    axs[0].set_ylabel("Fitness")
    
    axs[1].plot(peak)
    axs[1].set_title("Peak Fitness")
    axs[1].set_xlabel("Generations")
    axs[1].set_ylabel("Fitness")

    plt.show()


#Make New
#layers = [10, 10]
#MakeModel("TrueJohnSnake", layers, 200, 10000, 2) 

#Run AI
RunAI("TrueJohnSnake")

#Quick train (for demo)
#TrainModel("Waltuh2", 10, 5, 2)

#Long Train
#TrainModel("Waltuh2", 500, 1000, 2)


#plotStats()
from Game.Grid import Grid
from Game.GUI import GUI
from Game.Point import PointType
from Agent.Agents import *
from Agent.Training import Population
import tensorflow

tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)

defaultParameters = {
      "ateFoodScore": 50,
      "towardsFoodScore": 2,
      "awayFoodScore": -1,
}

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

#with open("config.json", 'r') as configFile:
#    conf = json.load(configFile)

def setupGrid(agent):
    cols = conf["gridHeight"]
    rows = conf["gridWidth"]
    grid = Grid(cols, rows, agent)
    grid.Setup()
    return grid

def runGameGUI(agent):
    grid = setupGrid(agent)
    gui = GUI(conf, grid)
    gui.startGameLoop()

def runGameNoGUI(agent):
    grid = setupGrid(agent)
    grid.startLoopNoGUI(throttle=0)

def QuickStart(agent):
    runGameGUI(agent)

def RunAI(modelName):
    model = tensorflow.keras.models.load_model("Agent\\Models\\"+modelName)
    agent = AIAgent(model)
    runGameGUI(agent)
def MakeModel(modelName, layers, populationSize, generations, parents):
    pop = Population(conf)
    pop.buildModel(layers, modelName)
    pop.run(populationSize, generations, parents, modelName)

def TrainModel(modelName, populationSize, generations, parents):
    pop = Population(conf, modelName=modelName)
    pop.run(populationSize, generations, parents, modelName)



#--------------FOR DEMO-----------------

#Make New
#layers = [24, 12]
#MakeModel("NewModel", layers, 20, 5, 2)

#Run AI
#RunAI("Waltuh")

#Quick train
#TrainModel("test", 10, 5, 2)

#Long Train
TrainModel("Waltuh", 200, 2500, 20)
from Game.Grid import Grid
from Game.GUI import GUI
from Game.Point import PointType
from Agent.Agents import *
from Agent.Training import Population


defaultParameters = {
      "ateFoodScore": 50,
      "towardsFoodScore": 2,
      "awayFoodScore": -1,
}

conf = {
    "gridHeight": 40,
    "gridWidth": 40,
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


pop = Population(conf)
pop.test()
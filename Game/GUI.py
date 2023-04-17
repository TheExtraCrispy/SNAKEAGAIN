import tkinter as tk
from tkinter import ttk
from Game.Grid import Grid
from Game.Point import PointType

class MainMenu:
    def __init__(self) -> None:
        print("TODO")
    
    def startup(self):
        self.r = tk.Tk()

class GUI:
    def __init__(self, config, grid):
        self.conf = config
        self.grid = None
        self.gameCanvas = None
        self.grid = grid
        

    def startGameLoop(self):
        self.grid.gameRunning = True
        self.setupWindow(self.grid.gameLoop)    
        
    def setupWindow(self, gameLoop):
        self.r = tk.Tk()
        r = self.r
        r.title("Snake")
        r.configure(bg='#262626')
        r.resizable(False, False)

        #Sizing according to grid
        canvasSize = self.conf["canvasSize"]
        smaller = min(self.grid.colNum, self.grid.rowNum)
        ratio = (self.grid.colNum/smaller, self.grid.rowNum/smaller)
        geom = str(round(canvasSize/ratio[1]))+"x"+str(round(canvasSize/ratio[0]))
        r.geometry(geom)

        #Set up canvas and size of pixels
        self.pixelSize = min(canvasSize//self.grid.colNum, canvasSize//self.grid.rowNum)
        self.gameCanvas = tk.Canvas(master=r, width=round(canvasSize/ratio[1]), height=round(canvasSize/ratio[0]), bg=self.conf["colorPalette"][PointType.EMPTY])
        self.gameCanvas.pack(anchor=tk.CENTER)
        self.drawGame(gameLoop)
        r.mainloop()
    
    def pickColor(self, type):
        return self.conf["colorPalette"][type]

    

    def drawGame(self, gameLoop):
        canvas = self.gameCanvas
        canvas.delete(tk.ALL)
        for x in range(self.grid.colNum):
            for y in range(self.grid.rowNum):
                x1 = x*self.pixelSize
                x2 = x1+self.pixelSize

                y1 = y*self.pixelSize
                y2 = y1+self.pixelSize

                pointType = self.grid.getPoint(x, y).GetType()
                if(pointType != PointType.EMPTY):
                    canvas.create_rectangle(x1, y1, x2, y2, fill=self.pickColor(pointType))
        
        
        if(self.grid.gameRunning):
            canvas.after(self.conf["updateRate"], self.drawGame, gameLoop)
            gameLoop()
        else:
            print("Game over!")
            print("Score:", self.grid.agent.fitness)
            print("")
            self.r.after(1000, self.r.destroy)
        canvas.update()

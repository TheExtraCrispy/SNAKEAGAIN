from Game.Point import Point, PointType
from Game.Grid import Grid, Direction
from collections import deque
class Snake:
    
    def __init__(self, grid, startSize, heading):
        self.heading = heading
        self.bodySize = startSize
        self.grid = grid
        self.body = deque()
        self.heading = None
        self.head = None
        

    def BuildBody(self, position, heading):
        self.heading = heading
        #Adding head first
        curSegment = self.grid.getPoint(*position)
        curSegment.SetType(PointType.HEAD)
        self.body.append(curSegment)
        self.head = curSegment

        #Adding remainder of body off of head
        buildDir = Direction.reverse(heading)
        while(len(self.body) < self.bodySize):
            nextSegment = self.grid.getAdjPoint(curSegment, buildDir)
            
            #Turn if obstacle in way of body
            if(nextSegment.GetType() != PointType.EMPTY):
                buildDir = Direction.rotateCW(buildDir)
            else:
                curSegment = nextSegment
                curSegment.SetType(PointType.BODY)
                self.body.append(curSegment)
            
    
    #Moves in current direction, returns true if food was eaten
    def MoveForward(self):
        #Get head and spot snake is about to move into
        head = self.body[0]
        newPos = self.grid.getAdjPoint(head, self.heading)

        #Snake has eaten food, same as normal movement, just doesn't delete tail
        if newPos.GetType() == PointType.FOOD:
            head.SetType(PointType.BODY)
            newPos.SetType(PointType.HEAD)
            self.body.appendleft(newPos)
            self.grid.placeRandomFood()
            self.head = newPos
            return True

        #Snake has hit itself or a wall
        elif newPos.GetType()!=PointType.EMPTY:
            self.grid.GameOver()
        
        #Snake has moved into empty space
        else:
            #Remove end of tail
            tail = self.body.pop()
            tail.SetType(PointType.EMPTY)

            #Move head into space
            head.SetType(PointType.BODY)
            newPos.SetType(PointType.HEAD)
            self.body.appendleft(newPos)
            self.head = newPos
            return False
            
        

    def TurnRight(self):
        self.heading = Direction.rotateCW(self.heading)
        return self.MoveForward()

    def TurnLeft(self):
        self.heading = Direction.rotateCCW(self.heading)
        return self.MoveForward()

    def MakeMove(self, choice):
        if(choice == "left"):
            return self.TurnLeft()
        if(choice=="straight"):
            return self.MoveForward()
        if(choice == "right"):
            return self.TurnRight()
        
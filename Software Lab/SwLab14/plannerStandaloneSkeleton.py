import math
import lib601.ucSearch as ucSearch
import lib601.util as util
import lib601.basicGridMap as basicGridMap
import lib601.gridMap as gridMap
import lib601.sm as sm



######################################################################
###         Picking worlds
######################################################################

mapTestWorld = ['mapTestWorld.py', 0.2, util.Point(2.0, 5.5),
                util.Pose(2.0, 0.5, 0.0)]
bigPlanWorld = ['bigPlanWorld.py', 0.25, util.Point(3.0, 1.0),
                util.Pose(1.0, 1.0, 0.0)]


class GridDynamics(sm.SM):
    
    legalInputs = None
    
    def __init__(self, theMap):
        pass

    def getNextValues(self, state, inp):
        pass



class TestGridMap(gridMap.GridMap):
    def __init__(self, gridSquareSize):
        gridMap.GridMap.__init__(self, 0, gridSquareSize * 5,
                               0, gridSquareSize * 5, gridSquareSize, 100)

    def makeStartingGrid(self):
        grid = util.make2DArray(5, 5, False)
        for i in range(5):
            grid[i][0] = True
            grid[i][4] = True
        for j in range(5):
            grid[0][j] = True
            grid[4][j] = True
        grid[3][3] = True
        return grid

    def robotCanOccupy(self, (xIndex, yIndex)):
        return not self.grid[xIndex][yIndex]

def testGridDynamics():
    gm = TestGridMap(0.15)
    print 'For TestGridMap(0.15):'
    r = GridDynamics(gm)
    print 'legalInputs', util.prettyString(r.legalInputs)
    ans1 = [r.getNextValues((1,1), a) for a in r.legalInputs]
    print 'starting from (1,1)', util.prettyString(ans1)
    ans2 = [r.getNextValues((2,3), a) for a in r.legalInputs]
    print 'starting from (2,3)', util.prettyString(ans2)
    ans3 = [r.getNextValues((3, 2), a) for a in r.legalInputs]
    print 'starting from (3,2)', util.prettyString(ans3)
    gm2 = TestGridMap(0.4)
    print 'For TestGridMap(0.4):'
    r2 = GridDynamics(gm2)
    ans4 = [r2.getNextValues((2,3), a) for a in r2.legalInputs]
    print 'starting from (2,3)', util.prettyString(ans4)

def planner(initialPose, goalPoint, worldPath, gridSquareSize):
    pass

def testPlanner(world):
    (worldPath, gridSquareSize, goalPoint, initialPose) = world
    planner(initialPose, goalPoint, worldPath, gridSquareSize)



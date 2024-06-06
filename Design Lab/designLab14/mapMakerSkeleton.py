import math
import lib601.sonarDist as sonarDist
import lib601.sm as sm
import lib601.util as util
import lib601.gridMap as gridMap
import lib601.dynamicGridMap as dynamicGridMap
import lib601.dynamicCountingGridMap as dynamicCountingGridMap
import bayesMapSkeleton as bayesMap
reload(bayesMap)

class MapMaker(sm.SM):
    def __init__(self, xMin, xMax, yMin, yMax, gridSquareSize):
         self.startState = dynamicGridMap.DynamicGridMap(xMin, xMax, yMin, yMax, gridSquareSize)
         #self.startState = bayesMap.BayesGridMap(xMin, xMax, yMin, yMax, gridSquareSize)
    def getNextValues(self, state, inp):
        sonar=inp.sonars
        pose=inp.odometry
        #code:
        #for i in range(len(sonarDist.sonarPoses)):
            #if sonar[i]< sonarDist.sonarMax:
                #black=state.pointToIndices(sonarDist.sonarHit(sonar[i],sonarDist.sonarPoses[i],pose))
                #state.setCell(black)
        #return (state,state)
        #improvement:
        for i in range(len(sonarDist.sonarPoses)):
            if sonar[i]< sonarDist.sonarMax:
                black=state.pointToIndices(sonarDist.sonarHit(sonar[i],sonarDist.sonarPoses[i],pose))#hits location
                state.setCell(black)
                for j in util.lineIndices(state.pointToIndices(pose.transformPoint(sonarDist.sonarPoses[i].point())),black)[:-1]:#clear
                    state.clearCell(j)
            else :
                sonar[i]=sonarDist.sonarMax#To a valid value
                black=state.pointToIndices(sonarDist.sonarHit(sonar[i],sonarDist.sonarPoses[i],pose))
                state.setCell(black)
                for j in util.lineIndices(state.pointToIndices(pose.transformPoint(sonarDist.sonarPoses[i].point())),black):
                    state.clearCell(j)
        return(state,state)
    #testMapMaker(testData)
class SensorInput:
    def __init__(self, sonars, odometry):
        self.sonars = sonars
        self.odometry = odometry

testData = [SensorInput([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
                        util.Pose(1.0, 2.0, 0.0)),
            SensorInput([0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                        util.Pose(4.0, 2.0, -math.pi))]

testClearData = [SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
                             util.Pose(1.0, 2.0, 0.0)),
                 SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
                             util.Pose(4.0, 2.0, -math.pi))]

def testMapMaker(data):
    (xMin, xMax, yMin, yMax, gridSquareSize) = (0, 5, 0, 5, 0.1)
    mapper = MapMaker(xMin, xMax, yMin, yMax, gridSquareSize)
    mapper.transduce(data)
    mapper.startState.drawWorld()

def testMapMakerClear(data):
    (xMin, xMax, yMin, yMax, gridSquareSize) = (0, 5, 0, 5, 0.1)
    mapper = MapMaker(xMin, xMax, yMin, yMax, gridSquareSize)
    for i in range(50):
        for j in range(50):
            mapper.startState.setCell((i, j))
    mapper.transduce(data)
    mapper.startState.drawWorld()

def testMapMakerN(n, data):
    (xMin, xMax, yMin, yMax, gridSquareSize) = (0, 5, 0, 5, 0.1)
    mapper = MapMaker(xMin, xMax, yMin, yMax, gridSquareSize)
    mapper.transduce(data*n)
    mapper.startState.drawWorld()

testClearData = [SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
                             util.Pose(1.0, 2.0, 0.0)),
                 SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
                             util.Pose(4.0, 2.0, -math.pi))]


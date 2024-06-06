import lib601.dist as dist
import lib601.util as util
import lib601.colors as colors
import lib601.ssm as ssm
import lib601.seFast as seFast
import lib601.dynamicGridMap as dynamicGridMap

import py_compile
py_compile.compile('bayesMapSkeleton.py')
# Define the stochastic state-machine model for a given cell here.
#The car is running in soar:
hitP1 = 0.1
freeP1 = 0.9
'''
step15 parameter:
hitP1=0.05
freeP1=0.95
'''
hitP2 = 0.75
freeP2 = 0.25
initPOcc = 0.3
occ_max = 0.75
# Observation model:  P(obs | state)
def oGivenS(state):
    if state == 'empty':
        return dist.DDist({'hit': hitP1, 'free': freeP1})
    return dist.DDist({'hit': hitP2, 'free': freeP2})   
# Transition model: P(newState | s | a)
def uGivenAS(a):
     return lambda s: dist.DDist({s: 1.0})

cellSSM = ssm.StochasticSM(dist.DDist({'occ': initPOcc, 'empty': 1 - initPOcc}), uGivenAS, oGivenS)

class BayesGridMap(dynamicGridMap.DynamicGridMap):    
    def squareColor(self, (xIndex, yIndex)):
        p = self.occProb((xIndex, yIndex))
        if self.robotCanOccupy((xIndex,yIndex)):
            return colors.probToMapColor(p, colors.greenHue)
        elif self.occupied((xIndex, yIndex)):
            return 'black'
        else:
            return 'red'
    def occProb(self, (xIndex, yIndex)):
        sm = self.grid[xIndex][yIndex]
        return sm.state.prob('occ')  
    def makeStartingGrid(self):
        def makeEstimator(ix, iy):
            m = seFast.StateEstimator(cellSSM)
            m.start()
            return m
        return util.make2DArrayFill(self.xN, self.yN, makeEstimator)

    def setCell(self, (xIndex, yIndex)):
        sm = self.grid[xIndex][yIndex]
        sm.step(('hit', None))
        self.drawSquare((xIndex, yIndex))
        return
    def clearCell(self, (xIndex, yIndex)):
        sm = self.grid[xIndex][yIndex]
        sm.step(('free', None))
        return
        self.drawSquare((xIndex, yIndex))
    def occupied(self, (xIndex, yIndex)):
        Pr_occ = self.occProb((xIndex, yIndex))
        return Pr_occ > occ_max   

mostlyHits = [('hit', None), ('hit', None), ('hit', None), ('free', None)]
mostlyFree = [('free', None), ('free', None), ('free', None), ('hit', None)]

def testCellDynamics(cellSSM, input):
    se = seFast.StateEstimator(cellSSM)
    return se.transduce(input)


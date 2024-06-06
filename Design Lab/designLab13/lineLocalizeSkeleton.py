import lib601.util as util
import lib601.util as util
import lib601.dist as dist
import lib601.distPlot as distPlot
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.sonarDist as sonarDist
import lib601.move as move
import lib601.seGraphics as seGraphics
import lib601.idealReadings as idealReadings

# For testing your preprocessor
class SensorInput:
    def __init__(self, sonars, odometry):
        self.sonars = sonars
        self.odometry = odometry

preProcessTestData = [SensorInput([0.8, 1.0], util.Pose(1.0, 0.5, 0.0)),
                       SensorInput([0.25, 1.2], util.Pose(2.4, 0.5, 0.0)),
                       SensorInput([0.16, 0.2], util.Pose(7.3, 0.5, 0.0))]
testIdealReadings = ( 5, 1, 1, 5, 1, 1, 1, 5, 1, 5 )
testIdealReadings100 = ( 50, 10, 10, 50, 10, 10, 10, 50, 10, 50 )


class PreProcess(sm.SM):
    
    def __init__(self, numObservations, stateWidth):
        self.startState = (None, None)
        self.numObservations = numObservations
        self.stateWidth = stateWidth

    def getNextValues(self, state, inp):
        (lastUpdatePose, lastUpdateSonar) = state
        currentPose = inp.odometry
        currentSonar = idealReadings.discreteSonar(inp.sonars[0],
                                                   self.numObservations)
        # Handle the first step
        if lastUpdatePose == None:
            return ((currentPose, currentSonar), None)
        else:
            action = discreteAction(lastUpdatePose, currentPose,
                                    self.stateWidth)
            print (lastUpdateSonar, action)
            return ((currentPose, currentSonar), (lastUpdateSonar, action))


# Only works when headed to the right
def discreteAction(oldPose, newPose, stateWidth):
    return int(round(oldPose.distance(newPose) / stateWidth))


def makeRobotNavModel(ideal, xMin, xMax, numStates, numObservations):

    startDistribution = dist.squareDist(0, numStates)    # redefine this

    def observationModel(ix):
        # ix is a discrete location of the robot
        # return a distribution over observations in that state
        # if ix < numObservations:
        #     d = dist.DeltaDist(dist.triangleDist(ideal[ix], (xMax - xMin) / numObservations))
        # else:
        #     d =
        d1 = dist.triangleDist(ideal[ix], 4)
        d2 = dist.DeltaDist(numObservations - 1)
        d3 = dist.squareDist(0, numObservations)
        md1 = dist.MixtureDist(d1, d2, 0.9)
        return dist.MixtureDist(md1, d3, 0.95)

    def transitionModel(a):
        # a is a discrete action
        # returns a conditional probability distribution on the next state
        # given the previous state
        def x(previous_state):
            if a + previous_state > numStates - 1:
                
                return dist.DeltaDist(numStates - 1)
            elif a + previous_state == numStates - 1:
                return dist.MixtureDist(dist.DeltaDist(numStates-1), dist.DeltaDist(numStates-2), 0.9)
            else:
                return dist.MixtureDist(dist.DeltaDist(a+previous_state), dist.MixtureDist(dist.DeltaDist(a+previous_state - 1), dist.DeltaDist(a + previous_state + 1), 0.5), 0.8)
        return x

    return ssm.StochasticSM(startDistribution, transitionModel,
                            observationModel)


# Main procedure
def makeLineLocalizer(numObservations, numStates, ideal, xMin, xMax, robotY):
    pre_process = PreProcess(numObservations, (xMax - xMin)/numStates)#预处理
    estimator = seGraphics.StateEstimator(makeRobotNavModel(ideal, xMin, xMax, numStates, numObservations))#状态估计
    driver = move.MoveToFixedPose(util.Pose(xMax, robotY, 0.0), maxVel=0.5)#驱动程序
    return sm.Cascade(sm.Parallel(sm.Cascade(pre_process, estimator), driver), sm.Select(1))#组装出的复合机器


#model = makeRobotNavModel(testIdealReadings, 0.0, 10.0, 10, 10)
#d = model.observationDistribution(7)
# distPlot.plot(d)

#ppEst1 = sm.Cascade(PreProcess(10, 1), seGraphics.StateEstimator(makeRobotNavModel(testIdealReadings, 0.0, 10.0, 10, 10)))
#ppEst1.transduce(preProcessTestData)

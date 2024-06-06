import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

class MySMClass(sm.SM):
    startState='go_straight'#初始化
    furtherState='turn_right'
    def getNextValues(self, state, inp):
        print(state)
        if state=='go_straight':#开始行动
            if ((inp.sonars[2] < 0.25 and inp.sonars[5] < 0.25) or inp.sonars[3]<0.15 or inp.sonars[4]<0.15 or (inp.sonars[3] < 0.2 and inp.sonars[4] < 0.2) or inp.sonars[2] + inp.sonars[3] + inp.sonars[4] + inp.sonars[6] < 0.75):
                return ('conor', io.Action(fvel=-0.3, rvel=0.4))  # 墙角
            elif inp.sonars[3]>0.5 and inp.sonars[4]>0.5 and inp.sonars[0]>0.5 and inp.sonars[7]>0.5:
                return ('go_straight',io.Action(fvel = 0.1,rvel = 0))
            else:
                return ('near',io.Action(fvel = 0.08,rvel = 0))


        if state=='conor':
            if ((inp.sonars[2] < 0.25 and inp.sonars[5] < 0.25) or inp.sonars[3]<0.15 or inp.sonars[4]<0.15 or (inp.sonars[3] < 0.2 and inp.sonars[4] < 0.2) or inp.sonars[2] + inp.sonars[3] + inp.sonars[4] + inp.sonars[6] < 0.75):
                return ('conor', io.Action(fvel=-0.3, rvel=0.4)) 
            elif inp.sonars[3]>0.5 and inp.sonars[4]>0.5 and inp.sonars[0]>0.5 and inp.sonars[7]>0.5:
                return ('go_straight',io.Action(fvel = 0.1,rvel = 0))
            else:
                return ('near',io.Action(fvel = 0.08,rvel = 0))
            
        if state =='near':#在墙边
            if ((inp.sonars[2] < 0.25 and inp.sonars[5] < 0.25) or inp.sonars[3]<0.15 or inp.sonars[4]<0.15 or (inp.sonars[3] < 0.2 and inp.sonars[4] < 0.2) or inp.sonars[2] + inp.sonars[3] + inp.sonars[4] + inp.sonars[6] < 0.75):
                return ('conor', io.Action(fvel=-0.3, rvel=0.4)) 
            elif inp.sonars[3]>0.5 and inp.sonars[4]>0.5 and inp.sonars[0]>0.5 and inp.sonars[7]>0.5:
                return ('go_straight',io.Action(fvel = 0.1,rvel = 0))

            if inp.sonars[0]+inp.sonars[1]+inp.sonars[2]+inp.sonars[3]<inp.sonars[4]+inp.sonars[5]+inp.sonars[6]+inp.sonars[7]:#在左墙边
                furtherState='turn_right'
            else:#在右墙边
                furtherState='turn_left'
        #此处上下部分可以合并省去一个判断，为了好看才分开写的
            if furtherState=='turn_right':
                if (inp.sonars[0]<0.4 or inp.sonars[1]<0.4) and  inp.sonars[1] < 0.5:
                    return ('near', io.Action(fvel=-0.08, rvel=-0.5))
                elif (inp.sonars[0]<0.4 or inp.sonars[1]<0.4) and  inp.sonars[1] > 0.5:
                        return ('near', io.Action(fvel=0.08, rvel=-0.3))
                else:
                    return ('near',io.Action(fvel = 0.1,rvel = 0))
            elif furtherState=='turn_left':
                if (inp.sonars[6] < 0.4 or inp.sonars[7] < 0.4) and inp.sonars[6] < 0.5:
                    return ('near', io.Action(fvel=-0.08, rvel=0.5))
                elif (inp.sonars[6] < 0.4 or inp.sonars[7] < 0.4) and inp.sonars[6] > 0.5:
                    return ('near', io.Action(fvel=0.08, rvel=0.3))
                else:
                    return ('near',io.Action(fvel = 0.1,rvel = 0))


mySM = MySMClass()
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=True) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    ipt = [1,1,1,1,1,1,1,1]
    inp = io.SensorInput()
    #print(inp.sonars[0])
    for i in range(8):
        ipt[i]=inp.sonars[i]
    print(ipt)
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass

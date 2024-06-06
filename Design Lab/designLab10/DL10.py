import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io




class MySMClass(sm.SM):
    startState =  ['go',5,5,0] #第四个值代表flag
    def getNextValues(self, state, inp):
        if ( -state[2]+ inp.sonars[7]>=0.5) and state[1]>1 and state[3] != 2:
            state[3]=1
            state[0]='right'
        elif (-state[1]+ inp.sonars[0]>=0.5)and state[2]>1 and state[3] != 1:
            state[3]=2
            state[0]='left'
        else:
            state[1]= inp.sonars[0]
            state[2]= inp.sonars[7]
            if inp.sonars[0]<=0.3 or inp.sonars[1]<=0.33:
                 state[0] = 'right'
                 return (state,io.Action(fvel=0.05, rvel=-0.3))
            if inp.sonars[6]<=0.33 or inp.sonars[7]<=0.3:
                 state[0] = 'left'
                 return (state,io.Action(fvel=0.05, rvel=0.3))
            if inp.sonars[3]<=0.5 or inp.sonars[4]<=0.5:
                if inp.sonars[0]+inp.sonars[1]<=inp.sonars[6]+inp.sonars[7]:
                    state[0] = 'right'
                    return (state,io.Action(fvel=0.05, rvel=-0.3))
                else:
                    state[0] = 'left'
                    return (state,io.Action(fvel=0.05, rvel=0.3))
        print('state',state)
        print('state[3]',state[3])
        state[1] = inp.sonars[0]
        state[2] = inp.sonars[7]
        if state[3] ==0:
            state[0] = 'go'
            return (state, io.Action(fvel=0.3, rvel=0))
        else:
            if   state[3]==2:
                if inp.sonars[0]+inp.sonars[1]<=0.8:
                    state[3]=0
                return (state,io.Action(fvel=0.2, rvel=0.4))
            elif  state[3]==1:                
                if inp.sonars[6]+inp.sonars[7]<=0.8:
                    state[3]=0
                return (state,io.Action(fvel=0.2, rvel=-0.4))
        

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
                                  sonarMonitor=False) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    print inp.sonars[0] , inp.sonars[3] ,inp.sonars[7]     #打印三号声呐距离障碍物的距离,最远是1.5，大于1.5则一直显示5  
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass

import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

import os
labPath = os.getcwd()
from sys import path
if not labPath in path:
    path.append(labPath)
    print 'setting labPath to', labPath

######################################################################
###
###  If you want to call boundaryFollowerClass.py to 
###  implement the eyewall walk,please uncomment the following
###
###################################################################### 
from boundaryFollower import boundaryFollowerClass

######################################################################
###
###  If you want to call DL2.py to 
###  implement the eyewall walk,please uncomment the following
###
###################################################################### 
##from DL2 import DL2Class


class MySMClass(sm.SM):
    def __init__(self):
		pass
    def getNextValues(self, state, inp):
        V_Pot = inp.analogInputs[1]#voltage of the pot
        V_Motor = inp.analogInputs[2]#voltage of the 
        V_Pot_half = 5
        V_half = 10.5
        V_high = 10.2
        V_low = 9.8
        k1 = 0.5 #rotate gain
        k2 = 0.1 #speed gain
        rotatev = k1*(V_Pot_half - V_Pot)
        forwardv = k2*(V_Motor - V_half)
        print V_Pot
        print V_Motor
        if V01 <= 4.8 or V01 >= 5.2:##rotate
            return state, io.Action(fvel = 0, rvel = rotatev)
        else:
            if V02 >= V_low and V02 <= V_high:##stop
                return state, io.Action(fvel = 0, rvel = 0)
            else:##go/boundaryfollow
        ##################################################################################################
        ##If you want to call boundaryFollowerClass.py to implement the eyewall walk,please uncomment the following
        ##################################################################################################
                return boundaryFollowerClass.getNextValues(self, state, inp)
        ##################################################################################################
        ##If you want to call DL2.py to implement the eyewall walk,please uncomment the following
        ##################################################################################################
                ##return DL2Class.getNextValues(self, state, inp)

mySM = MySMClass()
mySM.name = 'brainSM'

# 取消注释使用沿墙走
# mySM = boundaryFollowerClass()

######################################################################
###
###          Brain methods
###
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False)

def brainStart():
    robot.behavior = mySM
    robot.behavior.start(robot.gfx.tasks())
    robot.data = []

def step():
    inp = io.SensorInput()
    robot.behavior.step(inp).execute()

def brainStop():
    pass

def shutdown():
    pass

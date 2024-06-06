import lib601.sf as sf
import lib601.optimize as optimize
import operator
import lib601.poly as poly

def delayPlusPropModel(k1, k2):
    T = 0.1
    V = 0.1

    # Controller:  your code here
    controller = sf.FeedforwardAdd(sf.Gain(k1),sf.Casade(sf.R(),sf.Gain(k2)))
    # The plant is like the one for the proportional controller.  Use
    # your definition from last week.
    plant1 = sf.Cascade(sf.Cascade(sf.R(),sf.Gain(T)),sf.FeedbackAdd(sf.Gain(1),sf.R()))
    plant2 = sf.Cascade(sf.Cascade(sf.R(),sf.Gain(V*T)),sf.FeedbackAdd(sf.Gain(1),sf.R()))
    # Combine the three parts
    sys = sf.FeedbackSubstract(sf.Casade(controller,sf.Casade(plant1,plant2)))
    return sys

# You might want to define, and then use this function to find a good
# value for k2.

# Given k1, return the value of k2 for which the system converges most
# quickly, within the range k2Min, k2Max.  Should call optimize.optOverLine.

def bestk2(k1, k2Min, k2Max, numSteps):
    return optimize.optOverLine(lambda k2 : max(poly.Polynomial([1,-2,0.001*k1+1,0.001*k2]).roots(),key=abs),k2Min,k2Max,numSteps)

def anglePlusPropModel(k3, k4):
    T = 0.1
    V = 0.1

    # plant 1 is as before
    # plant1 = sf.FeedbackSubstract(sf.Gain(1),sf.Cascade(sf.R(),sf.Gain(T),sf.FeedbackAdd(sf.Gain(1),sf.R()))),sf.Gain(k4)
    # plant2 is as before
    # plant2 = sf.Cascade(sf.R(),sf.Gain(V*T),sf.FeedbackAdd(sf.Gain(1),sf.R()))
    plant1 = sf.Cascade(sf.Cascade(sf.R(), sf.Gain(T)), sf.FeedbackAdd(sf.Gain(1), sf.R()))
    plant2 = sf.Cascade(sf.Cascade(sf.R(), sf.Gain(V * T)), sf.FeedbackAdd(sf.Gain(1), sf.R()))
    # The complete system
    sys = sf.FeedbackSubstract(sf.Gain(1),sf.Cascade(sf.Gain(k3),sf.FeedbackSubstract(sf.Gain(k4)),plant1,plant2))

    return sys


# Given k3, return the value of k4 for which the system converges most
# quickly, within the range k4Min, k4Max.  Should call optimize.optOverLine.

def bestk4(k3, k4Min, k4Max, numSteps):
    return optimize.optOverLine(lambda k4: max(poly.Polynomial([1, 0.1*k4-2, 1-0.1*k4+0.001*k3]).roots(), key=abs),
                                k4Min, k4Max, numSteps)

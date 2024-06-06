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

import lib601.sig as sig
import math
import cmax.simulate as simulate

def testSignal(simTime = 2.5):
    nsteps = int(simTime/simulate.Tsim)
    print __name__, 'nsteps ', nsteps
    ninter = math.pi/nsteps
    return (nsteps,
	    sig.ListSignal([{'motorAngle':3*math.pi/4,'lightAngle':(5*math.pi/4)-(i*ninter),'lightDist':3} for i in range(nsteps+1)]))

(nsteps, sigIn) = testSignal()
def runTest(lines, parent = None, nsteps = nsteps,meter=None):
    simulate.runCircuit(lines, sigIn, parent, nsteps,meter=meter)


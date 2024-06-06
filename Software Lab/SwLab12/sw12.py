import lib601.dist as dist
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.util as util

class StateEstimator(sm.SM):
    def __init__(self, model):
        self.model = model
        self.startState = model.startDistribution

    def getNextValues(self, state, inp):
        td = self.model.transitionDistribution
        (o, i) = inp
        belief = self.efficientBayes(state, o)
        dSPrime = self.totalProbability(belief, td(i))
        return (dSPrime, dSPrime)
    def efficientBayes(self,state,observation):
        dict1 = {}
        state_name = state.support()
        Pr = 0
        for name in state_name:
            dist.incrDictEntry(dict1,name,self.model.observationDistribution(name).prob(observation)*state.prob(name))
            Pr += dict1[name]
        for i in dict1.keys():
            dict1[i] = dict1[i] / Pr
        return dist.DDist(dict1)
    def totalProbability(self, belief, transDist):
        total = {}
        states = belief.support()
        for s1 in states:
            for s2 in states:
                if s2 not in total.keys():                             
                    total[s2] = belief.prob(s1) * transDist(s1).prob(s2)
                else:
                    total[s2] += belief.prob(s1) * transDist(s1).prob(s2)
        # Normalise the values in the dictionary 
        for k, v in total.items():
            total[k] = v / sum(total.values())
        return dist.DDist(total)

# Test

transitionTable = \
   {'good': dist.DDist({'good' : 0.7, 'bad' : 0.3}),
    'bad' : dist.DDist({'good' : 0.1, 'bad' : 0.9})}
observationTable = \
   {'good': dist.DDist({'perfect' : 0.8, 'smudged' : 0.1, 'black' : 0.1}),
    'bad': dist.DDist({'perfect' : 0.1, 'smudged' : 0.7, 'black' : 0.2})}

copyMachine = \
 ssm.StochasticSM(dist.DDist({'good' : 0.9, 'bad' : 0.1}),
                # Input is irrelevant; same dist no matter what
                lambda i: lambda s: transitionTable[s],
                lambda s: observationTable[s])
obs = [('perfect', 'step'), ('smudged', 'step'), ('perfect', 'step')]

cmse = StateEstimator(copyMachine)

print cmse.transduce(obs)



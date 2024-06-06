import lib601.search as search
import lib601.sm as sm

# Indices into the state tuple.
(farmer, goat, wolf, cabbage) = range(4)

class FarmerGoatWolfCabbage(sm.SM):
   startState = ('L','L','L','L')
   legalInputs = ['takeGoat','takeNone','takeWolf','takeCabbage']
   def __init__(self):
       self.state = ('L','L','L','L')
   def getNextValues(self, state, action):
       if action == 'takeNone':
          if state[1] == state[3] or state[1] == state[2]:#Determining whether it is illegal
               state=state
          else:
               state=next1(state,0,0)#ChangeState
       if action=='takeGoat':
          if state[0] != state[1]:#Determining whether it is illegal
             state=state
          else :
             state = next1(state,0,1)#ChangeState
       if action == 'takeWolf':
          if state[0] != state[2] or state[1] == state[3]:#Determining whether it is illegal
             state=state
          else:
             state = next1(state,0,2)#ChangeState
       if action == 'takeCabbage':
          if state[0] != state[3] or state[1] == state[2]:#Determining whether it is illegal
             state=state
          else :
             state =next1(state,0,3)#ChangeState
       return (state,state)
   def done(self, state):
       return state == ('R','R','R','R')
def next1(state,Farmer,item):
      state = list(state)
      if item != 0:
         if state[item] == 'L':
               state[item] = 'R'
         else :
               state[item] = 'L'
      if state[Farmer] == 'L':
         state[Farmer] = 'R'
      else :
         state[Farmer] = 'L'
      state = tuple(state)
      return state
print search.smSearch(FarmerGoatWolfCabbage(),depthFirst=False, DP=True)

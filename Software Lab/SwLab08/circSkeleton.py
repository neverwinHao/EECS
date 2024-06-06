"""
Describe a circuit in terms of its components; generates equations and
solves them.
"""

import lib601.le as le
import lib601.util as util

class Circuit:
    def __init__(self, components):
        """
        @param components: list of instances of C{Component} that make
           up this circuit
        """
        self.components = components

    def solve(self, gnd):
        """
        @param gnd: Name of the node to set to ground (string)
        @returns: instance of C{le.Solution}, mapping node names to values
        """
        es = le.EquationSet()
        n2c = NodeToCurrents()
        
        # Add constituent constraints, and the node/current
        # information induced by each component.
        for c in self.components:
            es.addEquation(c.getEquation())
            n2c.addCurrents(c.getCurrents())
        
        # Add KCL constraints
        es.addEquations(n2c.getKCLEquations(gnd))

        print 'Solving equations'
        print '*****************'
        for e in es.equations: print e
        print '*****************'

        # Solve
        return es.solve()

class NodeToCurrents:
    """
    Keep track of which currents are flowing in and out of which
    nodes in a circuit.
    """
    def __init__(self):

################
# Your code here
################

    def addCurrent(self, current, node, sign):

################
# Your code here
################

    def addCurrents(self, currents):

################
# Your code here
################

    def getKCLEquations(self, gnd):

################
# Your code here
################


class Component:
    """
    Generic superclass.  Every component type has to provide
      - C{getCurrents(self)}: Returns a list of tuples C{(i, node, sign)},
        where C{i} is the name of a current variable, C{node} is the name
        of a node,  and C{sign} is the sign of that current at that node.
      - C{getEquation(self)}: Returns an instance of
        C{le.Equation}, representing the constituent equation for this
        component.  
    """
    
    def getCurrents(self):
        """
        Default method that works for components with two leads,
        assuming they define attributes C{current}, C{n1}, and C{n2}. 
        """
        return [[self.current, self.n1, +1],
                [self.current, self.n2, -1]]

class VSrc(Component):
    def __init__(self, v, n1, n2):
        """
        @param v: voltage in Volts (number);  equal to voltage at C{n1} minus voltage at C{n2} 
        @param n1: name of node at one end of the voltage source (string)
        @param n2: name of node at the other end of the voltage source (string)
        """
        self.current = util.gensym('i_'+n1+'->'+n2)
        """
        Name of the current variable for this component
        """
        self.n1 = n1
        self.n2 = n2
        self.v = v
        
    def getEquation(self):
        return le.Equation([1.0, -1.0],
                           [self.n1, self.n2],
                           self.v)

    def __str__(self):
        return 'VSrc('+str(self.v)+', '+self.n1+', '+self.n2+')'

class ISrc(Component):
    def __init__(self, i, n1, n2):
        """
        @param i: current, in Amperes (number), flowing from C{n1} to C{n2}
        @param n1: name of node at one end of the current source (string)
        @param n2: name of node at the other end of the current source (string)
        """
        self.current = util.gensym('i_'+n1+'->'+n2)
        """
        Name of the current variable for this component
        """
        self.n1 = n1
        self.n2 = n2
        self.i = i
        
    def getEquation(self):
        return le.Equation([1.0],
                           [self.current],
                           self.i)
    def __str__(self):
        return 'ISrc('+str(self.i)+', '+self.n1+', '+self.n2+')'

class Wire(Component):
    """
    Just describes a wire between nodes C{n1} and C{n2}; nodes are
    specified by their names (strings)
    """
    def __init__(self, n1, n2):
        self.current = util.gensym('i_'+n1+'->'+n2)
        """
        Name of the current variable for this component
        """
        self.n1 = n1
        self.n2 = n2

    def getEquation(self):
        return le.Equation([1.0, -1.0],
                           [self.n1, self.n2],
                           0)
    def __str__(self):
        return 'Wire('+self.n1+', '+self.n2+')'

class Resistor(Component):
    def __init__(self, r, n1, n2):
        """
        @param r: resistance in Ohms (number)
        @param n1: name of node at one end of the resistor (string)
        @param n2: name of node at the other end of the resistor (string)
        """
        self.current = util.gensym('i_'+n1+'->'+n2)
        """
        Name of the current variable for this component
        """
        self.n1 = n1
        self.n2 = n2
        self.r = r

    def getEquation(self):

################
# Your code here
################

class OpAmp(Component):

    def __init__(self, nPlus, nMinus, nOut, K=10000):
        """
        @param nPlus: name of positive input node (string)
        @param nMinus: name of negative input node (string)
        @param nOut: name of positive output node (string)
        @param K: constant in op-amp model (number)
        """
        self.K = K
        self.nPlus = nPlus
        self.nMinus = nMinus
        self.nOut = nOut
        self.current = util.gensym('i->'+nOut)
        """
        Name of the current variable for this component
        """

    def getCurrents(self):
        return [[self.current, self.nOut, +1]]

    def getEquation(self):

################
# Your code here
################


        

# Remove quotes to test the Resistor components
'''
div = Circuit([
    VSrc(10, '10v', 'gnd'),
    Resistor(1000, '10v', 'vo'),
    Resistor(1000, 'vo', 'gnd'),
    Resistor(10, 'vo', 'gnd')
    ])
print div.solve('gnd')
'''

# Remove quotes to test the Resistor and OpAmp components
'''    
buf = Circuit([
    VSrc(10, '10v', 'gnd'),
    Resistor(1000, '10v', 'vo'),
    Resistor(1000, 'vo', 'gnd'),
    OpAmp('vo', 'v-', 'vb'),
    Wire('vb', 'v-'),
    Resistor(10, 'vb', 'gnd')
    ])
print buf.solve('gnd')
'''

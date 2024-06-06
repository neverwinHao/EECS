"""
Class and some supporting functions for representing and manipulating system functions. 
"""

import math
import lib601.poly as poly
import lib601.util as util


class SystemFunction:
    """
    Represent a system function as a ratio of polynomials in R
    """
    def __init__(self, numeratorPoly, denominatorPoly):
        self.numerator=numeratorPoly
        self.denominator=denominatorPoly
    def __str__(self):
        return 'SF(' + self.numerator.__str__('R') + \
               '/' + self.denominator.__str__('R') + ')'

    __repr__ = __str__
    def poles(self):
        z=self.denominator.coeffs[:]
        z.reverse()
        Poly1=poly.Polynomial(z)
        return Poly1.roots()
    def poleMagnitudes(self):
        list1=[]
        list2=self.poles()
        for i in range(len(list2)):
            list1.append(abs(list2[i]))
        return list1
    def dominantPole(self):
         return util.argmax(self.poles(), abs)
def Cascade(sf1, sf2):
    return SystemFunction(sf1.numerator * sf2.numerator, sf1.denominator * sf2.denominator)

def FeedbackSubtract(sf1, sf2=None):
    numerator=sf1.numerator*sf2.denominator
    denominator=sf1.denominator*sf2.denominator+sf1.numerator*sf2.numerator
    return SystemFunction(numerator,denominator)

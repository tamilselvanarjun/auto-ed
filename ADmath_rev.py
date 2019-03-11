"""Module for performing special functions on ADnum objects.
Take an ADnum object as input and return an ADnum object as output.
For real number inputs, returns a real number.
"""
import numpy as np
from ADnum_rev import ADnum

#TRIGONOMETRIC FUNCTIONS
def sin(X):
    try:
        y = ADnum(np.sin(X.val), der = np.cos(X.val)*X.der, ops = (1-X.counted)*X.ops+2, rops =1)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'sin', np.cos(X.val)))
        return y
    except AttributeError:
        return np.sin(X)

def cos(X):
    try:
        y = ADnum(np.cos(X.val), der = -np.sin(X.val)*X.der, ops = (1-X.counted)*X.ops+3, rops=2)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'cos', -np.sin(X.val)))
        return y
    except AttributeError:
        return np.cos(X)

def tan(X):
    try:
        y = ADnum(np.tan(X.val), der = (1/np.cos(X.val)**2)*X.der, ops = (1-X.counted)*X.ops+4, rops=3)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'tan', (1/np.cos(X.val))**2))
        return y
    except AttributeError:
        return np.tan(X)

def csc(X):
    try:
        y = ADnum(1/np.sin(X.val), der = (-1/np.tan(X.val))*(1/np.sin(X.val))*X.der, ops = (1-X.counted)*X.ops+5, rops=4)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'csc',(-1/np.tan(X.val))*(1/np.sin(X.val))))
        return y
    except:
        return 1/np.sin(X)

def sec(X):
    try:
        y = ADnum(1/np.cos(X.val), der = np.tan(X.val)/np.cos(X.val)*X.der, ops = (1-X.counted)*X.ops+4, rops=3)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'sec', np.tan(X.val)/np.cos(X.val)))
        return y
    except AttributeError:
        return 1/np.cos(X)

def cot(X):
    try:
        y = ADnum(1/np.tan(X.val), der = -1/(np.sin(X.val)**2)*X.der, ops = (1-X.counted)*X.ops+4, rops=3)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'cot', -1/(np.sin(X.val)**2)))
        return y
    except AttributeError:
        return 1/np.tan(X)

#INVERSE TRIGONOMETRIC FUNCTIONS
def arcsin(X):
    try:
        y = ADnum(np.arcsin(X.val), der = 1/np.sqrt(1-X.val**2)*X.der, ops = (1-X.counted)*X.ops+5, rops=4)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'arcsin', 1/np.sqrt(1-X.val**2)))
        return y
    except AttributeError:
        return np.arcsin(X)

def arccos(X):
    try:
        y = ADnum(np.arccos(X.val), der = -1/np.sqrt(1-X.val**2)*X.der, ops = (1-X.counted)*X.ops+5, rops=4)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'arccos', -1/np.sqrt(1-X.val**2)))
        return y
    except AttributeError:
        return np.arccos(X)

def arctan(X):
    try:
        y = ADnum(np.arctan(X.val), der = 1/(1+X.val**2)*X.der, ops = (1-X.counted)*X.ops+4, rops=3)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'arctan', 1/(1+X.val**2)))
        return y
    except AttributeError:
        return np.arctan(X)

#HYPERBOLIC TRIG FUNCTIONS
def sinh(X):
    try:
        y = ADnum(np.sinh(X.val), der = np.cosh(X.val)*X.der, ops = (1-X.counted)*X.ops+2, rops=1)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'sinh', np.cosh(X.val)))
        return y
    except AttributeError:
        return np.sinh(X)

def cosh(X):
    try:
        y = ADnum(np.cosh(X.val), der = np.sinh(X.val)*X.der, ops=(1-X.counted)*X.ops+2, rops=1)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'cosh', np.sinh(X.val)))
        return y
    except AttributeError:
        return np.cosh(X)

def tanh(X):
    try:
        y = ADnum(np.tanh(X.val), der = 1/(np.cosh(X.val)**2)*X.der, ops = (1-X.counted)*X.ops+4, rops=3)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'tanh', 1/(np.cosh(X.val)**2)))
        return y
    except AttributeError:
        return np.tanh(X)

#NATURAL EXPONENTIAL AND NATURAL LOGARITHM
def exp(X):
    try:
        y = ADnum(np.exp(X.val), der = np.exp(X.val)*X.der, ops = (1-X.counted)*X.ops+2, rops=1)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'exp', np.exp(X.val)))
        return y
    except AttributeError:
        return np.exp(X)

def log(X):
    try:
        y = ADnum(np.log(X.val), der = 1/X.val*X.der, ops = (1-X.counted)*X.ops+2, rops=1)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'log', 1/X.val))
        return y
    except AttributeError:
        return np.log(X)

def logistic(X):
    return 1/(1+exp(-1*X))


def sqrt(X):
    try:
        y = ADnum(np.sqrt(X.val), der = X.der/(2*np.sqrt(X.val)), ops=(1-X.counted)*X.ops+3, rops=3)
        X.counted = 1
        y.graph = X.graph
        if X not in y.graph:
            y.graph[X] = []
        y.graph[X].append((y, 'sqrt', 1/(2*np.sqrt(X.val))))
        return y
    except AttributeError:
        return np.sqrt(X)

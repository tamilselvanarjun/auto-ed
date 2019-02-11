"""Module to wrap numbers into ADnum object and do basic calculations.
Take value and specified derivative as given, wrap up as ADnum object, and return ADnum object for each basic calculation function.
"""
import numpy as np
class ADnum:
    """ Class to create ADnum objects on which to perform differentiation.

    ATTRIBUTES
    ==========
    val : scalar for scalar valued quantities or numpy array for vector valued functions, the value of the ADnum object for a set input value
    der : scalar for sclar functions of a single variable or numpy array for functions of multiple variables the derivative 
    graph : dictionary containing the edges of the computational graph
    constant : 0 or 1 indicating whether the ADnum object is constant

    METHODS
    =======
    This class overloads the methods for basic arithmetic operations.

    EXAMPLES
    ========
    # >>> x = ADnum(2, der = 1)
    # >>> f = 2*x+3
    # >>> print(f.val)
    # 7.0
    # >>> print(f.der)
    # 2.0
    """
    def __init__(self, value, **kwargs):
        try:
            scalarinput = (isinstance(value, int) or isinstance(value, float))
            value = np.array(value)
            value = value.astype(float)
            if 'der' not in kwargs:
                try:
                    ins = kwargs['ins']
                    ind = kwargs['ind']
                    if scalarinput:
                        der = np.zeros(ins)
                        der[ind] = 1.0
                    else:
                        if ins>1:
                            der = np.zeros((ins, len(value)))
                            der[ind, :] = 1.0 #np.ones(len(value))
                        else:
                            der = np.ones(len(value))
                except:
                    raise KeyError('Must provide ins and ind if der not provided.')
            else:
                der = kwargs['der']
                der = np.array(der)
                der = der.astype(float)
                if 'ins' in kwargs:
                    ins = kwargs['ins']
                    if len(der) != ins:
                        raise ValueError('Shape of derivative does not match number of inputs.')
        except:
            raise ValueError('Value and derivative of ADnum object must be numeric.')
        self.val = value
        self.der = der
        if 'graph' not in kwargs:
            self.graph = {}
        else:
            self.graph = kwargs['graph']
        if 'constant' not in kwargs:
            self.constant = 0
        else:
            self.constant = kwargs['constant']

    def __neg__(self):
        y = ADnum(-self.val, der = -self.der)
        y.graph = self.graph
        if self not in y.graph:
            y.graph[self] = []
        y.graph[self].append((y, 'neg'))
        return y

    def __mul__(self,other):
        try:
            graph = merge_dicts(self.graph, other.graph)
            y = ADnum(self.val*other.val, der = self.val*other.der+self.der*other.val)
            y.graph = graph
            if self not in y.graph:
                y.graph[self] = []
            y.graph[self].append((y, 'multiply'))
            if other not in y.graph:
                y.graph[other] = []
            y.graph[other].append((y, 'multiply'))
            return y
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return self*other

    def __rmul__(self,other):
        return self.__mul__(other)

    def __add__(self,other):
        try:
            graph = merge_dicts(self.graph, other.graph)
            y = ADnum(self.val+other.val, der = self.der+other.der)
            y.graph = graph
            if self not in y.graph:
                y.graph[self] = []
            y.graph[self].append((y, 'add'))
            if other not in y.graph:
                y.graph[other] = []
            y.graph[other].append((y, 'add'))
            return y        
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return self + other

    def __radd__(self,other):
        return self.__add__(other)

    def __sub__(self,other):
        try:
            graph = merge_dicts(self.graph, other.graph)
            y = ADnum(self.val-other.val,der = self.der-other.der)
            y.graph = graph
            if self not in y.graph:
                y.graph[self] = []
            y.graph[self].append((y, 'subtract'))
            if other not in y.graph:
                y.graph[other] = []
            y.graph[other].append((y, 'subtract'))
            return y
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return self-other

    def __rsub__(self, other):
        try:
            return ADnum(other.val-self.val, der = other.der-self.der)
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return other-self

    def __truediv__(self, other):
        try:
            graph = merge_dicts(self.graph, other.graph)
            y = ADnum(self.val/other.val, der = (other.val*self.der-self.val*other.der)/(other.val**2))
            y.graph = graph
            if self not in y.graph:
                y.graph[self] = []
            y.graph[self].append((y, 'divide'))
            if other not in y.graph:
                y.graph[other] = []
            y.graph[other].append((y, 'divide'))
            return y
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return self/other
    
    def __rtruediv__(self, other):
        try:
            return ADnum(other.val/self.val, der = (self.val*other.der-other.val*self.der)/(self.val**2))
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return other/self

    def __pow__(self, other, modulo=None):
        try:
            graph = merge_dicts(self.graph, other.graph)
            if self.val == 0:
                y = ADnum(self.val**other.val, der = other.val*(self.val**(other.val-1))*self.der+(self.val**other.val))
            else:
                y = ADnum(self.val**other.val, der = other.val*(self.val**(other.val-1))*self.der+(self.val**other.val)*np.log(np.abs(self.val))*other.der)
            y.graph = graph
            if self not in y.graph:
                y.graph[self] = []
            y.graph[self].append((y, 'pow'))
            if other not in y.graph:
                y.graph[other] = []
            y.graph[other].append((y, 'pow'))
            return y
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return self**other

    def __rpow__(self, other):
        try:
            return ADnum(other.val**self.val, der = self.val*(other.val**(self.val-1))*other.der+(other.val**self.val)*np.log(other.val)*self.der)
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return other**self

def merge_dicts(d1, d2):
    ''' Function to merge two dictionaries.

    INPUTS
    ======
    d1 : dictionary
    d2 : dictionary

    OUTPUTS
    =======
    dnew : new dictionary that is a combination of d1 and d2

    '''
    dnew = d1.copy()
    for key in d2:
        if key in dnew:
            dnew[key] = dnew[key]+d2[key]
        else:
            dnew[key] = d2[key]
    return dnew

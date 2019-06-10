"""Module to wrap numbers into ADnum object and do basic calculations.
Take value and specified derivative as given, wrap up as ADnum object, and return ADnum object for each basic calculation function.
"""
import numpy as np
from timeit import default_timer as timer

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
        self.ins = len(self.der)
        self.rder = None
        if 'graph' not in kwargs:
            self.graph = {}
        else:
            self.graph = kwargs['graph']
        if 'constant' not in kwargs:
            self.constant = 0
        else:
            self.constant = kwargs['constant']
        if 'ops' not in kwargs:
            self.ops = 0
        else:
            self.ops = kwargs['ops']
        if 'rops' not in kwargs:
            self.rops = 0
        else:
            self.rops = kwargs['rops']
        if 'tfops' not in kwargs:
            self.tfops = 0
        else:
            self.tfops = kwargs['tfops']
        if 'trops' not in kwargs:
            self.trops = 0
        else:
            self.trops = kwargs['trops']
        if 'ftime' not in kwargs:
            self.ftime = 0
        else:
            self.ftime = kwargs['ftime']
        if 'rtime' not in kwargs:
            self.rtime = 0
        else:
            self.rtime = kwargs['rtime']
        self.counted = 0

    def revder(self, f):
        f.rder = 1
        #tolops = 0
        if self.rder is None:
            try:
                children = f.graph[self]
                calc = 0
                for child in children:
                    calc = calc + child[2]*child[0].revder(f)#[0]
                    #tolops = tolops + child[0].revder(f)[1]+child[0].rops+2*self.ins
                self.rder = calc
            except KeyError:
                self.rder = 0
        return self.rder #, tolops

    def __neg__(self):
        fstart = timer()
        a=-self.der
        fend = timer()
        y = ADnum(-self.val, der = -self.der, ops = (1-self.counted)*self.ops+1, rops = 0, tfops = self.tfops+3*self.ins, trops = self.trops+4*self.ins, ftime = self.ftime+fend-fstart, rtime = self.rtime)
        self.counted = 1
        y.graph = self.graph
        rstart = timer()
        if self not in y.graph:
            y.graph[self] = []
        y.graph[self].append((y, 'neg', -1))
        rend = timer()
        y.rtime = y.rtime+rend-rstart
        return y

    def __mul__(self,other):
        try:
            graph = merge_dicts(self.graph, other.graph)
            if self.constant or other.constant:
                opcount = (1-self.counted)*self.ops*(1-self.constant)+(1-other.counted)*other.ops*(1-other.constant)+1
            else:
                opcount = (1-self.counted)*self.ops*(1-self.constant)+(1-other.counted)*other.ops*(1-other.constant)+3
            fstart = timer()
            a = self.val*other.der + self.der*other.val
            fend = timer()
            y = ADnum(self.val*other.val, der = self.val*other.der+self.der*other.val, ops = opcount, rops=0, tfops = 3*self.ins+self.tfops+other.tfops, trops = 4*self.ins+self.trops+other.trops, ftime = self.ftime+other.ftime+fend-fstart, rtime = self.rtime+other.rtime)
            self.counted = 1
            other.counted = 1
            y.graph = graph
            rstart = timer()
            if self not in y.graph:
                y.graph[self] = []
            y.graph[self].append((y, 'multiply', other.val))
            if other not in y.graph:
                y.graph[other] = []
            y.graph[other].append((y, 'multiply', self.val))
            rend = timer()
            y.rtime = y.rtime + rend-rstart
            return y
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return self*other

    def __rmul__(self,other):
        return self.__mul__(other)

    def __add__(self,other):
        try:
            graph = merge_dicts(self.graph, other.graph)
            opcount = (1-self.counted)*self.ops*(1-self.constant)+(1-other.counted)*other.ops*(1-other.constant)+1
            fstart = timer()
            a=self.der+other.der
            fend = timer()
            y = ADnum(self.val+other.val, der = self.der+other.der, ops = opcount, rops=0, tfops = self.tfops+other.tfops+self.ins, trops = self.trops + other.trops+2*self.ins, ftime = self.ftime+other.ftime+fend-fstart, rtime = self.rtime+other.rtime)
            self.counted = 1
            other.counted = 1
            y.graph = graph
            rstart = timer()
            if self not in y.graph:
                y.graph[self] = []
            y.graph[self].append((y, 'add', 1))
            if other not in y.graph:
                y.graph[other] = []
            y.graph[other].append((y, 'add', 1))
            rend = timer()
            y.rtime = y.rtime + rend-rstart
            return y        
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return self + other

    def __radd__(self,other):
        return self.__add__(other)

    def __sub__(self,other):
        try:
            graph = merge_dicts(self.graph, other.graph)
            opcount = (1-self.counted)*self.ops*(1-self.constant)+(1-other.counted)*other.ops*(1-other.constant)+1
            fstart = timer()
            a=self.der-other.der
            fend = timer()
            y = ADnum(self.val-other.val,der = self.der-other.der, ops = opcount, rops=0, tfops = self.tfops+other.tfops+self.ins, trops = self.trops+other.trops+2*self.ins, ftime = self.ftime+other.ftime+fend-fstart, rtime = self.rtime+other.rtime)
            self.counted = 1
            other.counted = 1
            y.graph = graph
            rstart = timer()
            if self not in y.graph:
                y.graph[self] = []
            y.graph[self].append((y, 'subtract', 1))
            if other not in y.graph:
                y.graph[other] = []
            y.graph[other].append((y, 'subtract', -1))
            rend = timer()
            y.rtime = y.rtime + rend-rstart
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
            opcount = (1-self.counted)*self.ops*(1-self.constant)+(1-other.counted)*other.ops*(1-other.constant)
            if self.constant and not other.constant:
                opcount = opcount + 3
            elif other.constant and not self.constant:
                opcount = opcount + 1
            else:
                opcount = opcount+5
            fstart = timer()
            a= (other.val*self.der-self.val*other.der)/(other.val**2)
            fend = timer()
            y = ADnum(self.val/other.val, der = (other.val*self.der-self.val*other.der)/(other.val**2), ops = opcount, rops = 1, tfops = self.tfops+other.tfops+5*self.ins, trops = self.trops+other.trops+4*self.ins, ftime = self.ftime+other.ftime+fend-fstart, rtime = self.rtime+other.rtime)
            self.counted = 1
            other.counted = 1
            y.graph = graph
            rstart = timer()
            if self not in y.graph:
                y.graph[self] = []
            y.graph[self].append((y, 'divide', 1/other.val))
            if other not in y.graph:
                y.graph[other] = []
            y.graph[other].append((y, 'divide', -1*self.val/(other.val**2)))
            rend = timer()
            y.rtime = y.rtime + rend - rstart
            return y
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return self/other
    
    def __rtruediv__(self, other):
        try:
            opcount = (1-self.counted)*self.ops*(1-self.constant)+(1-other.counted)*other.ops*(1-other.constant)
            if self.constant and not other.constant:
                opcount = opcount + 3
            elif other.constant and not self.constant:
                opcount = opcount + 1
            else:
                opcount = opcount+5
            fstart = timer()
            a=(self.val*other.der - other.val*self.der)/(self.val**2)
            fend = timer()
            return ADnum(other.val/self.val, der = (self.val*other.der-other.val*self.der)/(self.val**2), ops = opcount, tfops = self.tfops+other.tfops+5*self.ins, trops = self.trops+other.trops+4*self.ins, ftime = self.ftime+other.ftime+fend-fstart, rtime = self.rtime+other.rtime)
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return other/self

    def __pow__(self, other, modulo=None):
        try:
            graph = merge_dicts(self.graph, other.graph)
            opcount = (1-self.counted)*self.ops*(1-self.constant)+(1-other.counted)*other.ops*(1-other.constant)
            if self.constant and not other.constant:
                opcount = opcount + 4
            elif other.constant and not self.constant:
                opcount = opcount + 4
            else:
                opcount  = opcount + 10
            if self.val == 0:
                fstart = timer()
                a =other.val*(self.val**(other.val-1))*self.der+self.val**other.val
                fend = timer()
                y = ADnum(self.val**other.val, der = other.val*(self.val**(other.val-1))*self.der+(self.val**other.val), ops = opcount, rops=3, tfops = self.tfops+other.tfops+2+self.ins, trops = self.trops+other.trops+2+2*self.ins, ftime = self.ftime+other.ftime+fend-fstart, rtime = self.rtime+other.rtime)
                self.counted = 1
                other.counted =1
            else:
                fstart = timer()
                a=other.val*(self.val**(other.val-1))*self.der+(self.val**other.val)*np.log(np.abs(self.val))*other.der
                fend = timer()
                y = ADnum(self.val**other.val, der = other.val*(self.val**(other.val-1))*self.der+(self.val**other.val)*np.log(np.abs(self.val))*other.der, ops = opcount, tfops=self.tfops+other.tfops+2+self.ins, trops = self.trops+other.trops+2+2*self.ins, ftime = self.ftime+other.ftime+fend-fstart, rtime = self.rtime+other.rtime)
            self.counted = 1
            other.counted = 1
            y.graph = graph
            rstart = timer()
            if self not in y.graph:
                y.graph[self] = []
            y.graph[self].append((y, 'pow', other.val*self.val**(other.val-1)))
            if other not in y.graph:
                y.graph[other] = []
            y.graph[other].append((y, 'pow', self.val**other.val*np.log(np.abs(self.val))))
            rend = timer()
            y.rtime = y.rtime + rend-rstart
            return y
        except AttributeError:
            other = ADnum(other*np.ones(np.shape(self.val)), der = np.zeros(np.shape(self.der)), constant = 1)
            return self**other

    def __rpow__(self, other):
        try:
            opcount = (1-self.counted)*self.ops*(1-self.constant)+(1-other.counted)*other.ops*(1-other.constant)
            if self.constant and not other.constant:
                opcount = opcount + 4
            elif other.constant and not self.constant:
                opcount = opcount + 4
            else:
                opcount  = opcount + 10
            fstart = timer()
            a=self.val*(other.val**(self.val-1))*other.der+(other.val**self.val)*np.log(np.abs(other.val))*self.der
            fend = timer()
            return ADnum(other.val**self.val, der = self.val*(other.val**(self.val-1))*other.der+(other.val**self.val)*np.log(np.abs(other.val))*self.der, ops = (1-self.counted)*self.ops+other.ops+10, tfops=self.tfops+other.tfops+2+self.ins, trops=self.trops+other.trops+2+2*self.ins, ftime = self.ftime+other.ftime+fend-fstart, rtime = self.rtime+other.rtime)
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
            for item in d2[key]:
                if item not in dnew[key]:
                    dnew[key] = dnew[key]+[item]
        else:
            dnew[key] = d2[key]
    return dnew

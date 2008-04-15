__author__ = 'Tom Schaul, tom@idsia.ch; Justin Bayer, bayerj@in.tum.de'

import logging
import threading
import types
import os

from itertools import count
from math import sqrt
from random import random, choice
from string import split

from scipy import dot, where, array


def abstractMethod():
    """ This should be called when an abstract method is called that should have been 
    implemented by a subclass. It should not be called in situations where no implementation
    (i.e. a 'pass' behavior) is acceptable. """
    raise NotImplementedError('Method not implemented!')


def combineLists(ls):
    """ combine a list of lists into a single list """
    return reduce(lambda x,y: x+y, ls, [])


def drawIndex(probs, tolerant = False):
    """ draws an index given an array of probabilities """
    if not sum(probs) < 1.00001 or not sum(probs) > 0.99999:
        if tolerant:
            probs /= sum(probs)
        else:
            print probs, 1-sum(probs)
            raise ValueError()
    r = random()
    s = 0
    for i, p in enumerate(probs):
        s += p
        if s > r:
            return i
    return choice(range(len(probs)))


def iterCombinations(tup):
    """ all possible of integer tuples of the same dimension than tup, and each component being
    positive and strictly inferior to the corresponding entry in tup. """
    if len(tup) == 1:
        for i in range(tup[0]):
            yield (i,)
    elif len(tup) > 1:
        for prefix in iterCombinations(tup[:-1]):
            for i in range(tup[-1]):
                yield tuple(list(prefix)+[i])

    
def setAllArgs(obj, argdict):
    """ set all those internal variables which have the same name than an entry in the 
    given object's dictionnary. 
    This function can be useful for quick initializations. """
    xmlstore = isinstance(obj, XMLBuildable)
    for n in argdict.keys():
        if hasattr(obj, n):
            setattr(obj, n, argdict[n])    
            if xmlstore:
                obj.argdict[n] = argdict[n]  
        else:
            print 'Warning: parameter name', n, 'not found!'  
            
def linscale(d, lim):
    """ utility function to linearly scale array d to the interval defined by lim """
    return (d-d.min())*(lim[1]-lim[0]) + lim[0]


def percentError(out, true):
    """ return percentage of mismatch between out and target values (lists and arrays accepted) """
    arrout = array(out).flatten()
    wrong = where(arrout!=array(true).flatten())[0].size
    return 100.*float(wrong)/float(arrout.size)

            
class XMLBuildable(object):
    """ subclasses of this can be losslessly stored in XML, and 
    automatically reconstructed on reading. For this they need to store 
    their construction arguments in the variable <argdict>. """
    
    argdict = None
    
    def setArgs(self, **argdict):
        if not self.argdict:
            self.argdict = {}
        setAllArgs(self, argdict)
        

class Named(XMLBuildable):
    """Class whose objects are guaranteed to have a unique name."""

    _nameIds = count(0)

    def getName(self):
        logging.warning("Deprecated, use .name property instead.")
        return self.name
        
    def setName(self, newname):
        logging.warning("Deprecated, use .name property instead.")
        self.name = newname

    def _getName(self):
        """Returns the name, which is generated if it has not been already."""
        if self._name is None:
            self._name = self._generateName()
        return self._name
    
    def _setName(self, newname):
        """Change name to newname. Uniqueness is not guaranteed anymore."""
        self._name = newname

    _name = None
    name = property(_getName, _setName)
    
    def _generateName(self):
        """Return a unique name for this object."""
        return "%s-%i" % (self.__class__.__name__,  self._nameIds.next())
        
    def __repr__(self):
        """ The default representation of a named object is its name. """
        return "<%s '%s'>" % (self.__class__.__name__, self.name)

    
def fListToString( a_list, a_precision = 3 ):
    """ returns a string representing a list of floats with a given precision """
    # CHECKME: please tell me if you know a more comfortable way.. (print format specifier?)
    l_out = "["
    for i in a_list:
        l_out += " %% .%df" % a_precision % i
    l_out += "]"
    return l_out


def tupleRemoveItem(tup, index):
    """ remove the item at position index of the tuple and return a new tuple. """
    l = list(tup)
    return tuple(l[:index]+l[index+1:])


def confidenceIntervalSize(stdev, nbsamples):
    """ Determine the size of the confidence interval, given the standard deviation and the number of samples.
    t-test-percentile: 97.5%, infinitely many degrees of freedom,
    therfore on the two-sided interval: 95% """
    # CHECKME: for better precision, maybe get the percentile dynamically, from the scipy library?
    return 2*1.98*stdev/sqrt(nbsamples)   
    
    
def threaded(callback=lambda: None, daemonic=False):
    """Decorate  a function to run in its own thread and report the result
    by calling callback with it."""
    def innerDecorator(func):
        def inner(*args, **kwargs):
            target = lambda: callback(func(*args, **kwargs))
            t = threading.Thread(target=target)
            t.setDaemon(daemonic)
            t.start()
        return inner
    return innerDecorator
    
    
def memoize(func):
    """Decorate a function to 'memoize' results by holding it in a cache that
    maps call arguments to returns."""
    cache = {}
    def inner(*args, **kwargs):
        # Dictionaries and lists are unhashable
        args = tuple(args)
        # Make a set for checking in the cache, since the order of 
        # .iteritems() is undefined
        kwargs_set = frozenset(kwargs.iteritems())
        if (args, kwargs_set) in cache:
            result = cache[args, kwargs_set]
        else:
            result = func(*args, **kwargs)
            cache[args, kwargs_set] = result
        return result
    return inner
        
        
def _import(name):
    """Return module from a package.

    These two are equivalent:

        > from package import module as bar
        > bar = _import('package.module')
    
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

    
def substitute(target):
    """Substitute a function with the function found via import from the given
    string.
    
    If the function cannot be found, keep the old one and trigger an 
    information."""
    
    if os.environ.get('PYBRAIN_NO_SUBSTITUTE', None) is not None:
        logging.info("substitute deactivated since PYBRAIN_NO_SUBSTITUTE is"
                     " set for" )
        return lambda x: x
        
    def makeBuiltinWrapper(func):
        def builtinWrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        # To ease reading of error messages
        builtinWrapper.__name__ = func.__name__
        return builtinWrapper
        
    def decorator(func):
        import_path = target.split('.')
        module_path = import_path[:-1]
        func_name = import_path[-1]
        try:
            module = _import(".".join(module_path))
            opt_func = getattr(module, func_name)
        except (ImportError, AttributeError), e:
            #print e
            logging.info("Could not find substitution for %s. (Tried: %s)" 
                         % (func.__name__, target))
            #logging.info("from %s import %s" % (".".join(module_path), func_name))
            return func
        if type(opt_func) is types.BuiltinFunctionType:
            opt_func = makeBuiltinWrapper(opt_func)
        return opt_func
    return decorator
    
    
def lookupSubstitute(func):
    """Substitute a function/method by its optimized counterpart. 
    
    The lookup rules are as follows:
    TODO
    """
    raise NotImplemented("Use pybrain.tools.helpers.substitute")
    
    # The following does not work, since we cannot retrieve the methods 
    # classname during class initialization. Functions are not yet instance 
    # methods at that point.
    if type(func) is types.MethodType:
        func_name = func.im_class.__name__ + "_" + func_name
    import_path = func.__module__.split(".") + [func.__name__]
    target_path = import_path[:-2] + ["_" + import_path[-2], import_path[-1]]
    target = ".".join(target_path)
    return substitute(target)(func)
        
        
# tools for binary Gray code manipulation:

def int2gray(i):
    """ return the value of val in Gray encoding."""
    return i ^ (i >> 1)

    
def gray2int(g, size):
    """ transform a gray code back into an integer """
    res = 0
    for i in reversed(range(size)):
        gi = (g>>i)%2
        if i == size -1:
            bi = gi
        else:
            bi = bi ^ gi
        res += bi * 2**i
    return res

    
def asBinary(i):
    """ produce a string of an integers binary representation.
    (preceding zeros removed). """
    if i > 1:
        if i%2 == 1:
            return asBinary(i>>1)+'1'
        else:
            return asBinary(i>>1)+'0'
    else:
        return str(i)    
    
# TODO: use norm from scipy.linalg package instead? (tr)    
def norm(x):
    """ the norm of a vector """
    return sqrt(dot(x,x))


def canonicClassString(x):
    """ the __class__ attribute changed from old-style to new-style classes... """
    if isinstance(x, object):
        return split(repr(x.__class__), "'")[1]
    else:
        return repr(x.__class__)
    

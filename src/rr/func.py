"""Additional tools for functional-style programming in Python.

This module defines a set of higher-order functions to create new useful functions.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import functools
import operator

from future.moves import builtins

__version__ = "0.3.0"
__author__ = "Rui Rei"
__copyright__ = "Copyright 2016-2017 {author}".format(author=__author__)
__license__ = "MIT"

# We rebind 'map', 'reduce', 'filter' and 'partial' here just so that these functions can be used
# in the same manner as the functions actually defined in this module e.g. func.map(f, [2, 3])
# instead of having to import functools and using functional operators from different modules.
# The idea here is to make all functional operators accessible from this module.
map = builtins.map
filter = builtins.filter
reduce = functools.reduce
partial = functools.partial


def pipe(funcs, name=None, doc=None):
    """Create a pipeline of functions. The first function is passed the original arguments, and
    the remaining functions take as single argument the return value of the previous function.

        P = func.pipe([f, g, h])
        P(x)  # equivalent to... h(g(f(x)))

    The name and docstring of the newly created function can be given through the 'name' and
    'doc' arguments.
    """
    def pipe_func(*args, **kwargs):
        ifuncs = iter(funcs)
        result = next(ifuncs)(*args, **kwargs)
        for func in ifuncs:
            result = func(result)
        return result

    pipe_func.__name__ = name or "pipe({})".format(", ".join(f.__name__ for f in funcs))
    pipe_func.__doc__ = doc
    return pipe_func


def tee(funcs, name=None, doc=None):
    """Create a function which broadcasts all arguments it receives to a list of "sub-functions".
    The return value of the tee function is a generator expression containing the return values
    of the individual sub-functions.

        T = func.tee([f, g, h])
        T(x)  # equivalent to...  [f(x), g(x), h(x)] (as a generator expression, not a list!)

    The name and docstring of the newly created function can be given through the 'name' and
    'doc' arguments.
    """
    def tee_func(*args, **kwargs):
        return (func(*args, **kwargs) for func in funcs)

    tee_func.__name__ = name or "tee({})".format(", ".join(f.__name__ for f in funcs))
    tee_func.__doc__ = doc
    return tee_func


def star(func, name=None, doc=None):
    """Produces a function that takes up to two arguments, the first being an iterable and the
    second a dictionary. These are then passed to 'func' as star arguments, i.e. the first
    argument is expanded with one star to represent positional arguments, while the second is
    expanded with two stars and represents keyword arguments for 'func'. This may be useful to
    wrap a normal function and insert it in the middle of a function pipeline (see 'pipe()').

        S = func.star(f)
        S(args, kwargs)  # equivalent to... f(*args, **kwargs)

    The name and docstring of the newly created function can be given through the 'name' and
    'doc' arguments.
    """
    def star_func(args=(), kwargs={}):
        return func(*args, **kwargs)

    star_func.__name__ = name or "star({})".format(func.__name__)
    star_func.__doc__ = doc or func.__doc__
    return star_func


def negate(func, name=None, doc=None):
    """Create a function which merely negates the result of 'func'.

        N = func.negate(f)
        N(x)  # equivalent to... not f(x)

    The name and docstring of the newly created function can be given through the 'name' and
    'doc' arguments.
    """
    def negate_func(*args, **kwargs):
        return not func(*args, **kwargs)

    negate_func.__name__ = name or "negate({})".format(func.__name__)
    negate_func.__doc__ = doc
    return negate_func


def binop(op, left, right, name=None, doc=None):
    """Define a function which applies a binary operator to the results of the two operand
    functions `left` and `right`.

    The name and docstring of the newly created function can be given through the 'name' and
    'doc' arguments.
    """
    def binop_func(*args, **kwargs):
        return op(left(*args, **kwargs), right(*args, **kwargs))

    if not name:
        name = "binop({}, {}, {})".format(op.__name__, left.__name__, right.__name__)
    binop_func.__name__ = name
    binop_func.__doc__ = doc
    return binop_func


def aggregate(agg, funcs, name=None, doc=None):
    """Apply an aggregate function on the results of an arbitrary number of operand functions.

        A = func.aggregate(sum, [f, g, h])
        A(x)  # equivalent to... sum([f(x), g(x), h(x)])
        # this example is actually also equivalent to func.sum()

    This is very similar to reduce(), but operates on (and returns) functions instead.
    The name and docstring of the newly created function can be given through the 'name' and
    'doc' arguments.
    """
    if not name:
        name = "aggregate({}, {})".format(agg.__name__, [f.__name__ for f in funcs])
    return pipe([tee(funcs), agg], name=name, doc=doc)


# Below we define a set of binop()- and aggregate()-based arithmetic operators and common
# aggregations (sum, prod, min, max, any, all).

def add(f, g):
    return binop(operator.add, f, g)


def sub(f, g):
    return binop(operator.sub, f, g)


def mul(f, g):
    return binop(operator.mul, f, g)


def truediv(f, g):
    return binop(operator.truediv, f, g)


div = truediv


def floordiv(f, g):
    return binop(operator.floordiv, f, g)


def mod(f, g):
    return binop(operator.mod, f, g)


def pow(f, g):
    return binop(operator.pow, f, g)


def sum(funcs):
    return aggregate(builtins.sum, funcs)


def prod(funcs):
    return aggregate(partial(reduce, operator.mul), funcs)


def min(funcs):
    return aggregate(builtins.min, funcs)


def max(funcs):
    return aggregate(builtins.max, funcs)


def any(funcs):
    return aggregate(builtins.any, funcs)


def all(funcs):
    return aggregate(builtins.all, funcs)

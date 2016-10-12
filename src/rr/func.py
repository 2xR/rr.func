"""
Additional tools for functional-style programming in Python.
"""
from __future__ import absolute_import
from future.moves import builtins

import collections
import functools
import operator


__version__ = "0.1.0"
__author__ = "Rui Rei"
__copyright__ = "Copyright 2016 {author}".format(author=__author__)
__license__ = "MIT"

# We rebind 'map', 'reduce', 'filter' and 'partial' here just so that these functions
# can be used in the same manner as the functions actually defined in this module e.g.
# func.map(f, [2, 3])
map = builtins.map
filter = builtins.filter
reduce = functools.reduce
partial = functools.partial


def pipe(*funcs, **kwargs):
    """Create a pipeline of functions. The first function is passed the original arguments, and
    the remaining functions take as single argument the return value of the previous function.

        P = func.pipe(f, g, h)
        P(x)  # equivalent to... h(g(f(x)))

    The name and docstring of the newly created function can be given through the 'name' and
    'doc' keyword arguments.
    """
    def pipe_func(*args, **kwargs):
        ifuncs = iter(pipe_func.funcs)
        result = next(ifuncs)(*args, **kwargs)
        for func in ifuncs:
            result = func(result)
        return result

    pipe_func.funcs = list(funcs)
    pipe_func.__name__ = kwargs.get("name", "pipe_func")
    pipe_func.__doc__ = kwargs.get("doc", None)
    return pipe_func


def star(func, **kwargs):
    """Produces a function that takes up to two arguments, the first being an iterable and the
    second a dictionary. These are then passed to 'func' as star arguments, i.e. the first
    argument is expanded with one star to represent positional arguments, while the second is
    expanded with two stars and represents keyword arguments for 'func'. This may be useful to
    wrap a normal function and insert it in the middle of a function pipeline (see 'pipe()').

        S = func.star(f)
        S(args, kwargs)  # equivalent to... f(*args, **kwargs)

    The name and docstring of the newly created function can be given through the 'name' and
    'doc' keyword arguments.
    """
    def star_func(args=None, kwargs=None):
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        return func(*args, **kwargs)

    star_func.__name__ = kwargs.get("name", func.__name__)
    star_func.__doc__ = kwargs.get("doc", func.__doc__)
    return star_func


def tee(*funcs, **kwargs):
    """Create a function which broadcasts all arguments it receives to a list of "sub-functions".
    The return value of the tee function is a generator expression containing with the return
    values of the individual sub-functions.

        T = func.tee(f, g, h)
        T(x)  # equivalent to...  [f(x), g(x), h(x)] (as a generator expression, not a list!)

    The name and docstring of the newly created function can be given through the 'name' and
    'doc' keyword arguments.
    """
    def tee_func(*args, **kwargs):
        return (func(*args, **kwargs) for func in tee_func.funcs)

    tee_func.funcs = list(funcs)
    tee_func.__name__ = kwargs.get("name", "tee_func")
    tee_func.__doc__ = kwargs.get("doc", None)
    return tee_func


def negate(func, **kwargs):
    """Create a function which merely negates the result of 'func'.

        N = func.negate(f)
        N(x)  # equivalent to... not f(x)

    The name and docstring of the newly created function can be given through the 'name' and
    'doc' keyword arguments.
    """
    def negate_func(*args, **kwargs):
        return not func(*args, **kwargs)

    negate_func.__name__ = kwargs.get("name", func.__name__)
    negate_func.__doc__ = kwargs.get("doc", None)
    return negate_func


def aggregate(agg, operands, **kwargs):
    """Apply an aggregate function on the results of an arbitrary number of operand functions.

        A = func.aggregate(sum, [f, g, h])
        A(x)  # equivalent to... sum([f(x), g(x), h(x)])
        # this example is actually also equivalent to func.sum()

    This is very similar to reduce(), but operates on (and returns) functions instead.
    The name and docstring of the newly created function can be given through the 'name' and
    'doc' keyword arguments.
    """
    return pipe(tee(*operands), agg, **kwargs)


# aggregate()-based arithmetic operators and other common aggregations (min, max, any, all)
# -----------------------------------------------------------------------------------------
def sum(*funcs):
    if len(funcs) == 1 and isinstance(funcs[0], collections.Iterable):
        funcs = funcs[0]
    return aggregate(builtins.sum, funcs)


def sub(f, g):
    return aggregate(partial(reduce, operator.sub), (f, g))


def prod(*funcs):
    if len(funcs) == 1 and isinstance(funcs[0], collections.Iterable):
        funcs = funcs[0]
    return aggregate(partial(reduce, operator.mul), funcs)


def truediv(f, g):
    return aggregate(partial(reduce, operator.truediv), (f, g))


div = truediv


def floordiv(f, g):
    return aggregate(partial(reduce, operator.floordiv), (f, g))


def mod(f, g):
    return aggregate(partial(reduce, operator.mod), (f, g))


def pow(f, g):
    return aggregate(partial(reduce, operator.pow), (f, g))


def min(*funcs):
    if len(funcs) == 1 and isinstance(funcs[0], collections.Iterable):
        funcs = funcs[0]
    return aggregate(builtins.min, funcs)


def max(*funcs):
    if len(funcs) == 1 and isinstance(funcs[0], collections.Iterable):
        funcs = funcs[0]
    return aggregate(builtins.max, funcs)


def any(funcs):
    return aggregate(builtins.any, funcs)


def all(funcs):
    return aggregate(builtins.all, funcs)

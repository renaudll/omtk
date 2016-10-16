import logging;
import math
import re

import pymel.core as pymel
from maya import cmds

from omtk.libs import libRigging

log = logging.getLogger(__name__);
log.setLevel(logging.INFO)


class Operator(object):
    @staticmethod
    def can_optimise(*args):
        for arg in args:
            if not isinstance(arg, (int, float, long)):
                return False
        return True

    @staticmethod
    def execute(arg1, arg2):
        raise NotImplementedError

    @staticmethod
    def create(arg1, arg2):
        raise NotImplementedError


class OperatorAddition(Operator):
    @staticmethod
    def execute(arg1, arg2):
        return arg1 + arg2

    @staticmethod
    def create(arg1, arg2):
        return libRigging.create_utility_node('plusMinusAverage', operation=1, input1D=[arg1, arg2]).output1D


class OperatorSubstraction(Operator):
    @staticmethod
    def execute(arg1, arg2):
        return arg1 - arg2

    @staticmethod
    def create(arg1, arg2):
        return libRigging.create_utility_node('plusMinusAverage', operation=2, input1D=[arg1, arg2]).output1D


class OperatorMultiplication(Operator):
    @staticmethod
    def execute(arg1, arg2):
        return arg1 * arg2;

    @staticmethod
    def create(arg1, arg2):
        return libRigging.create_utility_node('multiplyDivide', operation=1, input1X=arg1, input2X=arg2).outputX


class OperatorDivision(Operator):
    @staticmethod
    def execute(arg1, arg2):
        return arg1 / arg2;

    @staticmethod
    def create(arg1, arg2):
        u = libRigging.create_utility_node('multiplyDivide', input1X=arg1, input2X=arg2)
        u.operation.set(2)  # HACK: Prevent division by zero by changing the operator at the last second.
        return u.outputX


class OperatorPow(Operator):
    @staticmethod
    def execute(arg1, arg2):
        try:
            return math.pow(arg1, arg2)
        except Exception, e:
            log.error("Can't execute {0} ^ {1}: {2}".format(arg1, arg2, e)),

        return math.pow(arg1, arg2)

    @staticmethod
    def create(arg1, arg2):
        return libRigging.create_utility_node('multiplyDivide', operation=3, input1X=arg1, input2X=arg2).outputX


class OperatorDistance(Operator):
    # Ensure that we correctly cast the arguments if '0' is provided.
    # ex: 0~a where 'a' is a vector or a matrix
    @staticmethod
    def _get_identity_by_type(type):
        if type == pymel.datatypes.Matrix:
            return pymel.datatypes.Matrix()
        if type == pymel.datatypes.Vector:
            return pymel.datatypes.Vector()
        raise Exception("Cannot cast type {0}".format(type))

    @staticmethod
    def _handle_args(arg1, arg2):
        if arg1 == 0 and not isinstance(arg2, (int, float, long)):
            arg1 = OperatorDistance._get_identity_by_type(type(arg2))
        if arg2 == 0 and not isinstance(arg1, (int, float, long)):
            arg2 = OperatorDistance._get_identity_by_type(type(arg1))
        return arg1, arg2

    @staticmethod
    def execute(arg1, arg2):
        arg1, arg2 = OperatorDistance._handle_args(arg1, arg2)
        log.debug('[distance:execute] {0} * {1}'.format(arg1, arg2))

        # todo: check for matrix

        return arg1 * arg2

    @staticmethod
    def create(arg1, arg2):
        arg1, arg2 = OperatorDistance._handle_args(arg1, arg2)
        log.debug('[distance:create] {0} * {1}'.format(arg1, arg2))
        # todo: check if we want to use inMatrix1 & inMatrix2 or point1 & point2
        kwargs = {}

        if isinstance(arg1, pymel.datatypes.Matrix) or (isinstance(arg1, pymel.Attribute) or arg1.type() == 'matrix'):
            kwargs['inMatrix1'] = arg1
        elif isinstance(arg1, pymel.nodetypes.Transform):
            kwargs['inMatrix1'] = arg1.worldMatrix
        else:
            kwargs['point1'] = arg1

        if isinstance(arg2, pymel.datatypes.Matrix) or (isinstance(arg2, pymel.Attribute) or arg2.type() == 'matrix'):
            kwargs['inMatrix2'] = arg2
        elif isinstance(arg2, pymel.nodetypes.Transform):
            kwargs['inMatrix2'] = arg2.worldMatrix
        else:
            kwargs['point2'] = arg2

        return libRigging.create_utility_node('distanceBetween', **kwargs).distance


class OperatorEqual(Operator):
    @staticmethod
    def execute(arg1, arg2):
        log.execute('[equal:execute] {0} * {1}'.format(arg1, arg2))
        return arg1 == arg2;

    @staticmethod
    def create(arg1, arg2):
        log.debug('[equal:create] {0} * {1}'.format(arg1, arg2))
        return libRigging.create_utility_node('condition', operation=0, colorIfTrue=1.0, colorIfFalse=0.0).outColorR


class OperatorNotEqual(Operator):
    @staticmethod
    def execute(arg1, arg2):
        return arg1 != arg2;

    @staticmethod
    def create(*args, **kwargs):
        return libRigging.create_utility_node('condition', operation=1, colorIfTrue=1.0, colorIfFalse=0.0).outColorR


class OperatorGreater(Operator):
    @staticmethod
    def execute(arg1, arg2):
        return arg1 > arg2

    @staticmethod
    def create(*args, **kwargs):
        return libRigging.create_utility_node('condition', operation=2, colorIfTrue=1.0, colorIfFalse=0.0).outColorR


class OperatorGreaterOrEqual(Operator):
    @staticmethod
    def execute(arg1, arg2):
        return arg1 >= arg2;

    @staticmethod
    def create(*args, **kwargs):
        return libRigging.create_utility_node('condition', operation=3, colorIfTrue=1.0, colorIfFalse=0.0).outColorR


class OperatorSmaller(Operator):
    @staticmethod
    def execute(arg1, arg2):
        return arg1 < arg2;

    @staticmethod
    def create(*args, **kwargs):
        return libRigging.create_utility_node('condition', operation=4, colorIfTrue=1.0, colorIfFalse=0.0).outColorR


class OperatorSmallerOrEqual(Operator):
    @staticmethod
    def execute(arg1, arg2):
        return arg1 <= arg2;

    @staticmethod
    def create(*args, **kwargs):
        return libRigging.create_utility_node('condition', operation=5, colorIfTrue=1.0, colorIfFalse=0.0).outColorR


# src: http://www.mathcentre.ac.uk/resources/workbooks/mathcentre/rules.pdf
_sorted_operators = [
    {
        '~': OperatorDistance,
    },
    {
        '^': OperatorPow,
    },
    {
        '*': OperatorMultiplication,
        '/': OperatorDivision,
    },
    {
        '+': OperatorAddition,
        '-': OperatorSubstraction,
    },
    {
        '=': OperatorEqual,
        '!=': OperatorNotEqual,
        '>': OperatorGreater,
        '>=': OperatorGreaterOrEqual,
        '<': OperatorSmaller,
        '<=': OperatorSmallerOrEqual
    }
]

_all_operators = {}
for operators in _sorted_operators: _all_operators.update(operators)
_varDelimiters = ['(', ')', '.'] + _all_operators.keys()
_regex_splitVariables = '|'.join(re.escape(str) for str in _varDelimiters)

_variables = {}


def basic_cast(str):
    # try float conversion
    try:
        return float(str)
    except:
        pass

    # try int conversion
    try:
        return int(str)
    except:
        pass

    return str


def convert_basic_value(str):
    # handle parenthesis
    if isinstance(str, list):
        return _create_nodes(*str)

    return basic_cast(str)


def rlen(L):
    i = 0
    for l in L:
        if isinstance(l, list):
            i += rlen(l)
        else:
            i += 1
    return i


def optimise_replaceVariables(args):
    global _variables
    fnIsVariable = lambda x: isinstance(x, basestring) and x in _variables

    out = []
    for arg in args:
        if fnIsVariable(arg):
            arg = basic_cast(_variables[arg])
        elif isinstance(arg, list):
            arg = optimise_replaceVariables(arg)
        else:
            arg = basic_cast(arg)
        out.append(arg)
    return out


def _optimise_formula_remove_prefix(args):
    # import logging; log = logging.getLogger(__name__)
    if len(args) < 2:
        raise Exception("A minimum of 2 arguments are necessary! Got: {0}".format(args))
    fnRecursive_call = lambda x: _optimise_formula_remove_prefix(x) if isinstance(x, list) else x
    # args[0] = fnRecursive_call(args[0])
    pos = 0
    imax = len(args)
    while pos < imax - 1:
        # log.debug('| current position: {0}'.format(pos))
        # log.debug('| current operator: {0}'.format(args[0]))
        # log.debug('| memory: {0} {1} {2}'.format((args[pos-1] if pos != 0 else None), args[pos], args[pos+1]))
        # log.debug('| memory (all): {0}'.format(args))
        preArg = args[pos - 1] if pos > 0 else None
        args[pos] = perArg = fnRecursive_call(args[pos])
        args[pos + 1] = posArg = fnRecursive_call(args[pos + 1])
        if perArg == '-':
            if preArg is None or preArg in _all_operators:  # If the formula start with '-' or '-' is prefixed by an operator
                del args[pos]

                if isinstance(posArg, (int, float, long)):
                    args[pos] = -1 * posArg
                else:
                    args[pos] = [-1, '*', posArg]
                imax = len(args)
            pos += 1
        else:
            pos += 1
    # log.debug('exiting... {0}'.format(args))
    return args


# Generic method to optimize a formula via a suite of operators
# For now only 'sandwitched' operators are supported
def _optimise_formula_with_operators(args, fnName, fnFilterName=None):
    if len(args) < 3:
        raise Exception("A minimum of 3 arguments are necessary! Got: {0}".format(args))
    fnRecursive_call = lambda x: _optimise_formula_with_operators(x, fnName, fnFilterName=fnFilterName) if isinstance(x,
                                                                                                                      list) else x
    for operators in _sorted_operators:
        args[0] = fnRecursive_call(args[0])
        i = 1
        imax = len(args)
        while i < imax - 1:
            preArg = args[i - 1]
            perArg = args[i]
            posArg = args[i + 1] = fnRecursive_call(args[i + 1])
            # Ensure we're working with operators
            if not isinstance(perArg, basestring):
                raise IOError("Invalid operator '{0}', expected a string".format(perArg))
            cls = operators.get(perArg, None)
            if cls and (not fnFilterName or getattr(cls, fnFilterName)(preArg, posArg)):
                fn = getattr(cls, fnName)
                result = fn(preArg, posArg)
                # Inject result in args
                args[i - 1] = result
                del args[i]
                del args[i]
                imax -= 2
            else:
                i += 2
    return args if len(args) > 1 else args[0]  # never return a single array


# This minimise the weight of the formula, we make sure we're not applying operator on constants.
# ex: "2 + 3 * a"   ->   "5 * a"
# ex: "a ^ (2 + 3)" ->   "a ^ 5"
def _optimise_cleanConstants(args):
    return _optimise_formula_with_operators(args, 'execute', 'can_optimise')


def _create_nodes(args):
    return _optimise_formula_with_operators(args, 'create')


def parse(str, **inkwargs):
    log.debug("--------------------")
    log.debug("PARSING: {0}".format(str))

    if not isinstance(str, basestring):
        log.debug("Formula provided is not a string! Skipped")
        return str

    # step 1: identify variables
    vars = (var.strip() for var in re.split(_regex_splitVariables, str))
    vars = [var for var in vars if not var.isdigit()]
    vars = filter(lambda x: x, vars)
    # print 'found vars:', vars

    # hack: add mathematical constants in variables
    kwargs = {
        'e': math.e,
        'pi': math.pi
    }
    kwargs.update(inkwargs)

    # step 2: ensure all variables are defined
    # todo: validate vars types
    global _variables
    _variables = {}
    for var in vars:
        if not var in kwargs:
            raise KeyError("Variable '{0}' is not defined".format(var))
        _variables[var] = kwargs[var]
        # log.debug('\t{0} = {1}'.format(var, kwargs[var]))
    # print 'defined variables are:', dicVariables

    # Convert parenthesis and operators to nested string lists
    # src: http://stackoverflow.com/questions/5454322/python-how-to-match-nested-parentheses-with-regex
    from omtk.deps import pyparsing  # make sure you have this installed
    content = pyparsing.Word(pyparsing.alphanums + '.' + '_')
    for op in _all_operators.keys(): content |= op  # defined operators
    nestedExpr = pyparsing.nestedExpr(opener='(', closer=')', content=content)
    res = nestedExpr.parseString('({0})'.format(str))  # wrap all string in parenthesis, or it won't work
    args = res.asList()[0]

    num_args = len(args)
    if num_args == 0:
        raise IOError("Expected at least 1 argument!")

    # Replace variables by their real value
    # We're only iterating on every operators (ex: range(1,4,2)
    args = optimise_replaceVariables(args)
    if not isinstance(args, list): return args
    log.debug("\tWithout variables ({0} calls) : {1}".format(rlen(args), args))

    # Hack: Convert '-' prefix before a variable to a multiply operator
    # ex: x*-3 -> x * (3 * -1)
    args = _optimise_formula_remove_prefix(args)
    if not isinstance(args, list): return args
    log.debug("\tWithout '-' prefix ({0} calls): {1}".format(rlen(args), args))

    # Calculate out the constants
    args = _optimise_cleanConstants(args)
    if not isinstance(args, list): return args
    log.debug("\tWithout constants ({0} calls) : {1}".format(rlen(args), args))

    # Create nodes
    # log.debug("Creating nodes...")
    return _create_nodes(args)
    # log.debug("ALL DONE!")

    return None


def parseToVar(name, formula, vars):
    attr = parse(formula, **vars)
    attr.node().rename(name)
    vars[name] = attr


#
# A wrapper to
#
# todo: Fix regression of automatic node renaming
class Formula(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def add_variable(self, name, formula, **kwargs):
        kwargs.update(self.__dict__)
        value = parse(formula, **kwargs)
        self.__dict__[name] = value
        return value

    def __setattr__(self, key, value):
        self.add_variable(key, value)
        # parseToVar(key, value, self.__dict__)

    '''
    def parse(self, formula=None)
        if formula is None:
            self
        return parse(self._formula_, **self._vars_)
    '''


#
# Unit testing
#

def _test_squash():
    # ex:creating a bell-curve type squash
    cmds.file(new=True, f=True)
    transform, shape = pymel.sphere()
    stretch = transform.sy
    squash = parse("1 / (e^(x^2))", x=stretch)
    pymel.connectAttr(squash, transform.sx)
    pymel.connectAttr(squash, transform.sz)
    return True


def _test_squash2(step_size=10):
    cmds.file(new=True, f=True)
    root = pymel.createNode('transform', name='root')
    pymel.addAttr(root, longName='amount', defaultValue=1.0, k=True)
    pymel.addAttr(root, longName='shape', defaultValue=math.e, k=True)
    pymel.addAttr(root, longName='offset', defaultValue=0.0, k=True)
    attAmount = root.attr('amount')
    attShape = root.attr('shape')
    attOffset = root.attr('offset')
    attInput = parse("amount^2", amount=attAmount)
    for i in range(0, 100, step_size):
        cyl, make = pymel.cylinder()
        cyl.rz.set(90)
        cyl.ty.set(i + step_size / 2)
        make.heightRatio.set(step_size)
        attSquash = parse("amount^(1/(shape^((x+offset)^2)))", x=(i - 50) / 50.0, amount=attInput, shape=attShape,
                          offset=attOffset)
        pymel.connectAttr(attSquash, cyl.sy)
        pymel.connectAttr(attSquash, cyl.sz)
    return True



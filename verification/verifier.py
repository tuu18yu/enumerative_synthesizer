"""
CSC410 Final Project: Enumerative Synthesizer
by Victor Nicolet and Danya Lette

Fill in this file to complete the verification portion
of the assignment.
"""

from z3 import *
from lang.ast import *


def recurse_expr(ex, var_list):
    """
    The recurse_expr symbolically evaluates the expression ex into z3 terms.
    @param ex The expression to evaluate.
    @param var_list The list of z3 variables for use.
    """

    # Case 1 : ex is a binary expression.
    if (isinstance(ex, BinaryExpr)):

        operator = ex.operator
        lhs = ex.left_operand
        rhs = ex.right_operand

        # Recurse again to get down to the variable elements and convert to z3 variables.
        if (isinstance(operator, Expression)):
            operator = recurse_expr(operator, var_list)
        if (isinstance(lhs, Expression)):
            lhs = recurse_expr(lhs, var_list)
        if (isinstance(rhs, Expression)):
            rhs = recurse_expr(rhs, var_list)

        # Return the python/z3 equivalent of each binary operator.
        if (operator == operator.PLUS):
            return lhs + rhs
        elif (operator == operator.MINUS):
            return lhs - rhs
        elif (operator == operator.TIMES):
            return lhs * rhs
        elif (operator == operator.DIV):
            return lhs / rhs
        elif (operator == operator.MODULO):
            return lhs % rhs
        elif (operator == operator.EQUALS):
            return lhs == rhs
        elif (operator == operator.GREATER):
            return lhs > rhs
        elif (operator == operator.GREATER_EQ):
            return lhs >= rhs
        elif (operator == operator.LESSTHAN):
            return lhs < rhs
        elif (operator == operator.LESSTHAN_EQ):
            return lhs <= rhs
        elif (operator == operator.AND):
            return And(lhs, rhs)
        elif (operator == operator.OR):
            return Or(lhs, rhs)
        elif (operator == operator.NOTEQUALS):
            return lhs != rhs

    # Case 2 : ex is a unary expression.
    elif (isinstance(ex, UnaryExpr)):

        operator = ex.operator
        operand = ex.operand

        # Recurse again to get down to the variable elements and convert to z3 variables.
        if (isinstance(operator, Expression)):
            operator = recurse_expr(operator, var_list)
        if (isinstance(operand, Expression)):
            operand = recurse_expr(operand, var_list)

        # Return the python/z3 equivalent of each unary operator.
        if (operator == operator.NOT):
            return Not(operand)
        elif (operator == operator.ABS):
            return abs(operand)
        elif (operator == operator.NEG):
            return -operand

    # Case 3 : ex is a if-then-else expression (a ternary expression).
    elif (isinstance(ex, Ite)):

        cond = ex.cond
        true_branch = ex.true_br
        false_branch = ex.false_br

        # Recurse again to get down to the variable elements and convert to z3 variables.
        if (isinstance(cond, Expression)):
            cond = recurse_expr(cond, var_list)
        if (isinstance(true_branch, Expression)):
            true_branch = recurse_expr(true_branch, var_list)
        if (isinstance(false_branch, Expression)):
            false_branch = recurse_expr(false_branch, var_list)

        # Return the python/z3 equivalent of an if-then-else statement.
        return If(cond, true_branch, false_branch)

    # Case 4 : ex is a constant.
    elif (isinstance(ex, IntConst) or isinstance(ex, BoolConst)):

        # If Integer or Boolean constant, simply return the value.
        return ex.value

    # Case 5 : ex is a variable.
    elif (isinstance(ex, VarExpr)):

        # Return the z3 variable for the associated variable.
        return var_list[ex.name]


def is_valid(formula: Expression) -> bool:
    """
    Returns true if the formula is valid.

    """
    # TODO: implement this function.
    # It should return true if the formula is valid.
    # To check that the formula is valid, you should use the Z3 api

    # Our z3 solver initialized.
    s = Solver()

    # A dictionary of all the z3 variables with key paddle name and value z3 variable.
    vars = {}

    # Iterate through all the variables in the formula and add them to our dictionary.
    for var in formula.uses():
        if str(var.type) == "int":
            v = Int(var.name)
        elif str(var.type) == "bool":
            v = Bool(var.name)
        else:
            raise Exception("Variable Type must be Int or Bool")

        vars[var.name] = v

    # Recursively find the formula in terms of z3 variables.
    f = recurse_expr(formula, vars)

    # Add the NOT value of formula to our solver.
    s.add(Not(f))

    # If we can find a satisfiable solution for the NOT formula, then the formula is not valid.
    if s.check() == unsat:
        return True
    else:
        return False
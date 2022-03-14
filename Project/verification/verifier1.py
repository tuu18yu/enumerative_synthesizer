"""
CSC410 Final Project: Enumerative Synthesizer
by Victor Nicolet and Danya Lette

Fill in this file to complete the verification portion
of the assignment.
"""

from z3 import Solver, Bool, And, Xor, Or, Not, BoolRef, Ints, prove, Int
from lang.ast import *


def is_valid(formula: Expression) -> bool:
    """
    Returns true if the formula is valid.

    """
    # TODO: implement this function.
    # It should return true if the formula is valid.
    # To check that the formula is valid, you should use the Z3 api

    s = Solver()


    # raise Exception("verifier.is_valid is not implemented.")

def build(ex: Expression, s: Solver):
    # Case 1 : ex is a binary expression.
    if isinstance(ex, BinaryExpr):
        operator = ex.operator
        lhs = ex.left_operand
        rhs = ex.right_operand
        # TODO: Do something with op, lhs and rhs...
        if isinstance(operator, Expression):
            operator = build(operator)
        if isinstance(lhs, Expression):
            lhs = build(lhs)
        if isinstance(rhs, Expression):
            rhs = build(rhs)
        s.add()

    # Case 2 : ex is a unary expression.
    elif isinstance(ex, UnaryExpr):
        operator = ex.operator
        operand = ex.operand
        # TODO: Do something with op and ope...
        if isinstance(operator, Expression):
            operator = build(operator)
        if isinstance(operand, Expression):
            operand = build(operand)
        result = UnaryExpr(operator, operand)

    # Case 3 : ex is a if-then-else expression (a ternary expression).
    elif isinstance(ex, Ite):
        cond = ex.cond
        true_branch = ex.true_br
        false_branch = ex.false_br
        # TODO: Do something with cond, true_branch and false_branch
        if isinstance(cond, Expression):
            cond = build(cond)
        if isinstance(true_branch, Expression):
            true_branch = build(true_branch)
        if isinstance(false_branch, Expression):
            false_branch = build(false_branch)
        result = Ite(cond, true_branch, false_branch)

    # Case 4: ex is a variable
    elif isinstance(ex, VarExpr):
        if ex.var.type == 1:
            result = Int(ex.var.name)
        else:
            result = Bool(ex.var.name)

    return result


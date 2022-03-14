"""
CSC410 Final Project: Enumerative Synthesizer
by Victor Nicolet and Danya Lette

Fill in this file to complete the synthesis portion
of the assignment.
"""

from os import stat
from typing import Mapping
from z3 import *
from lang.ast import *


class Synthesizer():
    """
    This class is has three methods `synth_method_1`, `synth_method_2` or
    `synth_method_3` for generating expression for a program's holes.

    You may also choose to add data attributes and methods to this class
    to enable instances of `Synthesizer` to remember information about
    previous runs.

    Calling `synth_method_1`, `synth_method_2` or `synth_method_3` should
    produce a new set of hole completions at each call for a given
    `Synthesizer` instance.
    For example, suppose the program p contains one hole `h1` with the
    grammar `[ G : int -> G + G | 0 | 1 ]`. Then, the following sequence
    is a possible execution:
    ```
    > s = Synthesizer(p)
    > s.synth_method_1()
    { "h1" : 0 }
    > s.synth_method_1()
    { "h1" : 1 }
    > s.synth_method_1()
    { "h1" : 0 + 1 }
    ...
    ```
    Each call produces a hole completion. The returned object should
    be a mapping from the hole id (its name) to the expression of the
    hole.
    Each `synth_method_..` should implement a different enumeration
    strategy (e.g. depth first, breadth first, constants-first,
    variables-first...).

    **Don't forget that we expect your third method to be the best on
    average!**

    *Hint*: the method `hole_can_use` in the `Program` class returns the
    set of variables that a given hole can use in its completions.
    e.g. `prog.hole_can_use("h1")` returns the variables that "h1" can use.
    """

    def __init__(self, ast: Program):
        """
        Initialize the Synthesizer.
        The Synthesizer can have a state or other data attributes and
        methods to remember which programs have been synthesized before.
        """
        self.state = None
        # The synthesizer is initialized with the program ast it needs
        # to synthesize hole completions for.
        self.ast = ast

    def set_state(self, i):
        prog = self.ast
        variables = prog.hole_can_use(prog.holes[i].var.name)
        hole_grammar = prog.holes[i].grammar.rules

        for j in range(len(hole_grammar)):
            temp = hole_grammar[j].productions
            const_var = []
            binary = []
            grammar_int = []
            unary = []
            ite = []

            for p in temp:
                if isinstance(p, IntConst):
                    const_var.append(p)
                elif isinstance(p, BoolConst):
                    const_var.append(p)
                elif isinstance(p, GrammarInteger):
                    grammar_int.append(p)
                elif isinstance(p, GrammarVar):
                    for var in variables:
                        result = VarExpr(var, var.name)
                        const_var.append(result)
                elif isinstance(p, BinaryExpr):
                    binary.append(p)
                elif isinstance(p, UnaryExpr):
                    unary.append(p)
                elif isinstance(p, Ite):
                    ite.append(p)
            temp = []

            if hole_grammar[j].symbol.type.name == 'INT':
                if len(const_var) == 0:
                    temp = grammar_int + unary + ite + binary
                else:
                    temp = unary + ite + binary + grammar_int
            else:
                temp = binary + unary + ite + grammar_int

            for k in range(len(temp)):
                self.state[f'{i} {hole_grammar[j].symbol.name} state {k}'] = None

            if j == 0:
                check = len(const_var)
            self.state[f'{i} {hole_grammar[j].symbol.name} constvar'] = const_var
            self.state[f'{i} {hole_grammar[j].symbol.name} grammar'] = temp
            self.state[f'{i} {hole_grammar[j].symbol.name} const key'] = 0
            if j != 0:
                second = self.generate_const(i, hole_grammar[j].symbol.name)
                const_var += second
                self.state[f'{i} {hole_grammar[j].symbol.name} constvar'] = const_var

        if check != 0:
            self.state[f'{i} isConst'] = True
        else:
            self.state[f'{i} isConst'] = False
    
    def get_const_completion(self, i, hole_name):
        key = self.state[f'{i} {hole_name} const key']
        const_var = self.state[f'{i} {hole_name} constvar']
        res = const_var[key]
        if key < len(const_var) - 1:
            key = key + 1
        else:
            key = 0
            self.state[f'{i} isConst'] = False
        self.state[f'{i} {hole_name} const key'] = key
        return res

    def generate_const(self, i, grammar_name):
        grammar = self.state[f'{i} {grammar_name} grammar']
        const_var = self.state[f'{i} {grammar_name} constvar']
        possible = []

        for key in range(len(grammar)):
            if isinstance(grammar[key], BinaryExpr):
                lo_name = grammar[key].left_operand.name
                ro_name = grammar[key].right_operand.name

                lo_list = self.state[f'{i} {lo_name} constvar']
                ro_list = self.state[f'{i} {ro_name} constvar']
                operator = grammar[key].operator

                if lo_name != grammar_name and ro_name != grammar_name:
                    for l in range(len(lo_list)):
                        for m in range(len(ro_list)):
                            lo = lo_list[l]
                            ro = ro_list[m]

                            res = BinaryExpr(operator, lo, ro)
                            possible.append(res)

                elif lo_name == grammar_name and ro_name == grammar_name:
                    if len(const_var) != 0:
                        for l in range(len(const_var)):
                            for m in range(len(const_var)):
                                lo = const_var[l]
                                ro = const_var[m]

                                res = BinaryExpr(operator, lo, ro)
                                possible.append(res)

            
            elif isinstance(grammar[key], UnaryExpr):
                operand_name = grammar[key].operand.name
                operand_list = self.state[f'{i} {operand_name} constvar']
                operator = grammar[key].operator

                if operand_name != grammar_name:
                    for l in range(len(operand_list)):
                        operand = operand_list[l]
                        res = UnaryExpr(operator, operand)
                        possible.append(res)

                elif operand_name == grammar_name:
                    if len(const_var) != 0:
                        for l in range(len(const_var)):
                            operand = const_var[l]
                            res = UnaryExpr(operator, operand)
                            possible.append(res)

            elif isinstance(grammar[key], GrammarInteger):
                ints = [0]
                for i in range(0, 100):
                   ints.extend([i, -i])
                for integer in ints:
                    expr =IntConst(integer)
                    possible.append(expr)
        return possible

    def synth_method_1(self,) -> Mapping[str, Expression]:
        """
        Returns a map from each hole id in the program `self.ast`
        to an expression (method 1).

        **Description of method**
        The basic idea of this method is breadth first search. When initially called, it will
        call functions self.set_state which will set up the required environment for this algorithm.

        This algorithm will first return all the possible constants and variables on each call. After all
        constants and variables are called it will rotate between each possible expression on every call. 
        """
        map = {}
        prog = self.ast

        if self.state == None:
            self.state = {}
            for i in range(len(prog.holes)):
                self.set_state(i)

        for i in range(len(prog.holes)):
            map[prog.holes[i].var.name] = None
            grammar_name = prog.holes[i].grammar.rules[0].symbol.name
            grammar = self.state[f'{i} {grammar_name} grammar']
            isConst = self.state[f'{i} isConst']
            key = self.state[f'{i} {grammar_name} const key']

            while map[prog.holes[i].var.name] == None:
                if isConst:
                    map[prog.holes[i].var.name] = self.get_const_completion(i, grammar_name)
                elif isinstance(grammar[key], BinaryExpr):
                    state = self.state[f'{i} {grammar_name} state {key}']

                    if state == None:
                        state = (0, 1)

                    lo_name = grammar[key].left_operand.name
                    ro_name = grammar[key].right_operand.name

                    lo = self.state[f'{i} {lo_name} constvar'][state[0]]
                    ro = self.state[f'{i} {ro_name} constvar'][state[1]]
                    operator = grammar[key].operator

                    res = BinaryExpr(operator, lo, ro)

                    self.state[f'{i} {grammar_name} constvar'].append(res)
                  
                    
                    state = (state[0] + 1, state[1] + 1)
                

                    self.state[f'{i} {grammar_name} state {key}'] = state

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
                    map[prog.holes[i].var.name] = res
                
                elif isinstance(grammar[key], UnaryExpr):
                    state = self.state[f'{i} {grammar_name} state {key}']
                    if state == None:
                        state = 0

                    operand_name = grammar[key].operand.name

                    operand = self.state[f'{i} {operand_name} constvar'][state]
                    operator = grammar[key].operator

                    res = UnaryExpr(operator, operand)

                    self.state[f'{i} {grammar_name} constvar'].append(res)
                    state = state + 1
                    self.state[f'{i} {grammar_name} state {key}'] = state

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
                    map[prog.holes[i].var.name] = res

                elif isinstance(grammar[key], Ite):
                    state = self.state[f'{i} {grammar_name} state {key}']
                    if state == None:
                        state = (0, 1, 0)

                    cond_name = grammar[key].cond.name
                    true_br_name = grammar[key].true_br.name
                    false_br_name = grammar[key].false_br.name

                    cond = self.state[f'{i} {cond_name} constvar'][state[0]]
                    true_br = self.state[f'{i} {true_br_name} constvar'][state[1]]
                    false_br = self.state[f'{i} {false_br_name} constvar'][state[2]]

                    res = Ite(cond, true_br, false_br)

                    self.state[f'{i} {grammar_name} constvar'].append(res)

                    state = (state[0] + 1, state[1] + 1, state[2] + 1)

                    self.state[f'{i} {grammar_name} state {key}'] = state

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
                    map[prog.holes[i].var.name] = res

                elif isinstance(grammar[key], GrammarInteger):
                    state = self.state[f'{i} {grammar_name} state {key}']
                    if state is None:
                        state = 0
                        self.state[f'{i} state {key}'] = state + 1
                        res = IntConst(state)
                        map[prog.holes[i].var.name] = res
                        self.state[f'{i} {grammar_name} constvar'].append(res)
                    elif state < 0:
                        self.state[f'{i} state {key}'] = -state + 1
                        res = IntConst(state)
                        map[prog.holes[i].var.name] = res
                        self.state[f'{i} {grammar_name} constvar'].append(res)
                    else:
                        self.state[f'{i} state {key}'] = -state
                        res = IntConst(state)
                        map[prog.holes[i].var.name] = res
                        self.state[f'{i} {grammar_name} constvar'].append(res)

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
        return map


    def synth_method_2(self,) -> Mapping[str, Expression]:
        """
        Returns a map from each hole id in the program `self.ast`
        to an expression (method 2).

        **Description of method**
        The basic algorithm is same as synth_method_1, but the algorithm
        has been improved by changing the way to iterate when calling operands.
        This allows same variable to be called twice
        """
        map = {}
        prog = self.ast

        if self.state == None:
            self.state = {}
            for i in range(len(prog.holes)):
                self.set_state(i)

        for i in range(len(prog.holes)):
            map[prog.holes[i].var.name] = None
            grammar_name = prog.holes[i].grammar.rules[0].symbol.name
            grammar = self.state[f'{i} {grammar_name} grammar']
            isConst = self.state[f'{i} isConst']
            key = self.state[f'{i} {grammar_name} const key']

            while map[prog.holes[i].var.name] == None:
                if isConst:
                    map[prog.holes[i].var.name] = self.get_const_completion(i, grammar_name)
                elif isinstance(grammar[key], BinaryExpr):
                    state = self.state[f'{i} {grammar_name} state {key}']

                    if state == None:
                        state = (0, 0)

                    lo_name = grammar[key].left_operand.name
                    ro_name = grammar[key].right_operand.name

                    lo = self.state[f'{i} {lo_name} constvar'][state[0]]
                    ro = self.state[f'{i} {ro_name} constvar'][state[1]]
                    operator = grammar[key].operator

                    res = BinaryExpr(operator, lo, ro)

                    self.state[f'{i} {grammar_name} constvar'].append(res)
                  
                    if state[0] == state[1]:
                        state = (state[0] + 1, state[1])
                    elif state[0] > state[1]:
                        state = (state[1], state[0])
                    else:
                        state = (state[0] + 1, state[1])

                    self.state[f'{i} {grammar_name} state {key}'] = state

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
                    map[prog.holes[i].var.name] = res
                
                elif isinstance(grammar[key], UnaryExpr):
                    state = self.state[f'{i} {grammar_name} state {key}']
                    if state == None:
                        state = 0

                    operand_name = grammar[key].operand.name

                    operand = self.state[f'{i} {operand_name} constvar'][state]
                    operator = grammar[key].operator

                    res = UnaryExpr(operator, operand)

                    self.state[f'{i} {grammar_name} constvar'].append(res)
                    state = state + 1
                    self.state[f'{i} {grammar_name} state {key}'] = state

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
                    map[prog.holes[i].var.name] = res

                elif isinstance(grammar[key], Ite):
                    state = self.state[f'{i} {grammar_name} state {key}']
                    if state == None:
                        state = (0, 1, 0)

                    cond_name = grammar[key].cond.name
                    true_br_name = grammar[key].true_br.name
                    false_br_name = grammar[key].false_br.name

                    cond = self.state[f'{i} {cond_name} constvar'][state[0]]
                    true_br = self.state[f'{i} {true_br_name} constvar'][state[1]]
                    false_br = self.state[f'{i} {false_br_name} constvar'][state[2]]

                    res = Ite(cond, true_br, false_br)

                    self.state[f'{i} {grammar_name} constvar'].append(res)

                    if state[1] == state[2]:
                        state = (state[0], state[1] + 1, state[2])
                    elif state[1] > state[2]:
                        state = (state[0], state[2], state[1])
                    else:
                        state = (state[0], state[1] + 1, state[2])

                    self.state[f'{i} {grammar_name} state {key}'] = state

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
                    map[prog.holes[i].var.name] = res

                elif isinstance(grammar[key], GrammarInteger):
                    state = self.state[f'{i} {grammar_name} state {key}']
                    if state is None:
                        state = 0
                        self.state[f'{i} state {key}'] = state + 1
                        res = IntConst(state)
                        map[prog.holes[i].var.name] = res
                        self.state[f'{i} {grammar_name} constvar'].append(res)
                    elif state < 0:
                        self.state[f'{i} state {key}'] = -state + 1
                        res = IntConst(state)
                        map[prog.holes[i].var.name] = res
                        self.state[f'{i} {grammar_name} constvar'].append(res)
                    else:
                        self.state[f'{i} state {key}'] = -state
                        res = IntConst(state)
                        map[prog.holes[i].var.name] = res
                        self.state[f'{i} {grammar_name} constvar'].append(res)

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
        return map
        

    def synth_method_3(self,) -> Mapping[str, Expression]:
        """
        Returns a map from each hole id in the program `self.ast`
        to an expression (method 3).

        **Description of method**
        The final algorithm has been improved upon synth_method_2
        """
        map = {}
        prog = self.ast

        if self.state == None:
            self.state = {}
            for i in range(len(prog.holes)):
                self.set_state(i)

        for i in range(len(prog.holes)):
            map[prog.holes[i].var.name] = None
            grammar_name = prog.holes[i].grammar.rules[0].symbol.name
            grammar = self.state[f'{i} {grammar_name} grammar']
            isConst = self.state[f'{i} isConst']
            key = self.state[f'{i} {grammar_name} const key']

            while map[prog.holes[i].var.name] == None:
                if isConst:
                    map[prog.holes[i].var.name] = self.get_const_completion(i, grammar_name)
                elif isinstance(grammar[key], BinaryExpr):
                    state = self.state[f'{i} {grammar_name} state {key}']

                    if state == None:
                        state = (0, 0)

                    lo_name = grammar[key].left_operand.name
                    ro_name = grammar[key].right_operand.name

                    lo = self.state[f'{i} {lo_name} constvar'][state[0]]
                    ro = self.state[f'{i} {ro_name} constvar'][state[1]]
                    operator = grammar[key].operator

                    res = BinaryExpr(operator, lo, ro)

                    self.state[f'{i} {grammar_name} constvar'].append(res)
                  
                    if state[0] == state[1]:
                        state = (state[0] + 1, state[1])
                    elif state[0] > state[1]:
                        state = (state[1], state[0])
                    else:
                        state = (state[0] + 1, state[1])

                    self.state[f'{i} {grammar_name} state {key}'] = state

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
                    map[prog.holes[i].var.name] = res
                
                elif isinstance(grammar[key], UnaryExpr):
                    state = self.state[f'{i} {grammar_name} state {key}']
                    if state == None:
                        state = 0

                    operand_name = grammar[key].operand.name

                    operand = self.state[f'{i} {operand_name} constvar'][state]
                    operator = grammar[key].operator

                    res = UnaryExpr(operator, operand)

                    self.state[f'{i} {grammar_name} constvar'].append(res)
                    state = state + 1
                    self.state[f'{i} {grammar_name} state {key}'] = state

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
                    map[prog.holes[i].var.name] = res

                elif isinstance(grammar[key], Ite):
                    state = self.state[f'{i} {grammar_name} state {key}']
                    if state == None:
                        state = (0, 1, 0)

                    cond_name = grammar[key].cond.name
                    true_br_name = grammar[key].true_br.name
                    false_br_name = grammar[key].false_br.name

                    cond = self.state[f'{i} {cond_name} constvar'][state[0]]
                    true_br = self.state[f'{i} {true_br_name} constvar'][state[1]]
                    false_br = self.state[f'{i} {false_br_name} constvar'][state[2]]

                    res = Ite(cond, true_br, false_br)

                    self.state[f'{i} {grammar_name} constvar'].append(res)

                    if state[1] == state[2]:
                        state = (state[0], state[1] + 1, state[2])
                    elif state[1] > state[2]:
                        state = (state[0], state[2], state[1])
                    else:
                        state = (state[0], state[1] + 1, state[2])

                    self.state[f'{i} {grammar_name} state {key}'] = state

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
                    map[prog.holes[i].var.name] = res

                elif isinstance(grammar[key], GrammarInteger):
                    state = self.state[f'{i} {grammar_name} state {key}']
                    if state is None:
                        state = 0
                        self.state[f'{i} state {key}'] = state + 1
                        res = IntConst(state)
                        map[prog.holes[i].var.name] = res
                        self.state[f'{i} {grammar_name} constvar'].append(res)
                    elif state < 0:
                        self.state[f'{i} state {key}'] = -state + 1
                        res = IntConst(state)
                        map[prog.holes[i].var.name] = res
                        self.state[f'{i} {grammar_name} constvar'].append(res)
                    else:
                        self.state[f'{i} state {key}'] = -state
                        res = IntConst(state)
                        map[prog.holes[i].var.name] = res
                        self.state[f'{i} {grammar_name} constvar'].append(res)

                    if key < len(grammar) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} {grammar_name} const key'] = key
        return map

    
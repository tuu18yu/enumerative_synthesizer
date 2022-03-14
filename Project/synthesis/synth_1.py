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

    # TODO: implement something that allows you to remember which
    # programs have already been generated.

    def set_state(self, i):
        prog = self.ast
        defined_var = prog.hole_can_use(prog.holes[i].var.name)
 
        hole_grammar = prog.holes[i].grammar.rules
        prod = {}

        for j in range(len(hole_grammar)):
            if j == 0:
                v_name = hole_grammar[j].symbol.name
    
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
                    for var in defined_var:
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
                temp = unary + ite + binary + grammar_int
            else:
                temp = binary + unary + ite + grammar_int

            self.state[f'{i} {hole_grammar[j].symbol.name} key'] = 0
            self.state[f'{i} {hole_grammar[j].symbol.name} const key'] = 0
            self.state[f'{i} {hole_grammar[j].symbol.name} constvar'] = const_var

            for k in range(len(temp)):
                self.state[f'{i} {hole_grammar[j].symbol.name} state {k}'] = None
                    
            prod[hole_grammar[j].symbol.name] = temp


        self.state[f'{i} name'] = v_name
        self.state[f'{i} prod'] = prod
        self.state[f'{i} integers'] = integers
        self.state[f'{i} booleans'] = booleans
        self.state[f'{i} variables'] = defined_var
        self.state[f'{i} isConst'] = True
        self.state[f'{i} key'] = 0

    def synth_method_1(self,) -> Mapping[str, Expression]:
        """
        Returns a map from each hole id in the program `self.ast`
        to an expression (method 1).

        **TODO: write a description of your approach in this method.**
        """
        # TODO : complete this method
        prog = self.ast
        map = {}

        if self.state == None:
            self.state = {}
            for i in range(len(prog.holes)):
                self.set_state(i)

        for i in range(len(prog.holes)):
            map[prog.holes[i].var.name] = None
            key = self.state[f'{i} key']
            prod = self.state[f'{i} prod']
            integers = self.statisConst = self.state[f'{i} isConst']e[f'{i} integers']
            booleans = self.state[f'{i} booleans']
            defined_var = self.state[f'{i} variables']
            v_name = self.state[f'{i} name']
            isConst = self.state[f'{i} isConst']

            while map[prog.holes[i].var.name] == None:
                if isConst:
                    map[prog.holes[i].var.name] = self.get_const_completion(self, i, prog.holes[i].var.name)

                elif isinstance(prod[key], BinaryExpr):
                    if (prod[key].left_operand.name == v_name) and (prod[key].left_operand.name == v_name):
                        if state is None:
                            state = [[],[]]

                        operator = prod[key].operator

                        if operator.value < 6:
                            check_list = integers
                        else:
                            check_list = defined_var

                        for var1 in check_list:
                            if var1 not in state[0]:
                                state[1] = []

                            if len(state[1]) < len(check_list):
                                if var1 not in state[0]:
                                    state[0].append(var1)

                                for var2 in check_list:
                                    if var2 not in state[1]:
                                        isFinished = True
                                        state[1].append(var2)
                                        if isinstance(var1, Variable):
                                            lo = VarExpr(var1, var1.name)
                                        else:
                                            lo = var1
                                        if isinstance(var1, Variable):
                                            ro = VarExpr(var2, var2.name)
                                        else:
                                            ro = var2
                                        res = BinaryExpr(operator, lo, ro)

                                        if operator.value < 6:
                                            integers.append(res)
                                            self.state[f'{i} integers'] = integers
                                        else:
                                            booleans.append(res)
                                            self.state[f'{i} booleans'] = booleans
                                    
                                        self.state[f'{i} state {key}'] = state
                                        map[prog.holes[i].var.name] = res
                                        if key < len(prod) - 1:
                                            key = key + 1
                                        else:
                                            key = 0
                                        self.state[f'{i} key'] = key
                                        break
                            if map[prog.holes[i].var.name] != None:
                                break
            

                    else:
                        if state is None:
                            state = [[],[]]

                        operator = prod[key].operator

                        if operator.value < 6:
                            check_list = integers
                        else:
                            check_list = defined_var

                        isFinished = False
                        for var1 in check_list:
                            if var1 not in state[0]:
                                state[1] = []

                            if len(state[1]) < len(check_list):
                                if var1 not in state[0]:
                                    state[0].append(var1)

                                ro = self._get_var(i, prod[key].right_operand.name)
                                if ro not in state[1]:
                                    isFinished = True
                                        
                                    state[1].append(ro)
                                    if isinstance(var1, Variable):
                                        lo = VarExpr(var1, var1.name)
                                    else:
                                        lo = var1
                                    
                                    res = BinaryExpr(operator, lo, ro)

                                    if operator.value < 6:
                                        integers.append(res)
                                        self.state[f'{i} integers'] = integers
                                    else:
                                        booleans.append(res)
                                        self.state[f'{i} booleans'] = booleans
                                
                                    self.state[f'{i} state {key}'] = state
                                    map[prog.holes[i].var.name] = res
                                    if key < len(prod) - 1:
                                            key = key + 1
                                    else:
                                        key = 0
                                    self.state[f'{i} key'] = key
                                    state = None
                                    self.state[f'{i} state {key}'] = None
                                    
                            if map[prog.holes[i].var.name] != None:
                                break
            
                        else:
                            lo = self._get_var(i, prod[key].left_operand.name)

                        if prod[key].right_operand.name == v_name:
                            if state is None:
                                state = []

                            for var in defined_var:
                                if var not in state:
                                    state.append(var)
                                    ro = VarExpr(var, var.name)
                                    self.state[f'{i} state {key}'] = state
                                    break
                        else:
                            ro = self._get_var(i, prod[key].right_operand.name)
                        if operator.value < 6:
                            integers.append(res)
                            self.state[f'{i} integers'] = integers
                        else:
                            booleans.append(res)
                            self.state[f'{i} booleans'] = booleans
                    
                        self.state[f'{i} state {key}'] = state
                        map[prog.holes[i].var.name] = res


                elif isinstance(prod[key], UnaryExpr):
                    if state is None:
                        state = []

                    cond = self._get_var(i, prod[key].condition.name)
                    isFinished = False
                    for var in defined_var:
                        if var not in state:
                            isFinished = True
                            state.append(var)
                            operator = prod[key].operator
                            operand = VarExpr(var, var.name)
                            self.state[f'{i} state {key}'] = state
                            map[prog.holes[i].var.name] = UnaryExpr(operator, operand)
                            break
                        isFinished = False

                    if not isFinished:
                        key = key + 1
                        self.state[f'{i} key'] = key
                        state = None
                        self.state[f'{i} state'] = None
                  
                elif isinstance(prod[key], Ite):
                    if state is None:
                        state = [[],[]]

                    cond = self._get_var(i, prod[key].cond.name)

                    for var1 in integers:
                        if var1 not in self.state[key][0]:
                            self.state[key][1] = []

                        if len(self.state[key][1]) < len(integers):
                            if var1 not in self.state[key][0]:
                                self.state[key][0].append(var1)

                            for var2 in integers:
                                if var2 not in self.state[key][1]:
                                    self.state[key][1].append(var2)
                                    lo = var1
                                    ro = var2
                                    res = BinaryExpr(operator, lo, ro)
                                    integers.append(res)
                                    map[prog.holes[i].var.name] = res
                                    return map

                elif isinstance(prod[key], GrammarInteger):
                    if state is None:
                        state = 0
                        self.state[f'{i} state {key}'] = state + 1
                        map[prog.holes[i].var.name] = IntConst(state)
                    elif state < 0:
                        self.state[f'{i} state {key}'] = -state + 1
                        map[prog.holes[i].var.name] = IntConst(state)
                    else:
                        self.state[f'{i} state {key}'] = -state
                        map[prog.holes[i].var.name] = IntConst(state)

                    if key < len(prod) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} key'] = key

    def synth_method_2(self,) -> Mapping[str, Expression]:
        """
        Returns a map from each hole id in the program `self.ast`
        to an expression (method 2).

        **TODO: write a description of your approach in this method.**
        """
        # TODO : complete this method
        raise Exception("Synth.synth_method_3 is not implemented.")
        

    def synth_method_3(self,) -> Mapping[str, Expression]:
        """
        Returns a map from each hole id in the program `self.ast`
        to an expression (method 3).

        **TODO: write a description of your approach in this method.**
        """
        # TODO : complete this method
        raise Exception("Synth.synth_method_3 is not implemented.")

    def set_state(self, i):
        prog = self.ast
        defined_var = prog.hole_can_use(prog.holes[i].var.name)
        integers = []
        booleans = []

        for v in defined_var:
            if v.type.value == 1:
                integers.append(v)
            else:
                booleans.append(v)

        hole_grammar = prog.holes[i].grammar.rules
        prod = {}

        for j in range(len(hole_grammar)):
            if j == 0:
                v_name = hole_grammar[j].symbol.name
    
            temp = hole_grammar[j].productions
            const_var = []
            binary = []
            grammar_int = []
            unary = []
            ite = []

            for p in temp:
                if isinstance(p, IntConst):
                    integers.append(p)
                    const_var.append(p)
                elif isinstance(p, BoolConst):
                    booleans.append(p)
                    const_var.append(p)
                elif isinstance(p, GrammarInteger):
                    grammar_int.append(p)
                elif isinstance(p, GrammarVar):
                    for var in defined_var:
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
                temp =  unary + ite + binary + grammar_int
            else:
                temp =  binary + unary + ite + grammar_int

            self.state[f'{i} {hole_grammar[j].symbol.name} key'] = 0
            self.state[f'{i} {hole_grammar[j].symbol.name} const key'] = 0
            self.state[f'{i} {hole_grammar[j].symbol.name} constvar'] = const_var

            for k in range(len(temp)):
                self.state[f'{i} {hole_grammar[j].symbol.name} state {k}'] = None
                    
            prod[hole_grammar[j].symbol.name] = temp


        self.state[f'{i} name'] = v_name
        self.state[f'{i} prod'] = prod
        self.state[f'{i} integers'] = integers
        self.state[f'{i} booleans'] = booleans
        self.state[f'{i} variables'] = defined_var
        self.state[f'{i} isConst'] = True
        self.state[f'{i} key'] = 0
        
    
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
    

    # def get_completion(self, i, hole_name):
    #     result = None
    #     prod = self.state[f'{i} prod'][hole_name]
    #     key = self.state[f'{i} {hole_name} key']
    #     state = self.state[f'{i} {hole_name} state {key}']
    #     defined_var = self.state[f'{i} variables']

    #     while result == None:
    #         if isinstance(prod[key], BinaryExpr):
    #             lo = self.get_completion(i, prod[key].left_operand.name)
    #             ro = self.get_completion(i, prod[key].right_operand.name)
    #             if (prod[key].left_operand.name == v_name) and (prod[key].left_operand.name == v_name):
    #                 if state is None:
    #                     state = [[],[]]

    #                 operator = prod[key].operator

    #                 if operator.value < 6:
    #                     check_list = integers
    #                 else:
    #                     check_list = defined_var

    #                 for var1 in check_list:
    #                     if var1 not in state[0]:
    #                         state[1] = []

    #                     if len(state[1]) < len(check_list):
    #                         if var1 not in state[0]:
    #                             state[0].append(var1)

    #                         for var2 in check_list:
    #                             if var2 not in state[1]:
    #                                 isFinished = True
    #                                 state[1].append(var2)
    #                                 if isinstance(var1, Variable):
    #                                     lo = VarExpr(var1, var1.name)
    #                                 else:
    #                                     lo = var1
    #                                 if isinstance(var1, Variable):
    #                                     ro = VarExpr(var2, var2.name)
    #                                 else:
    #                                     ro = var2
    #                                 res = BinaryExpr(operator, lo, ro)

    #                                 if operator.value < 6:
    #                                     integers.append(res)
    #                                     self.state[f'{i} integers'] = integers
    #                                 else:
    #                                     booleans.append(res)
    #                                     self.state[f'{i} booleans'] = booleans
                                
    #                                 self.state[f'{i} state {key}'] = state
    #                                 map[prog.holes[i].var.name] = res
    #                                 if key < len(prod) - 1:
    #                                     key = key + 1
    #                                 else:
    #                                     key = 0
    #                                 self.state[f'{i} key'] = key
    #                                 break
    #                     if map[prog.holes[i].var.name] != None:
    #                         break
        

    #             else:
    #                 if state is None:
    #                     state = [[],[]]

    #                 operator = prod[key].operator

    #                 if operator.value < 6:
    #                     check_list = integers
    #                 else:
    #                     check_list = defined_var

    #                 isFinished = False
    #                 for var1 in check_list:
    #                     if var1 not in state[0]:
    #                         state[1] = []

    #                     if len(state[1]) < len(check_list):
    #                         if var1 not in state[0]:
    #                             state[0].append(var1)

    #                         ro = self._get_var(i, prod[key].right_operand.name)
    #                         if ro not in state[1]:
    #                             isFinished = True
                                    
    #                             state[1].append(ro)
    #                             if isinstance(var1, Variable):
    #                                 lo = VarExpr(var1, var1.name)
    #                             else:
    #                                 lo = var1
                                
    #                             res = BinaryExpr(operator, lo, ro)

    #                             if operator.value < 6:
    #                                 integers.append(res)
    #                                 self.state[f'{i} integers'] = integers
    #                             else:
    #                                 booleans.append(res)
    #                                 self.state[f'{i} booleans'] = booleans
                            
    #                             self.state[f'{i} state {key}'] = state
    #                             map[prog.holes[i].var.name] = res
    #                             if key < len(prod) - 1:
    #                                     key = key + 1
    #                             else:
    #                                 key = 0
    #                             self.state[f'{i} key'] = key
    #                             state = None
    #                             self.state[f'{i} state {key}'] = None
                                
    #                     if map[prog.holes[i].var.name] != None:
    #                         break
        
    #                 else:
    #                     lo = self._get_var(i, prod[key].left_operand.name)

    #                 if prod[key].right_operand.name == v_name:
    #                     if state is None:
    #                         state = []

    #                     for var in defined_var:
    #                         if var not in state:
    #                             state.append(var)
    #                             ro = VarExpr(var, var.name)
    #                             self.state[f'{i} state {key}'] = state
    #                             break
    #                 else:
    #                     ro = self._get_var(i, prod[key].right_operand.name)
    #                 if operator.value < 6:
    #                     integers.append(res)
    #                     self.state[f'{i} integers'] = integers
    #                 else:
    #                     booleans.append(res)
    #                     self.state[f'{i} booleans'] = booleans
                
    #                 self.state[f'{i} state {key}'] = state
    #                 map[prog.holes[i].var.name] = res


    #         elif isinstance(prod[key], UnaryExpr):
    #             if state is None:
    #                 state = []

    #             operand = self.get_completion(i, prod[key].condition.name)
    #             isFinished = False
    #             for var in defined_var:
    #                 if var not in state:
    #                     isFinished = True
    #                     state.append(var)
    #                     operator = prod[key].operator
    #                     operand = VarExpr(var, var.name)
    #                     self.state[f'{i} state {key}'] = state
    #                     map[prog.holes[i].var.name] = UnaryExpr(operator, operand)
    #                     break
    #                 isFinished = False

    #             if not isFinished:
    #                 key = key + 1
    #                 self.state[f'{i} key'] = key
    #                 state = None
    #                 self.state[f'{i} state'] = None
                
    #         elif isinstance(prod[key], Ite):
    #             if state is None:
    #                 state = [[],[]]

    #             cond = self._get_var(i, prod[key].cond.name)

    #             for var1 in integers:
    #                 if var1 not in self.state[key][0]:
    #                     self.state[key][1] = []

    #                 if len(self.state[key][1]) < len(integers):
    #                     if var1 not in self.state[key][0]:
    #                         self.state[key][0].append(var1)

    #                     for var2 in integers:
    #                         if var2 not in self.state[key][1]:
    #                             self.state[key][1].append(var2)
    #                             lo = var1
    #                             ro = var2
    #                             res = BinaryExpr(operator, lo, ro)
    #                             integers.append(res)
    #                             map[prog.holes[i].var.name] = res
    #                             return map

    #         elif isinstance(prod[key], BoolConst):
    #             result = prod[key]
    #             if key < len(prod) - 1:
    #                 key = key + 1
    #             else:
    #                 key = 0
    #             self.state[f'{i} {hole_name} key'] = key
                
    #         elif isinstance(prod[key], IntConst):
    #             result = prod[key]
    #             if key < len(prod) - 1:
    #                 key = key + 1
    #             else:
    #                 key = 0
    #             self.state[f'{i} {hole_name} key'] = key

    #         elif isinstance(prod[key], GrammarInteger):
    #             if state is None:
    #                 state = 0
    #                 self.state[f'{i} {hole_name} state {key}'] = state + 1
    #                 result = IntConst(state)
    #             elif state < 0:
    #                 self.state[f'{i} {hole_name} state {key}'] = -state + 1
    #                 result = IntConst(state)
    #             else:
    #                 self.state[f'{i} {hole_name} state {key}'] = -state
    #                 result = IntConst(state)

    #             if key < len(prod) - 1:
    #                 key = key + 1
    #             else:
    #                 key = 0
    #             self.state[f'{i} {hole_name} key'] = key


    #         elif isinstance(prod[key], GrammarVar):
    #             if state is None:
    #                 state = []

    #             for var in defined_var:
    #                 if var not in state:
    #                     state.append(var)
    #                     self.state[f'{i} {hole_name} state {key}'] = state
    #                     result = VarExpr(var, var.name)

    #                     if key < len(prod) - 1:
    #                         key = key + 1
    #                     else:
    #                         key = 0
    #                     self.state[f'{i} {hole_name} key'] = key
    #                     break

    #             if result == None:
    #                 self.state[f'{i} {hole_name} state {key}'] = []

    #     return result
    
    
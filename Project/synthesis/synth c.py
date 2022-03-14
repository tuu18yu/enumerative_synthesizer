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

    def _get_var(self, i, name) -> Mapping[str, Expression]:
        """
        Returns a map from each hole id in the program `self.ast`
        to an expression (method 1).

        **TODO: write a description of your approach in this method.**
        """
        # TODO : complete this method
        result = None
        key =  self.state[f'{i} {name} key']
        prod = self.state[f'{i} other prod'][name]
        integers = self.state[f'{i} integers']
        booleans = self.state[f'{i} booleans']
        defined_var = self.state[f'{i} variables']
        state = self.state[f'{i} {name} state']
        v_name = self.state[f'{i} name']

        while result == None:
            # if isinstance(prod[key], BinaryExpr):
            #     if (prod[key].left_operand.name == v_name) and (prod[key].left_operand.name == v_name):
            #         if state is None:
            #             state = [[],[]]

            #         operator = prod[key].operator 
            #         isFinished = False
            #         for var1 in integers:
            #             if var1 not in state[0]:
            #                 state[1] = []

            #             if len(state[1]) < len(integers):
            #                 if var1 not in state[0]:
            #                     state[0].append(var1)

            #                 for var2 in integers:
            #                     if var2 not in state[1]:
            #                         isFinished = True
            #                         state[1].append(var2)
            #                         lo = VarExpr(var1, var1.name)
            #                         ro = VarExpr(var2, var2.name)
            #                         res = BinaryExpr(operator, lo, ro)
            #                         # integers.append(res)
            #                         # self.state[f'{i} integers'] = integers
            #                         self.state[f'{i} state'] = state
            #                         result = res
            #                         break
            #             if result != None:
            #                 break
        
            #         if not isFinished:
            #             key = key + 1
            #             self.state[f'{i} key'] = key
            #             state = None
            #             self.state[f'{i} state'] = None
            #     else:
            #         if prod[key].left_operand.name == v_name:
            #             if state is None:
            #                 state = []

            #             for var in defined_var:
            #                 if var not in state:
            #                     state.append(var)
            #                     lo = VarExpr(var, var.name)
            #                     self.state[f'{i} state'] = state
            #                     break
            #         else:
            #             lo = self._get_var(i, prod[key].left_operand.name)

            if isinstance(prod[key], UnaryExpr):
                if state is None:
                    state = []

                isFinished = False
                for var in defined_var:
                    if var not in state:
                        isFinished = True
                        state.append(var)
                        operator = prod[key].operator
                        if isinstance(var, Variable):
                            operand = VarExpr(var, var.name)
                        else:
                            operand = var
                        self.state[f'{i} {name} state'] = state
                        result = UnaryExpr(operator, operand)
                        break
                    isFinished = False

                if not isFinished:
                    key = key + 1
                    self.state[f'{i} {name} key'] = key
                    state = None
                    self.state[f'{i} {name} state'] = None
                
            # elif isinstance(prod[key], Ite):
            #     if self.state[key] is None:
            #         self.state[key] = [[],[],[]]

            #     operator = prod[key].operator 
            #     for var1 in integers:
            #         if var1 not in self.state[key][0]:
            #             self.state[key][1] = []

            #         if len(self.state[key][1]) < len(integers):
            #             if var1 not in self.state[key][0]:
            #                 self.state[key][0].append(var1)

            #             for var2 in integers:
            #                 if var2 not in self.state[key][1]:
            #                     self.state[key][1].append(var2)
            #                     lo = var1
            #                     ro = var2
            #                     res = BinaryExpr(operator, lo, ro)
            #                     integers.append(res)
            #                     map[prog.holes[i].var.name] = res
            #                     return map

            elif isinstance(prod[key], BoolConst):
                result = prod[key]
                key = key + 1
                self.state[f'{i} {name} key'] = key
                state = None
                self.state[f'{i} {name} state'] = None

                
            elif isinstance(prod[key], IntConst):
                result = prod[key]
                key = key + 1
                self.state[f'{i} {name} key'] = key
                state = None
                self.state[f'{i} {name} state'] = None

            elif isinstance(prod[key], GrammarInteger):
                if state is None:
                    state = 0
                    self.state[f'{i} {name} state'] = state + 1
                    result = IntConst(state)
                elif state < 0:
                    self.state[f'{i} {name} state'] = -state + 1
                    result = IntConst(state)
                else:
                    self.state[f'{i} {name} state'] = -state
                    result = IntConst(state)


            elif isinstance(prod[key], GrammarVar):
                if state is None:
                    state = []

                isFinished = False
                for var in defined_var:
                    if var not in state:
                        isFinished = True
                        state.append(var)
                        self.state[f'{i} {name} state'] = state
                        result = VarExpr(var, var.name)
                        break
                    isFinished = False

                if not isFinished:    
                    key = key + 1
                    self.state[f'{i} {name} key'] = key
                    state = None
                    self.state[f'{i} {name} state'] = None
        return result

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
                
                defined_var = prog.hole_can_use(prog.holes[i].var.name)
                integers = []
                booleans = []

                for v in defined_var:
                    if v.type.value == 1:
                        integers.append(v)
                    else:
                        booleans.append(v)

                hole_grammar = prog.holes[i].grammar.rules
                prod = []
                other_prod = {}

                for j in range(len(hole_grammar)):
                    if j == 0:
                        prod += hole_grammar[j].productions
                        v_name = hole_grammar[j].symbol.name
                        self.state[f'{i} {hole_grammar[j].symbol.name} key'] = 0
                        self.state[f'{i} {hole_grammar[j].symbol.name} state'] = None
                        other_prod[hole_grammar[j].symbol.name] = prod
                    else:
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
                                const_var.append(p)
                            elif isinstance(p, BinaryExpr):
                                binary.append(p)
                            elif isinstance(p, UnaryExpr):
                                unary.append(p)
                            elif isinstance(p, Ite):
                                ite.append(p)
                        temp = []

                        if hole_grammar[j].symbol.type.name == 'INT':
                            temp = const_var + unary + ite + binary + grammar_int
                        else:
                            temp = const_var + binary + unary + ite + grammar_int

                        self.state[f'{i} {hole_grammar[j].symbol.name} key'] = 0
                        self.state[f'{i} {hole_grammar[j].symbol.name} state'] = None
                                
                        other_prod[hole_grammar[j].symbol.name] = temp

                const_var = []
                binary = []
                grammar_int = []
                unary = []
                ite = []

                for p in prod:
                    if isinstance(p, IntConst):
                        integers.append(p)
                        const_var.append(p)
                    elif isinstance(p, BoolConst):
                        booleans.append(p)
                        const_var.append(p)
                    elif isinstance(p, GrammarInteger):
                        grammar_int.append(p)
                    elif isinstance(p, GrammarVar):
                        const_var.append(p)
                    elif isinstance(p, BinaryExpr):
                        binary.append(p)
                    elif isinstance(p, UnaryExpr):
                        unary.append(p)
                    elif isinstance(p, Ite):
                        ite.append(p)
                prod = []
                if hole_grammar[j].symbol.type.name == 'INT':
                    prod = const_var + unary + ite + binary + grammar_int
                else:
                    prod = const_var + binary + unary + ite + grammar_int

                self.state[f'{i} name'] = v_name
                self.state[f'{i} prod'] = prod
                self.state[f'{i} other prod'] = other_prod
                self.state[f'{i} integers'] = integers
                self.state[f'{i} booleans'] = booleans
                self.state[f'{i} variables'] = defined_var
                self.state[f'{i} key'] = 0
                self.state[f'{i} state'] = None

        for i in range(len(prog.holes)):
            map[prog.holes[i].var.name] = None
            key = self.state[f'{i} key']
            prod = self.state[f'{i} prod']
            other_prod = self.state[f'{i} other prod']
            integers = self.state[f'{i} integers']
            booleans = self.state[f'{i} booleans']
            defined_var = self.state[f'{i} variables']
            state = self.state[f'{i} state']
            v_name = self.state[f'{i} name']

            while map[prog.holes[i].var.name] == None:
                if isinstance(prod[key], BinaryExpr):
                    if (prod[key].left_operand.name == v_name) and (prod[key].left_operand.name == v_name):
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
                                    
                                        self.state[f'{i} state'] = state
                                        map[prog.holes[i].var.name] = res
                                        break
                            if map[prog.holes[i].var.name] != None:
                                break
            
                        if not isFinished:
                            key = key + 1
                            self.state[f'{i} key'] = key
                            state = None
                            self.state[f'{i} state'] = None
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

                                ro = self._get_var(i, prod[key].right_operand.name, state[1])
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
                                
                                    self.state[f'{i} state'] = state
                                    map[prog.holes[i].var.name] = res
                                    
                            if map[prog.holes[i].var.name] != None:
                                break
            
                        if not isFinished:
                            key = key + 1
                            self.state[f'{i} key'] = key
                            state = None
                            self.state[f'{i} state'] = None
                            
                        else:
                            lo = self._get_var(i, prod[key].left_operand.name)

                        if prod[key].right_operand.name == v_name:
                            if state is None:
                                state = []

                            for var in defined_var:
                                if var not in state:
                                    state.append(var)
                                    ro = VarExpr(var, var.name)
                                    self.state[f'{i} state'] = state
                                    break
                        else:
                            ro = self._get_var(i, prod[key].right_operand.name, state[1])
                        if operator.value < 6:
                            integers.append(res)
                            self.state[f'{i} integers'] = integers
                        else:
                            booleans.append(res)
                            self.state[f'{i} booleans'] = booleans
                    
                        self.state[f'{i} state'] = state
                        map[prog.holes[i].var.name] = res

                elif isinstance(prod[key], UnaryExpr):
                    if state is None:
                        state = []

                    isFinished = False
                    for var in defined_var:
                        if var not in state:
                            isFinished = True
                            state.append(var)
                            operator = prod[key].operator
                            operand = VarExpr(var, var.name)
                            self.state[f'{i} state'] = state
                            map[prog.holes[i].var.name] = UnaryExpr(operator, operand)
                            break
                        isFinished = False

                    if not isFinished:
                        key = key + 1
                        self.state[f'{i} key'] = key
                        state = None
                        self.state[f'{i} state'] = None
                  
                elif isinstance(prod[key], Ite):
                    if self.state[key] is None:
                        self.state[key] = [[],[],[]]

                    operator = prod[key].operator 
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

                elif isinstance(prod[key], BoolConst):
                    res = prod[key]
                    map[prog.holes[i].var.name] = res
                    key = key + 1
                    self.state[f'{i} key'] = key
                    state = None
                    self.state[f'{i} state'] = None

                    
                elif isinstance(prod[key], IntConst):
                    res = prod[key]
                    map[prog.holes[i].var.name] = res
                    key = key + 1
                    self.state[f'{i} key'] = key
                    state = None
                    self.state[f'{i} state'] = None

                elif isinstance(prod[key], GrammarInteger):
                    if state is None:
                        state = 0
                        self.state[f'{i} state'] = state + 1
                        map[prog.holes[i].var.name] = IntConst(state)
                    elif state < 0:
                        self.state[f'{i} state'] = -state + 1
                        map[prog.holes[i].var.name] = IntConst(state)
                    else:
                        self.state[f'{i} state'] = -state
                        map[prog.holes[i].var.name] = IntConst(state)


                elif isinstance(prod[key], GrammarVar):
                    if state is None:
                        state = []

                    isFinished = False
                    for var in defined_var:
                        if var not in state:
                            isFinished = True
                            state.append(var)
                            self.state[f'{i} state'] = state
                            map[prog.holes[i].var.name] = VarExpr(var, var.name)
                            break
                        isFinished = False

                    if not isFinished:    
                        key = key + 1
                        self.state[f'{i} key'] = key
                        state = None
                        self.state[f'{i} state'] = None
        return map
        # raise Exception("Synth.Synthesizer.synth_method_1 is not implemented.")

    def synth_method_2(self,) -> Mapping[str, Expression]:
        """
        Returns a map from each hole id in the program `self.ast`
        to an expression (method 2).

        **TODO: write a description of your approach in this method.**
        """
        # TODO : complete this method
        prog = self.ast
        map = {}

        if self.state == None:
            self.state = {}

            for i in range(len(prog.holes)):
                
                defined_var = prog.hole_can_use(prog.holes[i].var.name)
                integers = []
                booleans = []

                for v in defined_var:
                    if v.type.value == 1:
                        integers.append(v)
                    else:
                        booleans.append(v)

                hole_grammar = prog.holes[i].grammar.rules
                prod = []
                other_prod = {}

                for j in range(len(hole_grammar)):
                    if j == 0:
                        prod += hole_grammar[j].productions
                        v_name = hole_grammar[j].symbol.name
                        self.state[f'{i} {hole_grammar[j].symbol.name} key'] = 0
                        self.state[f'{i} {hole_grammar[j].symbol.name} state'] = None
                        other_prod[hole_grammar[j].symbol.name] = prod
                    else:
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
                                const_var.append(p)
                            elif isinstance(p, BinaryExpr):
                                binary.append(p)
                            elif isinstance(p, UnaryExpr):
                                unary.append(p)
                            elif isinstance(p, Ite):
                                ite.append(p)
                        temp = []

                        if hole_grammar[j].symbol.type.name == 'INT':
                            temp = const_var + unary + ite + binary + grammar_int
                        else:
                            temp = const_var + binary + unary + ite + grammar_int

                        self.state[f'{i} {hole_grammar[j].symbol.name} key'] = 0
                        self.state[f'{i} {hole_grammar[j].symbol.name} state'] = None
                                
                        other_prod[hole_grammar[j].symbol.name] = temp

                const_var = []
                binary = []
                grammar_int = []
                unary = []
                ite = []

                for p in prod:
                    if isinstance(p, IntConst):
                        integers.append(p)
                        const_var.append(p)
                    elif isinstance(p, BoolConst):
                        booleans.append(p)
                        const_var.append(p)
                    elif isinstance(p, GrammarInteger):
                        grammar_int.append(p)
                    elif isinstance(p, GrammarVar):
                        const_var.append(p)
                    elif isinstance(p, BinaryExpr):
                        binary.append(p)
                    elif isinstance(p, UnaryExpr):
                        unary.append(p)
                    elif isinstance(p, Ite):
                        ite.append(p)
                prod = []
                if hole_grammar[j].symbol.type.name == 'INT':
                    prod = const_var + unary + ite + binary + grammar_int
                else:
                    prod = const_var + binary + unary + ite + grammar_int

                for k in range(len(prod)):
                    self.state[f'{i} state {k}'] = None

                self.state[f'{i} name'] = v_name
                self.state[f'{i} prod'] = prod
                self.state[f'{i} other prod'] = other_prod
                self.state[f'{i} integers'] = integers
                self.state[f'{i} booleans'] = booleans
                self.state[f'{i} variables'] = defined_var
                self.state[f'{i} key'] = 0

        for i in range(len(prog.holes)):
            map[prog.holes[i].var.name] = None
            key = self.state[f'{i} key']
            prod = self.state[f'{i} prod']
            other_prod = self.state[f'{i} other prod']
            integers = self.state[f'{i} integers']
            booleans = self.state[f'{i} booleans']
            defined_var = self.state[f'{i} variables']
            state = self.state[f'{i} state {key}']
            v_name = self.state[f'{i} name']

            while map[prog.holes[i].var.name] == None:
                if isinstance(prod[key], BinaryExpr):
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

                elif isinstance(prod[key], BoolConst):
                    res = prod[key]
                    map[prog.holes[i].var.name] = res
                    new_prod = []
                    for p in prod:
                        if p != res:
                            new_prod.append(p)

                    self.state[f'{i} prod'] = new_prod
                    if key < len(prod) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} key'] = key

                    
                elif isinstance(prod[key], IntConst):
                    res = prod[key]
                    map[prog.holes[i].var.name] = res

                    new_prod = []
                    for p in prod:
                        if p != res:
                            new_prod.append(p)

                    self.state[f'{i} prod'] = new_prod
                    if key < len(prod) - 1:
                        key = key + 1
                    else:
                        key = 0
                    self.state[f'{i} key'] = key

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
        


                elif isinstance(prod[key], GrammarVar):
                    if state is None:
                        state = []

                    for var in defined_var:
                        if var not in state:
                            state.append(var)
                            self.state[f'{i} state {key}'] = state
                            map[prog.holes[i].var.name] = VarExpr(var, var.name)

                            if key < len(prod) - 1:
                                key = key + 1
                            else:
                                key = 0
                            self.state[f'{i} key'] = key
                            self.state[f'{i} state {key}'] = None
                            break
                    if map[prog.holes[i].var.name] == None:
                        new_prod = []
                        for p in prod:
                            if p != res:
                                new_prod.append(p)

                        self.state[f'{i} prod'] = new_prod
                        if key < len(prod) - 1:
                                key = key
                        else:
                            key = 0
                        self.state[f'{i} key'] = key
                   
        return map

    def synth_method_3(self,) -> Mapping[str, Expression]:
        """
        Returns a map from each hole id in the program `self.ast`
        to an expression (method 3).

        **TODO: write a description of your approach in this method.**
        """
        # TODO : complete this method
        raise Exception("Synth.synth_method_3 is not implemented.")
    
    
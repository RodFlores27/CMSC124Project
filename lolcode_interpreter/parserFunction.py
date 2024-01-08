import re
from macros import LOLMacros
from decimal import Decimal


class LOLCodeParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.get_tokens()
        self.current_token_index = 0
        self.errored = False
        self.macros = LOLMacros()

        self.it = dict()  # Implicit 'it' variable. See variables section on specifications and expression statements

        self.currentIdentifier = None

        # self.variables = {
        #     variableName: {'type': 'NOOB', 'value': None} for variableName in lexer.get_variable_names()}

        self.variables = dict()

        print(self.variables)
        # for token in self.tokens:
        #     print(token.get('type'), token.get('value'))

        # Lists of values
        self.literalTypes = [self.macros.NUMBR, self.macros.NUMBAR,
                             self.macros.TROOF, 'YARN', self.macros.STRING]
        self.arithmetic_operators = [self.macros.SUM_OF, self.macros.DIFF_OF, self.macros.PRODUKT_OF,
                                     self.macros.QUOSHUNT_OF, self.macros.MOD_OF, self.macros.BIGGR_OF, self.macros.SMALLR_OF]
        print("Arithmetic Operators:", self.arithmetic_operators)
        self.infinite_booling = False
        self.bool_operators = [self.macros.BOTH_OF, self.macros.EITHER_OF,
                               self.macros.WON_OF, self.macros.NOT, self.macros.ANY_OF, self.macros.ALL_OF]
        print("Bool Operators:", self.bool_operators)
        self.comparing = False
        self.comparison_operators = [
            self.macros.BOTH_SAEM, self.macros.DIFFRINT]
        print("Comparison Operators:", self.comparison_operators)

    def parse(self):
        self.program()

    def match(self, expected_type):        # find the macroName of the expectedType
        if self.current_token().get('type') == expected_type:
            macroNameOfExpectedType = [attr for attr in dir(
                self.macros) if getattr(self.macros, attr) == expected_type][0]
            print(self.current_token().get('type'))
            self.consume_token()
        elif type(expected_type) == list:
            macroNameOfExpectedType = [attr for attr in dir(
                self.macros) if getattr(self.macros, attr) == expected_type]
            if self.current_token().get('type') in expected_type:
                print(self.current_token().get('value'))
                self.consume_token()
        else:
            print("Current Token", self.current_token())
            print(
                f"Syntax Error: Expected {expected_type}: {macroNameOfExpectedType}, but instead found {self.current_token()}")
            self.errored = True

    def current_token(self):
        return self.tokens[self.current_token_index]

    def consume_token(self):
        self.current_token_index += 1

    def program(self):
        # should be able to implement: functions, comments  before HAI

        self.match(self.macros.HAI)
        # Loop over all tokens until KTHXBYE is found

        while not self.current_token().get('type') == 'Program End Delimiter':
            self.statement()  # Parse the next statement

        self.match(self.macros.KTHXBYE)

        # should be able to implement: functions, comments  before HAI
        if not self.errored:
            print("\nProgram ended cleanly.")
        else:
            print("\nProgram has syntax error.")

    def data_segment(self):
        '''
        Features (so far): can declare/initialize multiple variables; can reinitialize existing variable value; uninitialized variables have data_type of NOOB
        '''

        self.match(self.macros.WAZZUP)
        # Optional declaration or initialization of variables
        if self.current_token().get('type') == self.macros.I_HAS_A:
            # To deal with multiple declarations
            while self.tokens[self.current_token_index+1].get('type') != self.macros.BUHBYE and self.current_token().get('type') == self.macros.I_HAS_A:
                self.variable_declaration()
        self.match(self.macros.BUHBYE)

    # maek varident a? <literal> | varident is now a <literal>
    # TODO: maek; varident is now a

    def statement(self):
        print("Statementing... Current token:", self.current_token())
        # for printing
        if self.current_token().get('type') == 'Output Operator':
            self.match(self.macros.VISIBLE)
            self.print_statement([])
        # user input
        elif self.current_token().get('type') == "Input Operator":
            self.input_statement()
        # elif self.current_token() == "SMOOSH":
        #     self.str_concat()
        elif self.current_token().get('type') == 'Type Conversion Operator 1':  # MAEK
            self.type_cast()
        # statement starts with identifier
        elif self.current_token().get('type') == "Identifier":
            # TODO: looks like we should do nothing, but this can be used for functions later on.
            self.currentIdentifier = self.current_token().get('value')
            # implicitly assign self.it value
            self.it = self.variables[self.currentIdentifier]
            self.match(self.macros.IDENTIFIER)
            # if self.current_token() == 'Type Conversion Operator 3':
            #     self.type_cast()
            if self.current_token().get('type') == "Assignment Operator":
                self.assignment_statement()
        elif self.current_token().get('type') == 'Variable Declaration Start Delimiter':
            self.data_segment()
        # for arithmetic operations
        elif self.current_token().get('type') in self.arithmetic_operators:
            self.arithmetic_expr()
            print("arithmetic success")
        # for boolean operations
        elif self.current_token().get('type') in self.bool_operators:
            self.bool_expr()
            print("bool success")
        # for comparison operations
        elif self.current_token().get('type') in self.comparison_operators:
            self.comparison_expr()
            print("comparison success")
        # for if-then statements
        elif self.current_token().get('type') == 'If-Then Statement Start Delimiter':
            self.if_then_statement()
            print("if-then success")
        # for switch statements
        elif self.current_token().get('type') == 'Switch Statement Start Delimiter':
            self.switch_statement()
            print("switch statement success")
        # loops
        elif self.current_token().get('type') == 'Loop Statement Start Delimiter':
            self.loop()
            print("loop success")
        else:
            raise ValueError(f"Error: Unrecognized statement found.")

    def variable_declaration(self):
        self.match(self.macros.I_HAS_A)
        if self.current_token().get('type') == self.macros.IDENTIFIER:
            self.currentIdentifier = self.current_token().get('value')
            self.variables[self.currentIdentifier] = {
                'type': 'NOOB', 'value': None}
            self.match(self.macros.IDENTIFIER)
        else:
            raise ValueError(f"Error: variableIdentifier not found.")
        # the optional ITZ
        if self.current_token().get('type') == self.macros.ITZ:
            print(self.macros.ITZ)
            self.consume_token()
            # assign value of expression to identifier
            self.variables[self.currentIdentifier] = self.expression()
        print("Current variable values", self.variables)

    def print_statement(self, operands):
        # Operand accumulation for recursion
        operands.append(self.expression())
        # print("Print Operands", operands)

        # infinite arity implementation
        if self.current_token().get('type') == self.macros.PLUS:
            self.match(self.macros.PLUS)
            return self.print_statement(operands)

        string_to_print = ""
        for operand in operands:
            # to print NOOB
            if operand.get('value') == None and len(operands) == 1:
                string_to_print += "NOOB"
            else:
                string_to_print += str(operand.get('value'))
        print(string_to_print)

    def input_statement(self):
        self.match(self.macros.GIMMEH)
        variable_name = self.current_token().get('value')
        self.match(self.macros.IDENTIFIER)
        self.variables[variable_name] = {'type': 'String', 'value': input()}
        print("Current variable values", self.variables)

    def loop(self):
        self.match(self.macros.IM_IN_YR)
        # store current loop Identifier
        self.currentLoop = self.current_token().get('value')  # name of loop identifier
        print("Current loop:", self.currentLoop)
        self.match(self.macros.IDENTIFIER)
        # Set IncrementType
        loopIncrementType = None
        if self.current_token().get('type') == self.macros.NERFIN:
            loopIncrementType = 'NERFIN'
        elif self.current_token().get('type') == self.macros.UPPIN:
            loopIncrementType = 'UPPIN'
        self.match([self.macros.NERFIN, self.macros.UPPIN])
        self.match(self.macros.YR)
        # set loop counter
        loopCounter = self.current_token().get(
            'value')  # get the name of the identifier
        # assign initial value to reset loopCounter variable in global scope after loop
        # NOTE: remove if needed loopCounter variable to have value from previous loop
        # loopCounterInitialValue = self.variables[loopCounter]['value']
        self.match(self.macros.IDENTIFIER)
        # set loop delimeter
        loopConditionDelimiter = self.current_token().get('value')
        self.match([self.macros.TIL, self.macros.WILE])
        # condition
        indexOnCondition = self.current_token_index
        # TIL
        if loopConditionDelimiter == 'TIL':
            # while FAIL
            while self.expression().get('value') in (False, 'FAIL'):
                # run statements inside loop
                while self.current_token().get('type') not in (self.macros.IM_OUTTA_YR, self.macros.GTFO):
                    self.statement()
                # update loop-related variables
                if self.current_token().get('type') == self.macros.IM_OUTTA_YR:
                    if loopIncrementType == 'UPPIN':
                        self.variables[loopCounter]['value'] += 1
                    elif loopIncrementType == 'NERFIN':
                        self.variables[loopCounter]['value'] -= 1
                    # return token_index to where condition was
                    self.current_token_index = indexOnCondition
                elif self.current_token().get('type') == self.macros.GTFO:
                    self.match(self.macros.GTFO)
                    break
            # once the condition is True or GTFO is met, skip all line until IM_OUTTA_YR
            while self.current_token().get('type') != self.macros.IM_OUTTA_YR:
                self.consume_token()
        # WILE
        if loopConditionDelimiter == 'WILE':
            # while WIN
            while self.expression().get('value') in (True, 'WIN'):
                # run statements inside loop
                while self.current_token().get('type') not in (self.macros.IM_OUTTA_YR, self.macros.GTFO):
                    self.statement()
                # update loop-related variables
                if self.current_token().get('type') == self.macros.IM_OUTTA_YR:
                    if loopIncrementType == 'UPPIN':
                        self.variables[loopCounter]['value'] += 1
                    elif loopIncrementType == 'NERFIN':
                        self.variables[loopCounter]['value'] -= 1
                    # return token_index to where condition was
                    self.current_token_index = indexOnCondition
                elif self.current_token().get('type') == self.macros.GTFO:
                    self.match(self.macros.GTFO)
                    break
            # once the condition is False or GTFO is met, skip all line until IM_OUTTA_YR
            while self.current_token().get('type') != self.macros.IM_OUTTA_YR:
                self.consume_token()
        self.match(self.macros.IM_OUTTA_YR)
        if self.current_token().get('value') == self.currentLoop:
            self.match(self.macros.IDENTIFIER)
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting current loop identifier.")
        # reset loopCounter variable
        # NOTE: remove if needed loopCounter variable to have value from previous loop
        # self.variables[loopCounter]['value'] = loopCounterInitialValue

    def switch_statement(self):
        self.match(self.macros.WTF)
        print(self.current_token().get('value'))

        # optional switch cases
        # Flag for keeping execution of statements until GTFO or OIC is met
        self.switch_case_skipped_GTFO = False
        while self.current_token().get('type') != self.macros.OIC:
            self.switch_case()

        # end of switch statement
        self.match(self.macros.OIC)

    def switch_case(self):
        case = None
        if self.current_token().get('type') == self.macros.OMG:
            self.match(self.macros.OMG)
            case = self.expression().get('value')
            it_value = self.it.get('value')
            print("Case", case)
            print("IT", it_value)
            try:
                # integer cast-able strings
                if it_value.isnumeric():
                    it_value = int(it_value)
                # float cast-able strings
                else:
                    it_value = float(it_value)
            except:
                pass
            # usual case
            if case == it_value and not self.switch_case_skipped_GTFO:
                # keep parsing statements
                while self.current_token().get('type') not in (self.macros.GTFO, self.macros.OMG, self.macros.OMGWTF, self.macros.OIC):
                    self.statement()  # Parse the next statement
                if self.current_token().get('type') == self.macros.GTFO:
                    self.match(self.macros.GTFO)
                    # skip the rest of the cases
                    while self.current_token().get('type') != (self.macros.OIC):
                        self.consume_token()
                if self.current_token().get('type') in (self.macros.OMG, self.macros.OMGWTF):
                    self.switch_case_skipped_GTFO = True
                    return

            # special case
            elif self.switch_case_skipped_GTFO:
                while self.current_token().get('type') not in (self.macros.OMG, self.macros.OMGWTF, self.macros.GTFO):
                    self.statement()
                if self.current_token().get('type') == self.macros.GTFO:
                    self.match(self.macros.GTFO)
                    while self.current_token().get('type') != (self.macros.OIC):
                        self.consume_token()

            # case != IT, skip rest of lines until next case
            else:
                while self.current_token().get('type') not in (self.macros.OMG, self.macros.OMGWTF):
                    self.consume_token()

        # optional OMGWTF aka default case
        elif self.current_token().get('type') == self.macros.OMGWTF:
            self.match(self.macros.OMGWTF)
            while self.current_token().get('type') != self.macros.OIC:
                self.statement()  # Parse the next statement

    def if_then_statement(self):
        self.match(self.macros.O_RLY)

        # IT value is should be truthy
        if self.it.get('value'):
            # start if clause
            self.match(self.macros.YA_RLY)
            # keep parsing statements until NO WAI is met
            while not self.current_token().get('type') in (self.macros.NO_WAI, self.macros.OIC):
                self.statement()  # Parse the next statement
            # optional else statement
            if self.current_token().get('type') == self.macros.NO_WAI:
                self.match(self.macros.NO_WAI)
                while not self.current_token().get('type') == self.macros.OIC:
                    self.statement()  # Parse the next statement
            self.match(self.macros.OIC)
        # IT value is not truthy
        else:
            while self.current_token().get('type') != self.macros.OIC:
                self.consume_token()
            self.match(self.macros.OIC)

    def expression(self):
        '''
        Features (so far): able to be used in: 
                variable declaration and initialization, 
                variable assignment and re-assignment
                TODO: initialization of values from an expression
        '''

        tokenType = None

        # literal return value
        if (self.current_token().get('type') in self.literalTypes):
            tokenType = self.current_token().get('type')

            # TODO: get back once typecaster if fully working, maybe we can just use it instead of python's type function
            if tokenType == 'Numbr':
                tokenValue = int(self.current_token().get('value'))
            elif tokenType == 'Numbar':
                tokenValue = float(self.current_token().get('value'))
            # string
            else:
                tokenValue = self.current_token().get('value')

            self.match(tokenType)

        # identifier return value
        elif (self.current_token().get('type') == 'Identifier'):
            tokenType = self.variables[self.current_token().get(
                'value')].get('type')
            tokenValue = self.variables[self.current_token().get(
                'value')].get('value')
            self.match('Identifier')

        # arithmetic expression return value
        elif (self.current_token().get('type') in self.arithmetic_operators):
            self.arithmetic_expr()
            tokenType = self.it.get('type')
            tokenValue = self.it.get('value')
        # bool expression return value
        elif (self.current_token().get('type') in self.bool_operators):
            self.bool_expr()
            tokenType = self.it.get('type')
            tokenValue = self.it.get('value')
        # comparison expression return value
        elif (self.current_token().get('type') in self.comparison_operators):
            self.comparison_expr()
            tokenType = self.it.get('type')
            tokenValue = self.it.get('value')
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting literal, variable, or expression")
        return {'type': tokenType, 'value': tokenValue}

    def fetchOperand(self):
        '''
        Fetches an operand
        '''
        operand = None

        # int literal
        if self.current_token().get('type') == self.macros.NUMBR:
            operand = int(self.current_token().get('value'))
            self.consume_token()
        # float literal
        elif self.current_token().get('type') == self.macros.NUMBAR:
            operand = float(self.current_token().get('value'))
            self.consume_token()
        # identifier aka variable
        elif self.current_token().get('type') == 'Identifier':
            tokenValue = self.variables[self.current_token().get(
                'value')].get('value')
            if type(tokenValue) == str:
                try:
                    # integer cast-able strings
                    if tokenValue.isnumeric():
                        tokenValue = int(tokenValue)
                    # float cast-able strings
                    else:
                        tokenValue = float(tokenValue)
                except:
                    if self.comparing == True:
                        print("here")
                        raise SyntaxError(
                            f"Invalid token for comparison expression: {tokenValue}. Automatic Typecasting is disabled.")
                    # TODO: put appropriate error message here.
                    pass
            operand = tokenValue
            self.match('Identifier')
        # string literal
        elif self.current_token().get('type') == 'String':
            token = self.current_token()
            print(token)
            tokenValue = self.current_token().get('value')
            try:
                # integer cast-able strings
                if tokenValue.isnumeric():
                    tokenValue = int(tokenValue)
                # float cast-able strings
                else:
                    tokenValue = float(tokenValue)
            except:
                if self.comparing == True:
                    print("here")
                    raise SyntaxError(
                        f"Invalid token for comparison expression: {self.current_token()}. Automatic Typecasting is disabled.")
                # TODO: put appropriate error message here.
                pass
            operand = tokenValue
            self.match('String')
        # troof
        elif self.current_token().get('type') == 'Troof':
            if self.comparing == True:
                raise SyntaxError(
                    "Invalid token for comparison expression: {self.current_token()}. Automatic Typecasting is disabled.")

            operand = 1 if self.current_token().get('value') == 'WIN' else 0
            self.match(self.macros.TROOF)
        # an arithmetic_expr
        elif self.current_token().get('type') in self.arithmetic_operators:
            operand = self.arithmetic_expr()
        # a bool_expr
        elif self.current_token().get('type') in self.bool_operators:
            operand = self.bool_expr()
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}.")

        return operand

    def arithmetic_expr(self):
        operator = self.arithmetic_operator().get('type')

        operand1 = self.fetchOperand()
        self.match(self.macros.AN)
        operand2 = self.fetchOperand()

        print("Operand 1:", operand1)
        print("Operand 2:", operand2)

        answer = None
        if operator == 'Addition Operator':
            # Perform action for addition operator
            answer = operand1 + operand2
        elif operator == 'Subtraction Operator':
            # Perform action for subtraction operator
            answer = operand1 - operand2
        elif operator == 'Multiplication Operator':
            # Perform action for multiplication operator
            answer = operand1 * operand2
        elif operator == 'Division Operator':
            # Perform action for division operator
            if operand2 != 0:
                answer = operand1 / operand2
            else:
                raise ZeroDivisionError("Division by zero")
        elif operator == 'Modulo Operator':
            # Perform action for modulo operator
            answer = operand1 % operand2
        elif operator == 'Max Operator':
            # Perform action for Max operator
            answer = max(operand1, operand2)
        elif operator == 'Min Operator':
            # Perform action for Min operator
            answer = min(operand1, operand2)

        # assign values for implicit variable self.it
        self.it['value'] = answer

        # assign type of self.it
        if isinstance(answer, (int)):
            self.it['type'] = 'Numbr'

        elif isinstance(answer, (float)):
            self.it['type'] = 'Numbar'

        print("Implicit IT variable: ", self.it)

        return answer

    def arithmetic_operator(self):
        tokenType = None
        tokenValue = None
        if (self.current_token().get('type') in self.arithmetic_operators):
            tokenType = self.current_token().get('type')
            tokenValue = self.current_token().get('value')
            self.match(tokenType)
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting arithmetic operator")
        return {'type': tokenType, 'value': tokenValue}

    # def str_concat(self):
    #     self.match(self.macros.SMOOSH)
    #     strings_to_concat = []
    #     while True:
    #         if self.current_token().startswith('String') or self.current_token().startswith(self.macros.IDENTIFIER):
    #             strings_to_concat.append(self.current_token())
    #             self.consume_token()
    #             if self.current_token().startswith(self.macros.AN):
    #                 self.consume_token()
    #                 continue
    #             elif self.current_token().startswith(self.macros.MKAY):
    #                 self.consume_token()
    #                 break
    #             else:
    #                 break
    #         else:
    #             print(
    #                 f"Syntax Error: Expected string or identifier, but instead found {self.current_token()}")
    #             break
    #     print('STR_CONCAT - ', strings_to_concat)

    def assignment_statement(self):
        # TODO: should be allowed to assign value of an existing variable to LHS variable

        # R followed by an expression
        self.match(self.macros.R)
        self.variables[self.currentIdentifier] = self.expression()
        print("Current variable values", self.variables)

    def type_cast(self):
        '''
        Features (so far): can type_cast values into a string using MAEK
        '''

        # MAEK
        if self.current_token().get('type') == self.macros.MAEK:
            self.match(self.macros.MAEK)
            self.currentIdentifier = self.current_token().get('value')
            self.match(self.macros.IDENTIFIER)
            if self.current_token().get('type') == self.macros.A:
                self.match(self.macros.A)
            type_to_cast = self.current_token().get('value')
            self.match(self.literalTypes)
            if type_to_cast == 'YARN':
                self.variables[self.currentIdentifier]['type'] = 'String'
            # TODO apply type_casting of other types

            print("Current variable values", self.variables)
        # TODO apply other way of type_casting
        # varident IS_NOW_A
        # elif self.current_token().get('type') == self.macros.IS_NOW_A:
        #     self.match(self.macros.IS_NOW_A)
        #     self.match(self.literalTypes)

    def bool_expr(self):
        operator = self.bool_operator().get('type')
        # print("Operator", operator)

        # Not operator -> single arity
        if operator == self.macros.NOT:
            operand = self.fetchOperand()
            print("Operand for NOT:", operand)
            # Perform action for NOT operator
            if operand == 'FAIL':
                answer = 'WIN'
            else:
                answer = 'FAIL'

        # Binary arity bool operators
        elif operator in [self.macros.BOTH_OF, self.macros.EITHER_OF, self.macros, self.macros.WON_OF]:
            operand1 = self.fetchOperand()
            self.match(self.macros.AN)
            operand2 = self.fetchOperand()

            print("Operand 1:", operand1)
            print("Operand 2:", operand2)

            answer = None
            # booleans can make use of Troofs or 0's and 1's
            if operator == 'Logical AND Operator':
                # Perform action for AND operator
                if operand1 in (1, 'WIN') and operand2 in (1, 'WIN'):
                    answer = 'WIN'
                else:
                    answer = 'FAIL'

            elif operator == 'Logical OR Operator':
                # Perform action for OR operator
                if operand1 in (1, 'WIN') or operand2 in (1, 'WIN'):
                    answer = 'WIN'
                else:
                    answer = 'FAIL'

            elif operator == 'Logical XOR Operator':
                # Perform action for XOR operator
                operand1_bool = operand1 in (1, 'WIN')
                operand2_bool = operand2 in (1, 'WIN')

                if operand1_bool ^ operand2_bool:  # XOR operation
                    answer = 'WIN'
                else:
                    answer = 'FAIL'
        # Infinite arity bool operators
        elif (operator in [self.macros.ANY_OF, self.macros.ALL_OF]) and not self.infinite_booling:
            self.infinite_booling = True  # To disable argument that's an infinite arity bool
            first_operand = self.fetchOperand()
            operands = [first_operand]
            # infinite arity implementation
            while self.current_token().get('type') == self.macros.AN:
                self.match(self.macros.AN)
                operands.append(self.fetchOperand())
            print("Operands", operands)

            # statement terminator
            self.match(self.macros.MKAY)

            if operator == 'Infinite Arity Logical OR Operator':
                # Perform action for OR operator
                answer = any((operand != 'FAIL' and operand != 0)
                             for operand in operands)

            elif operator == 'Infinite Arity Logical AND Operator':
                # Perform action for AND operator
                answer = all((operand != 'FAIL' and operand !=
                             0) for operand in operands)
            self.infinite_booling = False

        # assign values for implicit variable self.it
        self.it['type'] = 'Troof'
        if answer == True or answer == 'WIN':
            self.it['value'] = 'WIN'
        elif answer == False or answer == 'FAIL':
            self.it['value'] = 'FAIL'

        print("Implicit IT variable: ", self.it)
        print("Current variables", self.variables)
        return answer

    def bool_operator(self):
        tokenType = None
        tokenValue = None
        if (self.current_token().get('type') in self.bool_operators):
            tokenType = self.current_token().get('type')
            tokenValue = self.current_token().get('value')
            self.match(tokenType)
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting bool operator")
        return {'type': tokenType, 'value': tokenValue}

    def comparison_expr(self):
        self.comparing = True
        operator = self.comparison_operator().get('type')
        print("Operation: ", operator)

        operand1 = self.fetchOperand()
        self.comparing = False
        self.match(self.macros.AN)
        operand2 = self.fetchOperand()
        self.comparing = False

        print("Operand 1:", operand1)
        print("Operand 2:", operand2)

        answer = None
        if operator == 'Equality Operator':
            # Perform action for equality operator
            answer = operand1 == operand2
        elif operator == 'Inequality Operator':
            # Perform action for inequality operator
            answer = operand1 != operand2

        # flag to set if comparing. Needed because comparing must disable implicit typecasting
        self.comparing = False

        # assign values for implicit variable self.it
        self.it['type'] = 'Troof'
        self.it['value'] = answer
        print("Implicit IT variable: ", self.it)

        return answer

    def comparison_operator(self):
        tokenType = None
        tokenValue = None
        if (self.current_token().get('type') in self.comparison_operators):
            tokenType = self.current_token().get('type')
            tokenValue = self.current_token().get('value')
            self.match(tokenType)
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting comparison operator")
        return {'type': tokenType, 'value': tokenValue}

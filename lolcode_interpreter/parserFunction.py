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
        #     print(token.get('token_type'), token.get('token_value'))

        # Lists of values
        self.arithmetic_operators = [self.macros.SUM_OF, self.macros.DIFF_OF, self.macros.PRODUKT_OF,
                                     self.macros.QUOSHUNT_OF, self.macros.MOD_OF, self.macros.BIGGR_OF, self.macros.SMALLR_OF]
        print(self.arithmetic_operators)
        self.literalTypes = [self.macros.NUMBR, self.macros.NUMBAR,
                             self.macros.TROOF, 'YARN', self.macros.STRING]

    def parse(self):
        self.program()

    def match(self, expected_type):        # find the macroName of the expectedType
        if self.current_token().get('token_type') == expected_type:
            macroNameOfExpectedType = [attr for attr in dir(
                self.macros) if getattr(self.macros, attr) == expected_type][0]
            print(self.current_token().get('token_type'))
            self.consume_token()
        elif type(expected_type) == list:
            macroNameOfExpectedType = [attr for attr in dir(
                self.macros) if getattr(self.macros, attr) == expected_type]
            if self.current_token().get('token_value') in expected_type:
                print(self.current_token().get('token_value'))
                self.consume_token()
        else:
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

        while not self.current_token().get('token_type') == 'Program End Delimiter':
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
        if self.current_token().get('token_type') == self.macros.I_HAS_A:
            # To deal with multiple declarations
            while self.tokens[self.current_token_index+1].get('token_type') != self.macros.BUHBYE and self.current_token().get('token_type') == self.macros.I_HAS_A:
                self.variable_declaration()
        self.match(self.macros.BUHBYE)

    # maek varident a? <literal> | varident is now a <literal>
    # TODO: maek; varident is now a

    def statement(self):
        print("Statementing... Current token:", self.current_token())
        # for printing
        if self.current_token().get('token_type') == 'Output Operator':
            self.match(self.macros.VISIBLE)
            self.print_statement([])
        elif self.current_token().get('token_type') == "Input Operator":
            self.input_statement()
        # elif self.current_token() == "SMOOSH":
        #     self.str_concat()
        elif self.current_token().get('token_type') == 'Type Conversion Operator 1':  # MAEK
            self.type_cast()
        # for statement starts with identifier
        elif self.current_token().get('token_type') == "Identifier":
            # TODO: looks like we should do nothing, but this can be used for functions later on.
            self.currentIdentifier = self.current_token().get('token_value')
            self.match(self.macros.IDENTIFIER)
            # if self.current_token() == 'Type Conversion Operator 3':
            #     self.type_cast()
            if self.current_token().get('token_type') == "Assignment Operator":
                self.assignment_statement()
        elif self.current_token().get('token_type') == 'Variable Declaration Start Delimiter':
            self.data_segment()
        # for arithmetic operations
        elif self.current_token().get('token_type') in self.arithmetic_operators:
            self.arithmetic_expr()
            print("success")

        else:
            raise ValueError(f"Error: Unrecognized statement found.")

    def variable_declaration(self):
        self.match(self.macros.I_HAS_A)
        if self.current_token().get('token_type') == self.macros.IDENTIFIER:
            self.currentIdentifier = self.current_token().get('token_value')
            self.variables[self.currentIdentifier] = {
                'type': 'NOOB', 'value': None}
            self.match(self.macros.IDENTIFIER)
        else:
            raise ValueError(f"Error: variableIdentifier not found.")
        # the optional ITZ
        if self.current_token().get('token_type') == self.macros.ITZ:
            print(self.macros.ITZ)
            self.consume_token()
            # assign value of expression to identifier
            self.variables[self.currentIdentifier] = self.expression()
        print("Current variable values", self.variables)

    def print_statement(self, operands):
        operands.append(self.expression())
        print("Print Operands", operands)

        # infinite arity implementation
        if self.current_token().get('token_type') == self.macros.PLUS:
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
        variable_name = self.current_token().get('token_value')
        self.match(self.macros.IDENTIFIER)
        self.variables[variable_name] = {'type': 'String', 'value': input()}
        print("Current variable values", self.variables)

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
        if self.current_token().get('token_type') == self.macros.MAEK:
            self.match(self.macros.MAEK)
            self.currentIdentifier = self.current_token().get('token_value')
            self.match(self.macros.IDENTIFIER)
            if self.current_token().get('token_type') == self.macros.A:
                self.match(self.macros.A)
            type_to_cast = self.current_token().get('token_value')
            self.match(self.literalTypes)
            if type_to_cast == 'YARN':
                self.variables[self.currentIdentifier]['type'] = 'String'
            # TODO apply type_casting of other types

            print("Current variable values", self.variables)
        # TODO apply other way of type_casting
        # varident IS_NOW_A
        # elif self.current_token().get('token_type') == self.macros.IS_NOW_A:
        #     self.match(self.macros.IS_NOW_A)
        #     self.match(self.literalTypes)

    def expression(self):
        '''
        Features (so far): able to be used in: 
                variable declaration and initialization, 
                variable assignment and re-assignment
                TODO: initialization of values from an expression
        '''

        tokenType = None

        # literal return value
        if (self.current_token().get('token_type') in self.literalTypes):
            tokenType = self.current_token().get('token_type')

            # TODO: get back once typecaster if fully working, maybe we can just use it instead of python's type function
            if tokenType == 'Numbr':
                tokenValue = int(self.current_token().get('token_value'))
            elif tokenType == 'Numbar':
                tokenValue = float(self.current_token().get('token_value'))
            # string
            else:
                tokenValue = self.current_token().get('token_value')

            self.match(tokenType)

        # identifier return value
        elif (self.current_token().get('token_type') == 'Identifier'):
            tokenType = self.variables[self.current_token().get(
                'token_value')].get('type')
            tokenValue = self.variables[self.current_token().get(
                'token_value')].get('value')
            self.match('Identifier')

        # arithmetic expression return value
        elif (self.current_token().get('token_type') in self.arithmetic_operators):
            self.arithmetic_expr()
            tokenType = self.it.get('type')
            tokenValue = self.it.get('value')
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting literal, variable, or expression")
        return {'type': tokenType, 'value': tokenValue}

    def arithmetic_expr(self):
        token_type = self.arithmetic_operator().get('type')
        operand1 = None
        operand2 = None

        # Fetch the first operand
        if self.current_token().get('token_type') in [self.macros.NUMBAR, self.macros.NUMBR]:
            operand1 = int(self.current_token().get('token_value'))
            self.consume_token()
        elif self.current_token().get('token_type') == 'Identifier':
            tokenValue = self.variables[self.current_token().get(
                'token_value')].get('value')
            try:
                # integer cast-able strings
                if tokenValue.isnumeric():
                    tokenValue = int(tokenValue)
                # float cast-able strings
                else:
                    tokenValue = float(tokenValue)
            except:
                pass
            operand1 = tokenValue
            self.match('Identifier')
        elif self.current_token().get('token_type') in self.arithmetic_operators:
            operand1 = self.arithmetic_expr()
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting numerical value")

        self.match(self.macros.AN)

        # Fetch the second operand
        if self.current_token().get('token_type') in [self.macros.NUMBAR, self.macros.NUMBR]:
            operand2 = int(self.current_token().get('token_value'))
            self.consume_token()
        elif self.current_token().get('token_type') == 'Identifier':
            tokenValue = self.variables[self.current_token().get(
                'token_value')].get('value')
            try:
                # integer cast-able strings
                if tokenValue.isnumeric():
                    tokenValue = int(tokenValue)
                # float cast-able strings
                else:
                    tokenValue = float(tokenValue)
            except:
                pass
            operand2 = tokenValue
            self.match('Identifier')
        elif self.current_token().get('token_type') in self.arithmetic_operators:
            operand2 = self.arithmetic_expr()
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting numerical value")

        print("Operand 1:", operand1)
        print("Operand 2:", operand2)

        answer = None
        if token_type == 'Addition Operator':
            # Perform action for addition operator
            answer = operand1 + operand2
        elif token_type == 'Subtraction Operator':
            # Perform action for subtraction operator
            answer = operand1 - operand2
        elif token_type == 'Multiplication Operator':
            # Perform action for multiplication operator
            answer = operand1 * operand2
        elif token_type == 'Division Operator':
            # Perform action for division operator
            if operand2 != 0:
                answer = operand1 / operand2
            else:
                raise ZeroDivisionError("Division by zero")
        elif token_type == 'Modulo Operator':
            # Perform action for modulo operator
            answer = operand1 % operand2
        elif token_type == 'Max Operator':
            # Perform action for Max operator
            answer = max(operand1, operand2)
        elif token_type == 'Min Operator':
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
        if (self.current_token().get('token_type') in self.arithmetic_operators):
            tokenType = self.current_token().get('token_type')
            tokenValue = self.current_token().get('token_value')
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

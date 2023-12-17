import re
from macros import LOLMacros


class LOLCodeParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.get_tokens()
        self.current_token_index = 0
        self.errored = False
        self.macros = LOLMacros()

        self.it = None  # Implicit 'it' variable. See variables section on specifications and expression statements

        self.currentIdentifier = None

        self.variables = {
            variableName: {'type': 'NOOB', 'value': None} for variableName in lexer.get_variable_names()}

        print(self.variables)
        # for token in self.tokens:
        #     print(token.get('token_type'), token.get('token_value'))

        # Lists of values
        self.arithmetic_operators = [self.macros.SUM_OF, self.macros.DIFF_OF, self.macros.PRODUKT_OF,
                                     self.macros.QUOSHUNT_OF, self.macros.MOD_OF, self.macros.BIGGR_OF, self.macros.SMALLR_OF]
        print(self.arithmetic_operators)
        self.literals = [self.macros.NUMBR, self.macros.NUMBAR,
                         self.macros.TROOF, self.macros.STRING]

    def parse(self):
        self.program()

    def match(self, expected_type):        # find the macroName of the expectedType
        macroNameOfExpectedType = [attr for attr in dir(
            self.macros) if getattr(self.macros, attr) == expected_type][0]

        if self.current_token().get('token_type') == expected_type:
            print(self.current_token().get('token_type'))
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

    # def statement_list(self):
    # '''
    # Puwede na siguro ito tanggalin, nalagay ko siya sa while loops ng data_segment at program()
    # '''
    #     while self.current_token_index < len(self.tokens):
    #         if self.current_token().startswith(KTHXBYE) or self.current_token().startswith(BUHBYE):
    #             break
    #         self.statement()

    def statement(self):
        print("Statementing... Current token:", self.current_token())
        # for printing
        if self.current_token().get('token_type') == 'Output Operator':
            self.print_statement()
        # elif self.current_token() == "GIMMEH":
        #     self.input_statement()
        # elif self.current_token() == "SMOOSH":
        #     self.str_concat()
        # elif self.current_token() == "MAEK":
        #     self.type_cast()
        # for statement starts with identifier
        elif self.current_token().get('token_type') == "Identifier":
            self.currentIdentifier = self.current_token().get('token_value')
            self.match(self.macros.IDENTIFIER)
            # if self.current_token() == "IS_NOW_A":
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
        self.match(self.macros.IDENTIFIER)
        # the optional ITZ
        if self.current_token().get('token_type') == self.macros.ITZ:
            self.consume_token()
            # assign value of expression to identifier
            self.variables[self.currentIdentifier] = self.expression()
            print("Current variable values", self.variables)

    def print_statement(self):
        # printing VISIBLE has infinite arity and concatenates all of its operands after casting them to YARNs. Each operand is  separated by a ‘+’ symbol.
        # At the moment, it can only print with single arity
        # TODO: allow printing with infinite arity
        self.match(self.macros.VISIBLE)
        operand = self.expression()
        if operand:
            print(operand.get('value'))

    def assignment_statement(self):
        # TODO: should be allowed to assign value of an existing variable to LHS variable

        # R followed by an expression
        self.match(self.macros.R)
        self.variables[self.currentIdentifier] = self.expression()
        print("Current variable values", self.variables)

    # def input_statement(self):
    #     self.match(self.macros.GIMMEH)
    #     variable_name = self.current_token()
    #     self.match(self.macros.IDENTIFIER)
    #     print('INPUT - ', variable_name)

    # def type_cast(self):
    #     if self.current_token().startswith(self.macros.MAEK):
    #         self.consume_token()
    #         self.match(self.macros.IDENTIFIER)
    #         if self.current_token().startswith(self.macros.A):
    #             self.consume_token()
    #         self.match(self.macros.TYPE)
    #     elif self.current_token().startswith(self.macros.IS_NOW_A):
    #         self.match(self.macros.IS_NOW_A)
    #         self.match(self.macros.TYPE)

    def expression(self):
        '''
        Features (so far): able to be used in: 
                variable declaration and initialization, 
                variable assignment and re-assignment
        '''

        tokenType = None
        if (self.current_token().get('token_type') == 'Numbr' or
            self.current_token().get('token_type') == 'String' or
            self.current_token().get('token_type') == 'Troof' or
                self.current_token().get('token_type') == 'Numbar'):

            tokenType = self.current_token().get('token_type')
            tokenValue = self.current_token().get('token_value')
            self.match(tokenType)

        elif (self.current_token().get('token_type') == 'Identifier'):
            tokenType = self.variables[self.current_token().get(
                'token_value')].get('type')
            tokenValue = self.variables[self.current_token().get(
                'token_value')].get('value')
            self.match('Identifier')
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting literal, variable, or expression")
        return {'type': tokenType, 'value': tokenValue}

    def arithmetic_expr(self):
        '''
        Features (so far): arithmetic operations can be applied with 2 arity; infinite arity not yet implemented.
        '''

        token_type = self.arithmetic_operator().get('type')
        operand1 = None
        operand2 = None

        # Fetch the first operand
        if self.current_token().get('token_type') in [self.macros.NUMBAR, self.macros.NUMBR]:
            operand1 = int(self.current_token().get('token_value'))
            self.consume_token()
        elif self.current_token().get('token_type') == 'Identifier':
            tokenValue = self.variables[self.current_token().get('token_value')].get('value')
            operand1 = int(tokenValue)
            self.match('Identifier')
        else:
            raise SyntaxError(f"Unexpected token in expression: {self.current_token()}. Expecting numerical value")

        self.match(self.macros.AN)

        # Fetch the second operand
        if self.current_token().get('token_type') in [self.macros.NUMBAR, self.macros.NUMBR]:
            operand2 = int(self.current_token().get('token_value'))
            self.consume_token()
        elif self.current_token().get('token_type') == 'Identifier':
            tokenValue = self.variables[self.current_token().get('token_value')].get('value')
            operand2 = int(tokenValue)
            self.match('Identifier')
        else:
            raise SyntaxError(f"Unexpected token in expression: {self.current_token()}. Expecting numerical value")

            # Add identifiers
            # if self.current_token.get('token_type') == 'Identifier'

        if token_type == 'Addition Operator':
            # Perform action for addition operator
            self.it = operand1 + operand2
        elif token_type == 'Subtraction Operator':
            # Perform action for subtraction operator
            self.it = operand1 - operand2
        elif token_type == 'Multiplication Operator':
            # Perform action for multiplication operator
            self.it = operand1 * operand2
        elif token_type == 'Division Operator':
            # Perform action for division operator
            if operand2 != 0:
                self.it = operand1 / operand2
            else:
                raise ZeroDivisionError("Division by zero")
        elif token_type == 'Modulo Operator':
            # Perform action for modulo operator
            self.it = operand1 % operand2
        elif token_type == 'Greater Than Operator':
            # Perform action for greater than operator
            self.it = operand1 > operand2
        elif token_type == 'Less Than Operator':
            # Perform action for less than operator
            self.it = operand1 < operand2
        print("Implicit IT variable: ", self.it)

    def arithmetic_operator(self):
        tokenType = self.current_token().get('token_type')
        if (tokenType == 'Addition Operator' or
            tokenType == 'Subtraction Operator' or
            tokenType == 'Multiplication Operator' or
            tokenType == 'Division Operator' or
            tokenType == 'Modulo Operator' or
            tokenType == 'Greater Than Operator' or
            tokenType == 'Less Than Operator'
            ):

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

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

    def parse(self):
        self.program()

    def match(self, expected_type):        # find the macroName of the expectedType
        macroNameOfExpectedType = [attr for attr in dir(
            self.macros) if getattr(self.macros, attr) == expected_type][0]
        print(self.current_token().get('token_type'))
        if self.current_token().get('token_type') == expected_type:
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

        # if self.current_token() == "VISIBLE":
        #     self.print_statement()
        # elif self.current_token() == "GIMMEH":
        #     self.input_statement()
        # elif self.current_token() == "SMOOSH":
        #     self.str_concat()
        # elif self.current_token() == "MAEK":
        #     self.type_cast()
        # elif self.current_token() == "IDENTIFIER":
        #     self.match(self.macros.IDENTIFIER)
        #     if self.current_token() == "IS_NOW_A":
        #         self.type_cast()
        #     elif self.current_token() == "R":
        #         self.assignment_statement()
        if self.current_token().get('token_type') == 'Variable Declaration Start Delimiter':
            self.data_segment()
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
            self.variables[self.currentIdentifier] = self.expression(
                self.currentIdentifier)
            print("Current variable values", self.variables)

    # def print_statement(self):
    #     self.match(self.macros.VISIBLE)
    #     self.expression()

    # def assignment_statement(self):
    #     self.match(self.macros.R)
    #     self.consume_token()

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

    def expression(self, identifier):
        tokenType = None
        if (self.current_token().get('token_type') == 'Numbr' or
            self.current_token().get('token_type') == 'Identifier' or
            self.current_token().get('token_type') == 'String' or
            self.current_token().get('token_type') == 'Troof' or
            self.current_token().get('token_type') == 'Numbar' or
                self.current_token().get('token_type') == 'Literal'):
            tokenType = self.current_token().get('token_type')
            tokenValue = self.current_token().get('token_value')
            self.match(tokenType)
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}. Expecting literal, variable, or expression")
        return {'type': tokenType, 'value': tokenValue}
        # TODO: finish return

    # def arithmetic_expr(self):
    #     self.arithmetic_operator()
    #     self.match(self.macros.NUMBR | self.macros.NUMBAR |
    #                self.arithmetic_expr())
    #     self.match(self.macros.AN)
    #     self.match(self.macros.NUMBR | self.macros.NUMBAR |
    #                self.arithmetic_expr())

    # def arithmetic_operator(self):
    #     self.match(self.macros.SUM_OF) or self.match(self.macros.DIFF_OF)

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

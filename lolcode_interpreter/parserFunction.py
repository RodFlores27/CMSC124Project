import re
from macros import *


class LOLCodeParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.get_tokens()
        self.current_token_index = 0

    def parse(self):
        # Start parsing from the top-level program
        self.program()

    def match(self, expected_type):
        # Check if the current token matches the expected type
        if self.current_token().startswith(expected_type):
            # Consume the token
            self.consume_token()
        else:
            print(
                f"Syntax Error: Expected {expected_type}, but found {self.current_token()}")

    def current_token(self):
        # Get the current token
        return self.tokens[self.current_token_index]

    def consume_token(self):
        # Move to the next token
        self.current_token_index += 1

    # Grammar rules

    def program(self):
        # Program → 'HAI' statement_list 'KTHXBYE'
        self.match(HAI)
        self.data_segment()
        self.statement_list()
        self.match(KTHXBYE)
        print("Program ended cleanly.")

    def data_segment(self):
        self.match(WAZZUP)
        self.variable_declaration() 
        self.match(BUHBYE)

    def statement_list(self):
        # statement_list → statement statement_list | ε
        while self.current_token_index < len(self.tokens):
            if self.current_token().startswith(KTHXBYE) or self.current_token().startswith(BUHBYE):
                break
            self.statement()

    def statement(self):
        # statement → variable_declaration | print_statement
        if self.current_token().startswith('Variable Declaration'):
            self.variable_declaration()
        elif self.current_token().startswith('Output Operator'):
            self.print_statement()
        elif self.current_token().startswith('Input Operator'):
            self.input_statement()
        # elif self.current_token().startswith('Program End Delimiter'):
        #     self.match(KTHXBYE)

        # Type_Casting
        elif self.current_token().startswith(MAEK):
            self.type_cast()
        elif self.current_token().startswith(IDENTIFIER):
            self.match(IDENTIFIER)
            if self.current_token().startswith(IS_NOW_A):
                self.type_cast()
            

    def variable_declaration(self):
        # i has a varident (itz (<varident | <expr> | <literal>))?
        self.match(I_HAS_A)
        self.match(IDENTIFIER) # Ended here
        if self.current_token().startswith(ITZ):
            self.consume_token()
            self.expression()  
        
    # def lolInput(self):
    #     self.match(GIMMEH)
    #     self.match(IDENTIFIER)

    def print_statement(self):
        # print_statement → 'VISIBLE' expression 'BUHBYE'
        self.match(VISIBLE)
        self.expression()

    def assignment_statement(self):
        # The current token should be an identifier
        self.match('IDENTIFIER')
        variable_name = self.current_token.value

        # The next token should be 'R'
        # self.consume_token()
        self.match('R')

        # The rest of the statement is an expression
        self.consume_token()
        value = self.expression()

        # Return a tuple representing the assignment statement
        print(f'ASSIGNMENT: {variable_name} - {value}')

    def input_statement(self):
        # The current token should be 'GIMMEH'
        self.match(GIMMEH)

        # The next token should be an identifier
        # self.consume_token()
        variable_name = self.current_token()
        self.match(IDENTIFIER)

        # Return a tuple representing the input statement
        print('INPUT - ', variable_name)

    def type_cast(self):
        # MAEK
        if self.current_token().startswith(MAEK):
            self.consume_token()
            self.match(IDENTIFIER)
            if self.current_token().startswith(A):
                self.consume_token()
            self.match(TYPE) # Literal

        # No MAEK
        elif self.current_token().startswith(IS_NOW_A):
            self.match(IS_NOW_A)
            self.match(TYPE)

    def expression(self):
        # expression → Numbr | Identifier | String | Troof | Numbar
        if self.current_token().startswith('Numbr'):
            self.match('Numbr')
        elif self.current_token().startswith('Identifier'):
            self.match('Identifier')
        elif self.current_token().startswith('String'):
            self.match('String')
        elif self.current_token().startswith('Troof'):
            self.match('Troof')
        elif self.current_token().startswith('Numbar'):
            self.match('Numbar')
        elif self.current_token().startswith('Literal'):
            self.match('Literal')
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}")
        
    
    ################################################################
    # The following methods are not used in the current version.   #
    # They are included here for completeness.                     #
    ################################################################

    def arithmetic_expr(self):
        self.arithmetic_operator()
        self.match(NUMBR|NUMBAR|self.arithmetic_expr())
        self.match(AN)
        self.match(NUMBR|NUMBAR|self.arithmetic_expr())

    def arithmetic_operator(self):
        self.match(SUM_OF) or self.match(DIFF_OF)

    def str_concat(self):
        self.match(SMOOSH)
        self.match(STRING) or self.str_concat()
        self.match(AN)
        self.match(STRING) or self.str_concat()

    
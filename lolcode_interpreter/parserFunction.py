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
        if self.current_token().startswith(
            ('Variable Declaration', 'Numbr', 'Output Operator',
             'Variable Declaration Start Delimiter')
        ):
            self.statement()

    def statement(self):
        # statement → variable_declaration | print_statement
        if self.current_token().startswith('Variable Declaration'):
            self.variable_declaration()
        elif self.current_token().startswith('Output Operator'):
            self.print_statement()

    def variable_declaration(self):
        # i has a varident (itz (<varident | <expr> | <literal>))?
        self.match(I_HAS_A)
        self.match(IDENTIFIER)

    def print_statement(self):
        # print_statement → 'VISIBLE' expression 'BUHBYE'
        self.match('Output Operator')
        self.expression()

    def expression(self):
        # expression → Numbr | Identifier
        if self.current_token().startswith('Numbr'):
            self.match('Numbr')
        elif self.current_token().startswith('Identifier'):
            self.match('Identifier')
        elif self.current_token().startswith('String'):
            self.match('String')
        else:
            raise SyntaxError(
                f"Unexpected token in expression: {self.current_token()}")

# lexical analyzer for the LOLCODE language
from parserFunction import LOLCodeParser
import sys
import re
from macros import *


class LOLCodeLexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.variable_names = set()
        self.string_literals = []

    def tokenize(self):
        # Define regular expressions for LOLCODE tokens
        token_patterns = [
            # keywords
            (r'^(HAI)', 'Program Start Delimiter'),
            (r'^(KTHXBYE)', 'Program End Delimiter'),
            (r'^(WAZZUP)', 'Variable Declaration Start Delimiter'),
            (r'^(BUHBYE)', 'Variable Declaration End Delimiter'),
            (r'^BTW', 'Single Line Comment Delimiter'),
            (r'^(OBTW)', 'Multi Line Comment Start Delimiter'),
            (r'^(TLDR)', 'Multi Line Comment End Delimiter'),
            (r'^((I HAS A))', 'Variable Declaration'),
            (r'^ITZ', 'Variable Assignment'),
            (r'^R', 'Assignment Operator'),
            (r'^(SUM OF)', 'Addition Operator'),
            (r'^(DIFF OF)', 'Subtraction Operator'),
            (r'^(PRODUKT OF)', 'Multiplication Operator'),
            (r'^(QUOSHUNT OF)', 'Division Operator'),
            (r'^(MOD OF)', 'Modulo Operator'),
            (r'^(BIGGR OF)', 'Greater Than Operator'),
            (r'^(SMALLR OF)', 'Less Than Operator'),
            (r'^(BOTH OF)', 'Logical AND Operator'),
            (r'^(EITHER OF)', 'Logical OR Operator'),
            (r'^(WON OF)', 'Logical XOR Operator'),
            (r'^(NOT)', 'Logical NOT Operator'),
            (r'^((ANY OF))', 'Logical OR operator'),
            (r'^((ALL OF))', 'Logical AND operator'),
            (r'^(BOTH SAEM)', 'Equality Operator'),
            (r'^(DIFFRINT)', 'Inequality Operator'),
            (r'^(SMOOSH)', 'String Concatenation Operator'),
            (r'^MAEK', 'Type Conversion Operator'),
            (r'^(AN)', 'Arity'),
            (r'^\b(A)\b', 'Type Conversion Operator'),
            (r'^(IS NOW A)', 'Type Conversion Operator'),
            (r'^(VISIBLE)', 'Output Operator'),
            (r'^(GIMMEH)', 'Input Operator'),
            (r'^(O RLY\?)', 'If-Then Statement Start Delimiter'),
            (r'^(YA RLY)', 'If Statement Delimiter'),
            (r'^(MEBBE)', 'Else If Statement Delimiter'),
            (r'^(NO WAI)', 'Else Statement Delimiter'),
            (r'^(OIC)', 'If-Then Statement End Delimiter'),
            (r'^(WTF\?)', 'Switch Statement Start Delimiter'),
            (r'^(OMG)\b', 'Case Statement Start Delimiter'),
            (r'^(OMGWTF)\b', 'Default Case Statement Start Delimiter'),
            (r'^((IM IN YR))', 'Loop Statement Start Delimiter'),
            (r'^UPPIN', 'Increment Operator'),
            (r'^NERFIN', 'Decrement Operator'),
            (r'^(YR)', 'Loop Variable Declaration'),
            (r'^TIL', 'Loop Condition Delimiter'),
            (r'^WILE', 'Loop Condition Delimiter'),
            (r'^(IM OUTTA YR)', 'Loop Statement End Delimiter'),
            (r'^((HOW IZ I))', 'Function Declaration Start Delimiter'),
            (r'^((IF U SAY SO))', 'Function Declaration End Delimiter'),
            (r'^(GTFO)', 'Break Statement'),
            (r'^(FOUND YR)', 'Return Statement Delimiter'),
            (r'^((I IZ))', 'Return Statement Delimiter'),
            (r'^MKAY', 'Function Call Delimiter'),

            # literals
            (r'^-?[0-9]+', 'Numbr'),  # Pattern for capturing integer literals
            # Pattern for capturing floating point literals
            (r'^-?[0-9]+\.[0-9]+', 'Numbar'),
            (r'^WIN', 'Troof'),  # Pattern for capturing boolean literals
            (r'^FAIL', 'Troof'),  # Pattern for capturing boolean literals
            # Pattern for capturing string literals
            (r'"([^"]*"*(?!""))*[^"]*"', 'String'),
            # Pattern for capturing type literals
            (r'^(NUMBR|NUMBAR|TROOF|YARN)', 'Type'),
            # identifiers
            # Pattern for capturing variable identifiers
            (r'^[a-zA-Z][a-zA-Z0-9_]*', 'Identifier'),
        ]

        # Split the source code into lines
        lines = self.source_code.split('\n')
        # print(f"Lines: {lines}\n\n")

        in_multiline_comment = False

        # Tokenize each line
        for line in lines:
            line = line.strip()
            while line:
                for pattern, token_type in token_patterns:
                    match = re.match(pattern, line)
                    if match:
                        token_value = match.group().strip()  # Remove leading and trailing whitespace

                        if in_multiline_comment:
                            if token_type == TLDR:  # 'Multi Line Comment End Delimiter'
                                in_multiline_comment = False
                            line = line[match.end():].lstrip()
                            break

                        if token_type == 'String':
                            # Remove the start and end quotes
                            token_value = token_value[1:-1]

                        if token_type not in {BTW, OBTW}:
                            self.tokens.append(f"{token_type} - {token_value}")

                        if token_type == 'Identifier':
                            variable_name = match.group().strip()  # Remove leading and trailing whitespace
                            self.variable_names.add(variable_name)
                        elif token_type == 'String':
                            string_literal = token_value
                            self.string_literals.append(string_literal)
                        elif token_type == BTW:  # 'Single Line Comment Delimiter'
                            line = ''  # Remove the rest of the line
                            break
                        elif token_type == OBTW:  # 'Multi Line Comment Start Delimiter'
                            in_multiline_comment = True

                        # Remove the matched token from the line
                        line = line[match.end():].lstrip()
                        break  # Break the for loop if a match is found
                else:
                    raise ValueError(
                        f"Error: Unrecognized token in line: {line}")
                    break  # Break the while loop if no match is found in the for loop

    def get_tokens(self):
        return self.tokens

    def get_variable_names(self):
        return self.variable_names

    def get_string_literals(self):
        return self.string_literals

    def __str__(self):
        return f"LOLCodeLexer(\ntokens={self.tokens}, \nvariable_names={self.variable_names}, \nstring_literals={self.string_literals}\n)"

# Example usage


def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>")
        return

    # Get the file name from the command-line arguments
    filename = sys.argv[1]

    # Now you can use the 'filename' variable in your code
    print(f"Interpreting LOLCODE file: {filename}")

    # Add your file processing logic here
    with open(filename, 'r') as f:
        file_content = f.read()

    lexer = LOLCodeLexer(file_content)
    lexer.tokenize()
    print(lexer)

    parser = LOLCodeParser(lexer)
    parser.parse()


if __name__ == "__main__":
    main()

# lexical analyzer for the LOLCODE language
from parserFunction import LOLCodeParser
import sys
import re
from macros import LOLMacros

# TODO: fix OBTW TLDR


class LOLCodeLexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.variable_names = set()
        self.string_literals = []
        self.macros = LOLMacros()

    def tokenize(self):
        # Define regular expressions for LOLCODE tokens
        token_patterns = [
            # keywords
            (r'^\b(HAI)\b', 'Program Start Delimiter'),
            (r'^\b(KTHXBYE)\b', 'Program End Delimiter'),
            (r'^\b(WAZZUP)\b', 'Variable Declaration Start Delimiter'),
            (r'^\b(BUHBYE)\b', 'Variable Declaration End Delimiter'),
            (r'^\bBTW\b', 'Single Line Comment Delimiter'),
            (r'^\b(OBTW)\b', 'Multi Line Comment Start Delimiter'),
            (r'^\b(TLDR)\b', 'Multi Line Comment End Delimiter'),
            (r'^\b((I HAS A))\b', 'Variable Declaration'),
            (r'^\bITZ\b', 'Variable Assignment'),
            (r'^\bR\b', 'Assignment Operator'),
            (r'^\b(SUM OF)\b', 'Addition Operator'),
            (r'^\b(DIFF OF)\b', 'Subtraction Operator'),
            (r'^\b(PRODUKT OF)\b', 'Multiplication Operator'),
            (r'^\b(QUOSHUNT OF)\b', 'Division Operator'),
            (r'^\b(MOD OF)\b', 'Modulo Operator'),
            (r'^\b(BIGGR OF)\b', 'Max Operator'),
            (r'^\b(SMALLR OF)\b', 'Min Operator'),
            (r'^\b(BOTH OF)\b', 'Logical AND Operator'),
            (r'^\b(EITHER OF)\b', 'Logical OR Operator'),
            (r'^\b(WON OF)\b', 'Logical XOR Operator'),
            (r'^\b(NOT)\b', 'Logical NOT Operator'),
            (r'^\b((ANY OF))\b', 'Infinite Arity Logical OR Operator'),
            (r'^\b((ALL OF))\b', 'Infinite Arity Logical AND Operator'),
            (r'^\b(BOTH SAEM)\b', 'Equality Operator'),
            (r'^\b(DIFFRINT)\b', 'Inequality Operator'),
            (r'^\b(SMOOSH)\b', 'String Concatenation Operator'),
            (r'^\bMAEK\b', 'Type Conversion Operator 1'),
            (r'^\b(AN)\b', 'Operand Connector'),
            (r'^\b(A)\b', 'Type Conversion Operator 2'),
            (r'^\b(IS NOW A)\b', 'Type Conversion Operator 3'),
            (r'^\b(VISIBLE)\b', 'Output Operator'),
            (r'^\b(GIMMEH)\b', 'Input Operator'),
            (r'^\b(O RLY\?)', 'If-Then Statement Start Delimiter'),
            (r'^\b(YA RLY)\b', 'If Statement Delimiter'),
            (r'^\b(MEBBE)\b', 'Else If Statement Delimiter'),
            (r'^\b(NO WAI)\b', 'Else Statement Delimiter'),
            (r'^\b(OIC)\b', 'If-Then Statement End Delimiter'),
            (r'^\b(WTF\?)\b', 'Switch Statement Start Delimiter'),
            (r'^\b(OMG)\b', 'Case Statement Start Delimiter'),
            (r'^\b(OMGWTF)\b', 'Default Case Statement Start Delimiter'),
            (r'^\b((IM IN YR))\b', 'Loop Statement Start Delimiter'),
            (r'^\bUPPIN\b', 'Increment Operator'),
            (r'^\bNERFIN\b', 'Decrement Operator'),
            (r'^\b(YR)\b', 'Loop Variable Declaration'),
            (r'^\bTIL\b', 'Loop Condition Delimiter 1'),
            (r'^\bWILE\b', 'Loop Condition Delimiter 2'),
            (r'^\b(IM OUTTA YR)\b', 'Loop Statement End Delimiter'),
            (r'^\b((HOW IZ I))\b', 'Function Declaration Start Delimiter'),
            (r'^\b((IF U SAY SO))\b', 'Function Declaration End Delimiter'),
            (r'^\b(GTFO)\b', 'Break Statement'),
            (r'^\b(FOUND YR)\b', 'Return Statement Delimiter 1'),
            (r'^\b((I IZ))\b', 'Return Statement Delimiter 2'),
            (r'^\bMKAY\b', 'Function Call Delimiter'),
            (r'\+', 'Print Concatenation Operator'),

            # literals
            # Pattern for capturing floating point literals
            (r'^\b-?[0-9]+\.[0-9]+\b', 'Numbar'),
            # Pattern for capturing integer literals
            (r'^\b-?[0-9]+\b', 'Numbr'),
            (r'^\bWIN\b', 'Troof'),  # Pattern for capturing boolean literals
            (r'^\bFAIL\b', 'Troof'),  # Pattern for capturing boolean literals
            # Pattern for capturing string literals
            (r'"([^"]*"*(?!""))(?=[^+])*"', 'String'),
            # Pattern for capturing type literals
            (r'^\b(NUMBR|NUMBAR|TROOF|YARN)\b', 'Type'),
            # identifiers
            # Pattern for capturing variable identifiers
            (r'^\b[a-zA-Z][a-zA-Z0-9_]*\b', 'Identifier'),
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
                            if token_type == self.macros.TLDR:  # 'Multi Line Comment End Delimiter'
                                in_multiline_comment = False
                            line = line[match.end():].lstrip()
                            break

                        if token_type == 'String':
                            # Remove the start and end quotes
                            token_value = token_value[1:-1]

                        if token_type not in {self.macros.BTW, self.macros.OBTW}:
                            self.tokens.append(
                                {'type': token_type, 'value': token_value})

                        if token_type == 'Identifier':
                            variable_name = match.group().strip()  # Remove leading and trailing whitespace
                            self.variable_names.add(variable_name)
                        elif token_type == 'String':
                            string_literal = token_value
                            self.string_literals.append(string_literal)
                        elif token_type == self.macros.BTW:  # 'Single Line Comment Delimiter'
                            line = ''  # Remove the rest of the line
                            break
                        elif token_type == self.macros.OBTW:  # 'Multi Line Comment Start Delimiter'
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
        return f"LOLCodeLexer(\ntokens={self.tokens}, \nvariable_names={self.variable_names}, \nstring_literals={self.string_literals})"

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

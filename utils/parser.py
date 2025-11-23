import os
import re

class SolidityParser:
    # parse solidity file and return intermediate structure

    def __init__(self, file_path):
        # Initialize the parser with the path to the Solidity file
        self.file_path = file_path
        self.code = None

    def read_file(self):
        # Read the Solidity file content
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File '{self.file_path}' does not exist.")
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.code = file.read()

    def delete_comments(self):
        # delete all comments except SPDX-License-Identifier
        if not self.code:
            raise ValueError("No code to process. Please read the file first.")

        # Regular expression to match single-line and multi-line comments
        comment_pattern = r"((?!\/\/ SPDX-License-Identifier:.*?$)\/\/.*?$|\/\*.*?\*\/)"
        self.code = re.sub(comment_pattern, "", self.code, flags=re.DOTALL | re.MULTILINE)

    def parse(self):
        # Main method to parse the Solidity file
        self.read_file()
        self.delete_comments()
        
        # Temporarily return the cleaned code
        # For more advanced processing, the code can be converted into a syntax tree or token stream
        return self.code
import sys
import os
# from src.layout_obfuscator import LayoutObfuscator
from src.dataflow import DataflowObfuscator
# from src.controlflow_obfuscator import ControlflowObfuscator
# from src.deadcode_obfuscator import DeadCodeObfuscator
# from src.string_obfuscator import StringObfuscator
from utils.parser import SolidityParser
from utils.tools import save_output

def main():
    """
    Main function for the obfuscation tool.
    Parses input, applies obfuscation, and saves the output.
    """
    if len(sys.argv) < 3:
        print("Error: Missing required arguments.")
        sys.exit(1)
        
    # Parse input and output file paths
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if len(sys.argv) == 3:
        options = ["--all"]     # Default to --all
    else:
        options = sys.argv[3:]  # Additional options for obfuscation techniques
    
    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
        
    # Parse the Solidity code from the input file
    try:
        print(f"Parsing input file '{input_file}'...")
        parser = SolidityParser(input_file)
        parsed_code = parser.parse()
    except Exception as e:
        print(f"Error: Failed to parse the input file. {e}")
        sys.exit(1)
        
    # Initialize and apply obfuscators
    obfuscated_code = parsed_code
        
    if "--dataflow" in options or "--all" in options:
        print("Applying dataflow obfuscation...")
        dataflow_obfuscator = DataflowObfuscator()
        obfuscated_code = dataflow_obfuscator.obfuscate(obfuscated_code)
        
    # Save the obfuscated code to the output file
    try:
        print(f"Saving obfuscated code to '{output_file}'...")
        save_output(output_file, obfuscated_code)
        print(f"Obfuscated code has been saved to '{output_file}'.")
    except Exception as e:
        print(f"Error: Failed to save the output file. {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
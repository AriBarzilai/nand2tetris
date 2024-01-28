import CodeWriter as Code
from Parser import Parser as ps
from Parser import COMMAND_TYPE as C
import os
import sys


def main():
    if len(sys.argv) < 2:
        raise ValueError("Error! Enter a path to a file or a directory as an argument.")
    
    path = os.path.normpath(sys.argv[1])
    path = os.path.abspath(path)
    
    if os.path.isdir(path):
        print("translating the files in {}".format(path))
        parent_dir, dir_name = os.path.split(path)
        file_name = output_file_name = f"{os.path.splitext(file_name)[0]}.asm"
        for file in os.listdir(path):
            if file.endswith(".vm"):
                translate_file(os.path.join(path, file))
    else:
        translate_file(path)
        
def translate_file(file_path):
    """Takes in a normalized file name as an argument and outputs to a .asm file
    Raises:
        ValueError: If no argument is given.
    """
    
    directory, file_name = os.path.split(file_path)
    parser = ps.Parser(file_path)
    output_file_name = f"{os.path.splitext(file_name)[0]}.hack"
    output_file = os.path.join(directory, output_file_name)
    
    with open(output_file, 'w') as file:
        print(f"Translating {file_name}...")
        while parser.has_more_commands():
                parser.advance()
                if parser.command_type == C.PUSH:
                    Code.write_push_pop(C.PUSH, parser.arg1(), parser.arg2())
                elif parser.command_type == C.POP:
                    Code.write_push_pop(C.POP, parser.arg1(), parser.arg2())
                elif parser.command_type == C.ARITHMETIC:
                    Code.write_arithmetic(parser.arg1())
                else:
                    continue
    print(f"Successfully assembled {file_name} into {output_file_name}.")

if __name__ == '__main__':
    main()
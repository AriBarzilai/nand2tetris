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
    parent_dir, file_name = os.path.split(path)              
    output_fname = f"{os.path.splitext(file_name)[0]}.asm"
    
    output_path = os.path.join(parent_dir, output_fname)        
    code_writer = Code.CodeWriter(output_path)
        
    if os.path.isdir(path):
        print("translating the files in {}".format(path))   
        for file in os.listdir(path):
            if file.endswith(".vm"):
                input_file = os.path.join(path, file)
                translate_file(input_file, code_writer)
    else:
        translate_file(path, code_writer)
        
    code_writer.close()
        
def translate_file(file_path, code_writer : Code):
    """Takes in a normalized file name as an argument and outputs to a .asm file
    Raises:
        ValueError: If no argument is given.
    """

    parser = ps.Parser(file_path)
    fname = os.path.basename(file_path)
    print(f"Translating {0}...".format(fname))
    while parser.has_more_commands():
            parser.advance()
            if parser.command_type == C.PUSH:
                code_writer.write_push_pop(C.PUSH, parser.arg1(), parser.arg2())
            elif parser.command_type == C.POP:
                code_writer.write_push_pop(C.POP, parser.arg1(), parser.arg2())
            elif parser.command_type == C.ARITHMETIC:
                code_writer.write_arithmetic(parser.arg1())
            else:
                continue
    print(f"Successfully assembled {fname} into {code_writer.get_file_name()}.")

if __name__ == '__main__':
    main()
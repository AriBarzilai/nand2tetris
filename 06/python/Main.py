import Code
import Parser as ps
import SymbolTable as st
import os
import sys

DEBUG_MODE = False # Prints additional information about the assembly process if set to True.

def main():
    if len(sys.argv) < 2:
        raise ValueError("Error! Enter a path to a file or a directory as an argument.")
    
    path = os.path.normpath(sys.argv[1])
    path = os.path.abspath(path)
    
    if os.path.isdir(path):
        print("assembling the files in {}".format(path))
        for file in os.listdir(path):
            if file.endswith(".asm"):
                assemble_file(os.path.join(path, file))
    else:
        assemble_file(path)

def assemble_file(file_path):
    """Takes in a normalized file name as an argument and outputs a .hack file with the same name as the input file.

    Raises:
        ValueError: If no argument is given.
    """
    
    directory, file_name = os.path.split(file_path)
    parser = ps.Parser(file_path)
    output_file_name = f"{os.path.splitext(file_name)[0]}.hack"
    output_file = os.path.join(directory, output_file_name)
    
    symbol_table = st.SymbolTable(parser)
    with open(output_file, 'w') as file:
        print(f"Assembling {file_name}...")
        while parser.has_more_commands():
                parser.advance()
                output = "111"
                try:
                    if parser.command_type == "C_COMMAND":
                        output += Code.comp(parser.comp())
                        output += Code.dest(parser.dest())
                        output += Code.jump(parser.jump())
                    elif parser.command_type == "A_COMMAND":
                        output = Code.symbol(parser.symbol(symbol_table))
                    else:
                        continue                  
                    file.write(output + "\n")
                except:
                    pass
                if DEBUG_MODE: debug(parser, symbol_table, output)
        if DEBUG_MODE: print(symbol_table.symbol_table)
    print(f"Successfully assembled {file_name} into {output_file_name}.")


def debug(parser, symbol_table, output):
    template = "{:<16} | {:<8} | dest {:<6} | comp {:<6} | jump {:<6} | symbol {:<5} | bin {:<16} | {:<7} {:3} {:3}"
    print(template.format(
        parser.current_line if parser.current_line is not None else "None",
        parser.command_type if parser.command_type is not None else "None",
        parser.dest() if parser.dest() is not None else "None",
        parser.comp() if parser.comp() is not None else "None",
        parser.jump() if parser.jump() is not None else "None",
        parser.symbol(symbol_table) if parser.symbol(symbol_table) is not None else "None",
        output if parser.command_type == "C_COMMAND" else Code.symbol(parser.symbol(symbol_table)) if Code.symbol(parser.symbol(symbol_table)) is not None else "None",
        Code.comp(parser.comp()),
        Code.dest(parser.dest()),
        Code.jump(parser.jump())
    ))

if __name__ == '__main__':
    main()
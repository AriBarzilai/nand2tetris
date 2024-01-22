import Code
import Parser as ps
import os
import sys



def main():
    if len(sys.argv) < 2:
        raise ValueError("Error! Enter a path to a file or a directory as an argument.")
    
    path = os.path.normpath(sys.argv[1])
    
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".asm"):
                assembleFile(os.path.join(path, file))
    else:
        assembleFile(path)

def assembleFile(filePath):
    """Takes in a file name as an argument and outputs a .hack file with the same name as the input file.

    Raises:
        ValueError: If no argument is given.
    """
    
    directory, filename = os.path.split(filePath)
    directory = os.path.join(os.path.dirname(__file__), directory)
    parser = ps.Parser(os.path.join(directory, filename))
    outputFileName = f"{os.path.splitext(filename)[0]}.hack"
    outputFile = os.path.join(directory, outputFileName)
    
    with open(outputFile, 'w') as file:
            print(f"Assembling {filename}...")
            while parser.has_more_commands():
                    parser.advance()
                    output = "111"
                    try:
                        if parser.command_type == "C_COMMAND":
                            output += Code.comp(parser.comp())
                            output += Code.dest(parser.dest())
                            output += Code.jump(parser.jump())
                        else:
                            output = Code.symbol(parser.symbol())                  
                        file.write(output + "\n")
                    except:
                        pass
                    #debug(parser, output)
    print(f"Successfully assembled {filename} into {outputFileName}.")


def debug(parser, output):
    template = "{:<5} | {:<8} | dest {:<6} | comp {:<6} | jump {:<6} | symbol {:<5} | bin {:<16} | {:<7} {:3} {:3}"
    print(template.format(
        parser.current_line if parser.current_line is not None else "None",
        parser.command_type if parser.command_type is not None else "None",
        parser.dest() if parser.dest() is not None else "None",
        parser.comp() if parser.comp() is not None else "None",
        parser.jump() if parser.jump() is not None else "None",
        parser.symbol() if parser.symbol() is not None else "None",
        output if parser.command_type == "C_COMMAND" else Code.symbol(parser.symbol()),
        Code.comp(parser.comp()),
        Code.dest(parser.dest()),
        Code.jump(parser.jump())
    ))

if __name__ == '__main__':
    main()
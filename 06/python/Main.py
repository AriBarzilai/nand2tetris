import Code
import Parser as ps
import os
import sys



def main():
    """Main function for the program.\n
    Takes in a file name as an argument and outputs a .hack file with the same name as the input file.

    Raises:
        ValueError: If no argument is given.
    """
    if len(sys.argv) < 2:
        raise ValueError("Error! Enter an argument")
    
    directory, filename = os.path.split(os.path.normpath(sys.argv[1]))
    directory = os.path.join(os.path.dirname(__file__), directory)
    parser = ps.Parser(os.path.join(directory, filename))
    outputFileName = f"{os.path.splitext(filename)[0]}.hack"
    outputFile = os.path.join(directory, outputFileName)
    
    with open(outputFile, 'w') as file:
            while parser.has_more_commands():
                    parser.advance()
                    output = "11"
                    try:
                        if parser.command_type == "C_COMMAND":
                            output += "1"
                            output += Code.comp(parser.comp())
                            output += Code.dest(parser.dest())
                            output += Code.jump(parser.jump())
                        else:
                            output += "0"                    
                        file.write(output + "\n")
                    except:
                        pass
                    template = "{:<5} | {:<8} | dest {:<6} comp {:<6} jump {:<6} symbol {:<5} code {:<16} | {:<7} {:3} {:3}"
                    print(template.format(
                        parser.current_line if parser.current_line is not None else "None",
                        parser.command_type if parser.command_type is not None else "None",
                        parser.dest() if parser.dest() is not None else "None",
                        parser.comp() if parser.comp() is not None else "None",
                        parser.jump() if parser.jump() is not None else "None",
                        parser.symbol() if parser.symbol() is not None else "None",
                        output,
                        Code.comp(parser.comp()),
                        Code.dest(parser.dest()),
                        Code.jump(parser.jump())
                    ))

if __name__ == '__main__':
    main()
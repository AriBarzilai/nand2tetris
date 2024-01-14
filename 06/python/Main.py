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
    
    directory, filename = os.path.split(sys.argv[1])
    parser = ps.Parser(sys.argv[1])
    outputFileName = f"{os.path.splitext(filename)}.hack"
    outputFile = os.path.join(directory, outputFileName)
    
    with open(outputFile, 'w') as file:
        while parser.has_more_commands():
            try:
                parser.advance()
            
                output = 24576
                if parser.commandType == "C_COMMAND":
                    output += 32768
                    output += Code.comp(parser.comp())
                    output += Code.dest(parser.dest())
                    output += Code.jump(parser.jump())
                else:
                    output += int(parser.symbol())
                    
                file.write(output + "\n")
            except:
                print("reached EOF")
        
        


if __name__ == '__main__':
    main()
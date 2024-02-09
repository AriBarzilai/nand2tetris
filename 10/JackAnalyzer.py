import sys
import re
from os import listdir
from os.path import isfile, isdir
from CompilationEngine import CompilationEngine

INVALID_ARGS_MESSAGE = "The file given as input is invalid..."
NUMBER_OF_ARGS = 2
XML_SUFFIX = ".xml"
JACK_SUFFIX = ".jack$"
VALID_INPUT_SUFFIX = ".*\.jack$"
JACK_SUFFIX_PATTERN = re.compile(VALID_INPUT_SUFFIX)
COMMENT = "//.*$"

class JackAnalyzer:
    """
    This program translate Jack code to xml.
    """

    def get_files(args):
        """
        param args: the arguments given to the program.
        return: the list of paths to .jack files
        """
        list_of_files_path = []
        if len(args) == NUMBER_OF_ARGS:
            if isfile(args[1]) and JACK_SUFFIX_PATTERN.match(args[1]):
                list_of_files_path.append(args[1])
            elif isdir(args[1]):
                for file in listdir(args[1]):
                    if JACK_SUFFIX_PATTERN.match(file):
                        list_of_files_path.append(args[1] + "/" + file)
            return list_of_files_path
        else:
            print(INVALID_ARGS_MESSAGE)
            exit()


    def file_output_path(file_path):
        """
        param file_path: The original file path
        return: the path to the output file (.xml).
        """
        temp_path = re.sub(JACK_SUFFIX, XML_SUFFIX, file_path)
        return temp_path

    if __name__ == "__main__":
        """
        The program create a new instance of CompilationEngine for every given 
        .jack file. The instance will create the desired .xml file.
        """
        list_of_files_path = get_files(sys.argv)
        for file_path in list_of_files_path:
            current_code = CompilationEngine(file_path, file_output_path(file_path))
            current_code.compileClass()
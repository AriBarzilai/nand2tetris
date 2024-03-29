import re

from enum import Enum, auto

class COMMAND_TYPE(Enum):
    ARITHMETIC = auto()
    PUSH = auto()
    POP = auto()
    LABEL = auto()
    GOTO = auto()
    IF = auto()
    FUNCTION = auto()
    RETURN = auto()
    CALL = auto()
C = COMMAND_TYPE
    
ARITHMETIC_OPERATIONS = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}

class Parser:
    
    def __init__(self, filePath: str):
        self._file = open(filePath, 'r')
        
    def has_more_commands(self):
        """ Checks if there are more commands in the input.

        Returns:
            _bool_: True if there are more commands in the input, False otherwise.
        """
        current_position = self._file.tell()
        next_line = self._file.readline()
        self._file.seek(current_position) 
        return (next_line != '')
    
    def advance(self):
        """Reads the next command from the input and makes it the current command.

        Returns:
            _str_: The current command.
        """

        while self.has_more_commands: # we continue scanning until a valid command is found and processed
            temp_str = self._file.readline()
            remove_whitespace = re.sub(r'\s+', ' ', temp_str)
            comment_index = remove_whitespace.find('//')  #  looks for comments in line, marked by '//'
            if comment_index != -1:
                remove_whitespace = remove_whitespace[:comment_index]
            remove_whitespace = remove_whitespace.strip()
            if remove_whitespace == '':
                continue
            self.current_line = remove_whitespace

            if 'push' in self.current_line:
                self.set_command_type(C.PUSH)
            elif 'pop' in self.current_line:
                self.set_command_type(C.POP)
            elif any(op in self.current_line for op in ARITHMETIC_OPERATIONS):
                self.set_command_type(C.ARITHMETIC)
            elif '' in self.current_line:  #TODO: Add the appropriate condition for C_LABEL
                self.set_command_type(C.LABEL)
            elif '' in self.current_line:  #TODO: Add the appropriate condition for C_GOTO
                self.set_command_type(C.GOTO)
            elif '' in self.current_line:  #TODO: Add the appropriate condition for C_IF
                self.set_command_type(C.IF)
            elif '' in self.current_line:  #TODO: Add the appropriate condition for C_FUNCTION
                self.set_command_type(C.FUNCTION)
            elif '' in self.current_line:  #TODO: Add the appropriate condition for C_RETURN
                self.set_command_type(C.RETURN)
            elif '' in self.current_line:  #TODO: Add the appropriate condition for C_CALL
                self.set_command_type(C.CALL)
                
            break  # Exit the loop after succesfully processing the command

    def set_command_type(self, command_type: COMMAND_TYPE):
        """Sets a command type for the current line.

        Args:
            string (_str_): The command type to be set.
        """
        self.command_type = command_type
        
    def arg1(self):
        if self.command_type == C.ARITHMETIC:
            return self.current_line
        elif self.command_type != C.RETURN:
            start_index = self.current_line.find(' ') + 1
            end_index = self.current_line[start_index:].find(' ') + start_index
            if end_index == -1:
                return self.current_line[start_index:]
            return self.current_line[start_index:end_index]
        
    def arg2(self):
        if self.command_type != C.RETURN:
            start_index = len(self.current_line) - self.current_line[::-1].find(' ')
            return self.current_line[start_index:]        
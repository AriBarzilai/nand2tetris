import re

class Parser:
    
    def __init__(self, filePath):
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
            remove_whitespace = re.sub(r'\s+', '', temp_str)
            comment_index = remove_whitespace.find('//')  #  looks for comments in line, marked by '//'
            if comment_index != -1:
                remove_whitespace = remove_whitespace[:comment_index]
            if remove_whitespace == '':
                continue
            self.current_line = remove_whitespace

            if 'add, sub, neg, mult div' in self.current_line:
                self.set_command_type("C_ARITHMETIC")
            if 'push' in self.current_line in self.current_line:
                self.set_command_type("C_PUSH")
            if 'pop' in self.current_line in self.current_line:
                self.set_command_type("C_POP")
            if '' in self.current_line in self.current_line:
                self.set_command_type("C_LABEL") 
            if '' in self.current_line in self.current_line:
                self.set_command_type("C_GOTO")
            if '' in self.current_line in self.current_line:
                self.set_command_type("C_IF")
            if '' in self.current_line in self.current_line:
                self.set_command_type("C_FUNCTION")
            if '' in self.current_line in self.current_line:
                self.set_command_type("C_RETURN")
            if '' in self.current_line in self.current_line:
                self.set_command_type("C_CALL")   
            break  # Exit the loop after succesfully processing the command

    def set_command_type(self, string):
        """Sets a command type for the current line.

        Args:
            string (_str_): The command type to be set.
        """
        self.command_type = string
        
    def arg1(self):
        if self.command_type == "C_ARITHMETIC":
            return self.current_line
        elif self.command_type != "C_RETURN":
            start_index = self.current_line.find(' ')
            end_index = self.current_line[start_index:].find(' ')
            if end_index == -1:
                return self.current_line[start_index:]
            return self.current_line[start_index:end_index]
        
    def arg2(self):
        start_index = len(self.current_line) - self.current_line[::-1].find(' ') - 1
        return self.current_line[start_index:]
            
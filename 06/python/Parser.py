import re
import SymbolTable as st

class Parser:
    file = None
    current_line = None
    command_type = None


    def __init__(self, filePath):
        self.file = open(filePath, 'r')
        
    def has_more_commands(self):
        """ Checks if there are more commands in the input.

        Returns:
            _bool_: True if there are more commands in the input, False otherwise.
        """
        current_position = self.file.tell()
        next_line = self.file.readline()
        self.file.seek(current_position) 
        return (next_line != '')

    def set_command_type(self, string):
        """Sets a command type for the current line.

        Args:
            string (_str_): The command type to be set.
        """
        self.command_type = string
        
    def advance(self):
        """Reads the next command from the input and makes it the current command.

        Returns:
            _str_: The current command.
        """
        while self.has_more_commands:
            temp_str = self.file.readline()
            remove_whitespace = re.sub(r'\s+', '', temp_str)
            comment_index = remove_whitespace.find('//')  # looks for inline comments
            if comment_index != -1:
                remove_whitespace = remove_whitespace[:comment_index]
            if remove_whitespace == '':
                continue
            self.current_line = remove_whitespace

            if '@' in self.current_line:
                self.set_command_type("A_COMMAND")
            if '(' in self.current_line and ')' in self.current_line:
                self.set_command_type("L_COMMAND")
            if '=' in self.current_line or ';' in self.current_line:
                self.set_command_type("C_COMMAND")
                
            break  # Exit the loop after processing the current line

    
    def symbol(self, symbol_table):
        """Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx).

        Returns:
            _str_: The symbol or decimal Xxx of the current command.
        """
        if self.command_type == "A_COMMAND":
            symbol = self.current_line[1:]
            try:
                return int(symbol)
            except:
                return symbol_table.get_address(symbol)
        elif self.command_type == "L_COMMAND":
            return self.current_line[1:-1]
        
    def dest(self):
        """Returns the dest mnemonic in the current C-command (8 possibilities).

        Returns:
            _str_: The dest mnemonic in the current C-command (8 possibilities).
        """
        if self.command_type == "C_COMMAND":
            equals_index = self.current_line.find("=")
            if equals_index != -1:
                return self.current_line[:equals_index]

    def comp(self):
        """Returns the comp mnemonic in the current C-command (28 possibilities).

        Returns:
            _str_: The comp mnemonic in the current C-command (28 possibilities).
        """
        if self.command_type == "C_COMMAND":
            semicolon_index = self.current_line.find(";")
            equals_index = self.current_line.find("=")
            
            if semicolon_index == -1:
                semicolon_index = len(self.current_line)
        
            return self.current_line[equals_index+1:semicolon_index]
                
    def jump(self):
        """Returns the jump mnemonic in the current C-command (8 possibilities).

        Returns:
            _str_: The jump mnemonic in the current C-command (8 possibilities).
        """
        if self.command_type == "C_COMMAND":
            semicolon_index = self.current_line.find(";")
            if semicolon_index != -1 and semicolon_index != len(self.current_line)-1:
                return self.current_line[semicolon_index+1:]
                
    def reset(self):
        self.file.seek(0)
        self.current_line = None
        self.command_type = None
            
            
        
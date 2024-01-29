class SymbolTable(object):
    """A class that stores the symbols in a Hack language program and their corresponding memory addresses."""
    
    def __init__(self, parser):
        # Creates and initializes a SymbolTable with the predefined symbols defined in the Hack language.
        self.symbol_table = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
               'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,
               'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15,
               'SCREEN':16384, 'KBD':24576}
        self.next_line_index = 0 # the ROM address of the next line of code to be scanned during initialization
        self.next_var_index = 16 # the RAM address of the next variable to be stored in the symbol table, starting from index 16
        self.add_labels_from_file(parser)      
    
    # Adds the pair (symbol,address) to the table.      
    def add_entry(self, symbol, address):
        self.symbol_table[symbol] = address
    
    # If symbol exists in the table, returns its address.
    # Otherwise, store it in the next available address, and return its address.
    # This command should be run only after all labels have been added to the symbol table.
    def get_address(self, symbol):
        if self.contains(symbol):
            return self.symbol_table.get(symbol)
        else:
            address = self.get_available_symbol_address()
            self.add_entry(symbol, address)
            self.next_var_index = address + 1
            return address
        
    # Checks if symbol exists in the table
    def contains(self, symbol):
        return symbol in self.symbol_table
    
    # Scans through the file and adds all the labels to the symbol table.
    def add_labels_from_file(self, parser):
        while parser.has_more_commands():
            parser.advance()
            try:
                if parser.command_type == "L_COMMAND":
                        self.add_entry(parser.symbol(self), self.next_line_index)
                elif parser.command_type == "C_COMMAND" or parser.command_type == "A_COMMAND":
                    self.next_line_index += 1
            except:
                pass
        parser.reset()
        
    # Returns the next available unoccupied memory address to store a variable in the symbol table.
    # Should be run only after all labels have been added to the symbol table.
    def get_available_symbol_address(self):
        address = self.next_var_index
        while address in self.symbol_table.values():
            address += 1
        return address
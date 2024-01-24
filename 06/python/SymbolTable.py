import Code
import Parser

class SymbolTable(object):
    
    symbol_table = {}
    next_index = 0 # the next available memory address
    
    def __init__(self, parser):
        # Creates and initializes a SymbolTable
        self.symbol_table = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
               'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,
               'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15,
               'SCREEN':16384, 'KBD':24576}
        self.next_index = 0
        self.add_symbols_from_file(parser)
        
    
    # Adds the pair (symbol,address) to the table.      
    def add_entry(self, symbol, address):
        self.symbol_table[symbol] = address
        
    # Checks if symbol exists in the table
    def contains(self, symbol):
        return symbol in self.symbol_table
        
    # Returns the address associated with the symbol.
    def get_address(self, symbol):
        return self.symbol_table.get(symbol)
    
    # Scans through the file and adds all the labels to the symbol table.
    def add_symbols_from_file(self, parser):
        while parser.has_more_commands():
                parser.advance()
                try:
                    if parser.command_type == "L_COMMAND":
                            self.add_entry(parser.symbol(self), self.next_index)
                    elif parser.command_type == "C_COMMAND" or parser.command_type == "A_COMMAND":
                        self.next_index += 1
                except:
                    pass
        parser.reset()
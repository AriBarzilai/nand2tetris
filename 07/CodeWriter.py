from Parser import COMMAND_TYPE as C

class CodeWriter:
    
    segment = {
        "argument": "ARG",
        "local": "LCL",
        "this": "THIS",
        "that": "THAT",
        "temp": "R5",
        'pointer': 3,
        'temp': 5,
        'static': 16,
    }
    
    def __init__(self, output_path: str):
        self._output_file = open(output_path, 'w')
        self._bool_count = 0 # Count of boolean comparisons
        self._file_name = ""

    def set_file_name(self, file_name: str):
        """Informs the code writer that the translation of a new VM file has started."""
        self._file_name = file_name

    def write_arithmetic(self, operation):
        """Writes the assembly code for the given arithmetic operation to the top value(s) on the stack."""
        if operation not in ['neg', 'not']: # Binary operator
            self._pop_stack_to_D()
        self._decrement_SP()
        self._set_A_to_stack()

        # Arithmetic operators
        if operation == 'add': 
            self._write('M=M+D')
        elif operation == 'sub':
            self._write('M=M-D')
        elif operation == 'and':
            self._write('M=M&D')
        elif operation == 'or':
            self._write('M=M|D')
        elif operation == 'neg':
            self._write('M=-M')
        elif operation == 'not':
            self._write('M=!M')
            
        # Boolean operators
        elif operation in ['eq', 'gt', 'lt']: 
            self._write('D=M-D')
            self._write('@BOOL{}'.format(self._bool_count))

            if operation == 'eq':
                self._write('D;JEQ') # if x == y
            elif operation == 'gt':
                self._write('D;JGT') # if x > y
            elif operation == 'lt':
                self._write('D;JLT') # if x < y

            self._set_A_to_stack()
            self._write('M=0') # False
            self._write('@ENDBOOL{}'.format(self._bool_count))
            self._write('0;JMP')

            self._write('(BOOL{})'.format(self._bool_count))
            self._set_A_to_stack()
            self._write('M=-1') # True

            self._write('(ENDBOOL{})'.format(self._bool_count))
            self._bool_count += 1
        else:
            raise ValueError("Invalid operator: {0}".format(operation))
        self._increment_SP()

    def write_push_pop(self, command_type, segment: str, index):
        """Writes the assembly code for pushing or popping the given segment at the given index to/from the stack."""
        
        self._seg_to_addr(segment, index)  
        if command_type == C.PUSH:
            if segment == "constant":
                self._write("D=A")
            else:
                self._write("D=M")
            self._push_D_to_stack()
            
        elif command_type == C.POP:
            self._write("D=A")
            self._write("@R13")
            self._write("M=D")
            self._pop_stack_to_D()
            self._write("@R13")
            self._write("A=M")
            self._write("M=D")
        else:
            raise ValueError("Invalid command: {0}".format(command_type))

    def close(self):
        self._output_file.close()

    def _write(self, asm_command: str):
        """Writes a given assembly command to the output file."""
        self._output_file.write(asm_command + "\n")

    def _seg_to_addr(self, segment: str, index: str):
        """Summary:
            Converts a segment to an address, and goes to that address.

        Args:
            segment (str): The segment type, as detailed in the Nand2Tetris VM language specification
            index (str): a numeric string representing the index relative to the segment
        """
        address = self.segment.get(segment)
        if segment == "constant":
            self._write("@" + index)
        elif segment == "static":
            self._write("@" + self._file_name + "." + index)
        else:
            try: # if the segment mapped to a constant (int) address
                self._write("@R" + str(address + int(index)))
            except: # if the segment mapped to a string
                self._write("@" + address)
                self._write("D=M")
                self._write("@" + index)
                self._write("A=D+A")

    def _push_D_to_stack(self):
        """Writes to file a common assembly operation: push D to top of stack"""
        self._write('@SP') # Get current stack pointer
        self._write('A=M') # Set address to current stack pointer
        self._write('M=D') # Write data to top of stack
        self._write('@SP') # Increment SP
        self._write('M=M+1')

    def _pop_stack_to_D(self):
        """Writes to file a common assembly operation: pop top of stack to D"""
        self._write('@SP')
        self._write('AM=M-1') # Decrement SP and set address to new stack pointer
        self._write('D=M') # Get data from top of stack

    def _decrement_SP(self):
        self._write('@SP')
        self._write('M=M-1')

    def _increment_SP(self):
        """Writes to file a common assembly operation: increment SP"""
        self._write('@SP')
        self._write('M=M+1')

    def _set_A_to_stack(self):
        """Writes to file a common assembly operation: set A to the top of the stack"""
        self._write('@SP')
        self._write('A=M')
from Parser import COMMAND_TYPE as C

class CodeWriter:
    
    segment = {
        "argument": "ARG",
        "local": "LCL",
        "this": "THIS",
        "that": "THAT",
        "temp": "R5",
    }
    
    def __init__(self, output_path: str):
        self._output_file = open(output_path, 'w')
        self.bool_count = 0 # Count of boolean comparisons
        self._file_name = ""
        
    def set_file_name(self, file_name: str):
        """Informs the code writer that the translation of a new VM file has started."""
        self._file_name = file_name
    
    def get_file_name(self):
        """Returns the name of the current VM file being translated."""
        return self._file_name
    
    def write_arithmetic(self, operation):
        """Writes the assembly code for the given arithmetic operation to the top value(s) on the stack."""
        if operation not in ['neg', 'not']: # Binary operator
            self._pop_stack_to_D()
        self._decrement_A()

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
            self._write('@BOOL{}'.format(self.bool_count))

            if operation == 'eq':
                self._write('D;JEQ') # if x == y
            elif operation == 'gt':
                self._write('D;JGT') # if x > y
            elif operation == 'lt':
                self._write('D;JLT') # if x < y

            self._set_A_to_stack()
            self._write('M=0') # False
            self._write('@ENDBOOL{}'.format(self.bool_count))
            self._write('0;JMP')

            self._write('(BOOL{})'.format(self.bool_count))
            self._set_A_to_stack()
            self._write('M=-1') # True

            self._write('(ENDBOOL{})'.format(self.bool_count))
            self.bool_count += 1
        else:
            raise ValueError('{} is an invalid argument'.format(operation))
        #self._increment_SP()
        
    def write_push_pop(self, command_type, segment: str, index: int):
        """Writes the assembly code for pushing or popping the given segment at the given index to/from the stack."""
        if command_type == C.PUSH:
            self._push(segment, index)
        elif command_type == C.POP:
            self._pop(segment, index)
        else:
            raise ValueError("Invalid command: {0}".format(command_type))
    
    def close(self):
        """Closes the output .asm file."""
        self._output_file.close()
        
    def _push(self, segment, index):
        """Writes to file the assembly code for pushing the given segment at the given index to the stack."""       
        # if constant, we set D=index. else, set: D=segment[index]
        if segment == "constant":
            self._write("@{0}".format(index))
            self._write("D=A")
        elif index == 0 and segment in self.segment:
            self._write("@{0}".format(self.segment[segment]))
            self._write("D=M")
        else:
            self._seg_to_addr(segment, index, True)
            self._write("D=M")        
        self._push_D_to_stack()
    
    def _pop(self, segment, index):
        """Writes to file the assembly code for popping the top element of the stack to a given segment's index."""
        if segment == "constant":
            raise ValueError("constant segment is invalid for pop command")        
        self._seg_to_addr(segment, index) 
          
        #store address we return value to  
        self._write("@R13")
        self._write("M=D")
        
        # pop value stored in top of stack, store it into D
        self._pop_SP()
        self._write("D=M")
        
        # go to address stored in @R13, and store in it D
        self._write("@R13")
        self._write("A=M")
        self._write("M=D")
    
    def _write(self, asm_command: str):
        """Writes a given assembly command to the output file."""
        self._output_file.write(asm_command + '\n')
        
    def _seg_to_const(self, segment_start: int, rel_index: int, max_index: int):
        """Converts a segment to a constant address, and checks if index exceeds pre-defined bounds"""
        index = segment_start + rel_index
        if index > max_index:
            raise ValueError("Index out of bounds: {0} (max: {1})".format(index, max_index))
        return "constant", index
    
    def _seg_to_addr(self, segment: str, index: str, isPush: bool = False):
        """Summary:
            Converts a segment to an address, and checks if index is out of bounds

        Args:
            segment (str): The segment type, as detailed in the Nand2Tetris VM language specification
            index (str): a numeric string representing the index relative to the segment
            isPush (bool, optional): Whether the operation applied is a Push operation. Defaults to False.

        Returns:
            str: the segment, after conversion to an address
            str: the index, after conversion to an address
        """
        if segment == "static": # convert to constant address
            segment, index = self._seg_to_const(16, index, 255)
        elif segment == "temp":
            index = str(int(index) + 5) # because temp is the actual address (located at 5), not a pointer
        elif segment == "pointer":
            if int(index):
                segment = "that"
            else:
                segment = "this"
            index = '0'
            
            if isPush:
                self._push(segment, index)
            else:
                self._pop(segment, index)
            return segment, index
         
        if segment in self.segment:
            segment = self.segment[segment]
            self._write_get_or_goto_arr_index(segment, index, isPush) # go to segment[index]
        return segment, index
    
    def _write_get_or_goto_arr_index(self, arr_index: int, rel_index: int, isPush: bool = False):
        """Given a pointer to an array and an index, writes to file the assembly code for storing symbol[index] in D"""
        self._write("@{0}".format(arr_index))
        self._write("D=M")
        self._write("@{0}".format(rel_index))
        if isPush:
            self._write("A=D+A")
        else:
            self._write("D=D+A")

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

    def _pop_SP(self):
        """Writes to file a common assembly operation: decrement SP"""
        self._write('@SP')
        self._write('AM=M-1')
        
    def _decrement_A(self):
        """Writes to file a common assembly operation: decrement A"""
        self._write('A=A-1')

    def _increment_SP(self):
        """Writes to file a common assembly operation: increment SP"""
        self._write('@SP')
        self._write('M=M+1')

    def _set_A_to_stack(self):
        """Writes to file a common assembly operation: set A to the top of the stack"""
        self._write('@SP')
        self._write('A=M')  
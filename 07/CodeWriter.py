from Parser import COMMAND_TYPE as C

class CodeWriter:
    
    segment = {
        "argument": "ARG",
        "local": "LCL",
    }
    
    def __init__(self, output_path: str):
        self._output_file = open(output_path, 'w')
        self.bool_count = 0 # Count of boolean comparisons
        self._file_name = ""
        
    def set_file_name(self, file_name: str):
        self._file_name = file_name
    
    def get_file_name(self):
        return self._file_name
    
    def write_arithmetic(self, operation):
            '''Apply operation to top of stack'''
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
            self._increment_SP()
        
    def write_push_pop(self, command_type, segment: str, index: int):
        if command_type == C.PUSH:
            self._push(segment, index)
        elif command_type == C.POP:
            self._pop(segment, index)
        else:
            raise ValueError("Invalid command: {0}".format(command_type))
    
    def close(self):
        self._output_file.close()
        
    def _push(self, segment, index):
        segment, index = self._seg_to_addr(segment, index)
        
        # if constant, set: D=index. else, set: D=segment[index]
        if segment == "constant":
            self._write("@{0}".format(index))
            self._write("D=A")
        else:
            self._write_goto_arr_index(self.segment[segment], index) 
            self._write("D=M")
        
        # set top of stack to D    
        self._write("@SP")
        self._write("A=M")
        self._write("M=D")
        
        # move stack pointer to top of stack
        self._write("@SP")
        self._write("M=M+1")
    
    def _pop(self, segment, index):
        if segment == "constant":
            raise ValueError("constant segment is invalid for pop command")
        segment, index = self._seg_to_addr(segment, index)
        
        # gets address we will pop value to
        if segment == "constant": # segment was originally static or temp; 
            self._write("@{0}".format(index))
        else:
            self._write_goto_arr_index(self.segment[segment], index) 
          
        #store address we return value to  
        self._write("D=A") 
        self._write("@R13")
        self._write("M=D")
        
        # get value stored in top of stack, pop it into D
        self._write("@SP")
        self._write("AM=M-1")
        self._write("D=M")
        
        # go to address stored in @R13, and store in it D
        self._write("@R13")
        self._write("A=M")
        self._write("M=D")
    
    def _write(self, asm_command: str):
        self._output_file.write(asm_command + '\n')
        
    def _seg_to_const(segment_start: int, rel_index: int, max_index: int):
        index = segment_start + rel_index
        if index > max_index:
            raise ValueError("Index out of bounds: {0} (max: {1})".format(index, max_index))
        return "constant", index
    
    def _seg_to_addr(self, segment, index):
        if segment == "static": # convert to constant address
            segment, index = self._seg_to_const(16, index, 255)
        elif segment == "temp": # convert to constant address
            segment, index = self._seg_to_const(5, index, 12)
        elif segment == "pointer":
            if index > 1:
                raise ValueError("Index out of bounds") 
            if index:
                segment = "this"
            else:
                segment = "that"
        return segment, index
    
    def _write_goto_arr_index(self, arr_index: int, rel_index: int):
        """Writes to file a common assembly operation: given an array's starting index and a relative index, goes to arr[rel_index]"""
        self._write("@{0}".format(arr_index))
        self._write("D=M")
        self._write("@{0}".format(rel_index))
        self._write("D=D+A")
        self._write("A=D")

    def _push_D_to_stack(self):
        '''Push from D onto top of stack, increment @SP'''
        self._write('@SP') # Get current stack pointer
        self._write('A=M') # Set address to current stack pointer
        self._write('M=D') # Write data to top of stack
        self._write('@SP') # Increment SP
        self._write('M=M+1')

    def _pop_stack_to_D(self):
        '''Decrement @SP, pop from top of stack onto D'''
        self._write('@SP')
        self._write('M=M-1') # Decrement SP
        self._write('A=M') # Set address to current stack pointer
        self._write('D=M') # Get data from top of stack

    def _decrement_SP(self):
        self._write('@SP')
        self._write('M=M-1')

    def _increment_SP(self):
        self._write('@SP')
        self._write('M=M+1')

    def _set_A_to_stack(self):
        self._write('@SP')
        self._write('A=M')  
from Parser import COMMAND_TYPE as C

class CodeWriter:
    
    segment = {
        'argument': 'ARG',
        'local': 'LCL',
        'this': 'THIS',
        'that': 'THAT',
        'temp': 'R5',
        'pointer': 3,
        'temp': 5,
        'static': 16,
    }
    
    def __init__(self, output_path: str, add_bootstrap: bool = False, DEBUG_MODE: bool = False):
        self._output_file = open(output_path, 'w')
        self._bool_count = 0 # Count of boolean comparisons so far; used for unique jump labels
        self._call_count = 0 # Count of function calls so far; used for unique jump labels to return address
        self._file_name = ''
        self._DEBUG_MODE = DEBUG_MODE
        if add_bootstrap:
            self.set_file_name('Sys.vm')
            self._write_sys_init()

    def set_file_name(self, file_name: str):
        """Informs the code writer that the translation of a new VM file has started."""
        if self._file_name != file_name:
            self._file_name = file_name
            if self._DEBUG_MODE: self._log('FILE {}:'.format(file_name))

    def write_arithmetic(self, operation: str):
        """Writes the assembly code for the given arithmetic operation to the top value(s) on the stack."""
        
        if self._DEBUG_MODE: self._log("COMMAND_TYPE.ARITHMETIC {0}".format(operation))
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
            raise ValueError('Invalid operator: {0}'.format(operation))
        self._increment_SP()

    def write_push_pop(self, command_type: C, segment: str, index: str):
        """Writes the assembly code for pushing or popping the given segment at the given index to/from the stack."""
        if self._DEBUG_MODE: self._log('{0} {1} {2}'.format(str(command_type), segment, index))
        
        self._seg_to_addr(segment, index)  
        if command_type == C.PUSH:
            if segment == 'constant':
                self._write('D=A')
            else:
                self._write('D=M')
            self._push_D_to_stack()
            
        elif command_type == C.POP:
            self._write('D=A')
            self._write('@R13')
            self._write('M=D')
            self._pop_stack_to_D()
            self._write('@R13')
            self._write('A=M')
            self._write('M=D')
        else:
            raise ValueError('Invalid command: {0}'.format(command_type))

    def write_label(self, label: str):
        """Writes the assembly code to define a label in the current VM file."""
        self._write('({})'.format(self._get_label(label)))

    def write_goto(self, label: str):
        """Writes the assembly code for an unconditional jump (goto) to the specified label in the current VM file."""
        self._write('@{}'.format(self._get_label(label)))
        self._write('0;JMP')

    def write_if(self, label: str):
        """Writes the assembly code for a conditional jump to the specified label in the current VM file."""
        if self._DEBUG_MODE: self._log("IF-GOTO {0}".format(label))
        self._pop_stack_to_D()
        self._write('@{}'.format(self._get_label(label)))
        self._write('D;JNE')

    def write_function(self, function_name: str, num_args: int):
        if self._DEBUG_MODE: self._log("FUNCTION {0}: {1} ARGS".format(function_name, num_args))
        """Writes the assembly code for a function command, which initializes a function with the given name and number of arguments."""
        self._write('({})'.format(self._get_function_label(function_name, num_args)))
        for _ in range(num_args): # Initialize num_args local arguments to 0
            self._write('D=0')
            self._push_D_to_stack()
            
    def write_function_call(self, function_label, num_args: int):
        if self._DEBUG_MODE: self._log("CALL {0}: {1} ARGS".format(function_label, num_args))
        """Writes the assembly code for a function call command, which calls the function with the given name and number of arguments."""
        function_label = self._get_function_label(function_label, num_args)
        return_label = function_label + '.RETURN' + str(self._call_count) # saves a unique return address for each function call
        self._call_count += 1

        # push return-address
        self._write('@' + return_label)
        self._write('D=A')
        self._push_D_to_stack()
        
        # push LCL, ARG, THIS, THAT to new function's stack 
        for address in ['LCL', 'ARG', 'THIS', 'THAT']:
            self._write("@" + address)
            self._write('D=M')
            self._push_D_to_stack()

        # sets LCL to new SP value
        self._write('@SP')
        self._write('D=M')
        self._write('@LCL')
        self._write('M=D')

        # sets ARG to SP - n - 5
        self._update_ARG(num_args)
        
        # handle end of function call
        self._write('@' + function_label)
        self._write('0;JMP')
        self._write('({})'.format(return_label))
        
    def write_return(self):
        if self._DEBUG_MODE: self._log("RETURN")
        
        # Temporary pointers to keep track of relative LCL and return address
        current_frame = 'R13'
        return_address = 'R14'

        # store LCL in our current frame pointer
        self._write('@LCL')
        self._write('D=M')
        self._write('@' + current_frame)
        self._write('M=D')

        self._frame_var_to_stack(current_frame, return_address, 5)

        # *ARG = pop()
        self._pop_stack_to_D()
        self._write('@ARG')
        self._write('A=M')
        self._write('M=D')

        # SP = ARG+1
        self._write('@ARG')
        self._write('D=M')
        self._write('@SP')
        self._write('M=D+1')

        for offset, address in enumerate(['THAT', 'THIS', 'ARG', 'LCL'], start=1):
            self._frame_var_to_stack(current_frame, address, offset)

        self._write('@' + return_address)
        self._write('A=M')
        self._write('0;JMP')


    def close(self):
        self._output_file.close()

    def _write(self, asm_command: str):
        """Writes a given assembly command to the output file."""
        self._output_file.write(asm_command + '\n')
        
    def _log(self, message: str):
        """Writes a given comment to the output file."""
        self._write('// ' + message)

    def _seg_to_addr(self, segment: str, index: str):
        """Summary:
            Converts a segment to an address, and goes to that address.

        Args:
            segment (str): The segment type, as detailed in the Nand2Tetris VM language specification
            index (str): a numeric string representing the index relative to the segment
        """
        address = self.segment.get(segment)
        if segment == 'constant':
            self._write('@' + index)
        elif segment == 'static':
            self._write('@{fname}.{index}'.format(fname=self._file_name, index=index))
        else:
            try: # if the segment mapped to a constant (int) address
                self._write('@R' + str(address + int(index)))
            except: # if the segment mapped to a string
                self._write('@' + address)
                self._write('D=M')
                self._write('@' + index)
                self._write('A=D+A')

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
    
    def _update_ARG(self, num_args: int):
        """Should be used when calling a VM function. Updates the ARG register to point to the first argument of the currently-called function."""
        self._write('@' + str(num_args + 5))
        self._write('D=D-A') # D = SP - (n + 5). SP stored in D by previous function, and n+5 is the number of arguments + SP, ARG, LCL, THIS, THAT
        self._write('@ARG')
        self._write('M=D')
        
    def _get_function_label(self, function_name: str, num_args):
        """Returns the function name's corresponding label, in the format FILE_NAME.FUNCTION_NAME.NUM_ARGS. We include num_args to enable function overloading."""
        return '{}.{}.{}ARGS'.format(self._file_name,function_name, num_args)
    
    def _get_label(self, label: str):
        """Returns the corresponding label, in the format FILE_NAME.LABEL."""
        return '{}${}'.format(self._file_name,label)

    def _frame_var_to_stack(self, current_frame: str, address: str, offset: int):
        """sets the value of address: address = *(FRAME-offset)"""
        self._write('@' + current_frame)
        self._write('D=M') # Save start of frame
        self._write('@' + str(offset))
        self._write('D=D-A') # Adjust address
        self._write('A=D') # Prepare to load value at address
        self._write('D=M') # Store value
        self._write('@' + address)
        self._write('M=D') # Save value
        
    def _write_sys_init(self):
        """Bootstrap code: This code should be placed at the beginning of the output file,
        when translating a folder.\n
        ASSUMPTION: there exists a file called Sys.vm, which contains the Sys.init function."""
        if self._DEBUG_MODE: self._log("BOOTSTRAP CODE: CALL SYS.INIT")        
        # Initialize SP to 256
        self._write('@256')
        self._write('D=A')
        self._write('@SP')
        self._write('M=D')
        # Call Sys.init
        self.write_function_call('Sys.init', 0)
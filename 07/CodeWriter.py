class CodeWriter:
    
    segment = {
        "argument": "ARG",
        "local": "LCL",
    }
    
    def __init__(self, output_path: str):
        self._output_file = open(output_path, 'w')
        
    def set_file_name(self, file_name: str):
        self._file_name = file_name
    
    def write_arithmetic(self, string):
        pass # write arithmetic here
    
    def write_push_pop(self, command, segment: str, index: int):
        if command == "C_PUSH":
            self._push(segment, index)
        elif command == "C_POP":
            self._pop(segment, index)
        else:
            raise ValueError("Invalid command: {0}".format(command))
    
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
        self._output_file.write(asm_command + "\n")
        
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
        
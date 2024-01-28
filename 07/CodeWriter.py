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
        pass
    
    def close(self):
        self._output_file.close()
        
    def _push(self, segment, index):
        segment, index = self._seg_to_addr(segment, index)
        
        # if constant, set: D=index. else, set: D=segment[index]
        if segment == "constant":
            self._write("@{0}".format(index))
            self._write("D=A")
        else:
            self._write("@{0}".format(self.segment[segment]))
            self._write("D=A")
            self._write("@{0}".format(index))
            self._write("D=D+A")
            self._write("@D")
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
        
        # get value stored in top of stack, and soft-delete it
        self._write("@SP")
        self._write("AM=M-1")
        self._write("D=M")
        
        if segment == "constant": # segment was originally static or temp
            self._write("@{0}".format(index))
            self._write("M=D")
        else:
            self._write("@{0}".format(self.segment[segment]))
        
        pass
    
    def _write(self, asm_command: str):
        self._output_file.write(asm_command)
        
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
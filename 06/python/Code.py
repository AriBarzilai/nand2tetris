_jump_codes = {None: '000',
               'JGT' : '001',
               'JEQ' : '010',
               'JGE' : '011',
               'JLT' : '100',
               'JNE' : '101',
               'JLE' : '110',
               'JMP' : '111'}
_dest_codes = {None: '000',
               'M' : '001',
               'D' : '010',
               'MD' : '011',
               'DM' : '011',
               'A' : '100',
               'AM' : '101',
               'AD' : '110',
               'AMD' : '111',
               'ADM' : '111'}
_comp_codes_dict = {
            None:'0000000',
            '0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100',
            'A':'0110000', '!D':'0001101', '!A':'0110001', '-D':'0001111',
            '-A':'0110011', 'D+1':'0011111','A+1':'0110111','D-1':'0001110',
            'A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111',
            'D&A':'0000000','D|A':'0010101',

            'M':'1110000', '!M':'1110001', '-M':'1110011', 'M+1':'1110111',
            'M-1':'1110010','D+M':'1000010','D-M':'1010011','M-D':'1000111',
            'D&M':'1000000', 'D|M':'1010101' }

def dest(mnemonic):
    """
    Summary:
    Returns the 3-bit binary code of the dest mnemonic.

    Args:
    mnemonic (str): The mnemonic string whose binary code is to be returned.
    """
    return _dest_codes.get(mnemonic)

def comp(mnemonic):
    """
    Summary:
    Returns the 7-bit binary code of the dest mnemonic.

    Args:
    mnemonic (str): The mnemonic string whose binary code is to be returned.
    """
    return _comp_codes_dict.get(mnemonic)
    
def jump(mnemonic):
    """
    Summary:
    Returns the 3-bit binary code of the jump mnemonic.

    Args:
    mnemonic (str): The mnemonic string whose binary code is to be returned.
    """
    return _jump_codes.get(mnemonic)

def symbol(num):
    """
    Summary:
    Returns the 16-bit binary code of the symbol.
    You should use this only on the symbol obtained from the symbol() method of the Parser class.

    Args:
    num (int): The number whose binary code is to be returned.
    """
    return bin(num)[2:].zfill(16) if num is not None else None
from elf_reader import * 
from IR import *
import IR2IR
from IR2ML import *
from ML2HL import *

def expand(n):
	return n[0]

analyzed_addr=[]
text_addr=text.header['sh_addr']
IR_list=[]
analyze_soon_addr=[ep_addr]#main addr
while analyze_soon_addr:
    addr=analyze_soon_addr.pop()
    a=opcode2asm(text_data[addr-text_addr:],addr)
    for dis,length in a:
        cg=dis.Instruction.Category
        type_opcode=cg&0xffff0000
        type_opcode_do=cg&0xffff
        if dis.Instruction.Mnemonic=='ret ' or dis.Instruction.Mnemonic=='hlt ':
            IR_list+=[[dis.Instruction.Mnemonic[:-1]]]
            analyzed_addr.append([addr,dis.VirtualAddr+length-1])
            break
        elif type_opcode_do == CONTROL_TRANSFER:
            if dis.Instruction.Mnemonic=='call ':
                if dis.Argument1.ArgType & CONSTANT_TYPE + RELATIVE_:
                    #call $
                    call_addr=h2i(dis.Argument1.ArgMnemonic)
                    if call_addr in map(expand,funcs):
                        IR_list+=[['call',funcs[map(expand,funcs).index(call_addr)][1]]]
                else:
                    IR_list+=IR(dis)

        else:
            rIR=IR(dis)
            if rIR == None:
                print dis.CompleteInstr
            else:
                IR_list+=rIR

IR_list=IR2IR.IR2IR(IR_list)
for x in IR_list:
        print x[:]
ML_list=IR2ML(IR_list)
HL_list=ML2HL(ML_list)

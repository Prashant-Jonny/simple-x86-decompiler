#get BeaEngine's struct
from BeaEnginePython import *
def h2i(s):
    return int(s[:-1],16)

def int2reg(n,s):
    '''s는레지스터 종류'''
    if s==REGISTER_TYPE + GENERAL_REG :
        if n==0:
            return 0
        elif n==REG0:
            return 'eax'
        elif n==REG1:
            return 'ecx'
        elif n==REG2:
            return 'edx'
        elif n==REG3:
            return 'ebx'
        elif n==REG4:
            return 'esp'
        elif n==REG5:
            return 'ebp'
        elif n==REG6:
            return 'esi'
        elif n==REG7:
            return 'edi'
        else:
            print hex(n)
            n=0/0


def IR(dis):
    #print dis.CompleteInstr
    cg=dis.Instruction.Category
    type_opcode=cg&0xffff0000
    type_opcode_do=cg&0xffff
    if type_opcode & GENERAL_PURPOSE_INSTRUCTION or type_opcode & SYSTEM_INSTRUCTION  :
        if dis.Instruction.Mnemonic=='nop ':
            return [['NOP']]
        elif type_opcode_do == DATA_TRANSFER:
            return IR_DATA_TRANSFER(dis)
            if IR_DATA_TRANSFER(dis) == None:
                print dis.CompleteInstr
        elif type_opcode_do == ARITHMETIC_INSTRUCTION:
            return IR_ARITHMETIC_INSTRUCTION(dis)
            if IR_ARITHMETIC_INSTRUCTION(dis) == None:
                print dis.CompleteInstr
        elif type_opcode_do == LOGICAL_INSTRUCTION :
            return IR_LOGICAL_INSTRUCTION(dis)
            if IR_LOGICAL_INSTRUCTION(dis) == None:
                print dis.CompleteInstr
        elif type_opcode_do == CONTROL_TRANSFER :
            return [[-1]]#print dis.CompleteInstr
        else:
            return [[-1]]#print dis.CompleteInstr,hex(dis.Instruction.Category)
    else:
        print 'u//u',dis.CompleteInstr
        return [[-1]]

def IR_DATA_TRANSFER(dis):
    if dis.Instruction.Mnemonic=='push ':
        #push는 push 정수, push reg 2가지 경우
        if dis.Argument2.ArgType & 0xffff0000 &  REGISTER_TYPE + GENERAL_REG  :
            return [['push',dis.Argument2.ArgMnemonic[:]]]
        elif dis.Argument2.ArgType & 0xffff0000 &  CONSTANT_TYPE + ABSOLUTE_:
            return [['push',int(dis.Argument2.ArgMnemonic[:-1],16)]]
        else:
            print dis.CompleteInstr
            return [[-1]]

    elif dis.Instruction.Mnemonic=='pop ':
        return [['pop',dis.Argument1.ArgMnemonic[:]]]
        
    elif dis.Instruction.Mnemonic=='mov ':
        if dis.Argument1.ArgType & 0xffff0000 & REGISTER_TYPE + GENERAL_REG  :
            #mov reg,???
            if dis.Argument2.ArgType & 0xffff0000 & REGISTER_TYPE + GENERAL_REG  :
                #mov reg,reg
                return [['mov',dis.Argument1.ArgMnemonic,dis.Argument2.ArgMnemonic]]
            elif dis.Argument2.ArgType & 0xffff0000 &  CONSTANT_TYPE + ABSOLUTE_ :
                #mov reg,int
                return [['mov',dis.Argument1.ArgMnemonic,int(dis.Argument2.ArgMnemonic[:-1],16)]]
            elif dis.Argument2.ArgType & 0xffff0000 &  MEMORY_TYPE  :
                #mov reg,[xxx]
                #->
                #mov tmp1,IndexRegister
                #mul tmp1,Scale
                #add tmp1,BaseRegister
                #add tmp1,Displacement
                #movfp reg,tmp1
                r=[]
                r+=[['movcalc','tmp1',int2reg(dis.Argument2.Memory.IndexRegister,REGISTER_TYPE + GENERAL_REG)
                     ,dis.Argument2.Memory.Scale,int2reg(dis.Argument2.Memory.BaseRegister,REGISTER_TYPE + GENERAL_REG)
                     ,dis.Argument2.Memory.Displacement]]#movcalc tmp1 eax a b c == mov tmp1 eax*a+b+c
                r+=[['movfp',dis.Argument1.ArgMnemonic,'tmp1']]
                return r
            
            else:
                return [[-1]]

        elif dis.Argument1.ArgType & 0xffff0000 &  MEMORY_TYPE:
            #mov [xxx],???
            if dis.Argument2.ArgType & 0xffff0000 &  CONSTANT_TYPE + ABSOLUTE_:
                #mov [xxx],int
                
                #mov tmp1,IndexRegister
                #mul tmp1,Scale
                #add tmp1,BaseRegister
                #add tmp1,Displacement
                #movpf tmp1,int
                r=[]
                r+=[['movcalc','tmp1',int2reg(dis.Argument1.Memory.IndexRegister,REGISTER_TYPE + GENERAL_REG)
                     ,dis.Argument1.Memory.Scale,int2reg(dis.Argument1.Memory.BaseRegister,REGISTER_TYPE + GENERAL_REG)
                     ,dis.Argument1.Memory.Displacement]]#movcalc tmp1 eax a b c == mov tmp1 eax*a+b+c
                r+=[['movpf','tmp1',h2i(dis.Argument2.ArgMnemonic),dis.Argument2.ArgSize]]
                return r
            elif dis.Argument2.ArgType & 0xffff0000 & REGISTER_TYPE + GENERAL_REG:
                #mov [xxx],reg
                r=[]
                r+=[['movcalc','tmp1',int2reg(dis.Argument1.Memory.IndexRegister,REGISTER_TYPE + GENERAL_REG)
                     ,dis.Argument1.Memory.Scale,int2reg(dis.Argument1.Memory.BaseRegister,REGISTER_TYPE + GENERAL_REG)
                     ,dis.Argument1.Memory.Displacement]]#movcalc tmp1 eax a b c == mov tmp1 eax*a+b+c
                r+=[['movpf','tmp1',dis.Argument2.ArgMnemonic]]
                return r
            else:
                print dis.CompleteInstr
                return [[-1]]
        else:
            print dis.CompleteInstr
            return [[-1]]
    else:
        print dis.CompleteInstr
        return [[-1]]

def IR_ARITHMETIC_INSTRUCTION(dis):
    if dis.Instruction.Mnemonic=='cmp ' or dis.Instruction.Mnemonic=='add ' or dis.Instruction.Mnemonic=='sub ':
        if dis.Argument1.ArgType & 0xffff0000 & REGISTER_TYPE + GENERAL_REG  :
            #xxx reg,???
            if dis.Argument2.ArgType & 0xffff0000 & REGISTER_TYPE + GENERAL_REG  :
                #xxx reg,reg
                return [[dis.Instruction.Mnemonic[:-1],dis.Argument1.ArgMnemonic,dis.Argument2.ArgMnemonic]]
            elif dis.Argument2.ArgType & 0xffff0000 &  CONSTANT_TYPE + ABSOLUTE_:
                #xxx reg,int
                return [[dis.Instruction.Mnemonic[:-1],dis.Argument1.ArgMnemonic,h2i(dis.Argument2.ArgMnemonic)]]
            else:
                print dis.CompleteInstr
                return [[-1]]
        elif dis.Argument1.ArgType & 0xffff0000 & MEMORY_TYPE :
            #xxx [xxx],???
            if dis.Argument2.ArgType & 0xffff0000 &  CONSTANT_TYPE + ABSOLUTE_:
                #xxx [xxx],int
                r=[]
                r+=[['movcalc','tmp1',int2reg(dis.Argument1.Memory.IndexRegister,REGISTER_TYPE + GENERAL_REG)
                     ,dis.Argument1.Memory.Scale,int2reg(dis.Argument1.Memory.BaseRegister,REGISTER_TYPE + GENERAL_REG)
                     ,dis.Argument1.Memory.Displacement]]#movcalc tmp1 eax a b c == mov tmp1 eax*a+b+c
                r+=[[dis.Instruction.Mnemonic[:-1],'tmp1',h2i(dis.Argument2.ArgMnemonic)]]
                return r
            else:
                print dis.CompleteInstr
                return [[-1]]                

        else:
            print dis.CompleteInstr
            return [[-1]]

    else:
        print dis.CompleteInstr
        return [[-1]]

def IR_LOGICAL_INSTRUCTION(dis):
    if dis.Instruction.Mnemonic=='xor ' or dis.Instruction.Mnemonic=='and ' or dis.Instruction.Mnemonic=='or ':
        if dis.Argument1.ArgType & 0xffff0000 & REGISTER_TYPE + GENERAL_REG  :
            #xxx reg,???
            if dis.Argument2.ArgType & 0xffff0000 & REGISTER_TYPE + GENERAL_REG  :
                # cmp reg,reg
                return [[dis.Instruction.Mnemonic[:-1],dis.Argument1.ArgMnemonic,dis.Argument2.ArgMnemonic]]
            elif dis.Argument2.ArgType & 0xffff0000 &  CONSTANT_TYPE + ABSOLUTE_:
                #cmp reg,int
                return [[dis.Instruction.Mnemonic[:-1],dis.Argument1.ArgMnemonic,h2i(dis.Argument2.ArgMnemonic)]]
            else:
                print dis.CompleteInstr
                return [[-1]]
        elif dis.Argument1.ArgType & 0xffff0000 & MEMORY_TYPE :
            if dis.Argument2.ArgType & 0xffff0000 &  CONSTANT_TYPE + ABSOLUTE_:
                r=[]
                r+=[['movcalc','tmp1',int2reg(dis.Argument1.Memory.IndexRegister,REGISTER_TYPE + GENERAL_REG)
                     ,dis.Argument1.Memory.Scale,int2reg(dis.Argument1.Memory.BaseRegister,REGISTER_TYPE + GENERAL_REG)
                     ,dis.Argument1.Memory.Displacement]]#movcalc tmp1 eax a b c == mov tmp1 eax*a+b+c
                r+=[[dis.Instruction.Mnemonic[:-1],'tmp1',h2i(dis.Argument2.ArgMnemonic)]]
                return r
            else:
                print dis.CompleteInstr
                return [[-1]]                

        else:
            print dis.CompleteInstr
            return [[-1]]

    else:
        print dis.CompleteInstr
        return [[-1]]

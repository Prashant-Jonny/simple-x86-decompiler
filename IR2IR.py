#[esp(sp),tmp1,tmp2,tmp3,eax,ebx,ecx,edx,edi,esi,ebp]
import IR2ML
def reg2int(s):
    global regs
    if 'v' in s:
        print regs
        return regs.index(s)
    else:
        return ["esp","tmp1","tmp2","eax","ebx","ecx","edx","edi","esi","ebp"].index(s)

def int2reg(n):
    global regs
    return ["esp","tmp1","tmp2","eax","ebx","ecx","edx","edi","esi","ebp"][n]

def IR2IR(IR_list):
    IR_list=remove_useless(IR_list)
    IR_list=insert_reg(IR_list)
    IR_list=set_stack(IR_list)
    return IR_list

def remove_useless(IR_list):
    R_IR_list=[]
    for ir in IR_list:
        if len(ir)==3:
            if ir[1]=='tmp1':
                #if ir[0]=='mov' and ir[2]==0:
                #    continue
                if ir[0]=='mul' and ir[2]==1:
                    continue
        R_IR_list+=[ir]
    return R_IR_list
global regs
def insert_reg(IR_list):
    #reg 대신 변수를 넣는다
    vn=1
    sn=1
    #[esp(sp),tmp1,tmp2,tmp3,eax,ebx,ecx,edx,edi,esi,ebp]
    R_IR_list=[]
    stack=[]
    global regs
    regs=[0,'???','???','???','???','???','???','???','???','???']
    for n,ir in enumerate(IR_list):
        R_IR_list+=[[ir[0]]+[regs[:]]+[stack[:]]+ir[1:]]
        if ir[0]=='push':
            regs[0]+=4
            if hasattr(ir[1],'encode'):
                stack.append(regs[reg2int(ir[1])])
            elif hasattr(ir[1],'imag'):
                stack.append(ir[1])
        elif ir[0]=='pop':
            regs[0]-=4
            regs[reg2int(ir[1])]=stack.pop()
        elif ir[0]=='mov':
            if hasattr(ir[2],'encode'):
                #mov reg,reg
                regs[reg2int(ir[1])]=regs[reg2int(ir[2])]
                #R_IR_list[-1][4]=regs[reg2int(ir[2])]
            elif hasattr(ir[2],'imag'):
                #mov reg,int
                regs[reg2int(ir[1])]='v%s'%str(vn)
                R_IR_list[-1][3]='v%s'%str(vn)
                vn+=1
        elif ir[0]=='movcalc':
            regs[reg2int(ir[1])]='v%s'%str(vn)
            R_IR_list[-1][3]='v%s'%str(vn)
            vn+=1
        elif ir[0]=='movpf':
            if regs[reg2int(ir[1])]=='???':
                pass
            else:
                R_IR_list[-1][3]=regs[reg2int(ir[1])]
            if hasattr(ir[2],'encode'):
                if regs[reg2int(ir[2])]=='???':
                    regs[reg2int(ir[2])]='v%s'%str(vn)
                    R_IR_list[-1][4]='v%s'%str(vn)
                    vn+=1
                else:
                    R_IR_list[-1][4]=regs[reg2int(ir[2])]
                    
        elif ir[0]=='movfp':
            if hasattr(ir[1],'encode'):
                if regs[reg2int(ir[1])]=='???':
                    regs[reg2int(ir[1])]='v%s'%str(vn)
                    R_IR_list[-1][3]='v%s'%str(vn)
                    vn+=1
                else:
                    R_IR_list[-1][3]=regs[reg2int(ir[1])]
            if hasattr(ir[2],'encode'):
                if regs[reg2int(ir[2])]=='???':
                    regs[reg2int(ir[2])]='v%s'%str(vn)
                    R_IR_list[-1][4]='v%s'%str(vn)
                    vn+=1
                else:
                    R_IR_list[-1][4]=regs[reg2int(ir[2])]
        elif ir[0]=='call':
            regs=[0,'???','???','???','???','???','???','???','???','???']
        
        elif len(ir)>1:
            if ir[1]=='esp':
                if ir[0]=='sub':
                    if hasattr(ir[2],'encode'):
                        if regs[reg2int(ir[2])]=='???':
                            #sub esp,reg , dontknow reg
                            return -1
                        elif hasattr(regs[reg2int(ir[2])],'imag'):
                            #sub esp,reg , kwow reg
                            regs[0]+=regs[reg2int(ir[2])]
                            for x in range(regs[reg2int(ir[2])]/4):
                                stack.append('???')
                    else:
                        regs[0]+=ir[2]
                        for x in range(ir[2]/4):
                            stack.append('???')
                elif ir[0]=='add':
                    if hasattr(ir[2],'encode'):
                        if regs[reg2int(ir[2])]=='???':
                            #add esp,reg , dontknow reg
                            return -1
                        elif hasattr(regs[reg2int(ir[2])],'imag'):
                            #add esp,reg , kwow reg
                            for x in range(regs[reg2int(ir[2])]/4):
                                stack.pop()
                            regs[0]-=regs[reg2int(ir[2])]
                    else:
                        regs[0]+=ir[2]
                        for x in range(ir[2]/4):
                            stack.pop()
    return R_IR_list

def set_stack(IR_list):
    #지역변수 등 스텍내에 저장되는 변수 처리 -> savefstack,save2stack
    R_IR_list=[]
    n=0
    while n<len(IR_list)-1:
        ir=IR_list[n]
        if ir[0]=='movcalc':
            ir_next=IR_list[n+1]
            if ir_next[0]=='movfp' and ir[4]==0 and ir[6]=='esp':
                r=['savefstack']
                r.append(ir[1])
                r.append(ir[2])
                r.append(ir_next[3])
                r.append('s'+str(len(ir[2])-ir[7]/4))
                k=IR_list[n+2][2][len(IR_list[n+2][2])-1-ir[7]/4]
                if k=='???':
                    pass
                else:
                    pass
                n+=1
                R_IR_list.append(r)
                
            elif ir_next[0]=='movpf' and ir[4]==0 and ir[6]=='esp':
                r=['save2stack']
                r.append(ir[1])
                r.append(ir[2])
                r.append('s'+str(len(ir[2])-ir[7]/4))
                r.append(ir_next[4])
                IR_list[n+2][2][len(IR_list[n+2][2])-1-ir[7]/4]=ir_next[4]
                n+=1
                R_IR_list.append(r)
        else:
            R_IR_list.append(ir)
        n+=1
    return R_IR_list

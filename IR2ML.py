from elf_reader import * 
def IR2ML(IR_list):
    IR_list=find_used_onetime(IR_list) #GC?
    IR_list=remove_prologue(IR_list)
    IR_list=find_str(IR_list)
    return IR_list

#한번만 쓰이는 변수 제거

def find_str(IR_list):
    for n,ir in enumerate(IR_list):
        if len(ir)>4:
            d=ir[4]
            if rodata_addr_range[0] < d and rodata_addr_range[1] > d:
                d=repr(rodata_data[ir[4]-rodata_addr_range[0]:].split('\x00')[0])
                IR_list[n][4]=d
    return IR_list

def remove_prologue(IR_list):
    R_IR_list=[]
    n=0
    while n<len(IR_list):
        x=IR_list[n]
        if x[0]=='push' and x[3]=='ebp':
            if IR_list[n+1][0]=='mov' and IR_list[n+1][3]=='ebp' and IR_list[n+1][4]=='esp':
                n+=1
        else:
            R_IR_list.append(x)
        n+=1
    return R_IR_list

def find_used_onetime(IR_list):
    R_IR_list=[]
    r=set()
    for x in IR_list:
        x=x[1:]
        for y in x:
            if hasattr(y,'encode'):
                if y[0]=='v' or y[0]=='s':
                    r.add(y)
    var_list=list(r)
    var_count_list=[]
    for x in var_list:
        var_count_list.append([x,0])
    var_count_list.sort()
    var_list.sort()
    for x in IR_list:
        for y in x:
            try:
                i=var_list.index(y)
                var_count_list[i][1]+=1
            except:
                pass
    for x in var_count_list:
        print x
    
    return R_IR_list

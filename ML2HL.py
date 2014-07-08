def ML2HL(ML_list):
    HL_list=[]
    n=0
    var_list=collect_all_var(ML_list)
    print 'int',','.join(var_list)
    while n<len(ML_list):
        ml=ML_list[n]
        if ml[0]=='save2stack':
            print '%s = %s' %(str(ml[3]),str(ml[4]))
        elif ml[0]=='mov':
            print '%s = %s' %(str(ml[3]),str(ml[4]))
        elif ml[0]=='savefstack':
            print '%s = %s' %(str(ml[3]),str(ml[4]))
        elif ml[0]=='call':
            print '%s()'%(str(ml[3]))
        n+=1
    return ML_list

def collect_all_var(ML_list):
    r=set()
    for x in ML_list:
        x=x[1:]
        for y in x:
            if hasattr(y,'encode'):
                if y[0]=='v' or y[0]=='s':
                    r.add(y)
    r_=list(r)
    r_.sort()
    return r_

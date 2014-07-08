import struct
from elftools.elf.elffile import ELFFile

f=open('c2.exe', 'rb')
elf=ELFFile(f)
dynstr=elf.get_section_by_name('.dynstr').data()

plt=elf.get_section_by_name('.plt')
plt_data=plt.data()


rel_plt=elf.get_section_by_name('.rel.plt')
rel_plt_data=rel_plt.data()

dynsym=elf.get_section_by_name('.dynsym').data()
func_name=[]
funcs=[]
for x in range(0,len(dynsym),16):
    offset,addr,size,info,other,shndx=struct.unpack('IIIBBH',dynsym[x:x+16])
    func_name+=[dynstr[offset:].split('\x00')[0]]

for x in range(0,len(rel_plt_data),8):
    faddr,t=struct.unpack('II',rel_plt_data[x:x+8])
    funcs+=[[plt.header['sh_addr']+plt_data.index(rel_plt_data[x:x+4])-2,func_name[t>>8]]]

text=elf.get_section_by_name('.text')
text_addr=text.header['sh_addr']
text_data=text.data()
ep_addr,=struct.unpack('I',text_data[23+1:23+1+4])

rodata=elf.get_section_by_name('.rodata')
rodata_data=rodata.data()
rodata_addr_range=[rodata.header['sh_addr'],rodata.header['sh_addr']+len(rodata_data)]


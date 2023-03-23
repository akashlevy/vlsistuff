#! /usr/bin/env python3
# version 8.jun.2021 ilia
import os,sys,string
import random
''' activation:
obfuscate.py <FILENAME>  <SEED> [prefix]

obfuscate.py ../rtl/cucu.v   123456 keepme_
means:
    run on this file cucu.v
    the result file will be ../rtl/cucu_fub.v

    123456 is numeric seed. it is also printed on the first line.
    keepme_    : will refrain from translating any net that begins with this string.
        keep mechanism is simple and should be enough - as You control the rtl.

ifdef, ifndef ,else ,endif  : ARE NOT TREATED on purpose! Dont use them!!!
`define (s) all defines are moved to the beginning of the file.

'''



def main():
    global TOP,Reserved
    Fname = sys.argv[1]
    Seed  = eval(sys.argv[2])
    TOP  = sys.argv[3]
    print('TOP is "%s"' % TOP)
    if len(sys.argv)>4:
        Prefix = sys.argv[4]
    else:
        Prefix = False
    Fres = open('reserved')
    Reserved = Fres.read()
    Fres.close()
    Reserved = Reserved.split()

    Dir,Cell,Ext = cellName(Fname)
    random.seed(Seed)
    File = open(Fname)
    Text = File.read()
    Text2 = removeLineComments(Text)
    Text3 = removeComments0(Text2)
    Defines,Text4 = extractDefines(Text3)
    Wrds = tokenify(Text4)
    dddd("000000",Wrds)
    Modules,Inouts,Wires = externals(Wrds,Prefix)
    dddd("000000",Wrds)
    revork(Wrds,Modules,Inouts,Wires,Seed) 
    dddd("111111",Wrds)
    if Dir == '': Dir = '.'
    Ofilename = '%s/%s_fub.%s' % (Dir,Cell,Ext)
    saveWords(Ofilename,Defines,Wrds,Seed)
    for Key in TRANS:
        print("%s %s" % (Key,TRANS[Key]))

def dddd(Head,Wrds):
    WW = Wrds[:]
    while WW!=[]:
        Res = 'h%s: ' % Head
        while (len(Res)<128)and(WW!=[]):
            Res += ' '+WW.pop(0)
        print(Res)

TRANS = {}
def translate(Tok,Modules,Inouts,Wires):
    if Tok in Reserved: return Tok
#    if Tok in Inouts: return Tok
    if Tok in Keywords: return Tok
    if not token(Tok): return Tok
#    if Tok not in Wires+Modules+Inouts: return Tok
    if Tok in TRANS: return TRANS[Tok]
    X = random.randint(0xff,0xffffff)
    Res = 'o%04x'%X
    TRANS[Tok] = Res
    return Res



def revork(Wrds,Module,Inouts,Wires,Seed):
    for ind,Wrd in enumerate(Wrds):
        Wrd = translate(Wrd,Module,Inouts,Wires)
    X = list(TRANS.keys())
    random.shuffle(X)
    random.shuffle(X)
    if len(X)>0:
        TRANS[X[0]] = 'oo0%x' % Seed
    if len(X)>1:
        TRANS[X[1]] = 'oo1%x' % Seed
    if len(X)>2:
        TRANS[X[2]] = 'oo2%x' % Seed


    for ind,Wrd in enumerate(Wrds):
        Wrd = translate(Wrd,Module,Inouts,Wires)
        Wrds[ind] = Wrd
        


#  Defines,Text4 = extractDefines(Text3)
def  extractDefines(Text):
    Lines = Text.split('\n')
    Res = []
    Defines = []
    for Line in Lines:
        if '`define' in Line:
            Defines.append(Line)
        else: 
            Res.append(Line)
    return '\n'.join(Defines),'\n'.join(Res)


def saveWords(Foutname,Defines,Wrds,Seed):
    Fout = open(Foutname, 'w')
#   Fout.write('// %s\n'%(Seed))
    print('WRDS',len(Wrds))
    Fout.write('%s\n' % Defines)
    insertSeed(Wrds,Seed)
    while Wrds!=[]:
        Out = ''
        while (len(Out)<128)and(Wrds!=[]):
            Out = Out + ' ' + Wrds.pop(0)
        Fout.write('%s\n' % Out)
    Fout.close()

def insertSeed(Wrds,Seed):
    Wires = []
    for ind,Tok in enumerate(Wrds):
        if Tok == 'wire':
            Wires.append(Tok)
        elif Tok == 'reg':
            Wires.append(Tok)
        elif Tok == 'logic':
            Wires.append(Tok)
    


Keywords = '''or default case endcase parameter localparam module posedge negedge endmodule if else int integer input output inout reg wire always always_ff always_comb for begin end assign'''.split()

def externals(Wrds,Prefix):
    
    state = 'idle'
    Inouts = []
    Wires = []
    Modules = []
    for ind,Tok in enumerate(Wrds):
        if Tok == 'module':
            Module = Wrds[ind+1]
            Modules.append(Module)
        if state=='idle':
            if Tok in ['input','output','inout']:
                state = 'workio'
            if Tok in ['integer','wire','reg','logic', 'localparam','parameter']:
                state = 'workwire'
        elif state=='workio':
            if (Tok == ';') or (Tok == '='):
                state = 'idle'
            elif token(Tok): 
                Inouts.append(Tok)
        elif state=='workwire':
            if (Tok == ';') or (Tok == '='):
                state = 'idle'
            elif token(Tok) and ((not Prefix ) or (not Tok.startswith(Prefix))):
                    Wires.append(Tok)
                
    print('obfuscating %d wires' % len(Wires))
    return Modules,Inouts,Wires            
    
Letters = 'qwertyuiopasdfghjklzxcvbnm'+'QWERTYUIOPASDFGHJKLZXCVBNM'+'_' 
Digits = '0123456789'
def token(Txt):
    if Txt[0] not in Letters: return False
    if Txt in Keywords: return False
    for Chr in Txt:
        if Chr not in Letters+Digits:
            return False

    return True



def removeComments0(Text):
    Res = ''
    while '/*' in Text:
        Res = Text[:Text.index('/*')]
        Text = Text[Text.index('/*')+1:]
        Ind = Text.index('*/')
        Text = Text[Ind+2:]

    return Res+Text


def tokenify(Text):
    for Chr in './~`!|:<>+=-()*&^%#@,;{}[]':
        Text = Text.replace(Chr,' %s '%Chr)

    for Duo in ['*  *','!  =','<  =','=  =','<  <','>  >','>  =','&  &','|  |','-  :','+  :','(  *','*  )']:
        Rep = Duo.replace(' ','')
        Text = Text.replace(Duo,Rep)
    Text = Text.replace('` ','`')
    Text = Text.replace('` ','`')
    Wrds = Text.split()
    return Wrds



def removeLineComments(Text2):
    Lines = Text2.split('\n')
    Lines2 = []
    for Line in Lines:
        if '//' in Line:
            Line = Line[:Line.index('//')]
        wrds = Line.split()
        if len(wrds)!=0:
            Lines2.append(Line)
    return '\n'.join(Lines2) 

def cellName(Fname):
    Wrds0 = Fname.split('/')
    Wrds2 = Wrds0[-1].split('.')
    Cell = Wrds2[0]
    Ext  = Wrds2[-1]
    Dir = '/'.join(Wrds0[:-1])
    return Dir,Cell,Ext

if __name__ == '__main__': main()

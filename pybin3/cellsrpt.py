#! /usr/bin/env python3

import os,sys

CELLS = {}
def main():
    global Fout 
    Frpt = sys.argv[1]
    File = open(Frpt)
    readFile(File)
    Fout.write('endmodule\n')
    if Fout: Fout.close()

    Fout = open('nets.v','w')
    for Net in NETS:
        Hi,Lo = NETS[Net]
        if Hi < 0 :
            Fout.write('wire %s;\n' % Net)
        else:
            Fout.write('wire [%d:%d] %s;\n' % (Hi,Lo,Net))
    Fout.close()

def readFile(File):
    global Fout 
    state = 'idle'
    Instance,Type,Dir = '','',''
    Pins = []
    while True:
        line = File.readline()
        if line=='': 
            if Instance != '':
                dumpCell(Instance,Type,Pins)
            return
        wrds = line.split()
        if wrds==[]: 
            pass
        elif ('Connections for cell' in line):
            if Instance != '':
                dumpCell(Instance,Type,Pins)
            Instance = wrds[3][1:-2]
            Pins = []
            Type =  ''
            Dir = ''
        elif wrds[0] == 'Reference:':
            Type = wrds[1]
        elif wrds[0] == 'Input':
            Dir = 'input'
        elif wrds[0] == 'Output':
            Dir = 'output'
        elif (len(wrds) == 2) and (Dir in ['input','output']):
            Pins.append((wrds[0],wrds[1]))
                
Fout = False                
def dumpCell(Instance,Type,Pins):
    global Fout
    if not Fout:
        if len(sys.argv)>2:
            Fname = sys.argv[2]
        else:
            Fname = 'rtla.out.v'
        Fout = open(Fname,'w')
        Fout.write('module x;\n')
    Instance = Instance.replace('[','_')
    Instance = Instance.replace(']','_')
    Instance = Instance.replace('.','_')
    Instance = Instance.replace('/','_')
    Fout.write('%s %s (' % (Type,Instance))
    Pref = ''
    Long = 0
    for Pin,Net in Pins:
        Net = relaxNet(Net)
        Pin = relaxPin(Pin)
        addNet(Net)
        Fout.write(' %s.%s(%s)' % (Pref,Pin,Net))
        Long += len(' %s.%s(%s)' % (Pref,Pin,Net))
        Pref = ','
        if Long>128:
            Fout.write('\n    ')
            Long = 0
    Fout.write(');\n')
    if Type not in CELLS:
        CELLS[Type] = True
        createSkeleton(Type,Pins)

def createSkeleton(Type,Pins):
    if not os.path.exists('skeletons'): os.mkdir('skeletons')
    Fout = open('skeletons/%s.v' % Type,'w')
    Fout.write('module %s (\n' % Type)
    Pins.sort()
    Pref = ' '
    for Pin,_ in Pins:
        Fout.write('    %sinput %s\n' % (Pref,relaxPin(Pin)))
        Pref = ','
    Fout.write(');\nendmodule\n')
    Fout.close()



NETS = {}
def addNet(Net):
    if "'" in Net:
        return
    elif '[' in Net:
        xx = Net.replace('[',' ')
        xx = xx.replace(']',' ')
        ww = xx.split()
        Ind = eval(ww[1])
        if ww[0] in NETS:
            Hi,Lo = NETS[ww[0]]
            NETS[ww[0]] = (max(Ind,Hi),min(Ind,Lo))
        else:
            NETS[ww[0]] = (Ind,Ind)
        return
    NETS[Net] = (-1,0)

def relaxPin(Pin):
    Pin = Pin.replace('[','_')
    Pin = Pin.replace(']','_')
    return Pin

def relaxNet(Net):
    Net = Net.replace('/','_')
    if Net == '*Logic0*': return "1'b0"
    if Net == '*Logic1*': return "1'b1"
    Base,Bus = splitBaseBus(Net)
    Base = Base.replace('[','_')
    Base = Base.replace(']','_')
    Base = Base.replace('.','_')
    return Base+Bus
    
def splitBaseBus(Net):
    if Net[-1] != ']': return Net,''
    ww = Net.split('[')
    if len(ww)==2: return Net,''
    Bus = '['+ww[-1]
    Base = ''.join(ww[:-1])
    return Base,Bus




EXMPL = '''
    10 Connections for cell 'A43281':
    11     Reference:     IND2D4BWP240H8P57PDSVT Library: tsmc_std_7nm
    12
    13     Input Pins     Net -------------- -------------------
    14     A1             N68899
    15     B1             N68898
    16
    17     Output Pins    Net -------------- -------------------
    18     ZN             ctmn_64978
    19
    20
'''

main()

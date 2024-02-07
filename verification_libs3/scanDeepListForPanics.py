#! /usr/bin/python3

import os,sys,string

Path = os.path.expanduser('~/verification_libs')
sys.path.append(Path)

import logs


def main():
    if len(sys.argv)>1:
        Fname = sys.argv[1]
    else:
        Fname = 'deep.list'

    if len(sys.argv)>2:
        Prefix = sys.argv[2]
    else:
        Prefix = 'panic'



    work(Fname,Prefix)

def work(Fname,Prefix):
    if not os.path.exists(Fname):
        print('cannot open "%s" file, if parameter not given, i look for "deep.list" file.'%Fname)
        Fout = open('%ss.py' % Prefix,'w')
        Fout.write(EmptyPanics)
        Fout.close()

        return
    
    File = open(Fname)
    Fout,List = work2(File,Prefix)
    work3(Fout,List)
    File.close()
    Fout.close()

def work3(Fout,List):
    Fout.write('def snapshot():\n')
    for Net in List:
        Str = '    logs.log_info("SNP %x  XXX" % logs.peek("XXX"))\n'
        Str = Str.replace('XXX',Net)
        Fout.write(Str)



def work2(File,Prefix):
    Fout = open('%ss.py' % Prefix,'w')
    Fout.write(HEADER)
    List = []
    while 1:
        line = File.readline()
        if line=='':
            Fout.write(FOOTER)
            return Fout,List
        wrds = line.split()
        if len(wrds)==0:
            pass
        elif (wrds[0]=='son:'):
            pass
        elif (wrds[0]=='module:'):
            Path = wrds[2]
        elif (wrds[0] in ['reg:','net:']):
            Net = wrds[1]
            ww = Net.split('.')
            Panic = ww[-1]
            if Panic.startswith(Prefix) or Panic.endswith(Prefix):
                Fout.write('    %ss += monitorStuff("%s.%s")\n'%(Prefix,Path,Panic))
                List.append("%s.%s" % (Path,Panic))
        elif (wrds[0]=='arr:'):
            pass
        else:
            print('ilia? what is "%s"'%(string.join(wrds,' ')))

HEADER='''
import logs
import veri
def monitorStuff(Net):
    Val = logs.peek(Net)
    if Val!=0:
        logs.log_error('PANIC activated on %s %s'%(Net,veri.peek(Net)))
        return 1
    return 0


def monitorStuffs():
    panics=0
'''
FOOTER='''
    veri.force('tb.Panics',str(panics))
'''

EmptyPanics = '''
def monitorStuffs():
    return

'''




if __name__ == '__main__':
    main()

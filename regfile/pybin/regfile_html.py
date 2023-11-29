
import string,os,sys
import logs


header_string = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>CHIPCHIP regfile </title>
  </head>
  <body>
  <center>
      <h1>CHIPCHIP regfile </h1>
  </center> <left>
      <table border>
'''

table_header_string = '''
      <tr>
        <td align="center"> <font size="7"><b>regfile</b></font></td>
        <td align="center"> <font size="7"><b>addr</b></font></td>
        <td align="center"> <font size="7"><b>name</b></font></td>
        <td align="center"> <font size="7"><b>access</b></font></td>
        <td align="center"> <font size="7"><b>width</b></font></td>
        <td align="center"> <font size="7"><b>reset</b></font></td>
        <td align="center"> <font size="7"><b>external clk</b></font></td>
        <td colspan=8 align="center"> <font size="7"><b>description</b></font></td>
      </tr>
'''
Order = 'access width reset clk description'.split()

tail_string = '</table> </left> </body> </html>\n\n'
def switch_colors():
    global color,othercolor
    x = color
    color=othercolor
    othercolor=x


def getVal(Params,Key):
    if Key in Params:
        Val = Params[Key]
        if type(Val) is int: Val = hex(Val)
        return Val
    return ''

ChipOrder = 'bus reset width  base empty'.split()


def oneLine(Color,LL,ofile,Size=6):
    ofile.write('<tr bgcolor='+Color+'>\n')
    run_on_coding(LL,ofile,Size)
    ofile.write('<td align="center">'+' '+'</td>\n')
    ofile.write('</tr>\n')

FPYHEADER = '''
FIELDS = {}
REGS = {}
DEFAULTS = {}
ADDR_MAP = {}
# = (Width, Offset)


def prepfield(Name, Val):
    if Name in FIELDS:
        (Wid, Off) = FIELDS[Name]
        Mask = (1 << Wid)-1
        Res = (Mask & Val) << Off
        return Res, ~(Mask << Off)
    return 0, 0xffffffff


def setField(Reg, Field, Val):
    if Field == 'default':
        REGS[Reg] = DEFAULTS[Reg]
        return
    Prep, Mask = prepfield(Field, Val)
    if Reg not in REGS:
        REGS[Reg] = DEFAULTS[Reg]
    REGS[Reg] = (REGS[Reg] & Mask) | Prep


'''


def produce_md(Module,Db):
    Chip = Db['chip']
    Items = Db['items']
    Range = Chip.Addr+4
    Fmd = open('%s.md'%(Module),'w')
    Prmx = Db['chip'].Params
    Keys = list(Prmx.keys())
    Keys.sort()
    for Key in Keys:
        if Key != 'names':
            if Key=='empty':
                Fmd.write(' - %s %s\n'%(Key,hex(Prmx[Key])))
            else:
                Fmd.write(' - %s %s\n'%(Key,Prmx[Key]))

    Fmd.write('\n\n')
#    Fmd.write('|kind|access|width|pos|name|reset|addr|desc|\n')
    Fmd.write('|addr|reg   |field|pos|access|width|reset|desc|\n')
    Fmd.write('|----|------|-----|---|------|-----|-----|----|\n')

    for Item in Items:
        if 'reset' not in Item.Params: 
            Reset = ' '
        else:
            Reset = hex(Item.Params['reset'])
        if 'access' not in Item.Params: Item.Params['access']=''
        if 'width' not in Item.Params: Item.Params['width']=0
        if 'description' not in Item.Params: Item.Params['description'] = ''
        Desc = Item.Params['description']
        Desc0 = ' '
        if type(Desc) is str:
            Desc = Desc.replace('.',' ')
            Desc0 = Desc.replace('\\n','<br>')
            Desc0 = Desc0.replace('\n','<br>')
        if Item.Kind=='gap':
            Item.Params['names']=['gap']
        Addr = hex(Item.Addr)
        if Item.Addr<0: Addr = ''
        if 'position' in Item.Params:
            (H,L) = Item.Params['position']
            List = [Item.Kind,Item.Params['access'],Item.Params['width'],'[%s:%s]'%(H,L),Item.Params['names'][0],Reset,Addr,Desc]
            if List[0] == 'reg': List[0] = '**reg**'
            List = [Item.Kind,Item.Params['access'],Item.Params['width'],'[%s:%s]'%(H,L),Item.Params['names'][0],Reset,Addr,Desc0]
            List = [' ',' ',Item.Name,'[%s:%s]'%(H,L),' ',str(Item.Params['width']),Reset,Desc0]
            Fmd.write('|%s|\n'%('|'.join(List)))
        elif Item.Kind in ['ram','array']:
            List = [Addr,Item.Name,'**%s**  depth='%Item.Kind,str(Item.Params['depth']),Item.Params['access'],str(Item.Params['width']),Reset,Desc0]
            Fmd.write('|%s|\n'%('|'.join(List)))
        elif Item.Kind != 'gap':
            List = [Item.Kind,Item.Params['access'],Item.Params['width'],' ',Item.Name,Reset,Addr,Desc0.replace('\n',' ')]
            List = [Addr,Item.Name,' ',' ',Item.Params['access'],str(Item.Params['width']),Reset,Desc0]
            Fmd.write('|%s|\n'%('|'.join(List)))



    Fmd.close()


def produce_html(Module,Db):
    global color,othercolor
#    return                       # use first one.
    Chip = Db['chip']
    Items = Db['items']
    Range = Chip.Addr+4
    OpcodeWidth = 16
    ofile = open('%s_rgf.html'%(Module),'w')
    Fcsv = open('%s.csv'%(Module),'w')
#    Fmd = open('%s.md'%(Module),'w')
    Fcsv.write('kind,access,width,pos,name,reset,addr,desc\n')
#    Fmd.write('# register file "**%s**"\n'%Module)
    Fpy = open('%s.py'%Module,'w')
    Fpy.write(FPYHEADER)
    Prmx = Db['chip'].Params
    Keys = list(Prmx.keys())
    Keys.sort()
#    for Key in Keys:
#        if Key != 'names':
#            if Key=='empty':
#                Fmd.write(' - %s %s\n'%(Key,hex(Prmx[Key])))
#            else:
#                Fmd.write(' - %s %s\n'%(Key,Prmx[Key]))
#
#    Fmd.write('\n\n')
#    Fmd.write('|kind|access|width|pos|name|reset|addr|desc|\n')
#    Fmd.write('|----|------|-----|---|----|-----|----|----|\n')
    Str = header_string.replace('CHIPCHIP',Module)
    ofile.write(Str)
#    ofile.write(table_header_string.replace('OPCODEWIDTH',str(OpcodeWidth)))

    color = '#ffc0ff'
    othercolor = '#ffffc0'
    instruction = 'kind'
    color = '#80ff80'
    othercolor = '#ffffa0'
    color0 = '#c0a0c0'
    color1 = '#a0e0e0'

    Prmx = Db['chip'].Params
    Keys = list(Prmx.keys())
    Keys.sort()
    LL = [Module]
    for Key in Keys:
        if Key != 'names':
            if Key=='empty':
                LL.append('%s=%s'%(Key,hex(Prmx[Key])))
            else:
                LL.append('%s=%s'%(Key,Prmx[Key]))
    Str = '  '.join(LL)
    ofile.write('<font size="5"> %s  </font>\n'%Str)

    ofile.write('<tr bgcolor='+color0+'>\n')

    origarr = 'kind access width pos name  reset  addr expl'.split()
    ofile.write('<tr bgcolor='+color1+'>\n')
    run_on_coding(origarr,ofile)
    ofile.write('</tr>\n')

    Last = False
    for Item in Items:
        if Item.Kind=='gap':
            Item.Params['names']=['gap']
            Item.Name = 'gap'
            if Last:
                Diff = Item.Addr-Last.Addr
                Last.Params['diff']=Diff
            Last = Item
            Item.Params['diff'] = 0
        elif (Item.Addr>0)and Last:
            Diff = Item.Addr-Last.Addr
            Last.Params['diff']=Diff
            Last = False

    for Item in Items:
        if 'reset' not in Item.Params: 
            Reset = ' '
        else:
            Reset = hex(Item.Params['reset'])
        if 'access' not in Item.Params: Item.Params['access']=''
        if 'width' not in Item.Params: Item.Params['width']=0
        if 'description' not in Item.Params: Item.Params['description'] = ''

        Desc0 = ' '
        Desc = Item.Params['description']
        if type(Desc) is str:
            Desc = Desc.replace('.',' ')
            Desc0 = Desc.replace('\\n','<br>')
            Desc0 = Desc0.replace('\n','<br>')
        if Item.Kind=='gap':
            Item.Params['names']=['gap']
        Addr = hex(Item.Addr)
        if Item.Addr<0: Addr = ''
        if 'position' in Item.Params:
            (H,L) = Item.Params['position']
            List = [Item.Kind,Item.Params['access'],Item.Params['width'],'[%s:%s]'%(H,L),Item.Params['names'][0],Reset,Addr,Desc]
            Fcsv.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(List[0],List[1],List[2],List[3],List[4],List[5],List[6],List[7]))
            if List[0] == 'reg': List[0] = '**reg**'
            List = [Item.Kind,Item.Params['access'],Item.Params['width'],'[%s:%s]'%(H,L),Item.Params['names'][0],Reset,Addr,Desc0]
#            Fmd.write('|%s|%s|%s|%s|%s|%s|%s|%s|\n'%(List[0],List[1],List[2],List[3],List[4],List[5],List[6],List[7]))
            if Item.Name!='gap':
                Fpy.write('FIELDS["%s"] = (%s, %s)\n'%(Item.Name,H-L+1,L))
        elif Item.Kind == 'gap':
            List = [Item.Kind,Item.Params['access'],8*Item.Params['diff'],' ',Item.Name,'',Addr,Desc.replace('\n',' ')]
            Fcsv.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(List[0],List[1],List[2],List[3],List[4],List[5],List[6],List[7]))
        else:
            List = [Item.Kind,Item.Params['access'],Item.Params['width'],' ',Item.Name,Reset,Addr,Desc0.replace('\n',' ')]
            Fcsv.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(List[0],List[1],List[2],List[3],List[4],List[5],List[6],List[7]))
            if List[0] == 'reg': List[0] = '**reg**'
#            Fmd.write('|%s|%s|%s|%s|%s|%s|%s|%s|\n'%(List[0],List[1],List[2],List[3],List[4],List[5],List[6],Desc0))
            if 'reg' in List[0]:
                Fpy.write('ADDR_MAP["%s"] = %s\n'%(Item.Name,hex(Item.Addr)))
                Fpy.write('%s = %s\n'%(Item.Name,hex(Item.Addr)))
                if 'reset' not in Item.Params:
                    Reset = 0
                else:
                    Reset = Item.Params['reset']
                Fpy.write('DEFAULTS["%s"] = %s\n'%(Item.Name,hex(Reset)))

        acolor=color
#        ofile.write('<tr bgcolor='+color+'> <td><a target="_blank" href="file:chip_doc.html/#'+Inst+'">'+Inst+'</a></td>\n')
        ofile.write('<tr bgcolor='+color+'>')
        run_on_coding(List,ofile)
        ofile.write('</tr>\n')
        switch_colors()


    ofile.write(tail_string)
    ofile.close()
    Fcsv.close()
#    Fmd.close()
    Fpy.close()

def run_on_coding(wrds,ofile,Size=4):
    for word in wrds:
         ofile.write('<td align="left" > <font size="%s"> '%Size+str(word)+' </font> </td>\n')




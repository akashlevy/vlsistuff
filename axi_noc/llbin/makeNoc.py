#! /usr/bin/env python3
import os,sys,string

def main():
    Fname = sys.argv[1]
    File = open(Fname)
    Long = File.read()
    for X in ['{','}',';','<-']:
        Long = Long.replace(X,' %s ' %X)
    Wrds = Long.split()
    Module = work0(Wrds)
    if not Module: return
    runSm(Wrds)

#    for Item in Items:
#        Obj = Items[Item]
#        print('ITEM',Obj.Kind,Obj.Name,Obj.Inputs,' OUT',Obj.Outputs)

    Slvs,Msts = createCode(Module)
    createInstance(Module,Slvs,Msts)



def work0(Wrds):
    if Wrds[0] != 'digraph': 
        print('error! digraph "%s"' % Wrds[0])
        return 0
    else:
        Wrds.pop(0)

    Module = Wrds.pop(0)
    if (Wrds[0] != '{') or (Wrds[-1] != '}'):
        print('error! missing {}')
        return 0
    else:
        Wrds.pop(0)
        Wrds.pop(-1)
    return Module
   
def runSm(Wrds):
    state = 'idle'
    for ind,Wrd in enumerate(Wrds):
#        print(state,ind,Wrd)
        if (state == 'idle'):
            Src = Wrd
            state = '->'
        elif (state == '->'):
            if Wrd != '->':
                print('error! exp=-> act=%s at %d' % (Wrd,ind))
                return
            state = 'destination'
        elif (state == 'destination'):
            Dst = Wrd
            state = ';'
            record(Src,Dst)
        elif (state == ';'):
            if Wrd != ';':
                print('error! exp=; act=%s at %d' % (Wrd,ind))
                return
            state = 'idle'
Masters,Slaves,Clocks = {},{},{}
class itemClass:
    def __init__(self,Kind,Name):
        self.Kind = Kind
        self.Name = Name
        self.Inputs = []
        self.Outputs = []

Items = {}

def record(Src,Dst):
    if Src.startswith('split'):
        if Src not in Items:
            Items[Src] = itemClass('splitter',Src)

        if Dst.startswith('slv'):
            Slaves[Dst] = Src
            Items[Src].Outputs.append(Dst)
        elif Dst.startswith('merge'):
            Items[Src].Outputs.append(Dst)
            if Dst not in Items:
                Items[Dst] = itemClass('merger',Dst)
            Items[Dst].Inputs.append(Src)
        elif Dst.startswith('split'):
            Items[Src].Outputs.append(Dst)
            if Dst not in Items:
                Items[Dst] = itemClass('splitter',Dst)
            Items[Dst].Inputs.append(Src)
        elif Dst.startswith('clock'):
            Items[Src].Outputs.append(Dst)
            if Dst not in Items:
                Items[Dst] = itemClass('clocker',Dst)
            Items[Dst].Inputs.append(Src)
        elif Dst.startswith('slice'):
            Items[Src].Outputs.append(Dst)
            if Dst not in Items:
                Items[Dst] = itemClass('slicer',Dst)
            Items[Dst].Inputs.append(Src)
        else:
            print('error! record %s -> %s' % ( Src,Dst))

    elif Src.startswith('clock'):
        Clocks[Src] = True
        if Src not in Items:
            Items[Src] = itemClass('clocker',Src)
        if Dst.startswith('slv'):
            Slaves[Dst] = Src
            Items[Src].Outputs.append(Dst)
        elif Dst.startswith('split'):
            Items[Src].Outputs.append(Dst)
            if Dst not in Items:
                Items[Dst] = itemClass('splitter',Dst)
            Items[Dst].Inputs.append(Src)
        elif Dst.startswith('merge'):
            Items[Src].Outputs.append(Dst)
            if Dst not in Items:
                Items[Dst] = itemClass('merger',Dst)
            Items[Dst].Inputs.append(Src)
        else:
            print('error! record %s -> %s' % ( Src,Dst))
    elif Src.startswith('slice'):
        Clocks[Src] = True
        if Src not in Items:
            Items[Src] = itemClass('slicer',Src)
        if Dst.startswith('slv'):
            Slaves[Dst] = Src
            Items[Src].Outputs.append(Dst)
        elif Dst.startswith('split'):
            Items[Src].Outputs.append(Dst)
            if Dst not in Items:
                Items[Dst] = itemClass('splitter',Dst)
            Items[Dst].Inputs.append(Src)
        elif Dst.startswith('merge'):
            Items[Src].Outputs.append(Dst)
            if Dst not in Items:
                Items[Dst] = itemClass('merger',Dst)
            Items[Dst].Inputs.append(Src)
        else:
            print('error! record %s -> %s' % ( Src,Dst))

    elif Src.startswith('mst'):
        Masters[Src] = True
        if Dst.startswith('split'):
            if Dst not in Items:
                Items[Dst] = itemClass('splitter',Dst)
            Items[Dst].Inputs.append(Src)
        elif Dst.startswith('merge'):
            if Dst not in Items:
                Items[Dst] = itemClass('merger',Dst)
            Items[Dst].Inputs.append(Src)
        else:
            print('error! record %s -> %s' % ( Src,Dst))
    elif Src.startswith('merge'):
        if Src not in Items:
            Items[Src] = itemClass('merger',Src)
        if Dst.startswith('slv'):
            Slaves[Dst] = Src
            Items[Src].Outputs.append(Dst)
        elif Dst.startswith('split'):
            Items[Src].Outputs.append(Dst)
            if Dst not in Items:
                Items[Dst] = itemClass('splitter',Dst)
            Items[Dst].Inputs.append(Src)
        elif Dst.startswith('merge'):
            Items[Src].Outputs.append(Dst)
            if Dst not in Items:
                Items[Dst] = itemClass('merger',Dst)
            Items[Dst].Inputs.append(Src)
        else:
            print('error! record %s -> %s' % ( Src,Dst))
    else:
        print('error! record %s -> %s' % ( Src,Dst))

def createCode(Module):
    Fout = open('%s_noc.v' % Module,'w')
    Slvs = list(Slaves.keys())
    Slvs.sort()
    Header = HEADER.replace('MODULE',Module)
    Fout.write(Header)
    print('SLAVES',Slvs)
    for Slv in Slvs:
        Slvport = SLAVEPORT.replace('PRT',Slv)
        Fout.write(Slvport)
    Msts = list(Masters.keys())
    Msts.sort()
    print('MASTERS',Msts)
    for Mst in Msts: 
        Mstport = MASTERPORT.replace('PRT',Mst)
        Fout.write(Mstport)
    for Clk in Clocks.keys():
        Fout.write('    ,input %s\n' % Clk)

    Fout.write(');\n')
    for Item in Items:
        Obj = Items[Item]
        if Obj.Kind == 'splitter':
            Str = SPLITTER.replace('NAME',Obj.Name)
            if len(Obj.Inputs)!= 1:
                print('Error! splitter %s must have just one input "%s"' % (Obj.Name,Obj.Inputs))
                sys.exit()
            if (len(Obj.Outputs)>4)or(len(Obj.Outputs)<2):
                print('Error! splitter %s must have outputs 2,3 or 4 "%s"' % (Obj.Name,Obj.Outputs))
                sys.exit()
            if Obj.Inputs[0].startswith('mst'):
                Str = Str.replace('IN',Obj.Inputs[0])
            else:
                Str = Str.replace('IN',Obj.Inputs[0]+'_'+Obj.Name)
                defineWires(Fout,Obj.Inputs[0]+'_'+Obj.Name)
            for ind,Dst in enumerate(Obj.Outputs):
                BEF = ['AA','BB','CC','DD'][ind]
                if Dst.startswith('slv'):
                    Str = Str.replace(BEF,Dst)
                else:
                    Str = Str.replace(BEF,Obj.Name+'_'+Dst)
                    defineWires(Fout,Obj.Name+'_'+Dst)
            Fout.write(Str)
        elif Obj.Kind == 'merger':
            Str = MERGER.replace('NAME',Obj.Name)
            Dst = Obj.Outputs[0]
            if Obj.Outputs == []:
                print('Error! merger %s has no output' % (Obj.Name))
                sys.exit()
            elif len(Obj.Outputs)!=1:
                print('Error! merger %s can have only  one output' % (Obj.Name))
                sys.exit()
            elif Dst.startswith('slv'):
                Str = Str.replace('OUT',Dst)
            else:
                Str = Str.replace('OUT',Obj.Name+'_'+Obj.Outputs[0])
                defineWires(Fout,Obj.Name+'_'+Obj.Outputs[0])
            for ind,Src in enumerate(Obj.Inputs):
                BEF = ['AA','BB','CC','DD'][ind]
                if Src.startswith('mst'):
                    Str = Str.replace(BEF,Src)
                else:
                    Str = Str.replace(BEF,Src+'_'+Obj.Name)
                    defineWires(Fout,Src+'_'+Obj.Name)
            Fout.write(Str)
        elif Obj.Kind == 'clocker':
            Str = CLOCKER.replace('NAME',Obj.Name)
            Str = Str.replace('INCLOCK','clk')      # temporary solution
            Str = Str.replace('OUCLOCK',Obj.Name)   # temporary solution
            Dst = Obj.Outputs[0]
            Src = Obj.Inputs[0]
            if Obj.Outputs == []:
                print('Error! clocker %s has no output' % (Obj.Name))
                sys.exit()
            elif len(Obj.Outputs)!=1:
                print('Error! clocker %s can have only  one output' % (Obj.Name))
                sys.exit()
            elif len(Obj.Inputs)!=1:
                print('Error! clocker %s can have only  one input' % (Obj.Name))
                sys.exit()
            elif Dst.startswith('slv'):
                Str = Str.replace('BB',Dst)
            else:
                Str = Str.replace('BB',Obj.Name+'_'+Obj.Outputs[0])
                defineWires(Fout,Obj.Name+'_'+Obj.Outputs[0])
            if Src.startswith('mst'):
                Str = Str.replace('AA',Src)
            else:
                Str = Str.replace('AA',Src+'_'+Obj.Name)
                defineWires(Fout,Src+'_'+Obj.Name)
            Fout.write(Str)
        elif Obj.Kind == 'slicer':
            Str = SLICER.replace('NAME',Obj.Name)
            Str = Str.replace('INCLOCK','clk')      # temporary solution
            Dst = Obj.Outputs[0]
            Src = Obj.Inputs[0]
            if Obj.Outputs == []:
                print('Error! slicer %s has no output' % (Obj.Name))
                sys.exit()
            elif len(Obj.Outputs)!=1:
                print('Error! slicer %s can have only  one output' % (Obj.Name))
                sys.exit()
            elif len(Obj.Inputs)!=1:
                print('Error! slicer %s can have only  one input' % (Obj.Name))
                sys.exit()
            elif Dst.startswith('slv'):
                Str = Str.replace('BB',Dst)
            else:
                Str = Str.replace('BB',Obj.Name+'_'+Obj.Outputs[0])
                defineWires(Fout,Obj.Name+'_'+Obj.Outputs[0])
            if Src.startswith('mst'):
                Str = Str.replace('AA',Src)
            else:
                Str = Str.replace('AA',Src+'_'+Obj.Name)
                defineWires(Fout,Src+'_'+Obj.Name)
            Fout.write(Str)
        else:
            print('ERROR! object %s of %s kind is not trreated' % (Obj.Name,Obj.Kind))


    Fout.write('endmodule\n')
    Fout.close()
    return Slvs,Msts




FOOTER = '''

reg [1023:0] testname;
initial begin
   if ($value$plusargs("LOG=%s",testname)) begin 
        $python("pymonname()",testname);
    end  


    if ($value$plusargs("SEQ=%s",testname)) begin 
         $display(" Running SEQ= %s.",testname); 
    end else begin
        testname = 0; 
        $display(" default test");
    end  
    #10; 
    if (testname!=0) $python("sequence()",testname);
end 
endmodule

'''



INSTHEADER = '''
`timescale 1ns/1ps
module tb;
parameter IDWID=4; parameter DWID=64; parameter EXTRAS=8; parameter WSTRB=DWID/8;

integer    cycles;   initial cycles=0;
integer    errors;   initial errors=0;
integer    wrongs;   initial wrongs=0;
integer    Panics;   initial Panics=0;
integer    corrects; initial corrects=0;
reg [31:0] marker;   initial marker=0;
reg [31:0] marker0;   initial marker0=0;
reg [31:0] marker1;   initial marker1=0;
reg [31:0] marker2;   initial marker2=0;
reg [31:0] marker3;   initial marker3=0;
reg [31:0] Index;   initial Index=0;
integer    rqueuelen;   initial rqueuelen=0;
reg [31:0] seqptr;   initial seqptr=0;
reg [31:0] slv0_marker3;   initial slv0_marker3=0;
reg [31:0] slv1_marker3;   initial slv1_marker3=0;
reg [31:0] slv2_marker3;   initial slv2_marker3=0;
reg [31:0] slv3_marker3;   initial slv3_marker3=0;



reg clk; reg rst_n;
integer clk_HALFPERIOD = 100;
always begin
    clk = 0;
    #(clk_HALFPERIOD);
    clk = 1;
    #3;
    $python("negedge()");
    #3;
    $python("auxs()");
    #(clk_HALFPERIOD-6);
end
initial begin
    $dumpvars(0,tb);
    rst_n = 0;
    #100;
    rst_n = 1;
end
'''
MORE_CLOCKS = '''

integer CLOCK_HALFPERIOD = 100;
always begin
    CLOCK = 0;
    #(CLOCK_HALFPERIOD);
    CLOCK = 1;
    #(3);
    $python("CLOCK_negedge()");
    #(4);
    $python("CLOCK_auxs()");
    #(CLOCK_HALFPERIOD-7);
end
'''


def createInstance(Module,Slvs,Msts):
    Fout = open('%s_tb.v' % Module,'w')
    Fout.write(INSTHEADER.replace('MODULE',Module))
    for Clk in Clocks:
        Fout.write('\n\nreg %s; initial %s = 0;\n' % (Clk,Clk))
        Str = MORE_CLOCKS.replace('CLOCK',Clk)
        Fout.write(Str)
    for Slv in Slvs:
        Str = REGINST.replace('PRT',Slv) 
        Fout.write(Str)
        Str = WIREINST.replace('PRT',Slv) 
        Str = Str.replace('MOU','wire')
        Str = Str.replace('MIN','reg')
        Fout.write(Str)
        Fout.write('initial %s_arready = 0;\n' % Slv)
        Fout.write('initial %s_awready = 0;\n' % Slv)
        Fout.write('initial %s_rvalid = 0;\n' % Slv)
        Fout.write('initial %s_bvalid = 0;\n' % Slv)
    for Mst in Msts:
        Str = REGINST.replace('PRT',Mst) 
        Fout.write(Str)
        Str = WIREINST.replace('PRT',Mst) 
        Str = Str.replace('MOU','reg')
        Str = Str.replace('MIN','wire')
        Fout.write(Str)
        Fout.write('initial %s_bready = 0;\n' % Mst)
        Fout.write('initial %s_wvalid = 0;\n' % Mst)
        Fout.write('initial %s_arvalid = 0;\n' % Mst)
        Fout.write('initial %s_awvalid = 0;\n' % Mst)
        Fout.write('initial %s_rready = 0;\n' % Mst)

    Fout.write('%s dut ( .clk(clk),.rst_n(rst_n)\n' % (Module))
    for Clk in Clocks:
        Fout.write('   ,.%s(%s)\n' % (Clk,Clk))
    for Slv in Slvs:
        Str = SLVIF.replace('SLV',Slv)
        Fout.write(Str)
    for Mst in Msts:
        Str = MSTIF.replace('MST',Mst)
        Fout.write(Str)
    Fout.write(');\n')
    Fout.write(FOOTER)
    Fout.close()


MSTIF = '''
    ,.MST_araddr(MST_araddr[31:0])
    ,.MST_arburst(MST_arburst[1:0])
    ,.MST_arextras(MST_arextras[(EXTRAS - 1):0])
    ,.MST_arid(MST_arid)
    ,.MST_arlen(MST_arlen)
    ,.MST_arsize(MST_arsize)
    ,.MST_arready(MST_arready)
    ,.MST_arvalid(MST_arvalid)
    ,.MST_awaddr(MST_awaddr[31:0])
    ,.MST_awburst(MST_awburst[1:0])
    ,.MST_awextras(MST_awextras[(EXTRAS - 1):0])
    ,.MST_awid(MST_awid[(IDWID - 1):0])
    ,.MST_awlen(MST_awlen)
    ,.MST_awsize(MST_awsize)
    ,.MST_awready(MST_awready)
    ,.MST_awvalid(MST_awvalid)
    ,.MST_bid(MST_bid[(IDWID - 1):0])
    ,.MST_bready(MST_bready)
    ,.MST_bresp(MST_bresp[1:0])
    ,.MST_bvalid(MST_bvalid)
    ,.MST_rdata(MST_rdata[(DWID - 1):0])
    ,.MST_rid(MST_rid[(IDWID - 1):0])
    ,.MST_rlast(MST_rlast)
    ,.MST_rready(MST_rready)
    ,.MST_rresp(MST_rresp[1:0])
    ,.MST_rvalid(MST_rvalid)
    ,.MST_wdata(MST_wdata[(DWID - 1):0])
    ,.MST_wlast(MST_wlast)
    ,.MST_wready(MST_wready)
    ,.MST_wstrb(MST_wstrb[(WSTRB - 1):0])
    ,.MST_wvalid(MST_wvalid)
'''
SLVIF = '''
    ,.SLV_araddr(SLV_araddr[31:0])
    ,.SLV_arburst(SLV_arburst[1:0])
    ,.SLV_arextras(SLV_arextras[(EXTRAS - 1):0])
    ,.SLV_arid(SLV_arid)
    ,.SLV_arlen(SLV_arlen)
    ,.SLV_arsize(SLV_arsize)
    ,.SLV_arready(SLV_arready)
    ,.SLV_arvalid(SLV_arvalid)
    ,.SLV_awaddr(SLV_awaddr[31:0])
    ,.SLV_awburst(SLV_awburst[1:0])
    ,.SLV_awextras(SLV_awextras[(EXTRAS - 1):0])
    ,.SLV_awid(SLV_awid[(IDWID - 1):0])
    ,.SLV_awlen(SLV_awlen)
    ,.SLV_awsize(SLV_awsize)
    ,.SLV_awready(SLV_awready)
    ,.SLV_awvalid(SLV_awvalid)
    ,.SLV_bid(SLV_bid[(IDWID - 1):0])
    ,.SLV_bready(SLV_bready)
    ,.SLV_bresp(SLV_bresp[1:0])
    ,.SLV_bvalid(SLV_bvalid)
    ,.SLV_rdata(SLV_rdata[(DWID - 1):0])
    ,.SLV_rid(SLV_rid[(IDWID - 1):0])
    ,.SLV_rlast(SLV_rlast)
    ,.SLV_rready(SLV_rready)
    ,.SLV_rresp(SLV_rresp[1:0])
    ,.SLV_rvalid(SLV_rvalid)
    ,.SLV_wdata(SLV_wdata[(DWID - 1):0])
    ,.SLV_wlast(SLV_wlast)
    ,.SLV_wready(SLV_wready)
    ,.SLV_wstrb(SLV_wstrb[(WSTRB - 1):0])
    ,.SLV_wvalid(SLV_wvalid)

'''

REGINST = '''
// reg  [2:0] PRT_awsize ; initial PRT_awsize = 0;
// reg  [2:0] PRT_arsize ; initial PRT_arsize = 0;
'''
WIREINST = '''
MOU  [IDWID-1:0] PRT_arid ;
MOU  [31:0] PRT_araddr ;
MOU  [7:0] PRT_arlen ;
MOU  [2:0] PRT_arsize ;
MOU  [EXTRAS-1:0] PRT_arextras ;
MOU  [1:0] PRT_arburst ;
MOU  PRT_arvalid ;
MIN  PRT_arready ;
MIN  [IDWID-1:0] PRT_rid ;
MIN  [DWID-1:0] PRT_rdata ;
MIN  [1:0] PRT_rresp ;
MIN  PRT_rlast ;
MIN  PRT_rvalid ;
MOU  PRT_rready ;

MOU  [IDWID-1:0] PRT_awid ;
MOU  [31:0] PRT_awaddr ;
MOU  [7:0] PRT_awlen ;
MOU  [2:0] PRT_awsize ;
MOU  [EXTRAS-1:0] PRT_awextras ;
MOU  [1:0] PRT_awburst ;
MOU  PRT_awvalid ;
MIN  PRT_awready ;
MOU  [DWID-1:0] PRT_wdata ;
MOU  [WSTRB-1:0] PRT_wstrb ;
MOU  PRT_wlast ;
MOU  PRT_wvalid ;
MIN  PRT_wready ;
MIN  [IDWID-1:0] PRT_bid ;
MIN  [1:0] PRT_bresp ;
MIN  PRT_bvalid ;
MOU  PRT_bready ;

'''


PREFS = []
def defineWires(Fout,Pref):
    if Pref in PREFS: return
    Str = WIREPORT.replace('PRT',Pref)
    Fout.write(Str)
    PREFS.append(Pref)



HEADER = '''
    module MODULE #(parameter IDWID=4, parameter DWID=64, parameter EXTRAS=8, parameter WSTRB=DWID/8) ( input clk, input rst_n
'''

SLAVEPORT = '''
    ,output [IDWID-1:0] PRT_arid
    ,output [31:0] PRT_araddr
    ,output [7:0] PRT_arlen
    ,output [2:0] PRT_arsize
    ,output [EXTRAS-1:0] PRT_arextras
    ,output [1:0] PRT_arburst
    ,output PRT_arvalid
    ,input PRT_arready
    ,input [IDWID-1:0] PRT_rid
    ,input [DWID-1:0] PRT_rdata
    ,input [1:0] PRT_rresp
    ,input PRT_rlast
    ,input PRT_rvalid
    ,output PRT_rready

    ,output [IDWID-1:0] PRT_awid
    ,output [31:0] PRT_awaddr
    ,output [7:0] PRT_awlen
    ,output [2:0] PRT_awsize
    ,output [EXTRAS-1:0] PRT_awextras
    ,output [1:0] PRT_awburst
    ,output PRT_awvalid
    ,input PRT_awready
    ,output [DWID-1:0] PRT_wdata
    ,output [WSTRB-1:0] PRT_wstrb
    ,output PRT_wlast
    ,output PRT_wvalid
    ,input PRT_wready
    ,input [IDWID-1:0] PRT_bid
    ,input [1:0] PRT_bresp
    ,input PRT_bvalid
    ,output PRT_bready
'''

MASTERPORT = '''
    ,input [IDWID-1:0] PRT_arid
    ,input [31:0] PRT_araddr
    ,input [7:0] PRT_arlen
    ,input [2:0] PRT_arsize
    ,input [EXTRAS-1:0] PRT_arextras
    ,input [1:0] PRT_arburst
    ,input PRT_arvalid
    ,output PRT_arready
    ,output [IDWID-1:0] PRT_rid
    ,output [DWID-1:0] PRT_rdata
    ,output [1:0] PRT_rresp
    ,output PRT_rlast
    ,output PRT_rvalid
    ,input PRT_rready

    ,input [IDWID-1:0] PRT_awid
    ,input [31:0] PRT_awaddr
    ,input [7:0] PRT_awlen
    ,input [2:0] PRT_awsize
    ,input [EXTRAS-1:0] PRT_awextras
    ,input [1:0] PRT_awburst
    ,input PRT_awvalid
    ,output PRT_awready
    ,input [DWID-1:0] PRT_wdata
    ,input [WSTRB-1:0] PRT_wstrb
    ,input PRT_wlast
    ,input PRT_wvalid
    ,output PRT_wready
    ,output [IDWID-1:0] PRT_bid
    ,output [1:0] PRT_bresp
    ,output PRT_bvalid
    ,input PRT_bready
'''

WIREPORT = '''
wire [IDWID-1:0] PRT_arid ;
wire [31:0] PRT_araddr ;
wire [7:0] PRT_arlen ;
wire [2:0] PRT_arsize ;
wire [EXTRAS-1:0] PRT_arextras ;
wire [1:0] PRT_arburst ;
wire PRT_arvalid ;
wire PRT_arready ;
wire [IDWID-1:0] PRT_rid ;
wire [DWID-1:0] PRT_rdata ;
wire [1:0] PRT_rresp ;
wire PRT_rlast ;
wire PRT_rvalid ;
wire PRT_rready ;

wire [IDWID-1:0] PRT_awid ;
wire [31:0] PRT_awaddr ;
wire [7:0] PRT_awlen ;
wire [2:0] PRT_awsize ;
wire [EXTRAS-1:0] PRT_awextras ;
wire [1:0] PRT_awburst ;
wire PRT_awvalid ;
wire PRT_awready ;
wire [DWID-1:0] PRT_wdata ;
wire [WSTRB-1:0] PRT_wstrb ;
wire PRT_wlast ;
wire PRT_wvalid ;
wire PRT_wready ;
wire [IDWID-1:0] PRT_bid ;
wire [1:0] PRT_bresp ;
wire PRT_bvalid ;
wire PRT_bready ;

'''



SPLITTER = '''
axi_4_splitter NAME (
     .clk(clk) ,.rst_n(rst_n)

    ,.araddr(IN_araddr[31:0])
    ,.arburst(IN_arburst[1:0])
    ,.arextras(IN_arextras[(EXTRAS - 1):0])
    ,.arid(IN_arid)
    ,.arlen(IN_arlen)
    ,.arsize(IN_arsize)
    ,.arready(IN_arready)
    ,.arvalid(IN_arvalid)
    ,.awaddr(IN_awaddr[31:0])
    ,.awburst(IN_awburst[1:0])
    ,.awextras(IN_awextras[(EXTRAS - 1):0])
    ,.awid(IN_awid)
    ,.awlen(IN_awlen)
    ,.awsize(IN_awsize)
    ,.awready(IN_awready)
    ,.awvalid(IN_awvalid)
    ,.bid(IN_bid[(IDWID - 1):0])
    ,.bready(IN_bready)
    ,.bresp(IN_bresp[1:0])
    ,.bvalid(IN_bvalid)
    ,.rdata(IN_rdata[(DWID - 1):0])
    ,.rid(IN_rid[(IDWID - 1):0])
    ,.rlast(IN_rlast)
    ,.rready(IN_rready)
    ,.rresp(IN_rresp[1:0])
    ,.rvalid(IN_rvalid)
    ,.wdata(IN_wdata[(DWID - 1):0])
    ,.wlast(IN_wlast)
    ,.wready(IN_wready)
    ,.wstrb(IN_wstrb[(WSTRB - 1):0])
    ,.wvalid(IN_wvalid)

    ,.a_araddr(AA_araddr[31:0])
    ,.a_arburst(AA_arburst[1:0])
    ,.a_arextras(AA_arextras[(EXTRAS - 1):0])
    ,.a_arid(AA_arid)
    ,.a_arlen(AA_arlen)
    ,.a_arsize(AA_arsize)
    ,.a_arready(AA_arready)
    ,.a_arvalid(AA_arvalid)
    ,.a_awaddr(AA_awaddr[31:0])
    ,.a_awburst(AA_awburst[1:0])
    ,.a_awextras(AA_awextras[(EXTRAS - 1):0])
    ,.a_awid(AA_awid)
    ,.a_awlen(AA_awlen)
    ,.a_awsize(AA_awsize)
    ,.a_awready(AA_awready)
    ,.a_awvalid(AA_awvalid)
    ,.a_bid(AA_bid[(IDWID - 1):0])
    ,.a_bready(AA_bready)
    ,.a_bresp(AA_bresp[1:0])
    ,.a_bvalid(AA_bvalid)
    ,.a_rdata(AA_rdata[(DWID - 1):0])
    ,.a_rid(AA_rid[(IDWID - 1):0])
    ,.a_rlast(AA_rlast)
    ,.a_rready(AA_rready)
    ,.a_rresp(AA_rresp[1:0])
    ,.a_rvalid(AA_rvalid)
    ,.a_wdata(AA_wdata[(DWID - 1):0])
    ,.a_wlast(AA_wlast)
    ,.a_wready(AA_wready)
    ,.a_wstrb(AA_wstrb[(WSTRB - 1):0])
    ,.a_wvalid(AA_wvalid)
    ,.b_araddr(BB_araddr[31:0])
    ,.b_arburst(BB_arburst[1:0])
    ,.b_arextras(BB_arextras[(EXTRAS - 1):0])
    ,.b_arid(BB_arid)
    ,.b_arlen(BB_arlen)
    ,.b_arsize(BB_arsize)
    ,.b_arready(BB_arready)
    ,.b_arvalid(BB_arvalid)
    ,.b_awaddr(BB_awaddr[31:0])
    ,.b_awburst(BB_awburst[1:0])
    ,.b_awextras(BB_awextras[(EXTRAS - 1):0])
    ,.b_awid(BB_awid)
    ,.b_awlen(BB_awlen)
    ,.b_awsize(BB_awsize)
    ,.b_awready(BB_awready)
    ,.b_awvalid(BB_awvalid)
    ,.b_bid(BB_bid[(IDWID - 1):0])
    ,.b_bready(BB_bready)
    ,.b_bresp(BB_bresp[1:0])
    ,.b_bvalid(BB_bvalid)
    ,.b_rdata(BB_rdata[(DWID - 1):0])
    ,.b_rid(BB_rid[(IDWID - 1):0])
    ,.b_rlast(BB_rlast)
    ,.b_rready(BB_rready)
    ,.b_rresp(BB_rresp[1:0])
    ,.b_rvalid(BB_rvalid)
    ,.b_wdata(BB_wdata[(DWID - 1):0])
    ,.b_wlast(BB_wlast)
    ,.b_wready(BB_wready)
    ,.b_wstrb(BB_wstrb[(WSTRB - 1):0])
    ,.b_wvalid(BB_wvalid)
    ,.c_araddr(CC_araddr[31:0])
    ,.c_arburst(CC_arburst[1:0])
    ,.c_arextras(CC_arextras[(EXTRAS - 1):0])
    ,.c_arid(CC_arid)
    ,.c_arlen(CC_arlen)
    ,.c_arsize(CC_arsize)
    ,.c_arready(CC_arready)
    ,.c_arvalid(CC_arvalid)
    ,.c_awaddr(CC_awaddr[31:0])
    ,.c_awburst(CC_awburst[1:0])
    ,.c_awextras(CC_awextras[(EXTRAS - 1):0])
    ,.c_awid(CC_awid)
    ,.c_awlen(CC_awlen)
    ,.c_awsize(CC_awsize)
    ,.c_awready(CC_awready)
    ,.c_awvalid(CC_awvalid)
    ,.c_bid(CC_bid[(IDWID - 1):0])
    ,.c_bready(CC_bready)
    ,.c_bresp(CC_bresp[1:0])
    ,.c_bvalid(CC_bvalid)
    ,.c_rdata(CC_rdata[(DWID - 1):0])
    ,.c_rid(CC_rid[(IDWID - 1):0])
    ,.c_rlast(CC_rlast)
    ,.c_rready(CC_rready)
    ,.c_rresp(CC_rresp[1:0])
    ,.c_rvalid(CC_rvalid)
    ,.c_wdata(CC_wdata[(DWID - 1):0])
    ,.c_wlast(CC_wlast)
    ,.c_wready(CC_wready)
    ,.c_wstrb(CC_wstrb[(WSTRB - 1):0])
    ,.c_wvalid(CC_wvalid)
    ,.d_araddr(DD_araddr[31:0])
    ,.d_arburst(DD_arburst[1:0])
    ,.d_arextras(DD_arextras[(EXTRAS - 1):0])
    ,.d_arid(DD_arid[(IDWID - 1):0])
    ,.d_arlen(DD_arlen[7:0])
    ,.d_arsize(DD_arsize)
    ,.d_arready(DD_arready)
    ,.d_arvalid(DD_arvalid)
    ,.d_awaddr(DD_awaddr[31:0])
    ,.d_awburst(DD_awburst[1:0])
    ,.d_awextras(DD_awextras[(EXTRAS - 1):0])
    ,.d_awid(DD_awid)
    ,.d_awlen(DD_awlen)
    ,.d_awsize(DD_awsize)
    ,.d_awready(DD_awready)
    ,.d_awvalid(DD_awvalid)
    ,.d_bid(DD_bid[(IDWID - 1):0])
    ,.d_bready(DD_bready)
    ,.d_bresp(DD_bresp[1:0])
    ,.d_bvalid(DD_bvalid)
    ,.d_rdata(DD_rdata[(DWID - 1):0])
    ,.d_rid(DD_rid[(IDWID - 1):0])
    ,.d_rlast(DD_rlast)
    ,.d_rready(DD_rready)
    ,.d_rresp(DD_rresp[1:0])
    ,.d_rvalid(DD_rvalid)
    ,.d_wdata(DD_wdata[(DWID - 1):0])
    ,.d_wlast(DD_wlast)
    ,.d_wready(DD_wready)
    ,.d_wstrb(DD_wstrb[(WSTRB - 1):0])
    ,.d_wvalid(DD_wvalid)

);
'''

MERGER = '''
axi_4_merger NAME (
     .clk(clk),.rst_n(rst_n)
    ,.araddr(OUT_araddr[31:0])
    ,.arburst(OUT_arburst[1:0])
    ,.arextras(OUT_arextras[(EXTRAS - 1):0])
    ,.arid(OUT_arid)
    ,.arlen(OUT_arlen)
    ,.arsize(OUT_arsize)
    ,.arready(OUT_arready)
    ,.arvalid(OUT_arvalid)
    ,.awaddr(OUT_awaddr[31:0])
    ,.awburst(OUT_awburst[1:0])
    ,.awextras(OUT_awextras[(EXTRAS - 1):0])
    ,.awid(OUT_awid)
    ,.awlen(OUT_awlen)
    ,.awsize(OUT_awsize)
    ,.awready(OUT_awready)
    ,.awvalid(OUT_awvalid)
    ,.bid(OUT_bid[(IDWID - 1):0])
    ,.bready(OUT_bready)
    ,.bresp(OUT_bresp[1:0])
    ,.bvalid(OUT_bvalid)
    ,.rid(OUT_rid[(IDWID - 1):0])
    ,.rlast(OUT_rlast)
    ,.rready(OUT_rready)
    ,.rresp(OUT_rresp[1:0])
    ,.rvalid(OUT_rvalid)
    ,.rdata(OUT_rdata[(DWID - 1):0])
    ,.wdata(OUT_wdata[(DWID - 1):0])
    ,.wlast(OUT_wlast)
    ,.wready(OUT_wready)
    ,.wstrb(OUT_wstrb[(WSTRB - 1):0])
    ,.wvalid(OUT_wvalid)


    ,.a_araddr(AA_araddr[31:0])
    ,.a_arburst(AA_arburst[1:0])
    ,.a_arextras(AA_arextras[(EXTRAS - 1):0])
    ,.a_arid(AA_arid)
    ,.a_arlen(AA_arlen)
    ,.a_arsize(AA_arsize)
    ,.a_arready(AA_arready)
    ,.a_arvalid(AA_arvalid)
    ,.a_awaddr(AA_awaddr[31:0])
    ,.a_awburst(AA_awburst[1:0])
    ,.a_awextras(AA_awextras[(EXTRAS - 1):0])
    ,.a_awid(AA_awid)
    ,.a_awlen(AA_awlen)
    ,.a_awsize(AA_awsize)
    ,.a_awready(AA_awready)
    ,.a_awvalid(AA_awvalid)
    ,.a_bid(AA_bid[(IDWID - 1):0])
    ,.a_bready(AA_bready)
    ,.a_bresp(AA_bresp[1:0])
    ,.a_bvalid(AA_bvalid)
    ,.a_rdata(AA_rdata[(DWID - 1):0])
    ,.a_rid(AA_rid[(IDWID - 1):0])
    ,.a_rlast(AA_rlast)
    ,.a_rready(AA_rready)
    ,.a_rresp(AA_rresp[1:0])
    ,.a_rvalid(AA_rvalid)
    ,.a_wdata(AA_wdata[(DWID - 1):0])
    ,.a_wlast(AA_wlast)
    ,.a_wready(AA_wready)
    ,.a_wstrb(AA_wstrb[(WSTRB - 1):0])
    ,.a_wvalid(AA_wvalid)

    ,.b_araddr(BB_araddr[31:0])
    ,.b_arburst(BB_arburst[1:0])
    ,.b_arextras(BB_arextras[(EXTRAS - 1):0])
    ,.b_arid(BB_arid)
    ,.b_arlen(BB_arlen)
    ,.b_arsize(BB_arsize)
    ,.b_arready(BB_arready)
    ,.b_arvalid(BB_arvalid)
    ,.b_awaddr(BB_awaddr[31:0])
    ,.b_awburst(BB_awburst[1:0])
    ,.b_awextras(BB_awextras[(EXTRAS - 1):0])
    ,.b_awid(BB_awid)
    ,.b_awlen(BB_awlen)
    ,.b_awsize(BB_awsize)
    ,.b_awready(BB_awready)
    ,.b_awvalid(BB_awvalid)
    ,.b_bid(BB_bid[(IDWID - 1):0])
    ,.b_bready(BB_bready)
    ,.b_bresp(BB_bresp[1:0])
    ,.b_bvalid(BB_bvalid)
    ,.b_rdata(BB_rdata[(DWID - 1):0])
    ,.b_rid(BB_rid[(IDWID - 1):0])
    ,.b_rlast(BB_rlast)
    ,.b_rready(BB_rready)
    ,.b_rresp(BB_rresp[1:0])
    ,.b_rvalid(BB_rvalid)
    ,.b_wdata(BB_wdata[(DWID - 1):0])
    ,.b_wlast(BB_wlast)
    ,.b_wready(BB_wready)
    ,.b_wstrb(BB_wstrb[(WSTRB - 1):0])
    ,.b_wvalid(BB_wvalid)

    ,.c_araddr(CC_araddr[31:0])
    ,.c_arburst(CC_arburst[1:0])
    ,.c_arextras(CC_arextras[(EXTRAS - 1):0])
    ,.c_arid(CC_arid)
    ,.c_arlen(CC_arlen)
    ,.c_arsize(CC_arsize)
    ,.c_arready(CC_arready)
    ,.c_arvalid(CC_arvalid)
    ,.c_awaddr(CC_awaddr[31:0])
    ,.c_awburst(CC_awburst[1:0])
    ,.c_awextras(CC_awextras[(EXTRAS - 1):0])
    ,.c_awid(CC_awid)
    ,.c_awlen(CC_awlen)
    ,.c_awsize(CC_awsize)
    ,.c_awready(CC_awready)
    ,.c_awvalid(CC_awvalid)
    ,.c_bid(CC_bid[(IDWID - 1):0])
    ,.c_bready(CC_bready)
    ,.c_bresp(CC_bresp[1:0])
    ,.c_bvalid(CC_bvalid)
    ,.c_rdata(CC_rdata[(DWID - 1):0])
    ,.c_rid(CC_rid[(IDWID - 1):0])
    ,.c_rlast(CC_rlast)
    ,.c_rready(CC_rready)
    ,.c_rresp(CC_rresp[1:0])
    ,.c_rvalid(CC_rvalid)
    ,.c_wdata(CC_wdata[(DWID - 1):0])
    ,.c_wlast(CC_wlast)
    ,.c_wready(CC_wready)
    ,.c_wstrb(CC_wstrb[(WSTRB - 1):0])
    ,.c_wvalid(CC_wvalid)

    ,.d_araddr(DD_araddr[31:0])
    ,.d_arburst(DD_arburst[1:0])
    ,.d_arextras(DD_arextras[(EXTRAS - 1):0])
    ,.d_arid(DD_arid)
    ,.d_arlen(DD_arlen)
    ,.d_arsize(DD_arsize)
    ,.d_arready(DD_arready)
    ,.d_arvalid(DD_arvalid)
    ,.d_awaddr(DD_awaddr[31:0])
    ,.d_awburst(DD_awburst[1:0])
    ,.d_awextras(DD_awextras[(EXTRAS - 1):0])
    ,.d_awid(DD_awid)
    ,.d_awlen(DD_awlen)
    ,.d_awsize(DD_awsize)
    ,.d_awready(DD_awready)
    ,.d_awvalid(DD_awvalid)
    ,.d_bid(DD_bid[(IDWID - 1):0])
    ,.d_bready(DD_bready)
    ,.d_bresp(DD_bresp[1:0])
    ,.d_bvalid(DD_bvalid)
    ,.d_rdata(DD_rdata[(DWID - 1):0])
    ,.d_rid(DD_rid[(IDWID - 1):0])
    ,.d_rlast(DD_rlast)
    ,.d_rready(DD_rready)
    ,.d_rresp(DD_rresp[1:0])
    ,.d_rvalid(DD_rvalid)
    ,.d_wdata(DD_wdata[(DWID - 1):0])
    ,.d_wlast(DD_wlast)
    ,.d_wready(DD_wready)
    ,.d_wstrb(DD_wstrb[(WSTRB - 1):0])
    ,.d_wvalid(DD_wvalid)
);

'''

CLOCKER = '''
axi2clock axi_NAME (
     .in_clk(INCLOCK),.rst_n(rst_n)
    ,.ou_clk(OUCLOCK)


    ,.in_araddr(AA_araddr[31:0])
    ,.in_arburst(AA_arburst[1:0])
    ,.in_arextras(AA_arextras[(EXTRAS - 1):0])
    ,.in_arid(AA_arid)
    ,.in_arlen(AA_arlen)
    ,.in_arsize(AA_arsize)
    ,.in_arready(AA_arready)
    ,.in_arvalid(AA_arvalid)
    ,.in_awaddr(AA_awaddr[31:0])
    ,.in_awburst(AA_awburst[1:0])
    ,.in_awextras(AA_awextras[(EXTRAS - 1):0])
    ,.in_awid(AA_awid)
    ,.in_awlen(AA_awlen)
    ,.in_awsize(AA_awsize)
    ,.in_awready(AA_awready)
    ,.in_awvalid(AA_awvalid)
    ,.in_bid(AA_bid[(IDWID - 1):0])
    ,.in_bready(AA_bready)
    ,.in_bresp(AA_bresp[1:0])
    ,.in_bvalid(AA_bvalid)
    ,.in_rdata(AA_rdata[(DWID - 1):0])
    ,.in_rid(AA_rid[(IDWID - 1):0])
    ,.in_rlast(AA_rlast)
    ,.in_rready(AA_rready)
    ,.in_rresp(AA_rresp[1:0])
    ,.in_rvalid(AA_rvalid)
    ,.in_wdata(AA_wdata[(DWID - 1):0])
    ,.in_wlast(AA_wlast)
    ,.in_wready(AA_wready)
    ,.in_wstrb(AA_wstrb[(WSTRB - 1):0])
    ,.in_wvalid(AA_wvalid)

    ,.ou_araddr(BB_araddr[31:0])
    ,.ou_arburst(BB_arburst[1:0])
    ,.ou_arextras(BB_arextras[(EXTRAS - 1):0])
    ,.ou_arid(BB_arid[(IDWID - 1):0])
    ,.ou_arlen(BB_arlen[7:0])
    ,.ou_arsize(BB_arsize)
    ,.ou_arready(BB_arready)
    ,.ou_arvalid(BB_arvalid)
    ,.ou_awaddr(BB_awaddr[31:0])
    ,.ou_awburst(BB_awburst[1:0])
    ,.ou_awextras(BB_awextras[(EXTRAS - 1):0])
    ,.ou_awid(BB_awid)
    ,.ou_awlen(BB_awlen)
    ,.ou_awsize(BB_awsize)
    ,.ou_awready(BB_awready)
    ,.ou_awvalid(BB_awvalid)
    ,.ou_bid(BB_bid[(IDWID - 1):0])
    ,.ou_bready(BB_bready)
    ,.ou_bresp(BB_bresp[1:0])
    ,.ou_bvalid(BB_bvalid)
    ,.ou_rdata(BB_rdata[(DWID - 1):0])
    ,.ou_rid(BB_rid[(IDWID - 1):0])
    ,.ou_rlast(BB_rlast)
    ,.ou_rready(BB_rready)
    ,.ou_rresp(BB_rresp[1:0])
    ,.ou_rvalid(BB_rvalid)
    ,.ou_wdata(BB_wdata[(DWID - 1):0])
    ,.ou_wlast(BB_wlast)
    ,.ou_wready(BB_wready)
    ,.ou_wstrb(BB_wstrb[(WSTRB - 1):0])
    ,.ou_wvalid(BB_wvalid)

);

'''

SLICER = '''
axi_slice axi_NAME (
     .clk(INCLOCK),.rst_n(rst_n)
    ,.in_araddr(AA_araddr[31:0])
    ,.in_arburst(AA_arburst[1:0])
    ,.in_arextras(AA_arextras[(EXTRAS - 1):0])
    ,.in_arid(AA_arid)
    ,.in_arlen(AA_arlen)
    ,.in_arsize(AA_arsize)
    ,.in_arready(AA_arready)
    ,.in_arvalid(AA_arvalid)
    ,.in_awaddr(AA_awaddr[31:0])
    ,.in_awburst(AA_awburst[1:0])
    ,.in_awextras(AA_awextras[(EXTRAS - 1):0])
    ,.in_awid(AA_awid)
    ,.in_awlen(AA_awlen)
    ,.in_awsize(AA_awsize)
    ,.in_awready(AA_awready)
    ,.in_awvalid(AA_awvalid)
    ,.in_bid(AA_bid[(IDWID - 1):0])
    ,.in_bready(AA_bready)
    ,.in_bresp(AA_bresp[1:0])
    ,.in_bvalid(AA_bvalid)
    ,.in_rdata(AA_rdata[(DWID - 1):0])
    ,.in_rid(AA_rid[(IDWID - 1):0])
    ,.in_rlast(AA_rlast)
    ,.in_rready(AA_rready)
    ,.in_rresp(AA_rresp[1:0])
    ,.in_rvalid(AA_rvalid)
    ,.in_wdata(AA_wdata[(DWID - 1):0])
    ,.in_wlast(AA_wlast)
    ,.in_wready(AA_wready)
    ,.in_wstrb(AA_wstrb[(WSTRB - 1):0])
    ,.in_wvalid(AA_wvalid)

    ,.ou_araddr(BB_araddr[31:0])
    ,.ou_arburst(BB_arburst[1:0])
    ,.ou_arextras(BB_arextras[(EXTRAS - 1):0])
    ,.ou_arid(BB_arid[(IDWID - 1):0])
    ,.ou_arlen(BB_arlen[7:0])
    ,.ou_arsize(BB_arsize)
    ,.ou_arready(BB_arready)
    ,.ou_arvalid(BB_arvalid)
    ,.ou_awaddr(BB_awaddr[31:0])
    ,.ou_awburst(BB_awburst[1:0])
    ,.ou_awextras(BB_awextras[(EXTRAS - 1):0])
    ,.ou_awid(BB_awid)
    ,.ou_awlen(BB_awlen)
    ,.ou_awsize(BB_awsize)
    ,.ou_awready(BB_awready)
    ,.ou_awvalid(BB_awvalid)
    ,.ou_bid(BB_bid[(IDWID - 1):0])
    ,.ou_bready(BB_bready)
    ,.ou_bresp(BB_bresp[1:0])
    ,.ou_bvalid(BB_bvalid)
    ,.ou_rdata(BB_rdata[(DWID - 1):0])
    ,.ou_rid(BB_rid[(IDWID - 1):0])
    ,.ou_rlast(BB_rlast)
    ,.ou_rready(BB_rready)
    ,.ou_rresp(BB_rresp[1:0])
    ,.ou_rvalid(BB_rvalid)
    ,.ou_wdata(BB_wdata[(DWID - 1):0])
    ,.ou_wlast(BB_wlast)
    ,.ou_wready(BB_wready)
    ,.ou_wstrb(BB_wstrb[(WSTRB - 1):0])
    ,.ou_wvalid(BB_wvalid)

);

'''



if __name__ == '__main__': main()

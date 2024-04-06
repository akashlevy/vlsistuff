


module axi_rd_4_merger #(parameter AWID=32, parameter IDWID=4,parameter DWID=64, parameter EXTRAS=8)(

     input clk, input rst_n

    ,input [IDWID-1:0] a_arid
    ,input [AWID-1:0] a_araddr
    ,input [7:0] a_arlen
    ,input [2:0] a_arsize
    ,input [EXTRAS-1:0] a_arextras
    ,input [1:0] a_arburst
    ,input a_arvalid
    ,output a_arready
    ,output [IDWID-1:0] a_rid
    ,output [DWID-1:0] a_rdata
    ,output [1:0] a_rresp
    ,output a_rlast
    ,output a_rvalid
    ,input a_rready



    ,input [IDWID-1:0] b_arid
    ,input [AWID-1:0] b_araddr
    ,input [7:0] b_arlen
    ,input [2:0] b_arsize
    ,input [EXTRAS-1:0] b_arextras
    ,input [1:0] b_arburst
    ,input b_arvalid
    ,output b_arready
    ,output [IDWID-1:0] b_rid
    ,output [DWID-1:0] b_rdata
    ,output [1:0] b_rresp
    ,output b_rlast
    ,output b_rvalid
    ,input b_rready


    ,input [IDWID-1:0] c_arid
    ,input [AWID-1:0] c_araddr
    ,input [7:0] c_arlen
    ,input [2:0] c_arsize
    ,input [EXTRAS-1:0] c_arextras
    ,input [1:0] c_arburst
    ,input c_arvalid
    ,output c_arready
    ,output [IDWID-1:0] c_rid
    ,output [DWID-1:0] c_rdata
    ,output [1:0] c_rresp
    ,output c_rlast
    ,output c_rvalid
    ,input c_rready

    ,input [IDWID-1:0] d_arid
    ,input [AWID-1:0] d_araddr
    ,input [7:0] d_arlen
    ,input [2:0] d_arsize
    ,input [EXTRAS-1:0] d_arextras
    ,input [1:0] d_arburst
    ,input d_arvalid
    ,output d_arready
    ,output [IDWID-1:0] d_rid
    ,output [DWID-1:0] d_rdata
    ,output [1:0] d_rresp
    ,output d_rlast
    ,output d_rvalid
    ,input d_rready


    ,output [IDWID-1:0] arid
    ,output [AWID-1:0] araddr
    ,output [7:0] arlen
    ,output [2:0] arsize
    ,output [EXTRAS-1:0] arextras
    ,output [1:0] arburst
    ,output arvalid
    ,input arready
    ,input [IDWID-1:0] rid
    ,input [DWID-1:0] rdata
    ,input [1:0] rresp
    ,input rlast
    ,input rvalid
    ,output rready
);




reg [4:0] a_rcount,b_rcount,c_rcount,d_rcount;
wire a_ar_full,a_ar_empty;
assign a_arready = !a_ar_full && (a_rcount < 8);
wire b_ar_full,b_ar_empty;
assign b_arready = !b_ar_full && (b_rcount < 8);
wire c_ar_full,c_ar_empty;
assign c_arready = !c_ar_full && (c_rcount < 8);
wire d_ar_full,d_ar_empty;
assign d_arready = !d_ar_full && (d_rcount < 8);

localparam AWIDE = 3 + AWID + 8 + EXTRAS + 2+ IDWID;
wire [AWIDE-1:0] new_a_ar_entry = { a_arsize, a_araddr ,a_arlen ,a_arextras ,a_arburst ,a_arid };
wire [AWIDE-1:0] new_b_ar_entry = { b_arsize, b_araddr ,b_arlen ,b_arextras ,b_arburst ,b_arid };
wire [AWIDE-1:0] new_c_ar_entry = { c_arsize, c_araddr ,c_arlen ,c_arextras ,c_arburst ,c_arid };
wire [AWIDE-1:0] new_d_ar_entry = { d_arsize, d_araddr ,d_arlen ,d_arextras ,d_arburst ,d_arid };


wire [AWIDE-1:0] a_active_ar_entry;
wire [AWIDE-1:0] b_active_ar_entry;
wire [AWIDE-1:0] c_active_ar_entry;
wire [AWIDE-1:0] d_active_ar_entry;

syncfifo #(AWIDE,2) a_ar_fifo (.clk(clk),.rst_n(rst_n),.vldin(a_arvalid && a_arready)
    ,.din(new_a_ar_entry)
    ,.empty(a_ar_empty),.full(a_ar_full)
    ,.readout(take_a && arready)
    ,.dout(a_active_ar_entry)
    ,.count(),.overflow()
    ,.softreset(1'b0)
);
syncfifo #(AWIDE,2) b_ar_fifo (.clk(clk),.rst_n(rst_n),.vldin(b_arvalid && b_arready)
    ,.din(new_b_ar_entry)
    ,.empty(b_ar_empty),.full(b_ar_full)
    ,.readout(take_b && arready)
    ,.dout(b_active_ar_entry)
    ,.count(),.overflow()
    ,.softreset(1'b0)
);

syncfifo #(AWIDE,2) c_ar_fifo (.clk(clk),.rst_n(rst_n),.vldin(c_arvalid && c_arready)
    ,.din(new_c_ar_entry)
    ,.empty(c_ar_empty),.full(c_ar_full)
    ,.readout(take_c && arready)
    ,.dout(c_active_ar_entry)
    ,.count(),.overflow()
    ,.softreset(1'b0)
);

syncfifo #(AWIDE,2) d_ar_fifo (.clk(clk),.rst_n(rst_n),.vldin(d_arvalid && d_arready)
    ,.din(new_d_ar_entry)
    ,.empty(d_ar_empty),.full(d_ar_full)
    ,.readout(take_d && arready)
    ,.dout(d_active_ar_entry)
    ,.count(),.overflow()
    ,.softreset(1'b0)
);


wire [IDWID-1:0] id5 = 5;
wire [IDWID-1:0] id6 = 6;
wire [IDWID-1:0] id7 = 7;
wire [IDWID-1:0] id8 = 8;

wire a_ids_empty, b_ids_empty, c_ids_empty, d_ids_empty;
wire a_ids_full, b_ids_full, c_ids_full, d_ids_full;

assign take_a = !a_ar_empty && !a_ids_full;
assign take_b = !b_ar_empty && !b_ids_full && !take_a;
assign take_c = !c_ar_empty && !c_ids_full && !take_a && !take_b;
assign take_d = !d_ar_empty && !d_ids_full && !take_a && !take_b && !take_c;

assign arvalid = take_a || take_b || take_c || take_d;

wire [IDWID-1:0] orig_arid;
assign {arsize, araddr ,arlen ,arextras ,arburst, arid,orig_arid} = 
    (take_a) ? {a_active_ar_entry[AWIDE-1:IDWID],id5,a_active_ar_entry[IDWID-1:0]} :
    (take_b) ? {b_active_ar_entry[AWIDE-1:IDWID],id6,b_active_ar_entry[IDWID-1:0]} :
    (take_c) ? {c_active_ar_entry[AWIDE-1:IDWID],id7,c_active_ar_entry[IDWID-1:0]} :
    (take_d) ? {d_active_ar_entry[AWIDE-1:IDWID],id8,d_active_ar_entry[IDWID-1:0]} :
    0;



wire a_ids_readout = !a_ids_empty && a_rlast && a_rvalid && a_rready && (rid == id5);
wire b_ids_readout = !b_ids_empty && b_rlast && b_rvalid && b_rready && (rid == id6);
wire c_ids_readout = !c_ids_empty && c_rlast && c_rvalid && c_rready && (rid == id7);
wire d_ids_readout = !d_ids_empty && d_rlast && d_rvalid && d_rready && (rid == id8);

syncfifo_sampled #(IDWID,8) a_ids_fifo (.clk(clk),.rst_n(rst_n),.vldin(take_a && arvalid && arready)
    ,.din(orig_arid)
    ,.empty(a_ids_empty),.full(a_ids_full)
    ,.readout(a_ids_readout)
    ,.dout(a_rid)
    ,.count()
    ,.softreset(1'b0)
    ,.overflow(panic_a_ids_fifo)
);

syncfifo_sampled #(IDWID,8) b_ids_fifo (.clk(clk),.rst_n(rst_n),.vldin(take_b && arvalid && arready)
    ,.din(orig_arid)
    ,.empty(b_ids_empty),.full(b_ids_full)
    ,.readout(b_ids_readout)
    ,.dout(b_rid)
    ,.count()
    ,.softreset(1'b0)
    ,.overflow(panic_b_ids_fifo)
);

syncfifo_sampled #(IDWID,8) c_ids_fifo (.clk(clk),.rst_n(rst_n),.vldin(take_c && arvalid && arready)
    ,.din(orig_arid)
    ,.empty(c_ids_empty),.full(c_ids_full)
    ,.readout(c_ids_readout)
    ,.dout(c_rid)
    ,.count()
    ,.softreset(1'b0)
    ,.overflow(panic_c_ids_fifo)
);
syncfifo_sampled #(IDWID,8) d_ids_fifo (.clk(clk),.rst_n(rst_n),.vldin(take_d && arvalid && arready)
    ,.din(orig_arid)
    ,.empty(d_ids_empty),.full(d_ids_full)
    ,.readout(d_ids_readout)
    ,.dout(d_rid)
    ,.count()
    ,.softreset(1'b0)
    ,.overflow(panic_d_ids_fifo)
);


wire [DWID-1:0] x_rdata;
wire [1:0] x_rresp;
wire [IDWID-1:0] x_rid;
wire x_rlast;
wire rdata_fifo_empty,rdata_fifo_full,rdata_fifo_readout;
syncfifo #(1+2+DWID+IDWID,2) rdata_fifo (.clk(clk),.rst_n(rst_n)
    ,.vldin(rvalid && rready)
    ,.din({rlast,rresp,rdata,rid})
    ,.empty(rdata_fifo_empty),.full(rdata_fifo_full)
    ,.readout(rdata_fifo_readout)
    ,.dout({x_rlast,x_rresp,x_rdata,x_rid})
    ,.count(),.overflow()
    ,.softreset(1'b0)
);


assign rready = !rdata_fifo_full;

wire x_rvalid = !rdata_fifo_empty;


assign a_rvalid =  !a_ids_empty && x_rvalid && (x_rid == id5);
assign b_rvalid =  !b_ids_empty && x_rvalid && (x_rid == id6);
assign c_rvalid =  !c_ids_empty && x_rvalid && (x_rid == id7);
assign d_rvalid =  !d_ids_empty && x_rvalid && (x_rid == id8);


assign a_rdata = a_rvalid ? x_rdata : 0;
assign b_rdata = b_rvalid ? x_rdata : 0;
assign c_rdata = c_rvalid ? x_rdata : 0;
assign d_rdata = d_rvalid ? x_rdata : 0;

assign a_rresp = a_rvalid ? x_rresp : 0;
assign b_rresp = b_rvalid ? x_rresp : 0;
assign c_rresp = c_rvalid ? x_rresp : 0;
assign d_rresp = d_rvalid ? x_rresp : 0;

assign a_rlast = a_rvalid ? x_rlast : 0;
assign b_rlast = b_rvalid ? x_rlast : 0;
assign c_rlast = c_rvalid ? x_rlast : 0;
assign d_rlast = d_rvalid ? x_rlast : 0;

assign rdata_fifo_readout = d_rvalid ? d_rready : c_rvalid ? c_rready : b_rvalid ? b_rready : a_rvalid ? a_rready : 0;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        a_rcount <=0; b_rcount <=0; c_rcount <=0; d_rcount <=0; 
    end else begin
        if ((a_arvalid && a_arready) && !(a_rvalid && a_rlast && a_rready)) 
            a_rcount <= a_rcount + 1;
        else if (!(a_arvalid && a_arready) &&  (a_rvalid && a_rlast && a_rready)) 
            a_rcount <= a_rcount - 1;

        if ((b_arvalid && b_arready) && !(b_rvalid && b_rlast && b_rready)) 
            b_rcount <= b_rcount + 1;
        else if (!(b_arvalid && b_arready) &&  (b_rvalid && b_rlast && b_rready)) 
            b_rcount <= b_rcount - 1;

        if ((c_arvalid && c_arready) && !(c_rvalid && c_rlast && c_rready)) 
            c_rcount <= c_rcount + 1;
        else if (!(c_arvalid && c_arready) &&  (c_rvalid && c_rlast && c_rready)) 
            c_rcount <= c_rcount - 1;

        if ((d_arvalid && d_arready) && !(d_rvalid && d_rlast && d_rready)) 
            d_rcount <= d_rcount + 1;
        else if (!(d_arvalid && d_arready) &&  (d_rvalid && d_rlast && d_rready)) 
            d_rcount <= d_rcount - 1;
    end
end
wire [63:0]  sign_version = 64'h000a2b9022060424 ;
endmodule





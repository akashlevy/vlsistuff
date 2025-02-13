module syncfifo #(parameter WID = 32, parameter DEPTH=8, parameter AWID = $clog2(DEPTH))(
     input clk,input rst_n,input softreset
    ,input vldin, input [WID-1:0] din, output full
    ,input readout, output [WID-1:0] dout, output empty
    ,output reg [15:0] count
    ,output overflow
);
parameter DEPTH1 = DEPTH-1;
parameter AWID1  = AWID-1;
reg [WID-1:0] fifos [0:DEPTH1];
reg [AWID1:0] wptr,rptr;
assign   empty = count == 0;
assign   full = count == DEPTH;
assign   dout = empty ? {WID{1'b0}} : fifos[rptr];
assign overflow = vldin && full;
always @(posedge clk) begin
    if (vldin && !full) begin
        fifos[wptr] <= din;
    end 
end
always @(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        wptr <= 0; rptr <= 0; count<=0;
    end else if(softreset) begin
        wptr <= 0; rptr <= 0; count<=0;
    end else begin
        if(vldin && !full) begin
            wptr <= (wptr==(DEPTH1)) ? 0 : (wptr + 1'b1);
        end 
        if(readout && !empty) begin
            rptr <= (rptr==(DEPTH1)) ? 0 : (rptr + 1'b1);
        end 
        count <= 
            ((vldin && !full)&&(readout && !empty))  ? count :
            (vldin && !full)  ? (count+1'b1) :
            (readout && !empty)  ? (count-1'b1) :
            count;
    end 
end
wire [63:0]  sign_version = 64'h745641436e181224 ;
endmodule
// FROMFILE 74564 1436e 181224 :: /Users/iliagreenblat/project2/fpga_rtl/syncfifo.v


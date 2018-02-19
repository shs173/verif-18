// The baseline parameterized adder in behavioral Verilog

module adder64bit(clk, a, b, cin, s, cout);
input clk, a, b, cin;
output s, cout;

parameter n = 64;
wire [n-1:0] a, b, s;
wire cin;
wire [n:0] o;
wire cout;

assign o = a + b + cin;
assign s = o[n-1:0];
assign cout = o[n];

endmodule

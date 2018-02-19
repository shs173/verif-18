//  adder64bitmodular is a simple modular 64-bit adder that is constructed by
//  instantiating and wiring two instances of a parameterized 32-bit adder.
//  Ideally, one should keep the parameter n global, but as long as you pay
//  attention, you should be OK.

module adder64bitmodular(clk, a, b, cin, s, cout);
input clk, a, b, cin;
output s, cout;

parameter n = 64;
wire [n-1:0] a, b, s;
wire cin;
wire [n:0] o;
wire cout0, cout;

wire [n/2-1:0] s0, s1;

adder32bit adder0(clk, a[n/2-1:0], b[n/2-1:0], cin, s0, cout0);
adder32bit adder1(clk, a[n-1:n/2], b[n-1:n/2], cout0, s1, cout);

assign s = {s1,s0};

endmodule

// adder32bit is still behavioral RTL, and in your assignment, you cannot
// follow this style of coding. My expectation is that the CLA nature of
// your final design should be apparent/visible in the code.

module adder32bit(clk, a, b, cin, s, cout);
input clk, a, b, cin;
output s, cout;

parameter n = 32;
wire [n-1:0] a, b, s;
wire cin;
wire [n:0] o;
wire cout;

assign o = a + b + cin;
assign s = o[n-1:0];
assign cout = o[n];

endmodule

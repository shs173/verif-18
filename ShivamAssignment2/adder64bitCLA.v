module adder64bitCLA(clk, a, b, cin, s, cout);
input clk, a, b, cin;
output s, cout;

parameter n = 64;
wire [n-1:0] a, b, s;
wire cin, cout;

// All your wires and instantiations to construct the top-level module must go
// here. Do not change the input-output interface provided above since Vis will
// fail equivalence checking.

wire [15:0] s0,s1,s2,s3;
wire c16,c32,c48;

adder16bitCLA addr0(clk,a[15:0],b[15:0],cin,s0,c16);
adder16bitCLA addr1(clk,a[16:31],b[16:31],c16,s1,c32);
adder16bitCLA addr2(clk,a[32:47],b[32:47],c32,s2,c48);
adder16bitCLA addr3(clk,a[48:63],b[48:63],c48,s3,cout);

assign s = {s3,s2,s1,s0};
endmodule

// Your smallest adders must be modularized to at least 4 (or fewer) inputs in
// an adder4bitCLA (or appropriately named) module. You may need to design
// other modules, and all your code, with supporting documentation, must follow
// below this line.

module adder16bitCLA(clk,a,b,cin,s,cout);
input a,b;
input cin, clk;
output s;
output cout;
wire [15:0] a,b,s;
wire cin,cout;
wire [3:0] s0,s1,s2,s3;
wire gg0,pg0,gg4,pg4,gg8,pg8,gg12,pg12,c4,c8,c12; 

adder4bitCLA addr0(clk,a[3:0],b[3:0],cin,s0,c4);
adder4bitCLA addr1(clk,a[4:7],b[4:7],c4,s1,c8);
adder4bitCLA addr2(clk,a[8:11],b[8:11],c8,s2,c12);
adder4bitCLA addr3(clk,a[12:15],b[12:15],c12,s3,cout);

assign s = {s3,s2,s1,s0};
endmodule

module adder4bitCLA(clk,a,b,cin,s,cout);
input [3:0] a,b;
input cin, clk;
output[3:0] s;
output cout;
wire g0,g1,g2,g3,p0,p1,p2,p3,c1,c2,c3,gg,pg; 

gen gen0(a[0],b[0],g0);
gen gen1(a[1],b[1],g1);
gen gen2(a[2],b[2],g2);
gen gen3(a[3],b[3],g3);

prop prop0(a[0],b[0],p0);
prop prop1(a[1],b[1],p1);
prop prop2(a[2],b[2],p2);
prop prop3(a[3],b[3],p3);

carry cr1(p0,cin,g0,c1);
carry cr2(p1,c1,g1,c2);
carry cr3(p2,c2,g2,c3);
carry cr4(p3,c3,g3,cout);

xor(s[0],p0,cin);
xor(s[1],p1,c1);
xor(s[2],p2,c2);
xor(s[3],p3,c3);
endmodule

module gen(x,y,g);
input x,y;
output g;
and(g,x,y);
endmodule

module prop(x,y,p);
input x,y;
output p;
xor(p,x,y);
endmodule

module carry(x,y,z,c);
input x,y,z;
output c;
wire xy;
and(xy,x,y);
or(c,xy,z);
endmodule

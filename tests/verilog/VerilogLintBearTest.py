from bears.verilog.VerilogLintBear import VerilogLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
module mux2to1 (w0, w1, s, f);
  input w0, w1, s;
  output f;
  assign f = s ? w1 : w0;
endmodule
"""


bad_file = """
module updowncount(R, Clock, L, E, up_down, Q);
  parameter n=8;
  input [n-1:0] R;
  input Clock, L, E, up_down;
  output [n-1:0] Q;
  reg [n-1:0] Q;
  integer direction;
  always @(posedge Clock)
    begin
    if (up_down)
      direction = 1;
    else
      direction = -1;
    if (L)
      Q <= R;
    else if (E)
      Q <= Q + direction;
    end
endmodule
"""


VerilogLintBearTest = verify_local_bear(VerilogLintBear,
                                        valid_files=(good_file,),
                                        invalid_files=(bad_file,))

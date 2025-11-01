// max(7, 12) -> max

@7
D=A
@x
M=D          // x = 7

@12
D=A
@y
M=D          // y = 12

@x
D=M
@y
D=D-M        // D = x - y
@XGREATER
D;JGT        // if x > y goto XGREATER

// else: max = y
@y
D=M
@max
M=D
@END
0;JMP

(XGREATER)
@x
D=M
@max
M=D

(END)
@END
0;JMP

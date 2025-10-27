// this program is about implementing Multiplication operation between two Regiters in Hack assembly language

// mult = 0
@mult
M=0

// i = 0
@i
M=0

// a = R0 if R0 >= 0 else -R0
@R0
D=M

@R0Negative
D;JLT

// if R0 >= 0, a = R0 and go to LOOP
@a
M=D
@LOOP
0;JMP

(R0Negative)
// if R0 < 0, then a = -R0
@a
M=-D

(LOOP)
// calculating i - R0
@i
D=M
@a
D=D-M

// jump to BREAK if i - a == 0
@BREAK
D;JEQ

// mult = mult + R1
@R1
D=M
@mult
M=D+M

// i = i + 1
@i
M=M+1

// go to LOOP
@LOOP
0;JMP

(BREAK)
// if R0 >= 0, then go to END 
@R0
D=M
@END
D;JGE

// else negate result (mult)
@mult
M=-M

// Infinite empty loop
(END)
@END
0;JMP

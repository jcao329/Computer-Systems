// Adds 1+...+100.
@i // i refers to some mem. location.
M=1 // i=1
@2 // product refers to mem. location 2.
M=0 // sum=0
(LOOP)
@i
D=M // D=i
@0
D=D-M // D=i-R0
@END
D;JGT // If (i-100)>0 goto END
@1
D=M // D=R1
@prod
M=D+M // prod=prod+R1
@i
M=M+1 // i=i+1
@LOOP
0;JMP // Goto LOOP
(END)
@END
0;JMP // Infinite loop
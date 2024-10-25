(RESTART)
@SCREEN
D=A //Address of screen
@0
M=D  //Store screen location in R0

(KBDCHECK)
@KBD
D=M 
@BLACK
D;JGT //Jump to black if any KBD keys are pressed 
@WHITE 
D;JEQ //Jump to white if no keys are pressed (if D=0)

@KBDCHECK
0;JMP

(BLACK)
@1
M=-1 //Indicate fill screen with -1=111111111111
@CHANGE
0;JMP //Go to change the screen

(WHITE)
@1
M=0 //Indicate fill screen with 0=00000000
@CHANGE
0;JMP //Go to change the screen

(CHANGE)
@1 //Memory of what we are filling in screen with
D=M //check if it is black or white 

@0
A=M //Address of which pixel to fill
M=D //Fill the pixel

@0
D=M+1 //Next pixel
@KBD
D=A-D //KBD-SCREEN = A 

@0
M=M+1 //Increment to next pixel
A=M

@CHANGE
D;JGT //If A=0, the whole screen is black, so we exit. 

@RESTART
0;JMP
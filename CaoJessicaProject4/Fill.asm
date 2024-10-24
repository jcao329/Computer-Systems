@16384 // Set the base address for the screen (start at address 16384)
D=A
@SCREEN_START
M=D

@24575 // Set the end address for the screen (address 24575)
D=A
@SCREEN_END
M=D

(LOOP)
// Check if a key is pressed (check address 24576)
@24576
D=M

// If D == 0 (no key pressed), go to FILL_WHITE
@FILL_WHITE
D;JEQ

// If D != 0 (a key is pressed), go to FILL_BLACK
@FILL_BLACK
0;JMP

(FILL_BLACK)
// Fill the screen with black pixels (1111 1111 1111 1111)
@SCREEN_START
D=M
@BLACK_LOOP
@SCREEN_END
D;JGT
@END_BLACK
M=-1     // Set screen word to black (all 1s)
@BLACK_LOOP
D=D+1
M=D
@BLACK_LOOP
0;JMP

(END_BLACK)
// Go back to main loop
@LOOP
0;JML

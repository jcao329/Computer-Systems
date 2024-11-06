To run this code from terminal, be in the directory of where Assembler.py and your asm file lives. Then, in the 
command line, type:

python -c "from Assembler import assemble; assemble('filename.asm')"

Where filename is the name of your input file. 


11.6.2024 changed to use command line argument. Type this into the command line instead.

python3 Assembler.py 'filename.asm' 

Additionally, just so my code is not as buggy anymore, I changed the code so that if an uknown symbol is encountered, 
it takes next available address instead of binary code of the index in the symbol table 
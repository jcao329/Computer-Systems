To use this code, type python3 Compile.py input.jack code and the output should
return input.xml with the correct (hopefully!) corresponding xml commands. 

I tried to use the TextComparer on my computer, however, something was wrong 
with the permissions even after I ran chmod on the files, so I couldn't end up
comparing the text files. I did write my own compare function and it does say
that the files are the same, but there could be bugs with that (capitaliziation,
spelling, symbols, etc.). 

I mainly just used regex for tokenizing everything, then my compilation engine 
class is simply just a lot of checks to see if something is what it is and then 
writing it to the output file in the correct format. 

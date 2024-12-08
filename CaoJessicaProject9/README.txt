Well. I am not really sure what the problem is with my code, but something is seriously wrong with the memory

I will most likely try to fix this in the morning but it is late and I must go to work tomorrow. 

The idea behind this game is the card game War. A game begins with a shuffled deck of cards and two players. 
Each player begins with 26 cards dealt to them. Each round, the player takes the card at the top of their deck and 
places it face up. Whoever has the highest rank (number 1-13) wins the round and collects both of the cards played. 
If the rank is the same, then we enter war. Each player will take the top card of their deck and place it face down, 
and then draw the next card and place it face up as if they were playign a regular round. Whoever has the higher rank 
of the war cards will win and collect all cards played: the original equal rank cards, the face down cards, and 
the cards played during the war round. Players will keep playing the game until a player has the entire deck. 

I believe there is an issue with the code in the Card and Player class. It will compile with the Jack compiler, 
so it appears there are no syntax errors. 

It is a little hard to debug the code, but the outline of the idea is here. I think there is a problem with the 
plarRound logic and its recursion. I also think there is a problem with memory allocation for arrays of cards like within
the Deck class and Player class. 
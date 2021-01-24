# An Ant "AI" 

This program is a demonstration of using breeding, mutating, and selection to optimize specific values in an object.

Really, its more akin to simulated annealing than a neural network (it's not really anything like a neural network), but It's still doing things without my expressly telling them how to do them.

The goal is for the ants (the little white dots) to wander around the screen until they find food (the little red dots), then bring the food back to their home (the little dot in the center). I do this almost entirely from overloading the getScore() function, which tells them that food at home is very good, food you're holding is also good, and if we have food, then being closer to the center is good, and if you don't, being further from the center is good. From there the AI class takes it and makes generations of the Creature object, compares them, breeds the good ones, and then mutates them randomly. Pretty much everything has an option in the Gorgeous options menu, arrived at by pressing o. Check out my fantastic options structure at https://github.com/smartycope/Boilerplate. I am very proud of it, I've spent a lot of time on it.
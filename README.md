# Ant AI
This project demonstrates using evolutionary algorithms to select, breed, and mutate a population in order to optimize agents according to a specified value function. It's written as a library, which connects to a custom environment containing ants on a table wandering around to find food and bring it back to their home.

This is my Christmas break hobby project. Thus far, I've worked on it almost exclusively while on Christmas break cause I was bored. I made it to see if I could "evolve" simulated ants to find their way to food, vaugely like Richard Feynman observed ants doing in his classic book "Surely You Must be Joking Mr. Feynman!". It's not realistically meant to be used to compete with actual evolutionary algorithm libraries like scikit-learn.

## Running
```bash
git clone https://github.com/smartycope/AntAI.git
cd AntAI
pip install requirements.txt
python3 src
```

- All the driver code is in __main__.py.
- All the rendering and environment code is in TabletopEnv.py and SimpleGym.py.
- All the interesting code is in Generation.py.

## Explanation of my Custom Enviorment
The goal is for the ants (the little white dots) to wander around the screen until they find food (the little blue dots), then bring the food back to their home (the pink dot in the center).

The Ant's value function is specified by the reward() function, which goes something like this:
- Food at home is very good
- Food you're holding is also good
    - If we have food, then being closer to the center is good
    - If we don't have food, being further from the center is good (to encourage expolration)
- Try to minimize the number of steps in between food and home (to make shorter paths)

Generations have their own value functions, which go something like this:
- Sum all the rewards of the best `n` ants
- Subtract the number of steps the generation has taken * some large tweakable number, to encourage generations to be shorter, and the ants to act faster

Each generation (except the first, which is randomized) is generated from either the previous, the best of the previous `n` generations, or the best generation.

## Options
I finally found an excuse to work in a metaclass into one of my projects. I have the AddOptions metaclass which takes all the static members of a class and makes them into Options.
This is useful for specifying options, where each of the options have options with defaults. This way, you can use all of them like `Breeding.Cutoff` as well as `Breeding.Cutoff(min_cutoff_len=20, min_dna_len=10)` as well as `Breeding.Cutoff(20)`. I have a lot of options in this project, all of which are in the Options.py file, with lots of comments. Since this is just a hobby project to demonstrate a concept, I'm not writing documentation; you can go look in the file for more.

## Minor Disclaimer
This isn't really an AI, I just called it that and don't want to change the name. It is heuristic though.

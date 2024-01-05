# Ant AI
This project demonstrates using evolutionary algorithms to select, breed, and mutate a population in order to optimize agents according to a specified value function. It's written as a library, which connects to a custom environment containing ants on a table wandering around to find food and bring it back to their home.

I made this to see if I could "evolve" simulated ants to find their way to food, vaguely like Richard Feynman observed ants doing in his classic book "Surely You Must be Joking Mr. Feynman!". It's not realistically meant to be used to compete with actively developed evolutionary algorithm libraries like the add-on for scikit-learn.

## Running
This by itself is all you need to get going. There's a ton of config options with explanations you can play with in [__main\__.py](src/__main__.py) at the top of the file.
```bash
git clone https://github.com/smartycope/AntAI.git
cd AntAI
pip install -r requirements.txt
python src
```
- There are 2 modes, *rounds* mode *real time simulation* mode:
    - *rounds* mode is where we kill the generation of ants every so often, select new to breed & mutate, then make a new generation from a previous generation
    - *real time simulation* mode is where we have ants wander around and survival pressures (like age or a max number of ants allowed on the table) optimize them
- You can click anywhere to add food, and right click in real time simulation mode, it will add an ant there
- 'q' quits, up and down speed up and slow down the simulation, 'p' pauses, and 's' steps by frame
- Code Locations:
    - All the driver code is in [__main\__.py](src/__main__.py).
    - All the rendering and environment code is in [TabletopEnv.py](src/TabletopEnv.py) and [SimpleGym.py](src/SimpleGym.py).
    - All the interesting code is in [Generation.py](src/Generation.py).
    - All the explanations for the Options relating to Breeding, Mutating, Selecting, and Generating are in [Options.py](src/Options.py)

## Explanation of my Custom Environment
The goal is for the ants (the little white dots) to wander around the screen until they find food (the little blue dots), then bring the food back to their home (the pink dot in the center).

The Ant's value function is specified by the Ant.reward() function, which goes something like this:
- Food at home is very good
- Food you're holding is also good
    - If we have food, then being closer to the center is good
    - If we don't have food, being further from the center is good (to encourage exploration)
- Try to minimize the number of steps in between food and home (to make shorter paths)

The Generation class has its own value function, which goes something like this:
- Sum all the rewards of the best `score_by_top_n` ants
- Subtract the number of steps the generation has taken * some large tweakable number, to encourage generations to be shorter, so the ants to act faster

Each generation (except the first, which is randomized) is generated from either the previous, the best of the previous `n` generations, or the best of all the generations.

## Options
I finally found an excuse to work in a metaclass into one of my projects (though now that I've done more research, \_\_init_subclass\__ probably would have been sufficient). I have the AddOptions metaclass which takes all the static members of a class and makes them into Option instances.
This is useful for specifying options, where each of the options have options with defaults. This way, you can use all of them like `Breeding.Cutoff` as well as `Breeding.Cutoff(min_cutoff_len=20, min_dna_len=10)` as well as `Breeding.Cutoff(20)`. I have a lot of options in this project, all of which are in the Options.py file, with lots of comments. Since this is just a hobby project to demonstrate a concept, I'm not writing documentation; you can go look in the file for more.

## Minor Disclaimer
This isn't really an AI, I just called it that and don't want to change the name. It is heuristic though.

import time
from Options import *
from Generation import Generation
import numpy as np
from Ant import Ant
from TabletopEnv import TabletopEnv
from Movement import Movement
from rich.table import Table
from rich import print as rprint
from random import randint

def summarize(generations):
    sorted_gen = sorted(generations, reverse=True)

    table = Table(title='Generations')
    table.add_column('#')
    table.add_column('Rank')
    table.add_column('Steps')
    table.add_column('Ants')
    table.add_column('Reward')
    table.add_column('Food Collected')
    table.add_column('Food Gathered')
    table.add_column('ChampiAnt')
    # table.add_column('Worst Ant')

    for cnt, gen in enumerate(generations):
        sorted_ants = sorted(gen.creatures)
        table.add_row(
            str(cnt + 1),
            str(sorted_gen.index(gen) + 1),
            str(gen._steps),
            str(gen.size),
            str(round(gen.reward())),
            str(sum(map(lambda a: a.food_collected, gen.creatures))),
            str(sum(map(lambda a: a.food_gathered, gen.creatures))),
            repr(sorted_ants[-1]),
            # repr(sorted_ants[0]),
        )

    rprint(table)
    print(f'Best Generation: #{generations.index(sorted_gen[0])+1}: {sorted_gen[0]}')
    # Save the best ant's DNA
    with open('bestDNA.txt', 'w') as f:
        f.writelines(', '.join(map(str, sorted(sorted_gen[0].creatures)[-1].dna)))

if __name__ == '__main__':
    rounds = False

    # Config
    screen_size = 300
    # If not dynamically resetting, how long each generation lasts
    steps = 500
    # Reset after this many foods have been brought back to home. Or None, to reset after a certain number of steps
    dynamic_reset = 3
    # Sort the Generations and create a new Generation from the best one, instead of just the last one
    # If this is a number, it gets the best generation of the last n generations, and goes off of that
    use_best_generation_of = 5
    # How many generations do we do before we're done
    num_generations = 50

    start_paused = False
    show_events = False

    TabletopEnv.verbose = False
    Generation.verbose = False
    Ant.verbose = False
    Ant.rounds = TabletopEnv.rounds = rounds
    # How much each ant can move in any direction
    Movement.max_movement = 2
    TabletopEnv.color_by_reward = True
    TabletopEnv.bound_method = 'loop'
    # Range of how many foods to put on the table
    TabletopEnv.min_foods = 40
    TabletopEnv.max_foods = 100
    # Range of how much food each food area has in it
    TabletopEnv.min_food_amt = 220
    TabletopEnv.max_food_amt = 400
    TabletopEnv.fps = 30
    # How big the food, ants, and home are, in pixels
    TabletopEnv.food_size = 5
    TabletopEnv.ant_size = 3
    TabletopEnv.home_size = 10
    # Max number of ants allowed (only relevant in real-time simulation mode)
    TabletopEnv.max_ants = 300
    # Ants have to be alive for this many steps before they can breed
    TabletopEnv.age_of_maturity = 50
    # How many ants are in each generation
    Generation.size = 100
    # How many ants we look at when evaluating generations
    # Setting this to dynamic_reset alleviates the problem of the ants just hanging around food
    # and not bringing it back, because they're incentivised to gather food as well.
    Generation.score_by_top_n = dynamic_reset if dynamic_reset is not None else 10
    Generation.creature_type = Ant
    Generation.nucleotide_type = Movement
    # Delete any DNA after we gathered and returned a food
    Ant.limit_after_collected = True
    # Where the ants bring food back to
    Ant.home = np.array((screen_size//2,)*2)
    # Where the ants start (they don't have to start at home)
    Ant.start = Ant.home
    # Real-time simulation Options
    # How long the ants can survive without food
    Ant.stomach = 50
    # How much food an ant can hold
    Ant.food_capacity = 2
    # How old the ants can get. Set to None to not limit it
    Ant.max_age = 150
    # Max length of the DNA allowed
    Ant.memory = Ant.max_age

    # Options: see Options.py for details
    # "Generation generation": How we generate the next generation
    gen_gen_method = GenGen.FamilyLine(families=5)
    # How we breed ants together
    breeding_method = Breeding.Identical
    # How we select ants to be bred from the previous generation
    selection_method = Selection.WinnerSecond
    # How we mutate the ants
    mutation_method = Mutation.Induvidual(total_mutation_chance=0.8, mutation_chance=.3)

    if rounds:
        # Setup
        generations = [Generation()]
        table = TabletopEnv(generations[-1], steps, screen_size, start_paused=start_paused, show_events=show_events)

        # Run
        try:
            generation, info = table.reset()
            # Run for `num_generations`
            for i in range(num_generations):
                terminated = False
                prevSteps = -1
                # Run until the enviorment says we're done, or according to dynamic_reset
                while not terminated:
                    # If it went down instead of up, we've reset
                    if table.steps < prevSteps:
                        break
                    prevSteps = table.steps

                    # Render the table
                    table.render()

                    if table.just_full_reset:
                        print('Full resetting')
                        summarize(generations)
                        generations = [Generation()]
                        table.just_full_reset = False
                        # table.just_reset = False
                        break
                    # TODO Figure out why this doesn't work
                    # if table.just_reset:
                    #     print('Resetting')
                    #     table.just_reset = False
                    #     break

                    # If we're paused, pause, and if we want to increment, step once
                    if table.pause:
                        if table.increment:
                            table.increment = False
                            generation, rewards, terminated, _, info = table.step(generations[-1])
                        continue

                    # Finally, step
                    generation, rewards, terminated, _, info = table.step(generations[-1])
                    time.sleep(1/table.fps)
                    # Determine how we're terminating
                    terminated = terminated if dynamic_reset == None else table.food_collected >= dynamic_reset

                # The round is done
                if use_best_generation_of is True:
                    gen = sorted(generations, reverse=True)[0]
                elif use_best_generation_of is False:
                    gen = generations[-1]
                else:
                    gen = sorted(generations[-use_best_generation_of:], reverse=True)[0]

                generations.append(gen.generate(gen_gen_method, breeding_method, mutation_method, selection_method))
                # Not a full reset: this resets the ant positions, not the food or the ant's dna.
                table.reset()
        finally:
            table.close()
            summarize(generations)

    # Simulations, breeding real time, not rounds
    else:
        # Setup
        Ant.start = np.array((100,100))
        table = TabletopEnv(Generation(), steps, screen_size, start_paused=start_paused, show_events=show_events)

        # Run
        try:
            generation, info = table.reset()
            while True:
                terminated = False
                prevSteps = -1
                # Run until the enviorment says we're done, or according to dynamic_reset
                while not terminated:
                    # If it went down instead of up, we've reset
                    if table.steps < prevSteps:
                        break
                    prevSteps = table.steps

                    # Render the table
                    table.step_print(f'Ants: {len(table.generation.creatures)}')
                    table.render()

                    # If we're paused, pause, and if we want to increment, step once
                    if table.pause:
                        if table.increment:
                            table.increment = False
                            generation, rewards, terminated, _, info = table.step(generation, breed_method=breeding_method, mutation_method=mutation_method)
                        continue

                    # Finally, step
                    generation, rewards, terminated, _, info = table.step(generation, breed_method=breeding_method, mutation_method=mutation_method)
                    time.sleep(1/table.fps)
                    # Determine how we're terminating
                    terminated = False

                # The round is done
                generation, info = table.reset(full=True)
        finally:
            table.close()

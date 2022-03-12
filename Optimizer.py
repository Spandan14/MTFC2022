# these are our standard imports; numpy is used for mathematical and tensor calculations, while pymoo is a library for
# multi-objective optimization
import numpy as np
import copy
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.visualization.scatter import Scatter
from pymoo.optimize import minimize
import matplotlib.pyplot as plt
import tqdm
import imageio

from Crops import crop_class_loader  # import the data loader for crop data by county (acres planted, yield, type, etc.)
from Gradient import gradient_loader  # import the data loader for gradient data by county
from CountyMap import CountyMap  # import the county_map class for storing our irrigation technique data, finding
# connected components, and plotting
from Objectives import water_usage, technique_cost  # import objective functions for optimization

county_map = CountyMap()
county_map.load_counties("./data/CountyMapData.xlsx")  # load county list and data into county_map
county_map.load_connections("./data/CountyMapData.xlsx")  # load data of borders/graph connections between counties

TECHNIQUES = {0: "Center Pivot Irrigation",
              1: "Sprinkler Irrigation",
              2: "Drip Irrigation",
              3: "Furrow Irrigation"}

NODE_COLORS = {0: "red",
               1: "green",
               2: "purple",
               3: "blue"}

WATER_COST_PER_GALLON = 0.0025379

county_map.load_techniques(TECHNIQUES)  # populate county_map with necessary constants
county_map.load_node_colors(NODE_COLORS)

NUMBER_COUNTIES = len(county_map.COUNTY_LIST)

county_crops = crop_class_loader(source_xlsx="./data/CropData.xlsx")  # load classes for each crop for each county
county_gradients = gradient_loader(source_xlsx="./data/Gradients.xlsx")  # load gradient angles for each county

POPULATION_SIZE = 100
GENERATIONS = 200


class TechniqueProblem(ElementwiseProblem):
    # define problem class for the pymoo library to solve; this class inherits from ElementwiseProblem as we chose to
    # evaluate one solution at a time instead of multithreading the solution process
    def __init__(self):
        super().__init__(
            n_var=NUMBER_COUNTIES,  # each county's irrigation technique is represented as a variable
            n_obj=2,  # we have two objectives, water usage and cost
            n_constr=0,  # there are no constraints needed for our problem
            xl=0,  # the minimum value for our variables is 0 (this corresponds to T_1, but the code is 0-indexed)
            xu=3,  # the maximum value for our variables is 3 (this corresponds to T_4, but the code is 0-indexed)
            type_var=int  # because our variables are just classifiers for irrigation techniques, they should be
            # restricted to integers, (0 -> T_1, 1 -> T_2, 2 -> T_3, 3 -> T_4)
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # _evaluate is called every time the objectives need to be evaluated for a solution x; out is a dictionary
        # containing the objective function values
        for i in range(0, len(x)):
            county_map.assign_technique_to_county(i, x[i])  # assign the solution's set of irrigation techniques to all
                                                            # counties in county_map

        f_w = water_usage(county_crops, x, county_gradients)  # evaluate water usage
        f_c = technique_cost(county_crops, x, county_gradients,  # evaluate cost;
                             np.sum([len([comp for comp in county_map.connected_components_by_technique(technique)])
                                     for technique, description in TECHNIQUES.items()]))
        # note that the last argument supplied in technique_cost for the number of connected blocks of irrigation
        # techniques is derived from a list comprehension which sums the lengths of all connected blocks of counties for
        # all irrigation techniques in county_map

        out["F"] = [f_w, f_c]  # store objective values in the dictionary out
        out["G"] = []  # store constraint values in the dictionary out, which are blank as we have 0 constraints


algorithm = NSGA2(  # initialize an instance of the NSGA-II algorithm
    pop_size=POPULATION_SIZE,
    sampling=get_sampling("int_random"),  # we use integer sampling so we get random integers
    crossover=get_crossover("int_sbx", prob=1.0, eta=3.0),  # special crossover for integer variables
    mutation=get_mutation("int_pm", eta=3.0),  # special mutation for integer variables
    eliminate_duplicates=True,  # we do not want duplicate solutions
)

problem = TechniqueProblem()  # create an instance of our problem class

result = minimize(  # run the minimize function using our algorithm and problem object
    problem,
    algorithm,
    termination=('n_gen', GENERATIONS),  # set to terminate after n_gen = GENERATIONS
    seed=1,  # seed for random numbering, can be altered as desired
    save_history=True  # save history for analysis after the algorithm has finished
)

last_gen = result.history[-1]  # return the snapshot from the final generation of the algorithm by indexing the end of
                               # the result's history
# acquire and sort our solutions based on f_c
sol_pop = [np.concatenate([individual.F, individual.X]) for individual in last_gen.pop]
sol_pop = np.stack(sol_pop, axis=0)
sol_pop = sol_pop[np.argsort(sol_pop[:, 1])]


np.savetxt("solution.csv", sol_pop, delimiter=",")

"""
counter = 0
for gen in tqdm.tqdm(result.history):
    f_w = [individual.F[0] for individual in gen.pop]
    f_c = [individual.F[1] for individual in gen.pop]
    colors = ['red' if (i + 1) % 10 != 5 else 'blue' for i in range(0, len(f_w))]
    print([[f_w[i], f_c[i]] for i in range(0, len(f_w)) if (i + 1) % 10 == 5])
    plt.scatter([f / 1000000000000 for f in f_w], [f / 1000000 for f in f_c], c=colors, s=10)
    plt.title(f"Pareto Front for Optimal Irrigation Technique Placement \nin the Texas Panhandle | GENERATION {counter}")
    plt.ylabel("Total Annual Cost of Maintenance (millions of USD)")
    plt.xlabel("Total Annual Water Usage (trillions of gallons)")
    plt.savefig(f'./img/{counter}-image.png')
    plt.clf()
    counter += 1

with imageio.get_writer('nsga-convergence.gif', mode='I') as writer:
    for i in tqdm.tqdm(range(0, len(result.history))):
        image = imageio.imread(f'./img/{i}-image.png')
        writer.append_data(image)

"""

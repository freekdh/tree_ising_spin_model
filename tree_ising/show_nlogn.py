import math
import time

import matplotlib.pyplot as plt

from tree_ising.main import solve_ising_problem
from tree_ising.problem_loader import ProblemLoaderFromNSpins


def nlognplot():
    problem_loader_n_spins = ProblemLoaderFromNSpins()

    data = dict()
    for depth in range(2, 15):
        problem = problem_loader_n_spins.load_problem(depth=depth)

        start = time.time()
        solve_ising_problem(problem)
        end = time.time()
        data[depth] = end - start

    fig, ax = plt.subplots()

    xs, ys = [], []
    for depth, time in data.items():
        n_spins = 2 ** depth
        xs.append(n_spins * math.log(n_spins))
        ys.append(time)

    ax.scatter(x=xs, y=ys)
    ax.set_title("The algo is N log N")
    ax.set_ylabel("Time (seconds)")
    ax.set_xlabel("n log n (n: spins) of a regular tree")
    fig.savefig("algo_is_nlogn.png")


if __name__ == "__main__":
    nlognplot()

from functools import lru_cache

from tree_ising.problem import IsingTreeProblem
from tree_ising.problem_loader import ProblemLoaderFromFile


@lru_cache(maxsize=None)
def min_energy_configuration_subtree(focal_node: int, parent_node_spin: int):
    raise NotImplementedError


@lru_cache(maxsize=None)
def min_energy_subtree(focal_node: int, parent_node_spin: int):
    raise NotImplementedError


def solve_ising_problem(ising_problem: IsingTreeProblem):
    raise NotImplementedError
    print(ising_problem)


if __name__ == "__main__":
    problem_loader = ProblemLoaderFromFile()
    ising_problem = problem_loader.load_problem(
        file_path="tests/test_problems/input_test_problem.txt"
    )

    solve_ising_problem(ising_problem)

import pytest

from tree_ising.main import solve_ising_problem


@pytest.mark.parametrize("root_node", [0, 1, 3])
def test_get_min_energy(problem_loader_from_file, root_node):

    ising_problem = problem_loader_from_file.load_problem(
        file_path="tests/test_problems/input_test_problem.txt", root_node=root_node
    )

    assert solve_ising_problem(ising_problem) == -4

import pytest

from tree_ising.main import solve_ising_problem


@pytest.mark.parametrize("root_node", [0, 1, 3])
def test_solve_ising_problem(problem_loader_from_file, root_node):

    ising_problem = problem_loader_from_file.load_problem(
        file_path="tests/test_problems/input_test_problem.txt", root_node=root_node
    )

    optimal_configuration = solve_ising_problem(ising_problem)
    assert optimal_configuration.spin_assignment == {0: 1, 1: -1, 2: 1, 3: 1}
    assert optimal_configuration.energy == -4

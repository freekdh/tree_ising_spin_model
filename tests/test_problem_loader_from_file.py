import pytest
from glob import iglob

test_file = "tests/test_problems/input_test_problem.txt"


@pytest.mark.parametrize("root_node", [0, 1, 3])
def test_problem_loader_from_file(problem_loader_from_file, root_node):
    ising_problem = problem_loader_from_file.load_problem(
        file_path=test_file, root_node=root_node
    )

    assert ising_problem.get_n_nodes() == 4
    assert ising_problem.get_n_weights() == 6
    assert ising_problem.root_node == root_node

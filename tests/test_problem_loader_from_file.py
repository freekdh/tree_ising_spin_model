import pytest
from glob import iglob


@pytest.mark.parametrize("input_problem_path,expected_nodes,expected_weights", [("tests/test_problems/input_test_problem.txt", 4, 6)])
def test_problem_loader_from_file(problem_loader_from_file, input_problem_path, expected_nodes, expected_weights):
    ising_problem = problem_loader_from_file.load_problem(file_path=input_problem_path)

    assert ising_problem.get_n_nodes() == expected_nodes
    assert ising_problem.get_n_weights() == expected_weights

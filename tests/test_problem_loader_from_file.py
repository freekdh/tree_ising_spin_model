import pytest
from glob import iglob


@pytest.mark.parametrize("input_problem_path", iglob("tests/test_problems/*.txt"))
def test_problem_loader_from_file(problem_loader_from_file, input_problem_path):
    problem_loader_from_file.load_problem(file_path=input_problem_path)

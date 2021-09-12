import pytest
from tree_ising.problem_loader import ProblemLoaderFromFile


@pytest.fixture
def problem_loader_from_file() -> ProblemLoaderFromFile:
    return ProblemLoaderFromFile(seed=10)

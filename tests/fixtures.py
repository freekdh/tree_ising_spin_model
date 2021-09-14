import pytest

from tree_ising.problem_loader import ProblemLoaderFromFile, ProblemLoaderFromNSpins


@pytest.fixture
def problem_loader_from_file() -> ProblemLoaderFromFile:
    return ProblemLoaderFromFile(seed=10)


@pytest.fixture
def problem_loader_from_spins() -> ProblemLoaderFromNSpins:
    return ProblemLoaderFromNSpins(seed=10)

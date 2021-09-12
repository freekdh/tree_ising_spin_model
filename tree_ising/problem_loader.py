from tree_ising.problem import IsingTreeProblem
from abc import ABC, abstractmethod
from os import path


class ProblemLoader(ABC):
    """
    Base class for loading the ising tree problems
    """

    @abstractmethod
    def load_problem(self, file_path: str) -> IsingTreeProblem:
        pass


class ProblemLoaderFromFile(ProblemLoader):
    def load_problem(self, file_path: str) -> IsingTreeProblem:
        assert path.isfile(file_path)

        with open(file_path) as input_file:
            print(input_file.readlines())

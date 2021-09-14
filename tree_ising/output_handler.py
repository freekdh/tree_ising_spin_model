from abc import ABC, abstractmethod
from typing import Dict, Iterable

from tree_ising.main import PartialConfiguration


class OutputHandler(ABC):
    @abstractmethod
    def handle_configuration(self, solution: PartialConfiguration):
        pass


class FileOutputHandler(OutputHandler):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def _get_configuration_in_sequence_of_plus_and_min_symbols(
        self, spin_assignment: Dict
    ) -> Iterable:
        sorted_spin_assignments = sorted(spin_assignment.items())
        for spin, value in sorted_spin_assignments:
            if value == 1:
                yield "+"
            elif value == -1:
                yield "-"
            else:
                raise ValueError("expected all values of spins to be either -1 or 1")

    def handle_configuration(self, solution_configuration: PartialConfiguration):

        with open(self._file_path, "w") as output_file:
            output_file.write(f"{solution_configuration.energy}\n")
            output_file.write(
                "".join(
                    self._get_configuration_in_sequence_of_plus_and_min_symbols(
                        solution_configuration.spin_assignment
                    )
                )
            )

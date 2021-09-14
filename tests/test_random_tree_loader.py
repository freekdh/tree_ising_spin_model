from networkx.algorithms.dag import topological_sort


def test_random_tree_problem_loader(problem_loader_from_spins):
    ising_problem = problem_loader_from_spins.load_problem(depth=4)
    assert next(topological_sort(ising_problem.directed_graph)) == 0

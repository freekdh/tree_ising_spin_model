from tree_ising.main import PartialConfiguration


def test_comparison():
    assert PartialConfiguration(5, dict()) > PartialConfiguration(0, dict())
    assert PartialConfiguration(0, dict()) == PartialConfiguration(0, dict())

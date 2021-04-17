import unittest

from geneticlib import get_rank_function, evolve


def buildhiddenset():
    rows = [["hola mundo", "hola"],
            ["Bob Alice", "Bob"]]

    #rows = [["20-12", "12"],
    #        ["12-1", "1"]]
    return rows


class TestEvolve(unittest.TestCase):

    def test_evolve(self):
        rf = get_rank_function(buildhiddenset())
        winner = evolve(1, 'str', 500, rf, mutation_rate=0.2, breed_ingrate=0.1, p_exp=0.7, p_new=0.1)
        self.assertEqual(winner.evaluate(["Alice Bob"]), "Alice")


if __name__ == '__main__':
    unittest.main()

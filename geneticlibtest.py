import unittest

from geneticlib import getrankfunction, evolve


def buildhiddenset():
    rows = [["hola mundo", "hola"],
            ["Bob Alice", "Bob"]]

    #rows = [["20-12", "12"],
    #        ["12-1", "1"]]
    return rows


class TestEvolve(unittest.TestCase):

    def test_evolve(self):
        rf = getrankfunction(buildhiddenset())
        winner = evolve(1, 'str', 500, rf, mutationrate=0.2, breedingrate=0.1, pexp=0.7, pnew=0.1)
        self.assertEqual(winner.evaluate(["Alice Bob"]), "Alice")


if __name__ == '__main__':
    unittest.main()

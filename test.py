from geneticlib import evolve, getrankfunction


def hiddenfunction(x):
    return x[0: x.index(" ") - 1]




if __name__ == '__main__':
    rf = getrankfunction(buildhiddenset())
    winner = evolve(1, 'str', 500, rf, mutationrate=0.2, breedingrate=0.1, pexp=0.7, pnew=0.1)
    entrada = ""

    while entrada != "exit.":
        entrada = input("Next: ")
        print(winner.evaluate([entrada]))
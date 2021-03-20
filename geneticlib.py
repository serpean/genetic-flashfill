from copy import deepcopy
from difflib import SequenceMatcher
from math import log
from random import random, randint, choice

class Fwrapper:
    def __init__(self, function, params, name):
        self.function = function
        self.params = params
        self.name = name

class Node:
    def __init__(self, fw, children):
        self.function = fw.function
        self.name = fw.name
        self.children = children

    def evaluate(self, inp):
        results = [n.evaluate(inp) for n in self.children]
        return self.function(results)

    def display(self, indent=0):
        print((' ' * indent) + self.name)
        for c in self.children:
            c.display(indent + 1)


class ParamNode:
    def __init__(self, idx):
        self.idx = idx

    def evaluate(self, inp):
        return inp[self.idx]

    def display(self, indent=0):
        print('%sp%d' % (' ' * indent, self.idx))


class ConstNode:
    def __init__(self, v):
        self.v = v

    def evaluate(self, inp):
        return self.v

    def display(self, indent=0):
        print('%s%s' % (' ' * indent, self.v))


addw = Fwrapper(lambda l: l[0] + l[1], ['int', 'int'], 'add')
subw = Fwrapper(lambda l: l[0] - l[1], ['int', 'int'], 'subtract')
mulw = Fwrapper(lambda l: l[0] * l[1], ['int', 'int'], 'multiply')
ifw = Fwrapper(lambda l: l[1] if l[0] > 0 else l[2], ['int', 'int', 'int'], 'if')
gtw = Fwrapper(lambda l: 1 if l[0] > l[1] else 0, ['int', 'int'], 'isgreater')
substringw = Fwrapper(lambda l: l[0][l[1]: l[2]], ["str", "int", "int"], 'substring')
concatw = Fwrapper(lambda l: l[0] + l[1], ["str", "str"], 'concat')
indexw = Fwrapper(lambda l: l[0].index(l[1]), ["str", "str"], 'index') # FIXME: String cannot contains substring. In this case, max ratio will be use

flist = {'str': [substringw, concatw, indexw], 'int': [addw, subw]}


def makerandomtree(pc, datatype, maxdepth=4, fpr=0.5, ppr=0.5):
    if random() < fpr and maxdepth > 0:
        f = choice(flist[datatype])
        # Call makerandomtree with all the parameter types for f
        children = [makerandomtree(pc, type, maxdepth - 1, fpr, ppr) for type in f.params]
        return Node(f, children)
    elif random() < ppr and datatype == 'str':
        return ParamNode(randint(0, pc - 1))
    else:
        # return 1 to 10 if integer
        # else return common char
        if datatype == 'str':
            return ConstNode(choice([" ", ".", "-"]))
        else:
            return ConstNode(randint(0, 10))


def mutate(t, pc, datatype, probchange=0.1):
    if random() < probchange:
        return makerandomtree(pc, datatype)
    else:
        result = deepcopy(t)
        if hasattr(t, "children"):
            result.children = [mutate(c, pc, datatype, probchange) for c in t.children]
        return result


def crossover(t1, t2, probswap=0.7, top=1):
    if random() < probswap and not top:
        return deepcopy(t2)
    else:
        result = deepcopy(t1)
        if hasattr(t1, 'children') and hasattr(t2, 'children'):
            result.params = [crossover(c, choice(t2.children), probswap, 0)
                             for c in t1.children if hasattr(t1, 'funtion') and hasattr(t2, 'funtion') and t1.funtion.params == t2.funtion.params]
        return result


def scorefunction(tree, s):
    dif = 0
    for data in s:
        try:
            v = tree.evaluate([data[0]])
            dif += 1 - SequenceMatcher(None, data[1], str(v)).ratio()
        except:
            dif += 1
    return dif


def getrankfunction(dataset):
    def rankfunction(population):
        scores = [(scorefunction(t, dataset), t) for t in population]
        # scores.sort()
        scores.sort(key=lambda tup: tup[0])
        # print (scores)
        return scores

    return rankfunction


def evolve(pc,datatype, popsize, rankfunction, maxgen=500,
           mutationrate=0.1, breedingrate=0.4, pexp=0.7, pnew=0.05):
    # Returns a random number, tending towards lower numbers. The lower pexp
    # is, more lower numbers you will get
    def selectindex():
        return int(log(random()) / log(pexp))

    # Create a random initial population
    population = [makerandomtree(pc,datatype) for i in range(popsize)]
    for i in range(maxgen):
        scores = rankfunction(population)
        print(scores[0][0])
        if scores[0][0] == 0: break

        # The two best always make it
        newpop = [scores[0][1], scores[1][1]]

        # Build the next generation
        while len(newpop) < popsize:
            if random() > pnew:
                newpop.append(mutate(
                    crossover(scores[selectindex()][1],
                              scores[selectindex()][1],
                              probswap=breedingrate),
                    pc, datatype, probchange=mutationrate))
            else:
                # Add a random node to mix things up
                newpop.append(makerandomtree(pc, datatype))

        population = newpop
    #print("winner", scores[0][1].display())
    return scores[0][1]

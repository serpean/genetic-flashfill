import logging
from copy import deepcopy
from difflib import SequenceMatcher
from math import log
from random import random, randint, choice

logger = logging.getLogger(__name__)


class FWrapper:
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
        logger.info((' ' * indent) + self.name)
        for c in self.children:
            c.display(indent + 1)

    def to_dict(self):
        return {self.name: [c.to_dict() for c in self.children]}


class ParamNode:
    def __init__(self, idx):
        self.idx = idx

    def evaluate(self, inp):
        return inp[self.idx]

    def display(self, indent=0):
        logger.info('%sp%d' % (' ' * indent, self.idx))

    def to_dict(self):
        return 'p%d' % self.idx


class ConstNode:
    def __init__(self, v):
        self.v = v

    def evaluate(self, inp):
        return self.v

    def display(self, indent=0):
        logger.info('%s%s' % (' ' * indent, self.v))

    def to_dict(self):
        return self.v


addw = FWrapper(lambda l: l[0] + l[1], ['int', 'int'], 'add')
subw = FWrapper(lambda l: l[0] - l[1], ['int', 'int'], 'subtract')
mulw = FWrapper(lambda l: l[0] * l[1], ['int', 'int'], 'multiply')
ifw = FWrapper(lambda l: l[1] if l[0] > 0 else l[2], ['int', 'int', 'int'], 'if')
gtw = FWrapper(lambda l: 1 if l[0] > l[1] else 0, ['int', 'int'], 'isgreater')
substringw = FWrapper(lambda l: l[0][l[1]: l[2]], ["str", "int", "int"], 'substring')
concatw = FWrapper(lambda l: l[0] + l[1], ["str", "str"], 'concat')
indexw = FWrapper(lambda l: l[0].index(l[1]), ["str", "str"],
                  'index')  # FIXME: String cannot contains substring. In this case, max ratio will be use

f_list = {'str': [substringw, concatw, indexw], 'int': [addw, subw]}

reverse_f_list = {
    'add': addw,
    'subtract': subw,
    'multiply': mulw,
    'if': ifw,
    'isgreater': gtw,
    'substring': substringw,
    'concat': concatw,
    'index': indexw
}


def recreate_function(input_value):
    if isinstance(input_value, dict):
        for k in input_value.keys():
            return Node(reverse_f_list[k], [recreate_function(v) for v in input_value[k]])
    elif isinstance(input_value, str) and 'p' in input_value:
        return ParamNode(int(input_value[input_value.index('p') + 1:]))
    else:
        return ConstNode(input_value)


def make_random_tree(pc, datatype, max_depth=4, fpr=0.5, ppr=0.5):
    if random() < fpr and max_depth > 0:
        f = choice(f_list[datatype])
        # Call makerandomtree with all the parameter types for f
        children = [make_random_tree(pc, type, max_depth - 1, fpr, ppr) for type in f.params]
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


def mutate(t, pc, datatype, prob_change=0.1):
    if random() < prob_change:
        return make_random_tree(pc, datatype)
    else:
        result = deepcopy(t)
        if hasattr(t, "children"):
            result.children = [mutate(c, pc, datatype, prob_change) for c in t.children]
        return result


def crossover(t1, t2, prob_swap=0.7, top=1):
    if random() < prob_swap and not top:
        return deepcopy(t2)
    else:
        result = deepcopy(t1)
        if hasattr(t1, 'children') and hasattr(t2, 'children'):
            result.params = [crossover(c, choice(t2.children), prob_swap, 0)
                             for c in t1.children if hasattr(t1, 'funtion') and hasattr(t2,
                                                                                        'funtion') and t1.funtion.params == t2.funtion.params]
        return result


def score_function(tree, s):
    dif = 0
    for data in s:
        try:
            v = tree.evaluate([data[0]])
            dif += 1 - SequenceMatcher(None, data[1], str(v)).ratio()
        except:
            dif += 1
    return dif


def get_rank_function(dataset):
    def rankfunction(population):
        scores = [(score_function(t, dataset), t) for t in population]
        # scores.sort()
        scores.sort(key=lambda tup: tup[0])
        # logger.debug(scores)
        return scores

    return rankfunction


def evolve(pc, datatype, pop_size, rank_function, max_gen=500,
           mutation_rate=0.1, breed_ingrate=0.4, p_exp=0.7, p_new=0.05):
    # Returns a random number, tending towards lower numbers. The lower pexp
    # is, more lower numbers you will get
    def selectindex():
        return int(log(random()) / log(p_exp))

    # Create a random initial population
    population = [make_random_tree(pc, datatype) for i in range(pop_size)]
    for i in range(max_gen):
        scores = rank_function(population)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(scores[0][0])
        if scores[0][0] == 0: break

        # The two best always make it
        newpop = [scores[0][1], scores[1][1]]

        # Build the next generation
        while len(newpop) < pop_size:
            if random() > p_new:
                newpop.append(mutate(
                    crossover(scores[selectindex()][1],
                              scores[selectindex()][1],
                              prob_swap=breed_ingrate),
                    pc, datatype, prob_change=mutation_rate))
            else:
                # Add a random node to mix things up
                newpop.append(make_random_tree(pc, datatype))

        population = newpop
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("winner", scores[0][1].display())
    return scores[0][1]

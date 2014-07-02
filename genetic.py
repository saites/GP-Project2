from random import *
from copy import deepcopy
from numpy import *

class Primitive:
    def __init__(self,maxChildren):
        self.children = None
        self.maxChildren = maxChildren
    def getDepth(self):
        return max([0]+[c.getDepth() for c in self.children if c])+1
    def __str__(self):
        return ""
    def makeRand(self):
        pass

class Terminal:
    def __init__(self):
        pass
    def getDepth(self):
        return 1
    def __str__(self):
        return ""
    def makeRand(self):
        pass

def getNodeList(node):
    if isinstance(node, Terminal):
        return []
    nList = []
    toProcess = [node]
    while toProcess:
        node = toProcess.pop()
        nList += [node]
        toProcess += [n for n in node.children if isinstance(n,Primitive)]
    return nList

def chooseRandomPrimitive(prgm):
    return choice(getNodeList(prgm))

def crossOver(pgma, pgmb, crossDepth):
    pgm1 = deepcopy(pgma)
    pgm2 = deepcopy(pgmb)
    p1 = chooseRandomPrimitive(pgm1)
    p2 = chooseRandomPrimitive(pgm2)

    c1i = randint(0,len(p1.children)-1)
    c1 = p1.children.pop(c1i)

    c2i = randint(0,len(p2.children)-1)
    c2 = p2.children.pop(c2i)

    p2.children.insert(c2i, c1)
    p1.children.insert(c1i, c2)

    if pgm1.getDepth() > crossDepth:
        pgm1 = deepcopy(pgma)
    if pgm2.getDepth() > crossDepth:
        pgm2 = deepcopy(pgmb)
    return [pgm1, pgm2]


class GeneticProgram:
    def __init__(self, primitives, terminals, metric, crossDepth=20,
                 crossProb=.95, mutateProb=.05):
        self.primitives = primitives
        self.terminals = terminals
        self.crossDepth = crossDepth
        self.crossProb = crossProb
        self.mutateProb = mutateProb
        self.metric = metric

    def genNode(self, depth, toDepth):
        if depth > toDepth:
            return None
        if depth == toDepth:
            n = choice(self.terminals)()
            n.makeRand()
        else:
            n = choice(self.primitives)()
            n.makeRand()
            n.children = [self.genNode(depth+1, toDepth) \
                for i in xrange(n.maxChildren)] 
        return n
        
    def genPopulation(self, popSizeDict):
        '''
        popSizeDict should be a dictionary that tells how many individuals
        should be built at each size:
            {1: 50, 2: 50, 3: 30} creats 50 at each depth 1 and 2, and 
            30 more at depth 3.
        '''
        self.population = []
        for depth in popSizeDict:
            self.population +=\
                [self.genNode(0, depth) for i in xrange(popSizeDict[depth])]
            
    def breed(self):
        if len(self.population) == 1:
            return

        self.fitness = [(pgm, self.metric(pgm)) for pgm in self.population]
        self.fitness.sort(lambda x,y : x[1] - y[1])

        if self.fitness[-1][1] != 0:
            fsum = float(sum(f[1] for f in self.fitness))
        else:
            fsum = 1.
        percent = array([f[1] / fsum for f in self.fitness])
        for i in xrange(len(percent)-1):
            percent[i+1] += percent[i]

        newpop = deepcopy([self.fitness[-1][0]])
        while len(newpop) < len(self.population):
            n1 = deepcopy(self.fitness[where(percent >=\
                    random.random())[0][0]][0])
            if random.random() < self.crossProb \
                and not isinstance(n1, Terminal):
                n2 = n1
                while n1 == n2 or isinstance(n2, Terminal):
                    n2 = self.fitness[where(percent >=\
                        random.random())[0][0]][0]
                n1, n2 = crossOver(n1,n2,self.crossDepth)
                newpop.append(n2)
            if random.random() < self.mutateProb:
                n1 = self.genNode(0, randint(2, randint(3,6)))
            newpop.append(n1)

        if len(newpop) > len(self.population):
            newpop = newpop[:len(self.population)-len(newpop)]        
        self.population = newpop

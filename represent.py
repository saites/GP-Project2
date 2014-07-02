from genetic import *
import random
from numpy import *

class RandNumber(Terminal):
    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return str(self.value)

    def makeRand(self):
        self.value = random.random()

class PixelValue(Terminal):
    def __init__(self, x=0,y=0):
        self.x=x
        self.y=y

    def __str__(self):
        return "image[%d,%d]" % (self.y,self.x)

    def makeRand(self):
        self.x = random.randint(0,27)
        self.y = random.randint(0,27)

class BoxValue(Terminal):
    def __init__(self, a=0,b=0,c=0,d=0):
        self.bounds = (a,b,c,d)

    def __str__(self):
        return "sum(image[%d:%d,%d:%d])" % self.bounds

    def makeRand(self):
        self.bounds = tuple([random.randint(0,27) for i in xrange(4)])

class Operation(Primitive):
    SUM,SUB,MUL,DIV = range(4)
    OPSTR = dict(zip(xrange(4), ['+','-','*','/']))
    def __init__(self, op=0):
        Primitive.__init__(self, 2)
        self.op = op
        self.children = None
    
    def __str__(self):
        return "(%s %s %s)" % \
        (str(self.children[0]), Operation.OPSTR[self.op], str(self.children[1]))

    def makeRand(self):
        self.op = random.randint(0,3)

def getAnswer(node, image):
    if isinstance(node, RandNumber):
        return node.value
    elif isinstance(node, PixelValue):
        return image.reshape(28,28)[node.y, node.x]
    elif isinstance(node, BoxValue):
        return sum(image.reshape(28,28)[node.bounds[0]:node.bounds[1],\
            node.bounds[2]:node.bounds[3]])
    elif isinstance(node, Operation):
        c1 = getAnswer(node.children[0], image)
        c2 = getAnswer(node.children[1], image)
        if node.op == Operation.DIV and c2 == 0:
            return float('inf')
        else:
            return eval("%d %s %d" % (c1, Operation.OPSTR[node.op], c2))
    
def execute(node, dataset):
    hit = 0
    for idx, image in enumerate(dataset):
        if (idx/(len(dataset)/10)) == int(getAnswer(node, image) % 10):
            hit += 1
    return hit

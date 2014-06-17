from numpy import *
from pandas import read_csv
import random
from genetic import *
from represent import *

PATH = 'MNISTData'
programsLoc = 'programs'

# get images
data = read_csv(PATH+'/train.csv',delimiter=',').values
train_targets = data[:,0]
train_images = data[:,1:]
targets = identity(10) * 2 - 1
#test_images = read_csv(PATH+'/test.csv',delimiter=',').values

NUM_TRAIN = len(train_images)
#NUM_TEST  = len(test_images) 
NUM_DIGITS = 10

train_images = train_images[:1000]
train_targets = train_targets[:1000]

def metric(pgm):
    return execute(pgm, train_images, train_targets)

primitives = [Operation]
terminals = [RandNumber, PixelValue]
GP = GeneticProgram(primitives, terminals, metric, mutateProb=.1)

GP.genPopulation(dict(zip(range(1,6), [100]*5)))

for i in range(100):
    print i
    GP.breed()
    print [n[1] for n in GP.fitness]
    with open('%s/pgm%d.py' % (programsLoc, i), 'w') as F:
        F.write("from numpy import *\n")
        F.write("from pandas import read_csv\n")
        F.write("set_printoptions(suppress=True)\n")
        F.write("def getAns(image):\n")
        F.write("\treturn ")
        F.write(str(GP.fitness[-1][0])+"\n\n\n")
        F.write("PATH = '../MNISTData'\n")
        F.write("data = read_csv(PATH+'/train.csv',delimiter=',').values\n")
        F.write("train_targets = data[:,0]\n")
        F.write("train_images = data[:,1:]\n\n")
        F.write("conf = zeros((10,10))\n")
        F.write("invalid = 0\n")
        F.write("hits = 0\n")
        F.write("for i in range(len(train_images)):\n")
        F.write("\tprint i\n")
        F.write("\tbelief = int(getAns(train_images[i].reshape(28,28)))\n")
        F.write("\tif belief >= 0 and belief < 10:\n")
        F.write("\t\tconf[train_targets[i], belief] += 1\n")
        F.write("\t\tif belief == train_targets[i]:\n")
        F.write("\t\t\thits += 1\n")
        F.write("\telse:\n")
        F.write("\t\tinvalid += 1\n\n")
        F.write("print conf\n")
        F.write("print 'invalid:', invalid\n")
        F.write("print 'hits:', hits\n")
        F.write("print 'hit%:', float(hits)/float(len(train_images)-invalid)\n")

from numpy import *
from matplotlib.pyplot import plot,show,imshow
from pandas import read_csv
import random
from genetic import *
from represent import *

# constants
PATH = 'MNISTData'
programsLoc = 'programs'

# parameters
numGens = 300

# get dataset
data = read_csv(PATH+'/train.csv',delimiter=',').values
train_targets = data[:,0]
train_images = data[:,1:]
targets = identity(10) * 2 - 1
train_images = concatenate([train_images[train_targets==i][:100] \
                        for i in xrange(10)])
train_images = train_images.astype(float)/255.0

# genetic program
def metric(pgm):
    return execute(pgm, train_images)
primitives = [Operation]
terminals = [RandNumber, PixelValue, BoxValue]
GP = GeneticProgram(primitives, terminals, metric, mutateProb=.15)
GP.genPopulation(dict(zip(xrange(2,7), [100]*5)))

# genetic algorithm
keepfit = zeros((numGens,1))
avgfit = zeros((numGens,1))
for i in xrange(numGens):
    print i
    GP.breed()
    allfit = [n[1] for n in GP.fitness]
    print allfit
    keepfit[i] = allfit[-1]
    avgfit[i] = mean(allfit)
    
    #write out the best program from this generation
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
        F.write("for i in xrange(len(train_images)):\n")
        F.write("\tprint i\n")
        F.write("\tbelief = int(getAns(train_images[i].reshape(28,28))%10)\n")
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

# plot something useful
plot(keepfit)
show()
plot(avgfit)
show()

import random
import string
import matplotlib.pyplot as graph
from difflib import SequenceMatcher

PASSWORD = input("Enter Password:")
NUM_CHARS = len(PASSWORD)

def createFirstValues():
    values = []
    global NUM_CHARS
    word = ""
    letters = string.ascii_letters
    for i in range(0,200):
        for j in range(0,NUM_CHARS):
            word += random.choice(letters)
        values.append(word)
        word = ""
    return values

def calcFitness(member):
    global PASSWORD
    global NUM_CHARS
    numSimilar = 0
    for i in range(0,NUM_CHARS):
        if member[i] == PASSWORD[i]:
            numSimilar+=1
    fitness = numSimilar/NUM_CHARS
    return fitness

def findGenFitness(generation):
    fitnesses = []
    for member in generation:
        fitnesses.append(calcFitness(member))
    return fitnesses

def mutate(member):
    letters = string.ascii_letters
    newMember = list(member)
    global NUM_CHARS

    slot = random.randint(0,NUM_CHARS-1)
    newMember[slot] = random.choice(letters)
    newMember = ''.join(newMember)

    return newMember

def mutateGeneration(topBred):
    nextGeneration = []
    for member in topBred:
        for i in range(0,21):
            nextGeneration.append(mutate(member))
    return nextGeneration

def crossover(topGeneration):
    global NUM_CHARS
    bredGeneration = []
    for i in range(0,len(topGeneration)):
        parent1 = topGeneration[random.randint(0,len(topGeneration)-1)]
        parent2 = topGeneration[random.randint(0,len(topGeneration)-1)]
        parent2 = list(parent2)
        bredMember = list(parent1)
        selectionpoint1 = random.randint(0,NUM_CHARS-1)
        selectionpoint2 = random.randint(0,NUM_CHARS-1)
        if(selectionpoint2 > selectionpoint1):
            bredMember[selectionpoint1:selectionpoint2] = parent2[selectionpoint1:selectionpoint2]
        else:
            bredMember[selectionpoint2:selectionpoint1] = parent2[selectionpoint2:selectionpoint1]
        bredGeneration.append(''.join(bredMember))
    return bredGeneration

def sortByFitness(generation,fitness):
    fitGen = zip(fitness,generation)
    fitGen = sorted(fitGen,reverse = True)
    sortedGen = [gen for fit,gen in fitGen]
    sortedFit = [fit for fit,gen in fitGen]
    return sortedGen,sortedFit

def getTopMembers(sortedGen, sortedFit):
    topMembers = sortedGen[0:5]
    topFitness = sortedFit[0:5]
    return topMembers, topFitness

def getRandomMembers(sortedGen, sortedFit):
    randMemb = []
    randFit = []
    for i in range(5):
        rand = random.randint(0,len(sortedGen) - 1)
        randMemb.append(sortedGen[rand])
        randFit.append(sortedFit[rand])
    
    return randMemb

def mergeTopRand(topMembers, topFitness,randMembers):
    for member in randMembers:
        topMembers.append(member)
    return topMembers

def createNewGeneration(members):
    fitness = findGenFitness(members)
    sortedGen, sortedFit = sortByFitness(members,fitness)
    topMembers, topFitness = getTopMembers(sortedGen,sortedFit)
    randMembers = getRandomMembers(sortedGen,sortedFit)
    newParents = mergeTopRand(topMembers,topFitness,randMembers)
    lastGenBest = topFitness[0]
    lastGenBestMemb = topMembers[0]
    if lastGenBest < 0.90:
        bredGeneration = crossover(newParents)
        newGeneration = mutateGeneration(bredGeneration)
    else:
        newGeneration = mutateGeneration(newParents)
    return newGeneration, lastGenBest, lastGenBestMemb

def correct(topFitness):
    if topFitness == 1:
        return True
    else:
        return False

numGens = 0
avgGens = 0
totalGens = 0
x = []
y = []
test = input("run multiple tests? (y/n)")

if(test=='y'):
    test = True
else:
    test = False

if(test):
    numReps = int(input("Enter Number of reps: "))
    for i in range(0,numReps):
        generation = createFirstValues()
        isFound = False
        numGens = 0

        while not isFound:
            numGens+=1
            generation, lastGenBest, lastGenBestMemb = createNewGeneration(generation)
            isFound = correct(lastGenBest)

        print(numGens)
        totalGens += numGens
        x.append(i+1)
        y.append(numGens)
    graph.xlabel('# of Cycles')
    graph.ylabel('# of Generations')
    avgGens = totalGens/numReps
    print(avgGens)
else:
    isFound = False
    generation = createFirstValues()
    numGens = 0
    while not isFound:
        numGens+=1
        generation, lastGenBest, lastGenBestMemb = createNewGeneration(generation)
        isFound = correct(lastGenBest)
        print(lastGenBest)
        print(lastGenBestMemb)
        print(numGens)
        x.append(numGens)
        y.append(lastGenBest)
    graph.xlabel("# of Generations")
    graph.ylabel('Fitness')

graph.plot(x,y)
graph.show()
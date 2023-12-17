# Anirudh Gupta

# 11/26/23

# This is the final code for the Picobot Final Project

# The goal of this project is to write a genetic algorithm 
# that writes a program that can solve a picobot maze

import random
import copy

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5

POSSIBLE_SURROUNDINGS = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx']

class Program:
    def __init__(self):
        """Constructor for Program Objects
           Does not take any arguments
           Programs only have a rules attribute which is a dictionary
        """ 
        self.rules = {}

    def __repr__(self):
        """Represents the rules in a program object in a sorted order
        """
        unsortedKeys = list(self.rules.keys()) 
        sortedKeys = sorted(unsortedKeys)

        sortedRules = ""
        for x in range(len(self.rules)):
            if(len(sortedRules) > 0 and sortedRules[-14] != str(sortedKeys[x][0])):
                sortedRules += "\n"
            sortedRules += str(sortedKeys[x][0]) + " " + sortedKeys[x][1] + " -> " + self.rules[sortedKeys[x]][0] + " " + str(self.rules[sortedKeys[x]][1]) + "\n"

        return sortedRules

    def randomize(self):
        """Generates a random, full set of rules for the rules dictionary
        """
        for x in range(NUMSTATES):
            for y in POSSIBLE_SURROUNDINGS:
                possible_steps = []
                for step in 'NEWS':
                    if step not in y:
                        possible_steps += [step]
                self.rules[(x, y)] = (random.choice(possible_steps), random.randint(0, NUMSTATES - 1))

    def getMove(self, state, surroundings):
        """Accepts and integer state and string surroundings
           Returns tuple containing direction and new state 
           corresponding to the state and string in self.rules
        """

        return self.rules[(state, surroundings)]
    
    def mutate(self):
        """Chooses a random rule from self.rules and changes move
           and new state for that rule. Changed rule is different
           from original
        """

        change_key = random.choice(list(self.rules.keys()))
        while True:
            possible_steps = []
            for step in 'NEWS':
                if step not in change_key[1]:
                    possible_steps += [step]
            mutation = (random.choice(possible_steps), random.randint(0, NUMSTATES - 1))
            if(self.rules[change_key] != mutation):
                self.rules[change_key] = mutation
                break
    
    def crossover(self, other):
        """Accepts an other object of type Program.
           Returns an offspring of type program with
           some elements of self and some of other
        """
        offspring = copy.deepcopy(other)
        crossoverState = random.randint(1, NUMSTATES - 1)

        for x in range(crossoverState):
            for y in POSSIBLE_SURROUNDINGS:
                offspring.rules[(x, y)] = self.rules[(x,y)]

        return offspring
    
    def __gt__(self, other):
            """Greater-than operator -- works randomly, but works!"""
            return random.choice([True, False])

    def __lt__(self, other):
        """Less-than operator -- works randomly, but works!"""
        return random.choice([True, False])
    


class World:
    def __init__(self, initial_row, initial_col, program):
        """Constructor for the World Class
        """
        self.row = initial_row
        self.col = initial_col
        self.state = 0
        self.program = program
        self.room = [[' ']*WIDTH for row in range(HEIGHT)]
        for x in range(WIDTH):
              self.room[0][x] = '+'
              self.room[HEIGHT-1][x] = "+"
        for y in range(HEIGHT):
              self.room[y][0] = '+'
              self.room[y][WIDTH-1] = "+"
        self.room[self.row][self.col] = "P"

    def __repr__(self):
        """returns a string representation of the room
           " " for unvisited cells, "+" for walls
           "P" for picobot, "o" for visisted cells
        """
        drawroom = ""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                drawroom += self.room[y][x]
            drawroom += "\n"
        
        return drawroom
    
    def getCurrentSurroundings(self):
        """returns the surrounding string of the current picobot position
        """
        surroundings = ""
        if(self.room[self.row - 1][self.col] == "+"):
            surroundings += "N"
        else:
            surroundings += "x"
        if(self.room[self.row][self.col + 1] == "+"):
            surroundings += "E"
        else:
            surroundings += "x"
        if(self.room[self.row][self.col - 1] == "+"):
            surroundings += "W"
        else:
            surroundings += "x"
        if(self.room[self.row + 1][self.col] == "+"):
            surroundings += "S"
        else:
            surroundings += "x"

        return surroundings
    
    def step(self):
        """Moves the picobot one step, updates the room, and
           updates the state, row, and column of picobot
        """

        surroundings = self.getCurrentSurroundings()
        nextRule = self.program.getMove(self.state, surroundings)
        nextMove = nextRule[0]
        nextState = nextRule[1]

        if(nextMove == "N"):
            self.room[self.row][self.col] = "o"
            self.room[self.row - 1][self.col] = "P"
            self.row = self.row - 1
        elif(nextMove == "E"):
            self.room[self.row][self.col] = "o"
            self.room[self.row][self.col + 1] = "P"
            self.col = self.col + 1
        elif(nextMove == "W"):
            self.room[self.row][self.col] = "o"
            self.room[self.row][self.col - 1] = "P"
            self.col = self.col - 1
        else:
            self.room[self.row][self.col] = "o"
            self.room[self.row + 1][self.col] = "P"
            self.row = self.row + 1

        self.state = nextState

    def run(self, steps):
        """Executes the number of steps entered
        """
        for x in range(steps):
            self.step()

    def fractionVisitedCells(self):
        """Returns floating point fraction of cells in self.room that
           have been visited. Aka Fitness Score
        """
        totalCells = (HEIGHT - 2) * (WIDTH - 2)
        visitedCells = 0

        for y in range(HEIGHT):
            for x in range(WIDTH):
                if(self.room[y][x] == "P" or self.room[y][x] == "o"):
                    visitedCells += 1
        
        return visitedCells/totalCells
    

def generatePrograms(popSize):
    """generates a list of picobot programs of of size popSize
    """
    programs = []
    for x in range(popSize):
        program = Program()
        program.randomize()
        programs.append(program)

    return programs

def evaluateFitness(program, trials, steps):
    """Measures the fitness(fractionVisitedCells) of the input program over the given 
       number of steps with (trials) amount of different starting picobot positions
    """

    fitnessTotal = 0

    for x in range(trials):
        col = random.randint(1, WIDTH - 2)
        row = random.randint(1, HEIGHT - 2)
        simulation = World(row, col, program)
        simulation.run(steps)
        fitnessTotal += simulation.fractionVisitedCells()

    return round(fitnessTotal/trials, 4)

def GA(popsize, numgens):
    """Using a genetic algorithm creates a program that can solve or get close to 
       solving an empty picobot maze. Popsize is the number of programs per generation
       and numgens in the number of generations
    """
    print()
    print("Fitness is measured using 20 random trials and running for 800 steps per trial:")
    initialPopulation = generatePrograms(popsize)

    for y in range(numgens):
        L = []
        averagefitness = 0
        for prog in initialPopulation:
            L.append((evaluateFitness(prog, 20, 800), prog))
        for x in L:
            averagefitness += x[0]
        
        averagefitness = averagefitness/popsize
        L = sorted(L)
        bestfitness = L[popsize-1][0]
        bestProgram = L[popsize-1][1]

        print()
        print("Generation", y)
        print(" Average Fitness: ", averagefitness)
        print(" Best Fitness: ", bestfitness)

        while(len(L) > 0.1*popsize):
            L.pop(L.index(min(L)))

        childrenList = []
        for x in range(popsize):
            parent1 = random.choice(L)
            parent2 = random.choice(L)
            child = parent1[1].crossover(parent2[1])
            child.mutate()
            childrenList.append(child)
        
        initialPopulation = childrenList

    print()
    print("Best Picobot program:")
    print(bestProgram)





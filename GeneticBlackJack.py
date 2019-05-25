from random import random,randint
import argparse
import BlackJack

dna_bits = 20
population_size = 20

def coin(p) :
    if random() < p :
        return 1
    else :
        return 0

def tournament(c1_f1,c2_f2) :
    c1, f1 = c1_f1
    c2, f2 = c2_f2
    if f1 > f2 : return c1,fitness(c1)
    return c2,fitness(c2)

def selection(population_fitness) :
    N = len(population_fitness)
    new_population =[]
    for i in range(N) :
        i1, i2 = randint(0,N-1), randint(0,N-1)
        c1_f1 = population_fitness[i1]
        c2_f2 = population_fitness[i2]
        nc_nf = tournament(c1_f1,c2_f2)
        new_population.append(nc_nf)
    return new_population

def random_individual(n) :
    P=[]
    for i in range(n) :
        v=coin(0.5)
        P.append(v)
    return P

def fitness(s) :
    temp = ''.join(str(x) for x in s)
    pBoundary = int(temp[:5],2)
    dBoundary = int(temp[5:],2)
    print(pBoundary)
    print(dBoundary)
    def strategy (pHand, dHand, used) :
        pScore = BlackJack.Score(pHand)
        dScore = BlackJack.Score(dHand)
        if pScore < pBoundary and dScore < dBoundary and pScore < 21 :
            return True
        else : return False
    game = BlackJack.BlackJack(100,strategy).game_result
    
    return sum(game)/len(game)

def crossover(c1_f1,c2_f2) :
    c1, f1 = c1_f1
    c2, f2 = c2_f2
    p = randint(0,len(c1)-1)
    nc1 = c1[:p] + c2[p:]
    nc2 = c2[:p] + c1[p:]
    nc1_nf1 = nc1, fitness(nc1)
    nc2_nf2 = nc2, fitness(nc2)
    return nc1_nf1, nc2_nf2

def activate_crossover(rate, population_fitness) :
    N = len(population_fitness)
    new_population = []
    n=int(N/2)
    for i in range(n) :
        i1, i2 = randint(0, N-1), randint(0, N-1)
        c1_f1 = population_fitness[i1]
        c2_f2 = population_fitness[i2]
        if random() > rate :
            new_population.append(c1_f1)
            new_population.append(c2_f2)
        else :
            nc1_nf1, nc2_nf2 = crossover(c1_f1, c2_f2)
            new_population.append(nc1_nf1)
            new_population.append(nc2_nf2)
            #print ("CROSSOVER!!!! {},{} -> {},{}".format(c1_f1, c2_f2, nc1_nf1, nc2_nf2))
    return new_population


def activate_mutation(rate, population_fitness) :
    N = len(population_fitness)
    new_population = []
    for i in range(N) :
        if random() > rate :
            new_population.append(population_fitness[i])
        else :
            nc_nf = mutation(population_fitness[i])
            new_population.append(nc_nf)
            # print("Mutation!!! {} -> {}".format(population_fitness[i],nc_nf))
    return new_population




def initial_population(N,n) :
    P = []
    for i in range(N) :
        c = random_individual(n)
        P.append(c)
    return P


def mutation(c1_f1) :
    c1, f1 = c1_f1
    n=len(c1)
    p = randint(0,n-1)
    nc1 = c1[:]
    nc1[p] = 1 - nc1[p]
    return nc1, fitness(nc1)


if __name__ =='__main__' :

    pop_size = 20
    dna_bits = 10
    prob_cross = 0.6
    prob_mut = 0.05
    iter_num = 30

    population_size = pop_size
    dna_bits = dna_bits

    fileName = str(pop_size)+'_'+str(dna_bits)+'_'+str(prob_cross)+'_'+str(prob_mut)+'_'+str(iter_num)
    print(fileName)
    P = initial_population(population_size, dna_bits)

    pop_fit = []
    yValue=[]

    for s in P:
        s_f = s, fitness(s)
        pop_fit.append(s_f)

    for i in range(iter_num):
        tempY = 0
        for n in range(len(pop_fit)):
            c1, f1 = pop_fit[n]
            tempY = tempY + f1
        yValue.append(tempY)
        print("yValue : {}".format(yValue))


        pop_fit = selection(pop_fit)
        pop_fit = activate_crossover(prob_cross, pop_fit)
        pop_fit = activate_mutation(prob_mut, pop_fit)
        print ("{}".format(pop_fit))


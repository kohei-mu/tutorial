#/usr/bin/env python
# -*- coding: utf-8 -*-

import random, math

def hillclimboptimize(maxcount=5000, step=0.001):
    vec = random.randint(-2, 2)
    count = 0
    while count < maxcount:
        _dir = random.randint(0,1)
        _dir = (_dir - 0.5) * step
        newvec = vec + _dir
        newcost = costf(newvec)
        cost = costf(vec)
        if newcost < cost:
            vec = newvec
        count += 1
    return vec

def annealingoptimazaion(T=10000, cool=0.99, step=1):
    vec = random.randint(-2, 2)
    while T > 0.0001:
        _dir = random.random()
        _dir = (_dir - 0.5) * step
        newvec = vec + _dir
        newcost = costf(newvec)
        cost = costf(vec)
        p = pow(math.e, -abs(newcost - cost) / T)
        if newcost < cost or random.random() < p:
            vec = newvec
        T = T * cool
    return vec

class geneticoptimize():
    def __init__(self, popnum=None, popsize=None, step=None, mutprob=None, elite=None, maxiter=None):
        self.popnum = popnum
        self.popsize = popsize
        self.step = step
        self.mutprob = mutprob
        self.elite = elite
        self.maxiter = maxiter

    def mutate(self, vec):
        i = random.randint(0, self.popnum-1)
        return vec[0:i] + [random.randint(0,9)] + vec[i+1:]

    def crossover(self, r1, r2):
        i = random.randint(1, self.popsize-2)
        return r1[0:i] + r2[i:]

    def convertn(self, vec):
        x, y= 0, 0
        for v in vec:
            x += v * (10**y)
            y -= 1
        return x

    def main(self):
        pop = []
        for i in range(self.popsize):
            vec = [random.randint(0,9) for v in range(0, self.popnum)]
            pop.append(vec)
        topelite = int(self.elite * self.popsize)
        scores = []
        for i in range(self.maxiter):
            for vec in pop:
                x = self.convertn(vec)
                scores.append([costf(x), vec])
            scores.sort()
            ranked = [v for (s,v) in scores]
            pop = ranked[0:topelite]
            while len(pop) < self.popsize:
                if random.random() < self.mutprob:
                    c = random.randint(0, topelite)
                    pop.append(self.mutate(ranked[c]))
                else:
                    c1 = random.randint(0, topelite)
                    c2 = random.randint(0, topelite)
                    pop.append(self.crossover(ranked[c1], ranked[c2]))
        return self.convertn(scores[0][1])

def costf(x):
    f = (3*(x**4)) - (5*(x**3)) + (2*(x**2))
    return f

if __name__ == "__main__": 
    print "hillclimboptimize:",hillclimboptimize()
    print "annealingoptimazaion:",annealingoptimazaion()
    gene = geneticoptimize(popnum=6, popsize=10, step=1, mutprob=0.2, elite=0.2, maxiter=500)
    print "geneticoptimize:",gene.main()



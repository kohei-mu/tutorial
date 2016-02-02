import random
import math

def hillclimboptimize(maxcount=5000, cool=0.95, step=0.001):
	vec = random.randint(-2, 2)
	print "start =",vec

	count = 0

	while count < maxcount:
		dir = random.randint(0,1)
		if dir == 0:
			dir = -step
		else:
			dir = step

		newvec = vec + dir

		newcost = costf(newvec)
		cost = costf(vec)

		if newcost < cost:
			vec = newvec

		count += 1
	return vec


def annealingoptimazaion(T=10000, cool=0.99, step=1):
	vec = random.randint(-2,2)

	while T > 0.0001:

		dir = random.random()
		dir = (dir - 0.5) * step

		newvec = vec + dir

		newcost = costf(newvec)
		cost = costf(vec)

		p = pow(math.e, -abs(newcost - cost) / T)
		#print p 

		if newcost < cost or random.random() < p:
			vec = newvec

		T = T * cool

	return vec


def geneticoptimize(popnum=6, popsize=10, step=1, mutprob=0.2, elite=0.2, maxiter=500):

	def mutate(vec):
		i = random.randint(0, popnum-1)
		return vec[0:i] + [random.randint(0,9)] + vec[i+1:]

	def crossover(r1, r2):
		i = random.randint(1, popsize-2)
		return r1[0:i] + r2[i:]

	pop = []
	for i in range(popsize):
		vec = [random.randint(0,9) for v in range(0, popnum)]
		pop.append(vec)

	topelite = int(elite * popsize)

	scores = []
	for i in range(maxiter):
		for vec in pop:
			x = convertn(vec)
			scores.append([costf(x), vec])
		scores.sort()
		ranked = [v for (s,v) in scores]

		pop = ranked[0:topelite]

		while len(pop) < popsize:
			if random.random() < mutprob:
				c = random.randint(0, topelite)
				pop.append(mutate(ranked[c]))
			else:
				c1 = random.randint(0, topelite)
				c2 = random.randint(0, topelite)
				pop.append(crossover(ranked[c1], ranked[c2]))

	return convertn(scores[0][1])


def convertn(vec):
	x, y= 0, 0
	for v in vec:
		x += v * (10**y)
		y -= 1

	return x

def costf(x):
	f = (3*(x**4)) - (5*(x**3)) + (2*(x**2))

	return f

print "hillclimboptimize:",hillclimboptimize(),"\n"
print "annealingoptimazaion:",annealingoptimazaion(),"\n" 
print "geneticoptimize:",geneticoptimize()









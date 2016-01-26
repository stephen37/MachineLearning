import numpy as np
from pprint import pprint
import random

n = 10 ** 6
data = 10 ** 14 + np.random.uniform(0,1,n)

def mean_variance_np():
  

    variance = np.var(data)
    print(variance)

    mean = np.mean(data)
    print("moyenne" +str(mean))

#mean_variance_np()

def mean_variance() :
    res = 0
    for elt in data :
        res += elt

    mean = res/len(data)
    print("moyenne", mean)

    var = 0

    for elt in data :
        var += (elt - mean)**2
    
    print("variance : ", var/(len(data) -1))

    
#mean_variance()

def Welford(x) :
    s = []
    s_0 = 0
    m = []
    m_0 = x[0]
    m.append(m_0)
    s.append(0)

    for k in range(1, len(x)) :
        m.append(m[k-1] + (x[k] - m[k-1]) / k)
        s.append(s[k-1] + (x[k] - m[k-1]) * (x[k] - m[k]))
                         
    return m[len(m)-1] , s[len(s) - 1] / (len(x) - 1)

#welfordMean, welfordVar = Welford(data)

#print(welfordMean, welfordVar)



''' Exercice 3

4) Detection de spam, detection de voiture

'''
    

def data_reader(filename):
    to_binary = {"?": 3, "y": 2, "n": 1}
    labels = {"democrat": 1, "republican": -1}

    data = []
    for line in open(filename, "r"):
        line = line.strip()

        label = int(labels[line.split(",")[0]])
        observation = np.array([to_binary[obs] for obs in line.split(",")[1:]] + [1])
        data.append((label, observation))

    return data

data_read = data_reader("./house-votes-84.data")


def data_shuffle(data) :
    return random.shuffle(data) 

data_shuffle(data_read)


def spam_reader(filename):
    to_binary = {1: 1, 0: -1}
    data = []
    for line in open(filename, "r"):
        line = line.strip()
        label = to_binary[int(line.split(",")[-1])]
        observation = [float(obs) for obs in line.split(",")[:-1] + [1.0]]

        data.append((label, np.array(observation)))
        
    return data


data_learning = data_read[100:]
data_test = data_read[:100]


def classify(observation, vect) :
    if len(observation) == len(vect) :
        n = len(observation)
        res = 0.0
        for i in range(n) :
            res += vect[i] * observation[i]
    
        if res >= 0 :
            return 1
        else :
            return -1

    else:
        return "Erreur"


vect_test = [25, -12, 67, -104, -43, 46, -18, -10, 45, -33, 54, -39, 43, -19, 5, -2, 55]

def test(corpus, vect) :
    nbErrors = 0

    for line in corpus :
#        pprint(line)
        if line[0] != classify(line[1], vect) :
            nbErrors +=1

    return (1.0 * nbErrors / len(corpus)) * 100

print("value de test = ", test(data_test, vect_test))


def learn(corpus, nbPass) :
    w = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    errors = True
    while errors :
        for line in corpus : 
            if line[0] != classify(line[1], w):
                w += line[0] * line[1]
            else :
                errors = False
    return w

print(test(data_test, (learn(data_learning, 100000))))

#print(learn(data_test, 10))

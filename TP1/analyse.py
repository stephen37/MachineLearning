import re
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
import operator
import codecs

def nbJugements():
    corpus = open("./movie_lens.csv")
    '''
    allJudgement = []
    for line in corpus :
        line = line.split("|")
        line = line[0] + line[1]
        if not line in allJudgement :
            allJudgement.append(line)
    return allJudgement
    '''
    return len(corpus.readlines())
print("Nb jugements : " , nbJugements())


def nbUsers() :
    corpus = open("./test.csv")
    userList = []
    for line in corpus :
        user = line.split("|")[0]
        if (user not in userList):
            userList.append(user)

    return len(userList)

print("Nb users :", nbUsers())

def nbMovies() :
    corpus = open("./movie_lens.csv")
    moviesList = []
    for line in corpus :
        movie = line.split("|")[1]
        if (movie not in moviesList):
            moviesList.append(movie)

    return len(moviesList)

print("Nb movies : " , nbMovies())


def listMovies() :
    corpus = open("./movie_lens.csv")
    moviesList = []
    for line in corpus :
        movie = line.split("|")[1]
        if (movie not in moviesList):
            moviesList.append(movie)

    return moviesList




def mostRecentMovie():
    corpus = open("./movie_lens.csv")
    datesList = []
    min  = 20000000
    max  = 0
    for line in corpus :
        movie = line.split("|")[1]
        splitMovie = movie.split("(")
        date = re.search(r"\([1-9][0-9]{3}\)", movie)
        if date :
            date = date.group(0).replace("(", "").replace(")", "")
            date = int(date)
            if date < min:
                min = date
            if date > max :
                max = date     
    return ("min = " , min , "max = " , max)


print ("Most recent movie : " , mostRecentMovie())

def drawDistribNotes() :
    corpus = open("./movie_lens.csv")
    result = []

    for line in corpus :
        note = line.split("|")[2]
        note = int(note)

        result.append(note)
            
    plt.hist(result, 5, facecolor='g')
    plt.xlabel('notes')
    plt.ylabel('Number')
    plt.title('Histogram of notes')
    plt.axis([0, 5, 0, 50000])
    plt.grid(True)
    plt.show()


#drawDistribNotes()

'''

Moyenne  : 3.52 +- 1.13
105.72 +- 100,57

judgementsmin = 19; max 736
'''

    
def calcMeanAndVariance() :
    
    corpus = open("./movie_lens.csv")
    infoOnUsers = {}
    meanAndVarianceUser = {}

    for line in corpus :
        user = line.split("|")[0]
        movie = line.split("|")[1]
#        movie = re.sub(r" \([1-9][0-9]{3}\)", "", movie)
        
        note = line.split("|")[2]
        note = int(note.split("\n")[0])
        nbJuge = "nbJugements"
        if user not in infoOnUsers :
            infoOnUsers[user] = {movie: note}
        else :
            if movie not in infoOnUsers[user].keys() : 
                infoOnUsers[user][movie] = note



                
    smallestNbJudgements = 100000000000
    biggestNbJudgements = 0
    for user in infoOnUsers :
        sumNotes = 0
        sumVariance = 0
        if user not in meanAndVarianceUser :
            #sumNotes = sum(infoOnUsers[user].values())
            varianceNp = np.std(list(infoOnUsers[user].values()))
#            print("variance numpy", varianceNp)
            for value in infoOnUsers[user].values() :
#                value = int(value)
                sumNotes += value
                
#                print("value = ", int(value))
                nbNotes =  len(infoOnUsers[user].keys())
                if (nbNotes < smallestNbJudgements ) :
                    smallestNbJudgements = nbNotes
                elif nbNotes > biggestNbJudgements :
                    biggestNbJudgements = nbNotes
                    
                moyenne = 1.0 * sumNotes / nbNotes
                #sumVariance += (value - moyenne) **2
                #variance = 1.0 * 1/nbNotes * sumVariance 
                
               
                
                meanAndVarianceUser[user] = {"moyenne" : moyenne, "variance" : varianceNp}

    print("smallest nb judgements",smallestNbJudgements, "biggest one", biggestNbJudgements)
                

    '''
    La variance se calcule selon v(x) = 1/n * sum(xi - m)^2 ou m est la moyenne
    
    '''
    #    pprint(infoOnUsers)
#    pprint(meanAndVarianceUser)
    return meanAndVarianceUser, infoOnUsers

meanAndVariance, dicoInfoUsers = calcMeanAndVariance()

            
def recommandation2Films(film1, film2, dico) :
    

    infoOnUsers = dico
    
    vect1 = []
    vect2 = []
    infoOnFilms = {}
    
    for user in infoOnUsers :
        if film1 in infoOnUsers[user] :
            vect1.append(infoOnUsers[user][film1])
            if film2 in infoOnUsers[user] :
                vect2.append(infoOnUsers[user][film2])
            else :
                vect2.append(0)
        elif film2 in infoOnUsers [user] :
            vect2.append(infoOnUsers[user][film2])
            vect1.append(0)

#    print("vect1",vect1, "vect2", vect2)
    
    # Permet de calculer la correlation entre deux vecteurs
    if len(vect1) > 1 :
        cor = np.corrcoef(vect1,vect2)[0][1]
    elif len(vect1) == 1:
        cor = 1
    else :
        cor = 0
    return cor

#recommandation2Films("Scream (1996)", "Stargate (1994)")





def recommandationAllMovies(listMovies, dictionnaire) :

    dicoRecommandation = {}

    for film1 in listMovies :
        tmp = {}
        
        for film2 in listMovies :
            t = recommandation2Films(film1, film2, dictionnaire)
            tmp [film2] = t
#            print("Corr  pour " +film1 + " , " +film2+" = " +str(t))
        
        dicoRecommandation[film1] = tmp
    return dicoRecommandation
    #    pprint(dicoRecommandation)


corrFilms = recommandationAllMovies(listMovies(), dicoInfoUsers)

def best5(movie) :

    res = sorted(corrFilms[movie].items(), key = operator.itemgetter(1), reverse = True)
    dico5movies = {}
    if movie not in dico5movies :
        #Le 1er element est le film en lui meme donc on ne le prend pas
        dico5movies[movie] = res[1:6]
#    pprint(res)
    return dico5movies

#dicoBest5 = best5("Scream (1996)")


def writeRecommandations(dico) :

    
    with codecs.open("./reco.txt", "w", "utf-8") as myfile :
        for movie in dico :
            dico5 = best5(movie)
            
            for newMovie in dico5:
 #               pprint(dico5)
                myfile.write("--------------------------------\n ")
                myfile.write("The movie is : "+str(newMovie))
                myfile.write("\n-------------------------------- \n")
                count = 1
#                pprint(dico5[newMovie])
                for title in dico5[newMovie] :
                    myfile.write(str(count)+") " +str(title)+"\n")
                    count += 1
                count = 0
                        
    
                
writeRecommandations(corrFilms)


'''
Le temps qu'a pris ce calcul sur ma machine est 15min

'''
    

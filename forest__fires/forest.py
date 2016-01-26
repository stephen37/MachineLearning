from pprint import pprint
import codecs
import numpy as np
from numpy.random import uniform, normal, seed
import matplotlib.pyplot as plt
import pandas as pd



def basic_linear_regression(x,y) :

    length = len(x)
    sum_x = sum(x)
    sum_y = sum(y)

    sum_x_squared = sum(map(lambda a : a * a, x))

    sum_of_products = sum([x[i] * y[i] for i in range(length)])

    a = (sum_of_products - (sum_x * sum_y) / length ) / (sum_x_squared - ((sum_x ** 2) / length))
    b = (sum_y - a * sum_x) /length

    return a,b


def readFile(file):

    
    COLUMN_SEPARATOR = ","

    fire_data = pd.DataFrame.from_csv("./forestfires.csv", sep = COLUMN_SEPARATOR, header = None)

    pprint(fire_data)


    RAIN_INDEX = 11

    ISI = 7
    
    x = fire_data[RAIN_INDEX]
    y = fire_data[ISI]

    #print(basic_linear_regression(x,y))

#    regression = np.polyfit(x,y,1)

    ''' 
    with codecs.open(file, "r", encoding="utf-8") as myfile :
        for line in myfile :
            line = line.split(",")
            x = line[0]
            y = line[1]
            month = line[2]
            day = line[3]
            ffmc = line[4]
            dmc = line[5]
            dc = line[6]
            isi = line[7]
            temp = line[8]
            rh = line[9]
            wind = line[10]
            rain = line[11]
            area = line[12] #The burned area of the forest (in ha). This output variable is very skewed towards 0.0, thus it is recommanded to model with the logarithm transform

    '''



readFile("./forestfires.csv")

def exemple() :
    seed(1024)

    p = np.poly1d([0.087, -0.81, 1.69, -0.03])

    n = 50
    t_low, t_high = -2, 6
    noise_scale = 1

    #Sort x to be sure the points can be plotted
    x = sorted(uniform(low=t_low, high = t_high, size = n))
    x = np.array(x)
    y = p(x) + normal(loc = 0, scale = noise_scale, size = n)

    X = np.vstack([np.ones(n), x])
    m, c = np.linalg.lstsq(X.T, y)[0]

    plt.plot(x, m * x + c, "r+")
    plt.plot(x, p(x), "-x")
    plt.show()


#exemple()

""" MA3.py

Student:Amanda Holtmo   
Mail:amanda.holtmo.6661@student.uu.se
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
#from numba import njit


# Exc1
def approximate_pi(n, plot = False):
    # n is the number of points
    #Ac = pi * r^2
    #As = 4*r^2
    #pi = 4*(Ac/As)
    #pi = 4*(nc/(nc+ns))


    #r = x^2+y^2
    inside_x = []
    inside_y = []
    outside_x = []
    outside_y = []
    for i in range(n):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        if x**2 + y**2 <= 1:
            inside_x.append(x)
            inside_y.append(y)
        else:
            outside_x.append(x)
            outside_y.append(y)
    pi = 4*(len(inside_x)/n)

    if plot:
        fig, ax = plt.subplots()

        ax.scatter(inside_x,inside_y, c = 'b')    
        ax.scatter(outside_x,outside_y, c = 'r')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        plt.savefig(f"Plot {n}.png")

    return pi

# Exc2, approximation
def sphere_volume(n, d): 
    # n is the number of points
    # d is the number of dimensions of the sphere
 
    #List comperhansion
    points = [[random.uniform(-1,1) for i in range(d)] for i in range(n)]

    #map() filter()
    points_list = list(filter(lambda y: sum(map(lambda x: x**2 , y)) <= 1, points))

    #volym av ex.kub * in/tot 
    #points list ger punkter innom ex.sfär eller annat för annan dimension
    return 2**d *(len(points_list)/n)


#Exc2, real value
def hypersphere_exact(n, d):
    # n is the number of points
    # d is the number of dimensions of the sphere 
    return (m.pi ** (d / 2)) / m.gamma(d / 2 + 1)

#Exc3: numba version
#@njit
#def sphere_volume_numba(n:int, d:int)->float:
    # n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    points_inside = 0
    for i in range(n):
        a = 0
        for x in range(d):
            point = random.uniform(-1,1)
            a += point**2
        if a <= 1:
            points_inside += 1
    return 2**d*(points_inside/n)
    

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes

    #dela upp punkter på antal processes
    #// heltalsdivision
    count = [n//np]*np
    #% resten på första
    count[0] += n%np

    with future.ProcessPoolExecutor() as ex:
        results = ex.map(sphere_volume, count,[d]*np)
    
    #zip kopplar ihop, c är vikt om inte lika 
    tot = sum(r * c for r, c in zip(results, count)) / n
        

    return tot

    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        a = approximate_pi(n, plot = True)
        print("pi: ", a)
    
    # Exc2
    n = 100000
    d = 2
    print(f"approx volume of {d} dimentional sphere = {sphere_volume(n,d)}")
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")
    #3.14432
    #3.1415

    n = 100000
    d = 11
    print(f"approx volume of {d} dimentional sphere = {sphere_volume(n,d)}")
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")
    #1.699
    #1.884

    # Exc3
    n = 1000000
    d = 11
    for i in range(3):
        start = pc()
        sphere_volume(n, d)
        stop = pc()
        print(f"Exc3. run {i+1}: Sequential time of {d} and {n}: {stop-start}")
        print("What is numba time?")
    #1: 10.13
    #2: 9.68
    #3: 9.59
    
    for i in range(3):
        start = pc()
        #sphere_volume_numba(n, d)
        stop = pc()
        print(f"Exc3. numba run {i+1}: Sequential time of {d} and {n}: {stop-start}")
        print("What is numba time?")
    #1: 1.44
    #2: 0.2
    #3: 0.21

    #numba much faster, the first run takes longer then fast. But normal all takes the same time
    
    # Exc4
    n = 1000000
    d = 11
    start1 = pc()
    sphere_volume(n,d)
    stop1 = pc()
    start = pc()
    sphere_volume_parallel(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop1-start1}")
    print(f"Exc4: Parallel time time of {d} and {n}: {stop-start}")

    print("What is parallel time?")
    #Sequental time: 14.54
    #Parallel time: 6.14

    #Linux:
    #Sequental time: 12.9
    #Parallel time: 4.9

    #6.14-4.9)/6.14 = 0.2 = 20%

    
    

if __name__ == '__main__':
	main()

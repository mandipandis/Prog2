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
from numba import njit


# Exc1
def approximate_pi(n, plot = False):
    # n is the number of points
    #Ac = pi * r^2
    #As = 4*r^2
    #pi = 4*(Ac/As)
    #pi = 4*(nc/(nc+ns))


    #r = x^2+y^2
    inside_x, inside_y = [],[]
    outside_x, outside_y = [],[]
    for i in range(n):
        x, y = random.uniform(-1,1), random.uniform(-1,1)
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

    return 2**d *(len(points_list)/n)


#Exc2, real value
def hypersphere_exact(n, d):
    # n is the number of points
    # d is the number of dimensions of the sphere 
    return (m.pi ** (d / 2)) / m.gamma(d / 2 + 1)

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int)->float:
    # n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    points_inside = 0
    for i in range(n):
        sum_ = 0
        for x in range(d):
            rand = random.uniform(-1,1)
            sum_ += rand**2
        if sum_ <= 1:
            points_inside += 1
    return 2**d*(points_inside/n)
    

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    pass
    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    #for n in dots:
    #    a = approximate_pi(n, plot = True)
    #    print("pi: ", a)
    
    # Exc2
    n = 100000
    d = 2
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # Exc3
    n = 1000000
    d = 11
    for i in range(3):
        start = pc()
        sphere_volume(n, d)
        stop = pc()
        print(f"Exc3. run {i+1}: Sequential time of {d} and {n}: {stop-start}")
        print("What is numba time?")
    #1: 10.51
    #2: 10.69
    #3: 11.996
    
    for i in range(3):
        start = pc()
        sphere_volume_numba(n, d)
        stop = pc()
        print(f"Exc3. numba run {i+1}: Sequential time of {d} and {n}: {stop-start}")
        print("What is numba time?")
    #1: 10.51
    #2: 10.69
    #3: 11.996
    
    # Exc4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    
    

if __name__ == '__main__':
	main()

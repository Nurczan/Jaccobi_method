import csv
from copy import deepcopy
from math import *
from pprint import pprint
from time import time
import sys
import random
from enum import Enum

# csv format
# 5 - mesh dim
# 10 - top
# 15 - left
# 15 - right
# 8 - down
# h - in meters ex. 0.001
# f(x,y)= sin(x)+sin(y)
# residual

class Algs(Enum):
    RANDOM = "random"
    GAUSS = "normal_gauss"
    JACOB = "normal_jacob"
    EDGE = "edge"

class Mesh:

    def __init__(self,file):
        with open(file, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            self.dims = int(next(csvreader)[0])
            self.top = float(next(csvreader)[0])
            self.left = float(next(csvreader)[0])
            self.right = float(next(csvreader)[0])
            self.down = float(next(csvreader)[0])
            self.h = float(next(csvreader)[0])
            self.function = next(csvreader)[0]
            self.error_threshold = float(next(csvreader)[0])

        self.mesh = []
        self.generate_mesh()

        self.buffer_mesh = deepcopy(self.mesh)

        self.indicies = []

        for i in range(1, self.dims-1):
            for j in range(1,self.dims-1):
                self.indicies.append((i,j))

        pprint(f"function: {self.function}")
        pprint(f"h: {self.h}")

        self.algorithms_dict = {Algs.JACOB.value : self.normal_iter_jacob, Algs.GAUSS.value : self.normal_iter_gauss\
            ,Algs.EDGE.value : self.edge_iter, Algs.RANDOM.value : self.random_iter}
    
    def generate_mesh(self):
        minimum = min(self.top,self.right,self.left,self.down)
        self.mesh.clear()
        self.mesh.append([self.top for x in range(0, self.dims)])
        for i in range(self.dims-2):
            self.mesh.append([minimum for x in range(0, self.dims)])
            self.mesh[i+1][0] = self.left
            self.mesh[i+1][-1] = self.right
        self.mesh.append([self.down for x in range(0, self.dims)])
    
    def fun(self,x,y):
        d = {"sin":sin,"cos":cos,"x":x,"y":y}
        exec(f"a = {self.function}", d)
        return d["a"]
    
    def calculate(self, method : str, filename : str = "result"):
        __method = self.algorithms_dict[method]
        error = 9999
        iter_no = 0

        time_before = time()
        with open(filename,"w+",newline='') as res:
            write = csv.writer(res) 
            while error > self.error_threshold:
                error = __method()
                iter_no += 1
                write.writerows(self.mesh)
                write.writerow("")
                print(f"\rerror: {error}",end="")
                sys.stdout.flush()
        time_after = time()
        self.generate_mesh()

        print(f"\nsimulation of {method} ended in: {iter_no} iterations with error: {error} in {time_after-time_before}\n")


    def random_iter(self):
        choices = deepcopy(self.indicies)
        error = -1
        for i in range(1,self.dims-1):
            for j in range(1,self.dims-1):
                vec = random.choice(choices)
                error = max(self.calculation_gauss(vec[0],vec[1]),error)
        return error

    def edge_iter(self):
        vec = None
        temp_vec = [1,1]
        path_len = self.dims - 3
        error = -1
        
        while path_len > 0:
            vec = deepcopy(temp_vec)
            for i in range(path_len):
                vec[0] += 1
                error = max(self.calculation_gauss(vec[0],vec[1]),error)
            for i in range(path_len):
                vec[1] += 1
                error = max(self.calculation_gauss(vec[0],vec[1]),error)
            for i in range(path_len):
                vec[0] -= 1
                error = max(self.calculation_gauss(vec[0],vec[1]),error)
            for i in range(path_len):
                vec[1] -= 1
                error = max(self.calculation_gauss(vec[0],vec[1]),error)
            temp_vec[0] += 1
            temp_vec[1] += 1
            path_len -= 2
        
        if path_len == 0:
            error = max(self.calculation_gauss(temp_vec[0],temp_vec[1]),error)
        
        return error

    #region JACOBI
    def normal_iter_jacob(self):
        error = -1
        for i in range(1,self.dims-1):
            for j in range(1,self.dims-1):
                error = max(self.calculation_jacob(i,j),error)
        temp = self.buffer_mesh
        self.buffer_mesh = self.mesh
        self.mesh = temp
        return error

    def calculation_jacob(self,i,j):
        temp = (((self.h**2)*self.fun(i,j)) - self.mesh[i-1][j] - self.mesh[i+1][j] - self.mesh[i][j-1] - self.mesh[i][j+1])/(-4)
        temp_err = abs(self.mesh[i][j]-temp)
        self.buffer_mesh[i][j] = temp
        return temp_err
    #endregion
    
    #region GAUSS-SEIDEL
    def normal_iter_gauss(self):
        error = -1
        for i in range(1,self.dims-1):
            for j in range(1,self.dims-1):
                error = max(self.calculation_gauss(i,j),error)
        return error
    
    def calculation_gauss(self,i,j):
        temp = (((self.h**2)*self.fun(i,j)) - self.mesh[i-1][j] - self.mesh[i+1][j] - self.mesh[i][j-1] - self.mesh[i][j+1])/(-4)
        temp_err = abs(self.mesh[i][j]-temp)
        self.mesh[i][j] = temp
        return temp_err
    #endregion

if __name__ == "__main__":
    sim = Mesh("./input.csv")
    sim.calculate("normal_gauss", "GAUSS")
    sim.calculate("normal_jacob", "JACOB")
    sim.calculate("random", "RANDOM")
    sim.calculate("edge", "EDGE")
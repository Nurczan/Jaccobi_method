import csv
from copy import deepcopy
from math import *
from pprint import pprint
from time import time
import sys
# csv format
# 5 - mesh dim
# 10 - top
# 15 - left
# 15 - right
# 8 - down
# h - in meters ex. 0.001
# f(x,y)= sin(x)+sin(y)
# residual

class Mesh:

    def __init__(self,file):
        with open(file, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            self.dims = int(next(csvreader)[0])
            top = float(next(csvreader)[0])
            left = float(next(csvreader)[0])
            right = float(next(csvreader)[0])
            down = float(next(csvreader)[0])
            self.h = float(next(csvreader)[0])
            self.function = next(csvreader)[0]
            self.error_threshold = float(next(csvreader)[0])

        minimum = min(top,right,left,down)
        self.mesh = []
        self.mesh.append([top for x in range(0, self.dims)])
        for i in range(self.dims-2):
            self.mesh.append([minimum for x in range(0, self.dims)])
            self.mesh[i+1][0] = left
            self.mesh[i+1][-1] = right
        self.mesh.append([down for x in range(0, self.dims)])

        self.buffer_mesh = deepcopy(self.mesh)
        pprint(f"mesh: {self.mesh}")
        pprint(f"function: {self.function}")
        pprint(f"h: {self.h}")
    
    def fun(self,x,y):
        d = {"sin":sin,"cos":cos,"x":x,"y":y}
        exec(f"a = {self.function}", d)
        return d["a"]
    
    def calculate(self, method):
        __method = None
        error = 9999
        iter_no = 0

        if method == "normal":
            ___method = self.normal_iter
        else:
            raise AttributeError

        time_before = time()
        with open("./result","w+",newline='') as res:
            write = csv.writer(res) 
            while error > self.error_threshold:
                error = ___method()
                iter_no += 1
                write.writerows(self.mesh)
                write.writerow("")
                print(f"\rerror: {error}",end="")
                sys.stdout.flush()
        time_after = time()
        
        print(f"simulation ended in: {iter_no} iterations with error: {error} in {time_after-time_before}")
    
    def normal_iter(self):
        error = -1
        for i in range(1,self.dims-1):
            for j in range(1,self.dims-1):
                error = max(self.calculation(i,j),error)
        temp = self.buffer_mesh
        self.buffer_mesh = self.mesh
        self.mesh = temp
        return error

    def calculation(self,i,j):
        temp = (((self.h**2)*self.fun(i,j)) - self.mesh[i-1][j] - self.mesh[i+1][j] - self.mesh[i][j-1] - self.mesh[i][j+1])/(-4)
        temp_err = abs(self.mesh[i][j]-temp)
        self.buffer_mesh[i][j] = temp
        return temp_err

if __name__ == "__main__":
    sim = Mesh("./input.csv")
    sim.calculate("normal")

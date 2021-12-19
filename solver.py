from pprint import pprint
from random import choice

# self.mesh = [[0,0,0,0,0],[0,250,250,250,0],[0,250,250,250,0],[0,250,250,250,0],[0,0,0,0,0]]
# self.ERROR = 0.00001
# self.min_err = 1000
# self.h = 1.2
# self.iter_no = 0 [(10,20),(10,20)]

class MeshSim:

    def __init__(self):
        self.mesh = [[[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[250,0],[250,0],[250,0],[0,0]],[[0,0],[380,0],[0,0],[380,0],[0,0]],[[0,0],[350,0],[350,0],[350,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0]]]
        self.ERROR = 0.00001
        self.min_err = 1000
        self.h = 1.2
        self.iter_no = 0
        self.clear()

    def function(self,x):
        return 0

    def calculation(self,p1,p2,p3,p4):
        return (p1[0]+p2[0]+p3[0]+p4[0])/4

    def clear(self):
        self.iter_no = 0
        self.min_err = 1
        self.mesh = [[[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[8,0],[2,0],[2,0],[0,0]],[[0,0],[24,0],[-5,0],[3,0],[0,0]],[[0,0],[3,0],[3,0],[3,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0]]]

    # iterations
    def normal_iter(self):
        while self.min_err > self.ERROR:
            self.min_err = 0
            self.iter_no += 1
            for i in range(1,4):
                for j in range(1,4):
                    self.upierdliwe(i,j)
        pprint(self.mesh)
        print(f"finisself.hed in {self.iter_no}")
        self.clear()

    def edge_iter(self):
        while self.min_err > self.ERROR:
            self.min_err = 0
            self.iter_no += 1
            for i in range(1,4):
                for j in range(1,4):
                    self.upierdliwe(i,j)
        print(self.mesh)
        print(f"finisself.hed in {self.iter_no}")
        self.clear()

    def custom_iter(self):
        while self.min_err > self.ERROR:
            self.min_err = 0
            self.iter_no += 1

            self.upierdliwe(1,1)
            self.upierdliwe(1,2)
            self.upierdliwe(1,3)
            self.upierdliwe(2,3)
            self.upierdliwe(3,3)
            self.upierdliwe(3,2)
            self.upierdliwe(3,1)
            self.upierdliwe(2,1)
            self.upierdliwe(2,2)
            
        print(self.mesh)
        print(f"finisself.hed in {self.iter_no}")
        self.clear()
    
    def custom_iter2(self):
        while self.min_err > self.ERROR:
            self.min_err = 0
            self.iter_no += 1
            p = [(1,1),(1,2),(1,3),(2,3),(3,3),(3,2),(3,1),(2,1),(2,2)]
            while len(p) != 0:
                t = choice(p)
                self.upierdliwe(t[0],t[1])
                p.remove(t)

        print(self.mesh)
        print(f"finisself.hed in {self.iter_no}")
        self.clear()

    def upierdliwe(self,i,j):
        temp = self.calculation(self.mesh[i][j+1],self.mesh[i][j-1],self.mesh[i+1][j],self.mesh[i-1][j])
        temp_err = abs(self.mesh[i][j][0]-temp)
        self.mesh[i][j][0] = temp
        self.mesh[i][j][1] = temp_err
        if self.min_err < temp_err:
            self.min_err = temp_err


if __name__ == "__main__":
    m = MeshSim()
    m.normal_iter()
    m.custom_iter()
    m.custom_iter2()
from matplotlib import axes
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
from time import sleep
import os

FOLDER = "./visualisations"
DATA_FOLDER = "./meshes"
FILE = "RANDOM"                           # filename of mesh data, choos one of: GAUSS, JACOB, EDGE, RANDOM;
ANIM_NAME = "RANDOM_ANIMATION.gif"        # filename of animation
temp_arr = []
ims = []

def plot_errors():
    fig = plt.figure()
    os.makedirs(FOLDER, exist_ok=True)
    with open(f"{DATA_FOLDER}/{FILE}_errors", newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        temp_array = [float(x) for x in (next(csvreader)[:-1])]
    plt.plot(temp_array)
    plt.ylabel('residual')
    plt.xlabel('steps')
    plt.yscale('log')
    plt.savefig(f"{FOLDER}/{FILE}_errors.png")
    plt.show()
    plt.clf()

def visualize():
    fig = plt.figure()
    os.makedirs(FOLDER, exist_ok=True)
    with open(f"{DATA_FOLDER}/{FILE}", newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            if(len(row) == 0):
                ims.append([plt.imshow(temp_arr, animated=True)])
                temp_arr.clear()
            else:
                temp_arr.append([float(elem) for elem in row])
    plt.colorbar()

    ani = animation.ArtistAnimation(fig, ims, interval=30, blit=True,
                                    repeat_delay=1000)
    ani.save(f"{FOLDER}/{ANIM_NAME}")
    plt.show()
    plt.clf()


if __name__ == "__main__":
    plot_errors()
    visualize()
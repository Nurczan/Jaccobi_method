import matplotlib.pyplot as plt
import csv

FILE = "last_GAUSS.txt" # filename of mesh data

ims = []

with open(FILE, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        ims.append([float(elem) for elem in row])

plt.imshow(ims)
plt.show()
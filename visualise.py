import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
from time import sleep

FILE = "./result"
temp_arr = []
ims = []
fig = plt.figure()

with open(FILE, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    
    for row in csvreader:
        if(len(row) == 0):
            ims.append([plt.imshow(temp_arr, animated=True)])
            temp_arr.clear()
        else:
            temp_arr.append([float(elem) for elem in row])

ani = animation.ArtistAnimation(fig, ims, interval=30, blit=True,
                                repeat_delay=1000)

ani.save('dynamic_images.gif')

plt.show()
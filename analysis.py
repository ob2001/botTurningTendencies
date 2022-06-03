import os
import numpy as np
import matplotlib.pyplot as plt

# Import all data files for one bot
def readfile(botnum: str):
    filename = f"../Video Analysis/B{botnum}"

    n = 1
    # Get number of runs with this bot
    while(os.path.exists(f"{filename} - {n}.csv")):
        n += 1

    # Read in the data headers
    with open(filename + " - 1.csv", "r") as f:
        headers = f.readline().split(',')

    # Read in data from each file and store in separate sub-array
    data = []
    for i in range(1, n):
        data.append(np.asarray(np.loadtxt(f"{filename} - {i}.csv", delimiter = ',', skiprows = 1)))
    data = np.array(data)
    return n, headers, data

n, headers, data = readfile("3")
print(headers)

""" Plotting """
if(True):
    for i in range(n):
        fig = plt.figure(figsize = (17, 8))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection = "polar")
        ax1.plot(data[i,:,2], data[i,:,3])
        ax2.plot(-data[i,:,6]*2*np.pi/360, data[i,:,5])
        plt.show()

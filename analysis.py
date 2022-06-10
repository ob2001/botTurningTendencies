import os
import numpy as np
import matplotlib.pyplot as plt

# Read in all data files for one bot
def readbotfile(botnum: str):
    filename = f"../Video Analysis/B{botnum}"

    n = 1
    # Get number of runs with this bot
    while(os.path.exists(f"{filename} - {n}.csv")): n += 1

    # Read in the data headers
    with open(filename + " - 1.csv", "r") as f: headers = f.readline().split(',')

    # Read in data from each file and store in separate sub-array
    data = []
    for i in range(1, n):
        data.append(np.asarray(np.loadtxt(f"{filename} - {i}.csv", delimiter = ',', skiprows = 1)))
    data = np.array(data)
    return n, headers, data

# Read in voltage and time measurement data
def readvolts():
    filename = "./Bot measurements.csv"
    with open(filename) as f:
        headersl1 = f.readline().split(',')
        headersl2 = f.readline().split(',')
    temp = np.loadtxt(filename, delimiter = ',', skiprows = 2)
    cycle = np.array(temp[:, 0]).transpose()
    voltage = np.array(temp[:, 1:13]).transpose()
    vuncertainty = np.array(temp[:, 13:25]).transpose()
    dur = np.array(temp[:, 25:37]).transpose()
    duncertainty = np.array(temp[:, 37:49]).transpose()
    cdur = np.array(temp[:, 49:61]).transpose()
    data = {'cycle': cycle, 'voltage': voltage, 'vuncertainty': vuncertainty, 'dur': dur, 'duncertainty': duncertainty, 'cdur': cdur}
    return headersl1, headersl2, data

n, headers, data = readbotfile(5)
mheaders1, mheaders2, measurements = readvolts()

""" Plotting """
if(False):
    for i in range(n):
        fig = plt.figure(figsize = (17, 8))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection = "polar")
        ax1.plot(data[i,:,2], data[i,:,3])
        ax2.plot(-data[i,:,6]*2*np.pi/360, data[i,:,5])
        plt.show()

if(True):
    fig = plt.figure(figsize = (12, 9))
    ax1 = fig.add_subplot(111)
    ax1.plot(measurements['cdur'][1], measurements['voltage'][1])
    plt.show()
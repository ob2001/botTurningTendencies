import os
import argparse
import numpy as np

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('botnum', type = str)
    parser.add_argument('--traj', action = "store_true")
    parser.add_argument('--volt', action = "store_true")
    args = parser.parse_args()
    return args

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
    volt = np.array(temp[:, 1:13]).transpose()
    vunc = np.array(temp[:, 13:25]).transpose()
    dur = np.array(temp[:, 25:37]).transpose()
    dunc = np.array(temp[:, 37:49]).transpose()
    cdur = np.array(temp[:, 49:61]).transpose()
    data = {'cycle': cycle, 'voltage': volt, 'vuncertainty': vunc, 'dur': dur, 'duncertainty': dunc, 'cdur': cdur}
    return headersl1, headersl2, data
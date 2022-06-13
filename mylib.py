import os
import math
import argparse
import numpy as np

def arguments():
    # Use argparse to parse commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('botnum', type = str, nargs = '?', default = 3)
    parser.add_argument('--traj', action = "store_true", default = False)
    parser.add_argument('--volt', action = "store_true", default = False)
    parser.add_argument('--trimplot', action = "store_true", default = False)
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

    # Cycle number
    cycle = np.array(temp[:, 0]).transpose()

    # Voltage measurements
    volt = np.array(temp[:, 1:13]).transpose()

    # Voltage uncertainties
    vunc = np.array(temp[:, 13:25]).transpose()

    # Cycle duration
    dur = np.array(temp[:, 25:37]).transpose()

    # Uncertainty in cycle duration
    dunc = np.array(temp[:, 37:49]).transpose()

    # Cumulative duration
    cdur = np.array(temp[:, 49:61]).transpose()

    # Compile everything into a dictionary for easy access
    data = {'cycle': cycle, 'voltage': volt, 'vuncertainty': vunc, 'dur': dur, 'duncertainty': dunc, 'cdur': cdur}

    # Create a dictionary to associate bot numbers with order in list
    botdict = {"3": 0, "5": 1, "7": 2, "10": 3, "14": 4, "15": 5, "16": 6, "17": 7, "19": 8, "?": 9, "B": 10, "D": 11}
    return headersl1, headersl2, data, botdict
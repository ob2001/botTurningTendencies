import os
import argparse
import numpy as np

def arguments():
    # Use argparse to parse commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('botnum', nargs = '?', default = 3)
    parser.add_argument('--cycles', nargs = '*', default = [0, 0])
    parser.add_argument('--all', action = "store_true")
    parser.add_argument('--traj', action = "store_true")
    parser.add_argument('--volt', action = "store_true")
    parser.add_argument('--trimplot', action = "store_true")
    parser.add_argument('--getradii', action = "store_true")
    parser.add_argument('--plotradii', action = "store_true")
    parser.add_argument('--plotavgradii', action = "store_true")
    parser.add_argument('--plottogether', action = "store_true")
    parser.add_argument('--savefigs', action = "store_true")
    args = parser.parse_args()
    return args

# First-order central difference method
def cdiff(ys, dx, i):
    return (ys[i + 1] - ys[i - 1])/(2*dx)

# Second-order central difference method
def cdiff2(ys, dx, i):
    return 4*(ys[i + 1] - 2*ys[i] + ys[i - 1])/dx**2

# Determine which cycles of the chosen bot to use based on the
# --cycles command line argument
def cycles(args, data):
    start, stop = 0, 0
    # Use all cycles
    if(args.cycles[0] == "all" or args.all):
        start, stop = 0, len(data) - 1
    # Use only one cycle corresponding user's input number
    elif(args.cycles[0] <= len(data) - 1 and not args.cycles[1].exists()):
        start = stop = args.cycles[0]
    # Use cycles in the range between specified start and stop values
    elif(args.cycles[0] <= len(data) - 1 and args.cycles[1] <= len(data) - 1):
        start, stop = args.cycles[0], args.cycles[1]
    # Only use the first cycle
    else:
        start = stop = 0
    return start, stop

# Construct the centre of a circle from three points and obtain its radius
def getradius(xs, ys):
    # Construct midpoints
    mid1, mid2 = [(xs[0] + xs[1])/2, (ys[0] + ys[1])/2], [(xs[1] + xs[2])/2, (ys[1] + ys[2])/2]
    
    # Find slopes of perpendicular bisectors
    p1, p2 = -(xs[1] - xs[0])/(ys[1] - ys[0]), -(xs[2] - xs[1])/(ys[2] - ys[1])

    # x coordinate of centre of circle
    xc = (p1*mid1[0] - mid1[1] - p2*mid2[0] + mid2[1])/(p1 - p2)

    # y coordinate of centre of circle
    yc = p1*(xc - mid1[0]) + mid1[1]
    
    return np.sqrt((xc - xs[0])**2 + (yc - ys[0])**2) # Radius of circle

# Read in all data files for selected bot (for single-bot runs)
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
    cycle = np.array(temp[:, 0]).transpose() # Cycle number
    volt = np.array(temp[:, 1:13]).transpose() # Voltage measurements
    vunc = np.array(temp[:, 13:25]).transpose() # Voltage uncertainties
    dur = np.array(temp[:, 25:37]).transpose() # Cycle duration
    dunc = np.array(temp[:, 37:49]).transpose() # Uncertainty in cycle duration
    cdur = np.array(temp[:, 49:61]).transpose() # Cumulative duration

    # Compile everything into a dictionary for easy access
    data = {'cycle': cycle, 'voltage': volt, 'vuncertainty': vunc, 'dur': dur, 'duncertainty': dunc, 'cdur': cdur}

    # Create a dictionary to associate bot numbers with order in list
    botdict = {"3": 0, "5": 1, "7": 2, "10": 3, "14": 4, "15": 5, "16": 6, "17": 7, "19": 8, "U": 9, "B": 10, "D": 11}
    return headersl1, headersl2, data, botdict

# Step through a list which may have multiple occurences of None
# consecutively and remove all but one of those Nones
def trimnone(arr):
    flag, newarr = False, []
    for i in range(len(arr)):
        if arr[i] != None:
            newarr.append(arr[i])
            flag = False
        elif flag != True:
            flag = True
            newarr.append(None)
        else:
            continue
    return np.array(newarr)
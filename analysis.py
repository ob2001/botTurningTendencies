from mylib import *
import math
import matplotlib.pyplot as plt

# Trim data points to specified radii, maintaining the order of points.
# Separate resulting path segments with None values
def trimradius(X, Y, R, val):
    xnew, ynew = np.array([[x, y] if r < val else [None, None] for x, y, r in zip(X, Y, R)]).transpose()
    xnew, ynew = trimnone(xnew), trimnone(ynew)

    return xnew, ynew

# Calculate radius of curvature at each point
def getradii(xarr, yarr):
    i = 1
    maxr = 20000
    # Deal with the case where the first value in the list is None
    if(xarr[0] == None):
        i += 1
    radii, avgradii = [], []
    while(i < len(xarr) - 1):
        n, temp2 = 1, 0
        # Average turning radius over given segment
        while(i < len(xarr) - 1 and not any(xarr[i - 1:i + 2] == None)):
            ### temp1 = (cdiff(xarr, dt, i)*cdiff2(yarr, dt, i) - cdiff(yarr, dt, i)*cdiff2(xarr, dt, i))/(cdiff(xarr, dt, i)**2 + cdiff(yarr, dt, i)**2)**(3/2)

            temp1 = getradius(xarr[i - 1: i + 2], yarr[i - 1: i + 2])
            temp2 += temp1
            n += 1            
            i += 1
            # Append current value to list of turning radii at each point
            if(temp1 <= maxr):
                radii.append(temp1)
        # Append segment average to list
        if(temp2 <= maxr):
            avgradii.append(temp2/n)
        i += 3
    return radii, avgradii
    
args = arguments()
n, headers, data = readbotfile(args.botnum)
mheaders1, mheaders2, measurements, botdict = readvolts()

""" Plotting """
# Plot trajectory of chosen bot for all 1-minute periods
if(args.traj or args.all):
    xdim = 4 # Number of plots along horizontal edge
    axs = plt.subplots(math.ceil(len(data)/xdim), xdim, figsize = (18, 9))
    for i in range(n - 1):
        axs[1][math.floor(i/xdim)][i % xdim].plot(data[i,:,2], data[i,:,3])
    if(args.savefigs or args.all):
        plt.savefig(f"B{args.botnum} - trajectories.png")
    plt.show()

# Plot the voltage of the bot as a funtion of time
if(args.volt or args.all):
    fig = plt.figure(figsize = (12, 9))
    ax1 = fig.add_subplot(111)
    ax1.plot(measurements['cdur'][botdict[args.botnum]], measurements['voltage'][botdict[args.botnum]])
    if(args.savefigs or args.all):
        plt.savefig(f"B{args.botnum} - voltages.png")
    plt.show()

# Trim unwanted data points
cycle, rtrim = 0, 550
xnew, ynew = trimradius(data[cycle,:,2], data[cycle,:,3], data[cycle,:,5], rtrim)

# Plot trajectory of bot after trimming unwanted data points
if(args.trimplot or args.all):
    fig = plt.figure(figsize = (18, 9))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.plot(data[cycle,:,2], data[cycle,:,3])
    ax2.plot(xnew, ynew)
    if(args.savefigs or args.all):
        plt.savefig(f"B{args.botnum} - trimmed plot.png")
    plt.show()

# Calculate radius of curvature of path segments
if(args.getradii or args.plotradii or args.all):
    radii, avgradii = getradii(xnew, ynew)
    print(np.average(radii))
    if(args.plotradii or args.all):
        fig = plt.figure(figsize = (12, 9))
        ax = fig.add_subplot(111)
        ax.plot(radii)
        if(args.savefigs or args.all):
            plt.savefig(f"B{args.botnum} - radii.png")
        plt.show()
    if(args.plotavgradii or args.all):
        fig = plt.figure(figsize = (12, 9))
        ax = fig.add_subplot(111)
        ax.plot(avgradii)
        if(args.savefigs or args.all):
            plt.savefig(f"B{args.botnum} - average radii.png")
        plt.show()
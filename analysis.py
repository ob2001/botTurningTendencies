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
    maxr = 2000
    # Deal with the case where the first value in the list is None
    if(xarr[0] == None):
        i += 1
    radii, avgradii = [], []
    while(i < len(xarr) - 1):
        n, temp2 = 1, 0
        # Average turning radius over given segment
        while(i < len(xarr) - 1 and not any(xarr[i - 1:i + 2] == None)):
            #temp1 = 1/(np.abs((cdiff(xarr, 1/30, i)*cdiff2(yarr, 1/30, i) - cdiff(yarr, 1/30, i)*cdiff2(xarr, 1/30, i)))/(cdiff(xarr, 1/30, i)**2 + cdiff(yarr, 1/30, i)**2)**(3/2))
            temp1 = getradius(xarr[i - 1: i + 2], yarr[i - 1: i + 2])

            temp2 += temp1
            n += 1            
            i += 1
            # Append current value to list of turning radii at each point
            if(np.abs(temp1) <= maxr):
                radii.append(temp1)
        # Append segment average to list
        if(np.abs(temp2) <= maxr):
            avgradii.append(temp2/n)
        i += 3
    return radii, avgradii


args = arguments()
n, headers, data = readbotfile(args.botnum)
mheaders1, mheaders2, measurements, botdict = readvolts()
start, stop = cycles(args, data)
open(f"B{args.botnum} - avg radii.txt", "w").close()

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

for i in range(start, stop + 1):
    # Trim unwanted data points outside of specified radius
    rtrim = 550
    xnew, ynew = trimradius(data[i,:,2], data[i,:,3], data[i,:,5], rtrim)

    # Plot trajectory of bot after trimming unwanted data points
    if(args.trimplot or args.all):
        fig = plt.figure(figsize = (18, 9))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        ax1.plot(data[start,:,2], data[i,:,3])
        ax2.plot(xnew, ynew)
        if(args.savefigs or args.all):
            plt.savefig(f"B{args.botnum} - trimmed plot {i + 1}.png")
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
                plt.savefig(f"B{args.botnum} - radii {i + 1}.png")
            plt.show()
        if(args.plotavgradii or args.all):
            fig = plt.figure(figsize = (12, 9))
            ax = fig.add_subplot(111)
            ax.plot(avgradii)
            if(args.savefigs or args.all):
                plt.savefig(f"B{args.botnum} - average radii {i + 1}.png")
            plt.show()
        with open(f"B{args.botnum} - avg radii.txt", "a") as f:
            f.write(f"{np.average(radii)}\n")

    if(args.plottogether):
        radii, avgradii = getradii(xnew, ynew)
        avg = np.average(radii)
        print(avg)
        
        fig = plt.figure(figsize = (24, 18))
        ax1 = fig.add_subplot(221, title = "Bot trajectory untrimmed")
        ax2 = fig.add_subplot(222, title = f"Bot trajectory trimmed to $r = {rtrim}$")
        ax3 = fig.add_subplot(223, title = "Voltage curve for entire run with current voltage highlighted")
        ax4 = fig.add_subplot(224, title = "Turning radius of bot for 1 minute period. Average: $\\bar{r}_{turn} = %s$" %(avg))

        ax1.plot(data[i,:,2], data[i,:,3])
        ax2.plot(xnew, ynew)
        ax3.plot(measurements['cdur'][botdict[args.botnum]], measurements['voltage'][botdict[args.botnum]])
        ax3.plot(measurements['cdur'][botdict[args.botnum]][i], measurements['voltage'][botdict[args.botnum]][i], marker = 'o')
        ax4.plot(radii)

        if(args.savefigs):
            plt.savefig(f"B{args.botnum} - {i + 1}.png")
            
        ### Leave off to generate plots quickly
        # plt.show()
        
        with open(f"B{args.botnum} - avg radii.txt", "a") as f:
            f.write(f"{avg}\n")
from mylib import *
import matplotlib.pyplot as plt

# Trim data points to specified radii, maintaining the order of points.
# Separate resulting path segments with None values
def trimradius(X, Y, R, val):
    xnew, ynew = np.array([[x, y] if r < val else [None, None] for x, y, r in zip(X, Y, R)]).transpose()
    xnew, ynew = trimnone(xnew), trimnone(ynew)

    return xnew, ynew

args = arguments()
n, headers, data = readbotfile(args.botnum)
mheaders1, mheaders2, measurements, botdict = readvolts()

""" Plotting """
# Plot trajectory of chosen bot for all 1-minute periods
if(args.traj):
    xdim = 4 # Number of plots along horizontal edge
    axs = plt.subplots(math.ceil(len(data)/xdim), xdim, figsize = (18, 9))
    for i in range(n - 1):
        axs[1][math.floor(i/xdim)][i % xdim].plot(data[i,:,2], data[i,:,3])
    plt.show()

# Plot the voltage of the bot as a funtion of time
if(args.volt):
    fig = plt.figure(figsize = (12, 9))
    ax1 = fig.add_subplot(111)
    ax1.plot(measurements['cdur'][botdict[args.botnum]], measurements['voltage'][botdict[args.botnum]])
    plt.show()

# Plot trajectory of bot after trimming unwanted data points
if(args.trimplot):
    xnew, ynew = trimradius(data[0,:,2], data[0,:,3], data[0,:,5], 560)

    fig = plt.figure(figsize = (18, 9))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.plot(data[0,:,2], data[0,:,3])
    ax2.plot(xnew, ynew)
    plt.show()
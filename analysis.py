from mylib import *
import matplotlib.pyplot as plt

args = arguments()
n, headers, data = readbotfile(args.botnum)
mheaders1, mheaders2, measurements, botdict = readvolts()

""" Plotting """
if(args.traj):
    for i in range(n):
        fig = plt.figure(figsize = (17, 8))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection = "polar")
        ax1.plot(data[i,:,2], data[i,:,3])
        ax2.plot(-data[i,:,6]*2*np.pi/360, data[i,:,5])
        plt.show()

if(args.volt):
    fig = plt.figure(figsize = (12, 9))
    ax1 = fig.add_subplot(111)
    ax1.plot(measurements['cdur'][botdict[args.botnum]], measurements['voltage'][botdict[args.botnum]])
    plt.show()
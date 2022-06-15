# Usage
This Python code is used to analyze the trajectories of single bristle bots in an arena and extract their turning radius as a function of time as well as reading in various other information.

# Files and File Formats
The input files consist mostly of .csv files corresponding to one-minute periods of data collection from a given bristle bot. These files came directly from the MATLAB image analysis code, but were renamed to have the format "B{bot number} - {number in series}.csv". There is also a .csv file containing manual measurements for each bot. This file was simply named "Bot measurements.csv" and contains data on bot voltages and cycle durations as well as the uncertainties for each of these values.

# Command Line Arguments
Python's argparse module was used so that the program could be called conveniently from the command line without cluttering the code with hard-coded constants. There is one required positional argument, one optional positional argument, and several switches to modify the functionality of the program.

- botnum is the only required argument. It specifies which bot's data to analyze
- --cycles is an optional positional argument that allows the selection of which cycles of the chosen bot to analyze. If nothing is put here, the default functionality is to only analyze the first cycle for the chosen bot. "--cycles all" will analyze all the cycles for the given bot. "--cycles [start]" will analyze only the chosen cycle of the chosen bot. "--cycles [start] [stop]" will analyze the chosen range of cycles from [start] to [stop].
- --all is a switch which turns on the functionality of the entire program, except for the functionality activated by --plottogether (see below)
- --savefigs will save all figures generated by the program in the current directory.
- --traj generates a plot of the trajectory of the chosen bot in all cycles (regardless of what is chosen in --cycles).
- --volt generates a plot of the voltage of the chosen bot as a function of time for all cycles (regardless of what is chosen in --cycles).
- --trimplot generates a plot of the trajectory of the bot before and after points beyond a particular radius from the centre have been trimmed out of the trajectory.
- --getradii prints a list of the average radii of curvature of a bot for each cycle in the range specified by --cycles. It then writes these values to a text file.
- --plotradii plots the calculated radii of curvature as a function of time for each cycle in the range specified by --cycles.
- --plotavgradii plots the calculated radii of curvature averaged over each segment of the trajectory for each cycle in the range specified by --cycles.
- --plottogether generates a plot with several axes putting the plots of --trimplot, --volt and --plotradii into a single figure. This switch is not turned on by the --all switch.

# Code Functionality
The code first parses the command line arguments and reads in the data files for the chosen bot as well as reading in the data file of voltages and durations. Depending on the switches turned on from the command line, several different functions may occur.

A couple of switches cause a simple plot to be generated directly from the data read in from the data files (--traj, --volt,).

After these plots are generated (if the switches were turned on), we trim the list of [x, y] data points of entries whose radius is greater than rtrim using the list of [r] data as a reference. Where values are removed from the list, a None value is inserted in the list to maintain separation between distinct segments of the trajectory.

If the --trimplot switch was turned on, and figure is then generated of the trimmed trajectory next to the original, untrimmed trajectory, for comparison.

If any of --getradii, --plotradii, or --plottogether are turned on, the code will then extract turning radii from the trimmed list by taking points three at a time and finding the centre of the circle formed by them, and then finding the distance from one of the points to the centre of the circle. An upper limit was added for these radii as there would generally be a few (~5) outlying large values (~10000) which could majorly skew the calculated average turning radii. There is an alternate method for finding the radius of curvature using derivatives of x and y which has been commented out in favour of the more geometrical and intuitive approach. The different methods appear to produce similar but not identical results which I believe are due to differences in the errors produced by the numerical calculations rather than by any error in the programming itself.

--getradii will then simply print a list of the average of the radii of curvature for each cycle to the console and save it to a text file, --plotradii will plot the entire list of the radii of curvature over time for each cycle, and plottogether will do the same as --plotradii together with --trimplot and --volt.

# Math
The algorithm for finding the radius of curvature geometrically was found this way:

Given three points: $P=(x_0,y_0)$, $Q=(x_1,y_1)$, $R=(x_2,y_2)$

The midpoints between two pairs of points are: $mid_1=\frac{x_0+x_1}{2}$, $mid_2=\frac{x_1+x_2}{2}$

The slopes of the lines between these points are: $m_1=\frac{y_1-y_0}{x_1-x_0}$, $m_2=\frac{y_2-y_1}{x_2-x_1}$

The slopes of the perpendicular bisectors of these lines are: $p_1=-\frac{1}{m_1}$, $p_2=-\frac{1}{m_2}$

We then have a system of two equations to solve for the centre of the circle $C=(x_c,y_c)$:

$(y_c-y_{mid_1})=p_1(x_c-x_{mid_1})$

$(y_c-y_{mid{2}})=p_2(x_c-x_{mid_2})$

Solving, we get:

$x_c=\frac{p_1x_{mid_1}-y_{mid_1}-p_2x_{mid_2}+y_{mid_2}}{p_1-p_2}$

$y_c=p_1(x_c-x_{mid_1})+y_{mid_1}$

And finally, the radius of the circle is given by:

$r=\sqrt{(x_c-x_0)^2+(y_c-y_0)^2}$

The alternative analytic algorithm with derivatives is given by:

$\frac{1}{r}=\frac{\left|x'y''-y'x''\right|}{\left(x'^2+y'^2\right)^{\frac{3}{2}}}$
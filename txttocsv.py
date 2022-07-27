"""
Utility script used to convert the various .txt files into a single .csv file
"""

import os
import numpy as np

# Find .txt files in upper directory
files = os.listdir("..")
for i in range(len(files) - 1):
    if files[i][-4:] != ".txt":
        files.remove(files[i])

table = []
files = [f"../{file}" for file in files]

# Loop through found .txt files, appending the contents
# of each to a list
for file in files:
    news = np.zeros(27)
    with open(file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line != '\n':
                news[i] = float(line)
    table.append(news)

# Transpose table and save to .csv file
table = np.array(table).transpose()
np.savetxt("out.csv", table, fmt = "%3.5f", delimiter = ",")
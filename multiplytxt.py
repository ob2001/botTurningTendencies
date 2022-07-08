import os
import numpy as np

files = os.listdir("..")
for i in range(len(files) - 1):
    if files[i][-4:] != ".txt":
        files.remove(files[i])

table = []
files = [f"../{file}" for file in files]
for file in files:
    news = np.zeros(27)
    with open(file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line != '\n':
                news[i] = float(line)
    table.append(news)

table = np.array(table).transpose()
np.savetxt("out.csv", table, fmt = "%3.5f", delimiter = ",")
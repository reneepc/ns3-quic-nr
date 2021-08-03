#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import os
import statistics
from math import floor

desc_lines = 12;

def read_max():
    for root, dirs, files in os.walk("./maximos"):
        max_bytes = []
        files = [name for name in files if not name.startswith("google") ]
        fig, ax = plt.subplots(len(files))

        for i, name in enumerate(files):
            max_bytes.append([])
            with open(os.path.join(root, name)) as f:
                for _ in range(desc_lines):
                    next(f)
                for line in f:
                    if line[0] == "=":
                        break
                    max_bytes[i].append(int(line.split("|")[2]))
                ax[i].plot(max_bytes[i])
                limits = list(ax[i].get_ylim())
                print(limits);
                ax[i].set_yticks([int(statistics.mean(max_bytes[i])),
                    int(limits[1])])
                ax[i].yaxis.set_tick_params(labelsize=12)
                ax[i].set_ylim([0,2000]);
                ax[i].set_ylabel(name.split("-")[0], fontsize=16, rotation=0,
                        labelpad=35, color='slategray')
        plt.subplots_adjust(hspace=.0)
        ax[0].set_title("Tamanho máximo dos pacotes por intervalo de 1s", fontsize=24)
        plt.xlabel("Segundos", size=14, fontsize=20)
        ax[floor(i/2)].text(-55,-2000,"Máximo e média (Bytes)", rotation=90, size=14, fontsize=20);
        plt.show()
        fig.savefig("maximos-fonte.svg", format='svg')

read_max()

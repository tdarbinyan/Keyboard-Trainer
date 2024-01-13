import tkinter as tk
import time
import threading
import random
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from .Utility import Utility

class StatisticsShow:
    
    # -------------------- constructor --------------------
    # is responsible for rendering the heatmap in a new window
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Statistics")
        self.root.geometry("1000x600")
        img = tk.PhotoImage(file=Utility.get_file("../infographics/plot.png"), master=self.root)
        img_label = tk.Label(self.root, image=img)
        img_label.place(x=0, y=0)
        self.root.mainloop()
      
    # -------------------- draws the stat plot --------------------
    def plot_float_changes_over_time():
        timestamps = []
        first_float_values = []

        with open(Utility.get_file("../database/results.txt"), "r") as file:
            i = 0
            for line in file:
                i += 1
                values = line.strip().split()
                values[1] = values[0]
                values[0] = i
                if len(values) == 2:
                    timestamp, first_float = map(float, values)
                    timestamps.append(timestamp)
                    first_float_values.append(first_float)

        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, first_float_values, marker="o", linestyle="-")

        plt.xlabel("Time")
        plt.ylabel("First Float Value")
        plt.title("Changes of the First Float Value Over Time")

        plt.grid(True)
        plt.savefig(Utility.get_file("../infographics/plot.png"))
        StatisticsShow()
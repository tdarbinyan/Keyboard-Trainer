import tkinter as tk
import time
import threading
import random
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import os
from .StatPlot import StatisticsShow
from .Heatmap import HeatmapShow
from .Utility import Utility

matplotlib.use("Agg")

class TypeSpeedGUI:
    

    # -------------------- constructor --------------------
    # all the GUI elements of main window get declared and defined here
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Application")
        self.root.geometry("1000x600")

        self.cps = 0
        self.cpm = 0
        self.avgs = 0
        self.avgm = 0

        self.mistake_count = {key: 0 for key in Utility.keyboard_layout}

        self.texts = open(Utility.get_file("../database/texts.txt"), "r").read().split("\n")

        self.frame = tk.Frame(self.root)

        self.sample_label = tk.Label(self.frame, text=random.choice(self.texts), font=("Helvetica", 18))

        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.input_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyPress>", self.start)

        self.set_average()

        self.speed_label = tk.Label(
            self.frame,
            text=f"Speed: \n0.00 CPS\n0.00 CPM\n{self.avgs:.2f} Average CPS for last 10 tries\n{self.avgm:.2f} Average CPM for last 10 tries",
            font=("Helvetica", 18),
        )
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.clear_button = tk.Button(self.frame, text="Clear your statistics", command=self.clear)
        self.clear_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Show statistics plot", command=StatisticsShow.plot_float_changes_over_time)
        self.reset_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Show mistakes heatmap", command=self.draw_heatmap)
        self.reset_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False

        self.root.mainloop()

    # -------------------- starting function --------------------
    # has the main piece of driver code, responsible for checking if the sentence is right
    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()

        if not self.sample_label.cget("text").startswith(self.input_entry.get()):
            self.input_entry.config(fg="red")
            sample = self.sample_label.cget("text")
            inp = self.input_entry.get()
            for i in range(0, len(inp)):
                if sample[i] != inp[i] and sample[i] != " ":
                    self.mistake_count[sample[i].lower()] += 1
        else:
            self.input_entry.config(fg="black")

        if self.input_entry.get() == self.sample_label.cget("text")[:-1]:
            self.running = False
            self.input_entry.config(fg="green")
            open(Utility.get_file("../database/results.txt"), "a").write(str(self.cps) + " " + str(self.cpm) + "\n")
            self.set_average()
            self.speed_label.config(
                text=f"Speed: \n{self.cps:.2f} CPS\n{self.cpm:.2f} CPM\n{self.avgs:.2f} Average CPS for last 10 tries\n{self.avgm:.2f} Average CPM for last 10 tries"
            )

    # -------------------- method working with time --------------------
    # responsible for live display of required information
    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            self.cps = len(self.input_entry.get()) / self.counter
            self.cpm = self.cps * 60
            self.speed_label.config(
                text=f"Speed: \n{self.cps:.2f} CPS\n{self.cpm:.2f} CPM\n{self.avgs:.2f} Average CPS for last 10 tries\n{self.avgm:.2f} Average CPM for last 10 tries"
            )

    # -------------------- on click function for reset button --------------------
    # resets the current run
    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_label.config(
            text=f"Speed: \n0.00 CPS\n0.00 CPM\n{self.avgs:.2f} Average CPS for last 10 tries\n{self.avgm:.2f} Average CPM for last 10 tries"
        )
        self.sample_label.config(text=random.choice(self.texts))
        self.input_entry.delete(0, tk.END)

    # -------------------- on click function for clear button --------------------
    # clears the statistics for past runs
    def clear(self):
        open(Utility.get_file("../database/results.txt"), "w").close()
        self.avgs = 0
        self.avgm = 0
        self.reset()
        self.speed_label.config(
            text=f"Speed: \n0.00 CPS\n0.00 CPM\n0.00 Average CPS for last 10 tries\n0.00 Average CPM for last 10 tries"
        )
        self.mistake_count = {key: 0 for key in Utility.keyboard_layout}

    # -------------------- utility for drawing the heatmap --------------------
    def draw_heatmap(self):
        HeatmapShow.plot_heatmap(mistake_count=self.mistake_count)

    # -------------------- counts the average values of past runs --------------------
    def set_average(self):
        pair_arr = open(Utility.get_file("../database/results.txt"), "r").read().split("\n")
        length = len(pair_arr)
        self.avgs = 0
        self.avgm = 0
        i = 0

        while i < length - 1 and i < 10:
            pair = pair_arr[length - i - 2].split(" ")
            print(pair[0])
            print(pair[1])
            self.avgs += float(pair[0])
            self.avgm += float(pair[1])
            i += 1

        if i != 0:
            self.avgs /= i
            self.avgm /= i

TypeSpeedGUI()

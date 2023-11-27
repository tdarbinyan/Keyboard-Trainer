import tkinter as tk
import time
import threading
import random
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from .Utility import Utility

class HeatmapShow:
    
    # -------------------- constructor --------------------
    # is responsible for rendering the heatmap in a new window
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Statistics")
        self.root.geometry("1000x600")
        img = tk.PhotoImage(file=Utility.get_file("../infographics/heatmap.png"), master=self.root)
        img_label = tk.Label(self.root, image=img)
        img_label.place(x=0, y=0)
        self.root.mainloop()
    
    # -------------------- draws the heatmap --------------------
    def plot_heatmap(mistake_count):
        heatmap_data = np.zeros((4, 10))
        for key in mistake_count:
            row, col = divmod(Utility.positions[key], 10)
            print(f"Key: {key}, Row: {row}, Col: {col}")
            heatmap_data[row, col] = mistake_count[key]

        print(mistake_count)

        plt.figure(figsize=(10, 6))
        plt.imshow(heatmap_data, vmin=0, vmax=10)
        plt.colorbar()

        for key in mistake_count:
            row, col = divmod(Utility.positions[key], 10)
            plt.annotate(str(key), xy=(col, row), ha="center", va="center", color="white")

        plt.title("Keyboard Mistake Heatmap")
        plt.savefig(Utility.get_file("../infographics/heatmap.png"))
        HeatmapShow()
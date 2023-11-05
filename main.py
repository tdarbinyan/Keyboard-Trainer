import tkinter as tk
import time
import threading
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class ImageShow:
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("Statistics")
    self.root.geometry("1000x600")
    img = tk.PhotoImage(file="plot.png", master=self.root)
    img_label = tk.Label(self.root, image=img)
    img_label.place(x=0, y=0)
    self.root.mainloop()

class TypeSpeedGUI:
 


  def __init__(self):
    self.root = tk.Tk()
    self.root.title("Typing Speed Application")
    self.root.geometry("1000x600")

    self.cps = 0
    self.cpm = 0
    self.avgs = 0
    self.avgm = 0

    self.texts = open("texts.txt", "r").read().split("\n")

    self.frame = tk.Frame(self.root)

    self.sample_label = tk.Label(self.frame, text=random.choice(self.texts), font=("Helvetica", 18))
    self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

    self.input_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 24))
    self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
    self.input_entry.bind("<KeyPress>", self.start)

    self.set_average()
    self.speed_label = tk.Label(self.frame, text=f"Speed: \n0.00 CPS\n0.00 CPM\n{self.avgs:.2f} Average CPS for last 10 tries\n{self.avgm:.2f} Average CPM for last 10 tries", font=("Helvetica", 18))
    self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    self.clear_button = tk.Button(self.frame, text="Clear your statistics", command=self.clear)
    self.clear_button.grid(row = 3, column=0, columnspan=2, padx=5, pady=10)

    self.reset_button = tk.Button(self.frame, text="Show statistics plot", command=self.plot_float_changes_over_time)
    self.reset_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

    self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
    self.reset_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

    self.frame.pack(expand=True)

    self.counter = 0
    self.running = False

    self.root.mainloop()

  def start(self, event):
    if not self.running:
      if not event.keycode in [16, 17, 18]:
        self.running = True
        t = threading.Thread(target=self.time_thread)
        t.start()
    
    if not self.sample_label.cget('text').startswith(self.input_entry.get()):
      self.input_entry.config(fg="red")
    else:
      self.input_entry.config(fg="black")
       
    if self.input_entry.get() == self.sample_label.cget('text')[:-1]:
      self.running = False
      self.input_entry.config(fg="green")
      open("results.txt", "a").write(str(self.cps) + " " + str(self.cpm) + "\n")
      self.set_average()
      self.speed_label.config(text=f"Speed: \n{self.cps:.2f} CPS\n{self.cpm:.2f} CPM\n{self.avgs:.2f} Average CPS for last 10 tries\n{self.avgm:.2f} Average CPM for last 10 tries")


  def time_thread(self):
    while self.running:
      time.sleep(0.1)
      self.counter += 0.1
      self.cps = len(self.input_entry.get()) / self.counter
      self.cpm = self.cps * 60
      self.speed_label.config(text=f"Speed: \n{self.cps:.2f} CPS\n{self.cpm:.2f} CPM\n{self.avgs:.2f} Average CPS for last 10 tries\n{self.avgm:.2f} Average CPM for last 10 tries")

  def reset(self):
    self.running = False
    self.counter = 0
    self.speed_label.config(text=f"Speed: \n0.00 CPS\n0.00 CPM\n{self.avgs:.2f} Average CPS for last 10 tries\n{self.avgm:.2f} Average CPM for last 10 tries")
    self.sample_label.config(text=random.choice(self.texts))
    self.input_entry.delete(0, tk.END)

  def clear(self):
    open("results.txt", "w").close()
    self.reset()
    self.speed_label.config(text=f"Speed: \n0.00 CPS\n0.00 CPM\n0.00 Average CPS for last 10 tries\n0.00 Average CPM for last 10 tries")

  def set_average(self):
    pair_arr = open("results.txt", "r").read().split("\n")
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

  def plot_float_changes_over_time(self):
    # Initialize empty lists to store the data
    timestamps = []
    first_float_values = []

    # Read the file and extract data
    with open("results.txt", 'r') as file:
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

    # Create a line plot
    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.plot(timestamps, first_float_values, marker='o', linestyle='-')
    
    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('First Float Value')
    plt.title('Changes of the First Float Value Over Time')
    
    # Show the plot
    plt.grid(True)
    plt.savefig("plot.png")
    ImageShow()

TypeSpeedGUI()

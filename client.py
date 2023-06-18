import requests
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

import conf_loader as conf


class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")

        self.fig = Figure(figsize=(5, 4), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.update_graph()

    def update_graph(self):
        # clear the current plot
        self.fig.clear()

        # call the API
        response = requests.get('http://localhost:{0}/data'.format(conf.PORT))
        data = response.json()

        # create a new plot
        plot = self.fig.add_subplot(111)
        plot.plot(data['cpu']['total'])

        # refresh the canvas
        self.canvas.draw()

        # update the graph every second
        self.root.after(1000, self.update_graph)

root = tk.Tk()
app = App(root)
root.mainloop()

from tkinter import *
from time import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class Window(object):

    def __init__(self, loop=False):
        self.w = Tk()
        self.w.resizable(False, False)
        self.loop = loop
        self.labels = []
        self.bottons = []
        self.txt = ''
        self.frameRate = 0
        self.dolar = []
        self.euro = []
        self.btc = []

    def bottonPush(self, botton, column=0, row=0, command=None):
        self.bottons.append((botton, column, row))

    def setbottons(self, bottons):
        self.bottons = bottons

    def labelPush(self, label, column=0, row=0):
        self.labels.append((label, column, row))

    def setLabel(self, labels):
        self.labels = labels

    def setContainerTxt(self, txt):
        self.txt = txt

        self.renderQuote()

    def renderQuote(self):
        self.quote['text'] = self.txt

    def labelsRender(self):
        for label, col, row in self.labels:
            o = Label(self.w, text=label)
            o.grid(column=col, row=row, padx=10, pady=10)
        for label, col, row, command in self.bottons:
            o = Button(self.w, text=label, command=command)
            o.grid(column=col, row=row)

        self.quote = Label(self.w, text=self.txt)
        self.quote.grid(column=0, row=2)

    def mainLoop(self):
        if self.loop:

            self.w.mainloop()

    def title(self, title):
        self.w.title(title)

    def inLoop(self, cb):
        self.frameRate += 1
        dolar, euro, btc = cb()
        self.dolar.append(dolar)
        self.euro.append(euro)
        self.btc.append(btc)
        self.plot(self.canvas, self.ax)
        self.w.after(1000, lambda: self.inLoop(cb))

    def createCanvas(self):
        s = 2
        ss = 2
        fig = plt.figure(figsize=(ss, s))
        self.ax = fig.gca()
        self.canvas = FigureCanvasTkAgg(fig, master=self.w, )
        self.canvas.get_tk_widget().grid(row=3, column=0, )
        # canvas.show()

        # self.plotbutton = Button(
        #     master=self.w, text="plot", command=lambda: self.plot(self.canvas, self.ax))
        # self.plotbutton.grid(row=0, column=0)

    def plot(self, canvas: FigureCanvasTkAgg, ax):

        plt.plot(self.dolar)
        plt.plot(self.euro)
        plt.plot(self.btc)
        plt.legend(['dolar', 'euro', 'Bitcoin'])
        canvas.draw()
        ax.clear()

    def build(self, callback):
        self.labelsRender()
        self.createCanvas()
        self.inLoop(callback)

        self.mainLoop()

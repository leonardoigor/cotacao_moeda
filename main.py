import requests
# from PyInstaller.utils.hooks import collect_submodules
# collect_submodules('matplotlib')
from tkinter import *
from time import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class Window(object):

    def __init__(self, loop=False):
        self.w = Tk()
        # self.w.resizable(False, False)

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
            self.w.overrideredirect(True)
            self.w.bind('<Button-1>', self.clickwin)
            self.w.bind('<B1-Motion>', self.dragwin)

            Button(self.w, text='Sair', command=self.w.destroy).grid()
            self.w.mainloop()

    def dragwin(self, event):
        x = self.w.winfo_pointerx() - self.w._offsetx
        y = self.w.winfo_pointery() - self.w._offsety
        self.w.geometry('+{x}+{y}'.format(x=x, y=y))

    def clickwin(self, event):
        self.w._offsetx = event.x
        self.w._offsety = event.y

    def title(self, title):
        self.w.title(title)

    def checkSize(self):
        dolar = len(self.dolar)
        euro = len(self.euro)
        btc = len(self.btc)
        size = 100
        if dolar > size:
            self.dolar.pop(0)
        if euro > size:
            self.euro.pop(0)
        if btc > size:
            self.btc.pop(0)

    def inLoop(self, cb):
        self.frameRate += 1
        dolar, euro, btc = cb()
        self.dolar.append(dolar)
        self.euro.append(euro)
        self.btc.append(btc)
        self.plot(self.canvas, self.ax)
        self.checkSize()
        self.w.after(1000, lambda: self.inLoop(cb))

    def createCanvas(self):
        s = 2
        ss = 2

        fig, axs = plt.subplots(1)
        fig.set_figheight(ss, s)
        fig.set_figwidth(ss, s)
        fig.subplots_adjust(left=0.3, wspace=0.6)
        self.ax = axs
        self.canvas = FigureCanvasTkAgg(fig, master=self.w, )
        self.canvas.get_tk_widget().grid(row=3, column=0, )
        # canvas.show()

        # self.plotbutton = Button(
        #     master=self.w, text="plot", command=lambda: self.plot(self.canvas, self.ax))
        # self.plotbutton.grid(row=0, column=0)

    def plot(self, canvas: FigureCanvasTkAgg, ax):
        ax.plot(self.dolar)
        ax.plot(self.euro)
        ax.plot(self.btc)

        ax.legend(['dolar', 'euro', 'Bitcoin'])
        # plt.show()
        canvas.draw()
        ax.clear()

    def build(self, callback):
        self.labelsRender()
        self.createCanvas()
        self.inLoop(callback)

        self.mainLoop()


def get_coin_quote(uri='https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL'):
    req = requests.get(uri)
    req_dic = req.json()

    dolar = req_dic['USDBRL']['bid']
    euro = req_dic['EURBRL']['bid']
    btc = req_dic['BTCBRL']['bid']
    text = f'''
Dolar:    {dolar},  % Variação: {req_dic['USDBRL']['pctChange']}
Euro :    {euro},  % Variação: {req_dic['EURBRL']['pctChange']}
bitcoint: {btc}, % Variação: {req_dic['BTCBRL']['pctChange']}
    '''

    w.setContainerTxt(txt=text)
    return dolar, euro, btc


labels = [
    # ('Cotações das Moedas em Real-time', 0, 0),
]
bottons = [
    # ('Clique aqui', 0, 1, get_coin_quote),
]

w = Window(loop=True)
w.title('Cotação Atual das Moedas')
w.setLabel(labels)
w.setbottons(bottons)
w.build(callback=get_coin_quote)

#!/usr/bin/python

### Courtesy of: http://stackoverflow.com/questions/3294989/color-plot-animation-with-play-pause-stop-cabability-using-tkinter-with-pylab

from pylab import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Tkinter import *

colors=[None]*10
for i in range(len(colors)):
    colors[i]=rand(5,5)
    #colors = ['red','green','blue','orange','brown','black','white','purple','violet']
numcol=len(colors)

class App(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.top=Frame()
        self.top.grid()
        self.top.update_idletasks()

        self.makeWidgets()
        self.makeToolbar()

    def makeWidgets(self):
        # figsize (w,h tuple in inches) dpi (dots per inch)
        #f = Figure(figsize=(5,4), dpi=100)
        self.f = Figure()
        self.a = self.f.add_subplot(111)
        self.a.pcolor(rand(5,5))
        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.f, master=self.top)
        self.canvas.get_tk_widget().grid(row=3,column=0,columnspan=3)
        self.bClose = Button(self.top, text='Close',command=self.top.destroy)
        self.bClose.grid()
        #self.label = Label(self.top, text = 'Text',bg='orange')
        #self.label.grid()
        # initialize (time index t)
        self.t=0

    def makeToolbar(self):
        self.toolbar_text = ['Play','Pause','Stop']
        self.toolbar_length = len(self.toolbar_text)
        self.toolbar_buttons = [None] * self.toolbar_length

        for toolbar_index in range(self.toolbar_length):
            text = self.toolbar_text[toolbar_index]
            bg = 'yellow'
            button_id = Button(self.top,text=text,background=bg)
            button_id.grid(row=0, column=toolbar_index)
            self.toolbar_buttons[toolbar_index] = button_id

            def toolbar_button_handler(event, self=self, button=toolbar_index):
                return self.service_toolbar(button)

            button_id.bind("<Button-1>", toolbar_button_handler)

    # call blink() if start and set stop when stop            
    def service_toolbar(self, toolbar_index):
        if toolbar_index == 0:
            self.stop = False
            print self.stop
            self.blink()
        elif toolbar_index == 1:
            self.stop = True
            print self.stop
        elif toolbar_index == 2:
            self.stop = True
            print self.stop
            self.t=0

    # while in start, check if stop is clicked, if not, call blink recursivly
    def blink(self):
        if not self.stop:
            print 'looping',self.stop
            self.a.pcolor(colors[self.t])
            #draw()
            #self.label.configure(bg=colors[self.t])
            self.t += 1
            if self.t == numcol: # push stop button
                self.service_toolbar(2)
            self.canvas.show() # insert this line
            self.canvas.get_tk_widget().update_idletasks()
            self.canvas.get_tk_widget().update_idletasks()
            #self.label.update_idletasks()
            self.after(500, self.blink)

#root = Tk()
app=App()
app.mainloop()

# -*- encoding: utf-8 -*-

"""A simple graph viewer."""

import math
import sys
from random import random
from omtk.vendor.jurij import *

if sys.version.startswith('2'):
    from Tkinter import *
    from ScrolledText import *
else:
    from tkinter import *
    from tkinter.scrolledtext import *

help_text = """
The simple graph viewer allows you to draw various graphs and test
layout algorithms on them.

To draw a graph, enter its Python definition in the input field and
press the Draw! button. Examples of definitions:
  cycle(5)
  path(30)
  complete_graph(7)
  cone(cycle(10))
  product(path(3), cycle(4))
  igraph(5,2,1)
  cayley_graph(symmetric_group(4))
  cayley_graph(Group([1,2], operation=(lambda x,y: (x+y)%13)))
  cayley_graph(permutation_group([(1,0,2,3), (0,3,1,2)]))

You can also enter a specific graph by giving a list of edges or an
adjancency dictionary, for example:
  [(1,2), (2,3), (2,4), (3,4)]
  {1 : [2], 2 : [3,4], 3 : [4], 4 : []}

For further information on what is available see the modules jurij.graph,
jurij.group and jurij.library."""


class GraphViewer():
    def __init__(self, width=500, height=500):
        self.width=width
        self.height=height
        self._layout_worker = None
        self.window = Tk()
        self.window.title("Graph viewer")
        menu = Menu(self.window)
        self.window.config(menu = menu)
        layout_menu = Menu(self.window)
        menu.add_cascade(label='Layout', menu=layout_menu)
        layout_menu.add_command(label="Random", command=self.random_layout)
        layout_menu.add_command(label="Shake", command=self.shake_layout)
        layout_menu.add_command(label="Circular", command=self.circular_layout)
        layout_menu.add_command(label="Spring", command=self.spring_layout)
        layout_menu.add_separator()
        layout_menu.add_command(label="Help", command=self.help)
        label = Label(self.window, text='Graph:')
        label.grid(row=0,column=0, sticky=W)
        self.input_field = Entry(self.window)
        self.input_field.grid(row=0,column=1, sticky=E+W)
        button = Button(self.window, text='Draw!', command=self.menu_set_graph)
        button.grid(row=0, column=2, sticky=E)
        self.window.columnconfigure(1, weight=1)
        self.canvas = Canvas(self.window, width=self.width, height=self.height)
        self.canvas.grid(column=0, row=1, columnspan=3)
        self.set_graph(Graph())

    def start(self):
        '''Enter the main loop. This should be called after the graph viewer is created.'''
        self.window.mainloop()

    def help(self):
        help_window = Toplevel(master=self.window)
        help_window.title("Graph viewer help")
        text = ScrolledText(master=help_window)
        text.insert(END, help_text)
        text.grid(row=0,column=0)

    def set_graph(self,g):
        '''Set the graph displayed by the graph viewer with random initial layout.'''
        self.graph = g
        self.random_layout()

    def menu_set_graph(self):
        try:
            g = eval(self.input_field.get())
            if type(g) == dict or type(g) == list:
                g = Graph(g)
            self.set_graph(g)
        except Exception as e:
            # This should appear in a dialog window
            print ('Problem: {0}'.format(e))

    def bounding_box(self, layout):
        '''The bounding box of a graph layout.'''
        if layout == []:
            return (0,1,0,1)
        else:
            (minx,maxx) = (float('inf'), float('-inf'))
            (miny,maxy) = (float('inf'), float('-inf'))
            for (x,y) in layout.values():
                minx = min(minx,x)
                maxx = max(maxx,x)
                miny = min(miny,y)
                maxy = max(maxy,y)
            (cx, cy) = ((maxx+minx)/2, (maxy+miny)/2)
            r = max(maxx-minx, maxy-miny)/2
            return (cx-r, cx+r, cy-r, cy+r)

    def update_layout(self, layout):
        '''Set the graph layout.'''
        self.layout = layout
        self.canvas.delete(ALL)
        self.points = {}
        self.lines = {}
        (xmin,xmax,ymin,ymax) = self.bounding_box(self.layout)
        (dx,dy) = (xmax - xmin, ymax - ymin)
        for (u,v) in self.graph.edges():
            (x1,y1) = self.layout[u]
            (x2,y2) = self.layout[v]
            self.lines[(u,v)] = self.canvas.create_line(
                int(10 + (x1-xmin)/dx*(self.width-20)),
                int(10 + (ymax-y1)/dy*(self.height-20)),
                int(10 + (x2-xmin)/dx*(self.width-20)),
                int(10 + (ymax-y2)/dy*(self.height-20)))
        for v in self.graph.vertices():
            (x,y) = self.layout[v]
            x = int(10 + (x-xmin)/dx*(self.width-20))
            y = int(10 + (ymax-y)/dy*(self.height-20))
            self.points[v] = self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="white")

    def circular_layout(self):
        '''Map the vertices of a graph on the unit circle.'''
        layout = {}
        n = float(len(self.graph.vertices()))
        for (k,v) in enumerate(self.graph.vertices()):
            phi = 2 * math.pi * k / n
            layout[v] = (math.cos(phi), math.sin(phi))
        self.update_layout(layout)

    def random_layout(self):
        '''Map the vertices of a graph randomly onto the plane.'''
        self.update_layout(dict([(v,(random(), random())) for v in self.graph.vertices()]))

    def shake_layout(self):
        '''Petrurb the layout a bit.'''
        layout = self.layout
        (xmin,xmax,ymin,ymax) = self.bounding_box(layout)
        d = 0.1 * max(xmax-xmin, ymax-ymin)
        for (v,(x,y)) in layout.items():
            layout[v] = (x + d * random(), y + d * random())
        self.update_layout(layout)

    def spring_layout(self):
        if self._layout_worker: self.canvas.after_cancel(self._layout_worker)
        self.layout_iteration = 1000
        self.spring_layout_worker()

    def spring_layout_worker(self):
        columb = 1.0 # Intensity of Columb's force
        hook = 0.1 # Intensity of Hook's force
        dt = 0.5 # Time step
        layout = self.layout
        if self.layout_iteration > 0:
            self.layout_iteration = self.layout_iteration - 1
            # Compute change of layout
            kinetic = 0.0  # kinetic energy
            for u in self.graph.vertices():
                # Compute the acceleration of u
                (x,y) = layout[u]
                (ax, ay) = (0,0)
                for v in self.graph.vertices():
                    if u != v:
                        (a,b) = layout[v]
                        d = max(0.001, (x-a)*(x-a) + (y-b)*(y-b))
                        # Columb's law
                        ax -= columb * (a-x)/(d*d);
                        ay -= columb * (b-y)/(d*d);
                for v in self.graph.adjacency[u]:
                    # Hook's law
                    (a,b) = layout[v]
                    ax += hook * (a-x)
                    ay += hook * (b-y)
                for v in self.graph.opposite()[u]:
                    # Hook's law
                    (a,b) = layout[v]
                    ax += hook * (a-x)
                    ay += hook * (b-y)
                # Update velocities
                vx = dt * ax
                vy = dt * ay
                kinetic += vx * vx + vy * vy
                x = x + dt * vx + ax * dt * dt
                y = y + dt * vy + ay * dt * dt
                layout[u] = (x,y)
            if kinetic < 1e-6: self.layout_iteration = 0
            self.update_layout(layout)
            self._layout_worker = self.canvas.after(20, self.spring_layout_worker)



def show(g, width=500, height=500):
    viewer = GraphViewer(width=width, height=height)
    viewer.start()
    viewer.set_graph(g)

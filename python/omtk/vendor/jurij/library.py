# -*- encoding: utf-8 -*-

# A library of graphs

from omtk.vendor.jurij.graph import *

def complete_graph(n):
    '''Complete graph on n vertices.'''
    return Graph(vertices=range(n),
                 edges=[(i,j) for j in range(n) for i in range(j)])

def cycle(n):
    '''Cycle on n vertices.'''
    return Graph(dict([(k,[(k+1)%n]) for k in range(n)]))

def path(n):
    '''Path on n vertices.'''
    return Graph([(k,k+1) for k in range(n-1)])

def igraph(n,i,j):
    '''I-graph of type (n,i,j).'''
    return Graph(vertices = [(0,k) for k in range(n)] + [(1,k) for k in range(n)],
                 edges = [((0,k),(1,k)) for k in range(n)] +
                         [((0,k),(0,(k+i)%n)) for k in range(n)] +
                         [((1,k),(1,(k+j)%n)) for k in range(n)])

def cayley_graph(g):
    '''The Cayley graph of a finitely generated finite group.'''
    return Graph(g)

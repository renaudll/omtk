# -*- encoding: utf-8 -*-

# A very simple implementation of graphs in python, including graphs
# embedded in the plane.

class Graph():
    """A graph stored as an adjacency dictionary."""

    def __init__(self, data=None, vertices=None, edges=None,
                 vertex_labels=None, edge_labels=None):
        """Construct a graph to from the given data.
        The object must define methods vertices() and edges() which
        return iterators on vertices and edges, respectively. Vertices
        are required to be hashable objects while edges are pairs of
        vertices."""
        if type(data) == dict:
            # the graph is given as an adjancency dictionary
            self.adjacency = dict([(x,set(ys)) for (x,ys) in data.items()])
        elif type(data) in (list, tuple):
            # the graph is given as a list of edges
            self.adjacency = {}
            for (x,y) in data:
                self.adjacency[x] = set()
                self.adjacency[y] = set()
            for (x,y) in data: self.adjacency[x].add(y)
        elif data is None:
            self.adjacency = {}
            if vertices is not None:
                for x in vertices: self.adjacency[x] = set()
            if edges is not None:
                for (x,y) in edges:
                    if x not in self.adjacency: self.adjacency[x] = set()
                    if y not in self.adjacency: self.adjacency[y] = set()
                    self.adjacency[x].add(y)
        else:
            # the graph is given by an object which can produce
            # a list of vertices and a list of edges
            self.adjacency = dict([(x,set()) for x in data.vertices()])
            for (x,y) in data.edges(): self.adjacency[x].add(y)
        self.vertex_labels = {}
        if vertex_labels is not None:
            for x in self.adjacency:
                if x in vertex_labels:
                    self.vertex_labels[x] = vertex_labels[s]
        elif hasattr(data, 'vertex_label'):
            for x in self.adjacency:
                u = data.vertex_label(x)
                if u is not None: self.vertex_labels[x] = u
        self.edge_labels = {}
        if edge_labels is not None:
            for (x,ys) in self.adjacency.items():
                for y in ys:
                    if (x,y) in edge_labels:
                        self.edge_labels[(x,y)] = edge_labels[(x,y)]
        elif hasattr(data, 'edge_label'):
            for (x,ys) in self.adjacency.items():
                for y in ys:
                    u = data.edge_label((x,y))
                    if u is not None: self.edge_labels[(x,y)] = u

    def __repr__(self):
        return 'Graph({0})'.format(self.adjacency)

    def vertices(self):
        '''The set vertices of the graph as an iterator.'''
        return self.adjacency.keys()

    def edges(self):
        '''The edges of the graph as an iterator.'''
        for (u, vs) in self.adjacency.items():
            for v in vs:
                yield (u,v)

    def opposite(self):
        '''The opposite adjacency, i.e., with all edges reversed.'''
        if hasattr(self, '_opposite_adjacency'):
            return self._opposite_adjacency
        else:
            self._opposite_adjacency = dict([(x,set()) for x in self.vertices()])
            for (x, ys) in self.adjacency.items():
                for y in ys:
                    self._opposite_adjacency[y].add(x)
            return self._opposite_adjacency

    def vertex_label(self,x):
        return self.vertex_labels.get(x)

    def edge_label(self,e):
        return self.edge_labels.get(e)

    def add_vertex(self,x):
        if x not in self.adjacency:
            self.adjaceny[x] = set()

    def remove_vertex(self,x):
        del self.adjacency[x]
        for xs in self.adjacency.values():
            xs.remove(x)

    def add_edge(self,e):
        (x,y) = e
        self.adjacency[x].add(y)

    def remove_edge(self,e):
        (x,y) = e
        self.adjacency[x].remove(y)

    def vertex_size(self):
        return len(self.vertices())

    def edge_size(self):
        return len(self.edges())

def product(g,h):
    '''The product of graphs g and h.'''
    return Graph(vertices = [(x,y) for x in g.vertices() for y in h.vertices()],
                 edges = [((x,u), (x,v)) for x in g.vertices() for (u,v) in h.edges()] +
                         [((u,y), (v,y)) for (u,v) in g.edges() for y in h.vertices()])

def cone(g):
    '''The cone over g.'''
    k = 0
    adj = {}
    for x in g.vertices():
        adj[x] = g.adjacency[x]
        if type(x) == int: k = max(k, x+1)
    adj[k] = g.vertices()
    return Graph(adj)


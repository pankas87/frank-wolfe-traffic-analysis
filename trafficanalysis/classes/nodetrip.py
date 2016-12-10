import collections
import networkx as nx

class NodeTrip:
  start_node        = ''
  end_node          = ''
  vehicles_per_trip = 0.0
  path              = collections.OrderedDict()

  def __init__(self, start_node, end_node, vehicles_per_trip):
    self.start_node        = start_node
    self.end_node          = end_node
    self.vehicles_per_trip = vehicles_per_trip

  def set_path(self, path):
    self.path = path
    return self

  def get_shortest_path(self, graph):
    return nx.dijkstra_path( graph, self.start_node, self.end_node )

  def calculate_shortest_path(self, graph):
    self.set_path( self.get_shortest_path( graph ) )

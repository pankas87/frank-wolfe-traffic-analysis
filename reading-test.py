import networkx as nx
import matplotlib.pyplot as plt
import trafficanalysis as ta

node_reader = ta.NodeFileParser('ChicagoSketch.node')
nodes       = node_reader.read()

edge_reader = ta.NetFileParser('ChicagoSketch.net')
edges       = edge_reader.read()

graph = nx.Graph()

for node in nodes:
  graph.add_node( node.number, pos=( node.x, node.y ) )

for edge in edges:
  graph.add_edge( edge.tail_node, edge.head_node )

nx.draw( graph, nx.get_node_attributes( graph, 'pos' ) )
plt.show()
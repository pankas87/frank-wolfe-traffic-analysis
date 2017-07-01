from .resultsfilereader import ResultsFileReader
from .nodefileparser import NodeFileParser
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import networkx as nx
from array import array

class ResultsGraph:
  def __init__(self, nodes, edges):
    self.nodes             = nodes
    self.edges             = edges
    self.graph             = self.initialize_graph( self.nodes, self.edges )

  def initialize_graph(self, nodes, edges):
    graph = nx.DiGraph()

    for key, node in nodes.iteritems():
      graph.add_node( node.label, pos=( node.x, node.y ), label=node.label )

    for key, edge in edges.iteritems():
      congestion = edge.get_traffic_congestion( 0 )
      color      = self.get_color_from_congestion( congestion )
      
      graph.add_edge( edge.tail_node, edge.head_node, color=color  )

    return graph

  def render(self): 
    node_positions      = nx.get_node_attributes( self.graph, 'pos' )
    node_labels         = nx.get_node_attributes( self.graph, 'label' )
    edge_colors         = []
    edges               = self.graph.edges()

    for edge in edges:
      edge_data = self.graph.get_edge_data( edge[0], edge[1] ) 
      edge_colors.append( edge_data[ 'color' ] )


    nx.draw_networkx_nodes( self.graph, pos=node_positions, node_size=300, node_color="#AAAAAA" )

    nx.draw_networkx_labels( self.graph, pos=node_positions, labels=node_labels, font_size=9, font_color="#222222")

    nx.draw_networkx_edges( self.graph, node_positions, arrows=True, edge_color=tuple( edge_colors ) )

    plt.show()

    return self

  def get_color_from_congestion(self, congestion):
    green  = '#24BF05'
    yellow = '#FFFB00'
    orange = '#FF7000'
    red    = '#FF0000'

    if( congestion >= 0.0 and congestion < 0.50 ):
      return green
    elif( congestion >= 0.50 and congestion < 0.75 ):
      return yellow
    elif( congestion >= 0.75 and congestion < 1.0 ):
      return orange
    elif( congestion > 1.0 ):
      return red    

  @classmethod
  def from_files(cls, nodes_file_path, results_file_path):
    nodes = NodeFileParser( nodes_file_path ).read()
    edges = ResultsFileReader( results_file_path ).read()

    return cls( nodes, edges )
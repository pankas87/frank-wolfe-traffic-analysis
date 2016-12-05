import networkx as nx
import matplotlib.pyplot as plt

graph = nx.Graph()
nodes = [1,2,3,4,5,6,7,8]
edges = [[1,3],[1,4],[2,4],[2,3],[2,5],[4,5],[4,6],[4,7],[4,8],[6,1],[6,2],[6,3],[7,2],[8,3]]

graph.add_nodes_from( nodes )
graph.add_edges_from( edges )

nx.draw(graph)
plt.show()
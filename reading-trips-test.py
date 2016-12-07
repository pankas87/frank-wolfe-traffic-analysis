import networkx as nx
import matplotlib.pyplot as plt
import trafficanalysis as ta

trips_reader = ta.TripsFileParser('ChicagoSketch_trips.txt')
trips_matrix = trips_reader.read()

print str( trips_matrix[1][50].__dict__ )
print str( trips_matrix[10][23].__dict__ )
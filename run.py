import networkx as nx
import trafficanalysis as ta

analysis = ta.Analysis.from_files('ChicagoSketch.node', 'ChicagoSketch.net', 'ChicagoSketch_trips.txt', True).run()
#analysis = ta.Analysis.from_files('ChicagoSketch.node', 'ChicagoSketch.net', 'ChicagoSketch_trips.txt', True)
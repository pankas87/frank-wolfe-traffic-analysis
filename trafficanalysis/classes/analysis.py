from .nodefileparser import NodeFileParser
from .netfileparser import NetFileParser
from .tripsfileparser import TripsFileParser
from .nodetrip import NodeTrip
import networkx as nx
import time
from datetime import datetime
import multiprocessing as mp
import Queue

class Analysis:
  MAX_PARALLEL_PROCESSES = 90
  nodes                  = None
  edges                  = None 
  trips                  = None
  graph                  = None
  alpha                  = None
  n                      = 0
  convergence            = False

  def __init__(self, nodes, edges, trips, verbose = True):
    self.nodes   = nodes
    self.edges   = edges
    self.trips   = trips
    self.verbose = verbose

  def run(self):

    while( not self.convergence ):
      self.print_message('Starting Iteration: ' + str(self.n), True )

      self.graph = self.initialize_graph( self.n )
      self.trips = self.calculate_shortest_paths_over_trips( self.trips, self.graph )
      self.edges = self.assign_edges_traffic_change_from_trips( self.n, self.trips, self.edges )
      
      if( self.n > 0 ):
        for k, edge in self.edges.iteritems():
          self.print_message( 'Alpha Values:' )
          self.print_message( 'tail_node: ' + str( edge.tail_node ) )
          self.print_message( 'head_node: ' + str( edge.head_node ) )
          self.print_message( 'capacity: ' + str( edge.capacity ) )
          self.print_message( 'fftt: ' + str( edge.fftt ) )
          self.print_message( 'b: ' + str( edge.b ) )
          self.print_message( 'power: ' + str( edge.power ) )
          self.print_message( 'x[n]: ' + str( edge.get_traffic( self.n ) ) )
          self.print_message( 'y[n]: ' + str( edge.get_traffic_change( self.n ) ) )
          self.print_message( 'Alpha with 1: ' + str( edge.calculate_alpha_equation( self.n, 1 ) ) )
          self.print_message( 'Alpha with 0.5: ' + str( edge.calculate_alpha_equation( self.n, 0.5 ) ) )
          self.print_message( 'Alpha with 0: ' + str( edge.calculate_alpha_equation( self.n, 0 ) ) )
          self.print_message( '' )
          self.print_message( '', True )


      if( self.n == 1 ):
        self.convergence = True

      self.n += 1
    return self

  def initialize_graph(self, n):
    graph = nx.DiGraph()

    # Adding nodes to the graphs
    for key, node in self.nodes.iteritems():      
      graph.add_node( node.label, pos=( node.x, node.y ) )

    # Adding edges to the graph
    for key, edge in self.edges.iteritems():
      graph.add_edge( edge.tail_node, edge.head_node, label=edge.label, weight=edge.performance_function( n, True ) )

    return graph

  def calculate_shortest_paths_over_trips(self, trips, graph):
    q                = mp.Queue()
    processes        = []
    trips_to_process = len( trips )
    i                = 1
    starting_time    = datetime.fromtimestamp( time.time() )

    origins          = set()
    path_trees       = {}

    for key, trip in trips.iteritems():
      origins.add( trip.start_node )

    self.print_message( 'Starting calculation of shortest paths', True )

    while( origins ):
      origin               = origins.pop()
      path_trees[ origin ] = nx.single_source_dijkstra_path( graph, origin )

    for key, trip in trips.iteritems():
      path = path_trees[ trip.start_node ][ trip.end_node ]
      trip.set_path( path )

    return trips

  def parallel_shortest_path(self, graph, key, trip, q):
    result           = {}
    result[ 'path' ] = trip.get_shortest_path( graph )
    result[ 'key' ]  = key

    try:
      q.put( result, True )
    except Queue.Full:
      self.print_message( 'Queue is full', True )

    #self.print_message('Trip - From: ' + str(trip.start_node) + ' To: ' + str(trip.end_node) )
    #self.print_message( 'Path' )
    #self.print_message( str( result[ 'path' ] ) )

  def assign_edges_traffic_change_from_trips(self, n, trips, edges):

    for key, trip in trips.iteritems():

      i = 0
      j = 1

      while( j < len( trip.path ) ):
        edge_key = str( trip.path[i] ) + '-' + str( trip.path[j] )
        edge     = edges[ edge_key ]

        edge.add_traffic_change( trip.vehicles_per_trip, n )

        if( n == 0 ):
          edge.add_traffic( trip.vehicles_per_trip, n + 1 )

        i += 1
        j += 1

        # Debug message      
        self.print_message('Edge: ' + edge.label )
        self.print_message( 'Vehicles - From: ' + str( edge.get_traffic( n ) ) + ' to: ' + str( edge.get_traffic_change( n ) ) )
        self.print_message('')

    self.print_message('', True)

    return edges

  def solve_alpha(self, n, edges):
    return None

  def calculate_alpha_function(self, n, edges, alpha):
    sum = 0

    for key, edge in edges.iteritems():
      sum += edge.calculate_alpha_equation(n, alpha)

    return sum

  def assign_edges_traffic_with_alpha(self, n, trips, edges):
    return None

  def print_message(self, message, wait_for_user = False):
    if self.verbose:
      print message

    if( wait_for_user ):
      raw_input('Press Enter to Continue...')

  @classmethod
  def from_files(cls, nodes_file_path, edges_file_path, trips_file_path, verbose):
    nodes = NodeFileParser( nodes_file_path ).read()
    edges = NetFileParser( edges_file_path ).read()
    trips = TripsFileParser( trips_file_path ).read()

    return cls(nodes, edges, trips, verbose)

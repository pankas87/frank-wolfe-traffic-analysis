from .nodefileparser import NodeFileParser
from .netfileparser import NetFileParser
from .tripsfileparser import TripsFileParser
from .nodetrip import NodeTrip
from .logs import Logs
from .results import Results
import networkx as nx
import time
import datetime
import multiprocessing as mp
import Queue
import math

class Analysis:
  def __init__(self, nodes, edges, trips, verbose = True):
    self.ALPHA_PRECISSION       = Decimal( 0.000001 )
    self.CONVERGENCE_PRECISSION = Decimal( 0.01 )    
    self.NUM_ALPHA_CANDIDATES   = 35
    self.nodes                  = None
    self.edges                  = None 
    self.trips                  = None
    self.graph                  = None
    self.alpha                  = [None]
    self.f_alpha                = [None]
    self.n                      = 0
    self.convergence            = False
    self.convergence_sum        = [None]
    self.nodes                  = nodes
    self.edges                  = edges
    self.trips                  = trips
    self.verbose                = verbose
    self.logs                   = Logs()
    self.results                = Results( self.edges )

  def run(self):

    while( not self.convergence ):
      self.print_message('Starting Iteration: ' + str( self.n ), True )

      self.graph = self.initialize_graph( self.n )
      self.trips = self.calculate_shortest_paths_over_trips( self.trips, self.graph )
      self.edges = self.assign_edges_traffic_change_from_trips( self.n, self.trips, self.edges )      

      if( self.n >= 1 ):
        alpha_solution = self.solve_alpha( self.n, self.edges )
        self.alpha.append( alpha_solution[ 'alpha' ] )
        self.f_alpha.append( alpha_solution[ 'f_alpha' ] )

        self.edges = self.assign_edges_traffic_with_alpha( self.n, self.alpha[ self.n ], self.edges )

        self.print_message( 'Alpha:  ' + str( self.alpha[ self.n ] ), True )      

        self.convergence = self.is_convergent( self.n, self.edges )

        self.log_results()

      self.save_results( self.n );

      self.n += 1

    self.print_message( 'It is convergent at iteration: ' + str( self.n ) )

    print 'It is convergent at iteration: ' + str( self.n )
    print datetime.datetime.now().strftime( "%d %b %Y %H:%M:%S"  )
    raw_input( 'Ola ke ase? Termino o ke ase?' )

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

    return edges

  def solve_alpha(self, n, edges):
    found           = False
    closest_to_zero = { 'up': { 'alpha': 1.0, 'f_alpha': None }, 'down': { 'alpha': -1.0, 'f_alpha': None } }
    solution_alpha  = None
    
    # Debug message
    self.print_message( 'Looking for alpha solution' )


    while( not found ):

      candidate_alphas = self.calculate_candidate_alphas( closest_to_zero )

      # Debug message
      self.print_message( 'cand_alpha' + str( candidate_alphas ) )

      for alpha in candidate_alphas:
        f_alpha = self.calculate_alpha_function( n, edges, alpha )
        
        if( f_alpha >= Decimal( 0.0 ) ):
          if( closest_to_zero[ 'up' ][ 'f_alpha' ] == None or math.fabs( f_alpha ) < math.fabs( closest_to_zero[ 'up' ][ 'f_alpha' ] ) ):
            closest_to_zero[ 'up' ][ 'alpha' ]   = alpha
            closest_to_zero[ 'up' ][ 'f_alpha' ] = f_alpha
        if( f_alpha < Decimal( 0.0 ) ):
          if( closest_to_zero[ 'down' ][ 'f_alpha' ] == None or math.fabs( f_alpha ) < math.fabs( closest_to_zero[ 'down' ][ 'f_alpha' ] ) ):
            closest_to_zero[ 'down' ][ 'alpha' ]   = alpha
            closest_to_zero[ 'down' ][ 'f_alpha' ] = f_alpha

      if( math.fabs( closest_to_zero[ 'up' ][ 'f_alpha' ] ) <= math.fabs( closest_to_zero[ 'down' ][ 'f_alpha' ] ) ):
        alpha_to_test = closest_to_zero[ 'up' ]
      else:
        alpha_to_test = closest_to_zero[ 'down' ]

      if( alpha_to_test[ 'f_alpha' ] >= Decimal( 0 ) and alpha_to_test[ 'f_alpha' ] <= Decimal( self.ALPHA_PRECISSION ) ):
        solution_alpha = alpha_to_test
        found = True

        # Debug message
        self.print_message( 'solution_alpha: f(' + str( alpha_to_test[ 'alpha' ] ) + ')=' + str( alpha_to_test[ 'f_alpha' ] ) )
        self.print_message( '', True )

    return solution_alpha

  def calculate_candidate_alphas(self, closest_to_zero):
    result = []
    up     = Decimal( closest_to_zero[ 'up' ][ 'alpha' ] )
    down   = Decimal( closest_to_zero[ 'down' ][ 'alpha' ] )
    diff   = Decimal( math.fabs( up - down ) )
    step   = Decimal( diff / self.NUM_ALPHA_CANDIDATES )
    i      = up

    while( i >= down ):
      result.append( i )
      i -= step

    return result

  def calculate_alpha_function(self, n, edges, alpha):
    sum = Decimal( 0 )

    for key, edge in edges.iteritems():
      sum += Decimal( edge.calculate_alpha_equation(n, alpha) )

    return sum

  def assign_edges_traffic_with_alpha(self, n, alpha, edges):

    for key, edge in edges.iteritems():
      x           = Decimal( edge.get_traffic( n ) )
      y           = Decimal( edge.get_traffic_change( n ) )
      new_traffic = float( ( x ) + ( alpha * ( y - x ) ) )

      edge.add_traffic( new_traffic, n + 1 )

      # Debug message      
      self.print_message('Edge: ' + edge.label )
      self.print_message( 'New Vehicles - From: ' + str( edge.get_traffic( n ) ) + ' to: ' + str( edge.get_traffic( n + 1 ) ) )
      self.print_message('')

    return edges

  def is_convergent(self, n, edges):
    sum = Decimal( 0 )

    for key, edge in edges.iteritems():
      sum += Decimal( edge.convergence_function( n ) )

    self.convergence_sum.append(sum)

    if( sum >= Decimal( 0 ) and sum <= self.CONVERGENCE_PRECISSION ):
      return True
    else:
      return False

  def print_message(self, message, wait_for_user = False):
    if self.verbose:
      print message

    #if( wait_for_user ):
      #raw_input('Press Enter to Continue...')

  def log_results(self):
    self.logs.log( self.n, self.alpha, self.f_alpha, self.convergence_sum )

  def save_results(self, n):
    self.results.save( n )

  @classmethod
  def from_files(cls, nodes_file_path, edges_file_path, trips_file_path, verbose):
    nodes = NodeFileParser( nodes_file_path ).read()
    edges = NetFileParser( edges_file_path ).read()
    trips = TripsFileParser( trips_file_path ).read()

    return cls(nodes, edges, trips, verbose)

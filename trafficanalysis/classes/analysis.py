from .nodefileparser import NodeFileParser
from .netfileparser import NetFileParser
from .tripsfileparser import TripsFileParser
from .nodetrip import NodeTrip
from .logs import Logs
from .results import Results
from decimal import *
import networkx as nx
import time
import datetime
import multiprocessing as mp
import Queue
import math

class Analysis:
  def __init__(self, nodes, edges, trips, mode, verbose = True):
    self.ALPHA_PRECISSION       = Decimal( 0.0000001 )
    self.CONVERGENCE_PRECISSION = Decimal( 0.00000000001 )
    self.NUM_ALPHA_CANDIDATES   = 10
    self.nodes                  = None
    self.edges                  = None 
    self.trips                  = None
    self.graph                  = None
    self.alpha                  = [None]
    self.f_alpha                = [None]
    self.n                      = 0
    self.convergence            = False
    self.convergence_sums       = [None]
    self.nodes                  = nodes
    self.edges                  = edges
    self.trips                  = trips
    self.verbose                = verbose
    self.logs                   = Logs( mode )
    self.results                = Results( self.edges, mode )
    self.mode                   = mode

  def run(self):
    alpha_precision      = self.ALPHA_PRECISSION
    num_alpha_candidates = self.NUM_ALPHA_CANDIDATES

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
        sum        = self.convergence_sum( self.n, self.edges )        
        self.convergence_sums.append( sum )

        if( self.convergence_sums[ self.n ] < Decimal( 10.0 ) ):
          alpha_precision = Decimal( 0.000000000001 )
        elif( self.convergence_sums[ self.n ] < Decimal( 3.0 ) ):
          alpha_precision = Decimal( 0.0000000000001 )
        else:
          alpha_precision = self.ALPHA_PRECISSION

        self.log_results()

        self.convergence = self.is_convergent( self.convergence_sums[ self.n ] ) 

        self.print_message( 'Convergence Sum: ' + str( sum ) )
        self.print_message( '' )

      self.save_results( self.n );

      self.n += 1

    print 'It is convergent at iteration: ' + str( self.n - 1 )
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

    return edges

  def solve_alpha(self, n, edges):
    found           = False
    segments        = self.NUM_ALPHA_CANDIDATES
    closest_to_zero = { 'up': { 'alpha': Decimal( 1.0 ), 'f_alpha': None }, 'down': { 'alpha': Decimal( -1.0 ), 'f_alpha': None } }
    solution_alpha  = None
    iterations      = 0
    
    # Debug message
    self.print_message( 'Looking for alpha solution' )

    while( not found ):

      if( ( iterations % 30 ) == 0 ):
        closest_to_zero = { 'up': { 'alpha': Decimal( 1.0 ), 'f_alpha': None }, 'down': { 'alpha': Decimal( -1.0 ), 'f_alpha': None } }
        segments *= Decimal( 2.0 )

      self.print_message( 'Getting candidate alphas' )
      candidate_alphas = self.calculate_candidate_alphas( closest_to_zero, segments )
      self.print_message( 'Testing new array of candidate alphas' )

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

      if( math.fabs( alpha_to_test[ 'f_alpha' ] ) >= Decimal( 0 ) and math.fabs( alpha_to_test[ 'f_alpha' ] ) <= self.ALPHA_PRECISSION ):
        solution_alpha = alpha_to_test
        found = True

        # Debug message
        self.print_message( 'solution_alpha: f(' + str( alpha_to_test[ 'alpha' ] ) + ')=' + str( alpha_to_test[ 'f_alpha' ] ) )
        self.print_message( '', True )

      iterations += 1

    return solution_alpha

  def calculate_candidate_alphas(self, closest_to_zero, segments):
    result = []
    up     = closest_to_zero[ 'up' ][ 'alpha' ]
    down   = closest_to_zero[ 'down' ][ 'alpha' ]
    diff   = Decimal( math.fabs( up - down ) )
    step   = Decimal( diff / segments )
    i      = segments
    num    = up    

    while( i >= 0 ):
      result.append( num )
      
      num -= step
      i   -= 1

    return result

  def calculate_alpha_function(self, n, edges, alpha):
    sum = Decimal( 0 )

    for key, edge in edges.iteritems():
      sum += edge.calculate_alpha_equation(n, alpha)

    return sum

  def assign_edges_traffic_with_alpha(self, n, alpha, edges):

    for key, edge in edges.iteritems():
      x           = Decimal( edge.get_traffic( n ) )
      y           = Decimal( edge.get_traffic_change( n ) )
      new_traffic = float( ( x ) + ( alpha * ( y - x ) ) )

      edge.add_traffic( new_traffic, n + 1 )

    return edges

  def convergence_sum(self, n, edges):
    sum = Decimal( 0 )

    for key, edge in edges.iteritems():
      sum += edge.convergence_function( n )

    return sum

  def is_convergent(self, convergence_sum):
    if( convergence_sum >= Decimal( 0 ) and convergence_sum <= self.CONVERGENCE_PRECISSION ):
      return True
    else:
      return False

  def print_message(self, message, wait_for_user = False):
    if self.verbose:
      print message

    #if( wait_for_user ):
      #raw_input('Press Enter to Continue...')

  def log_results(self):
    self.logs.log( self.n, self.alpha, self.f_alpha, self.convergence_sums )

  def save_results(self, n):
    self.results.save( n )

  @classmethod
  def from_files(cls, nodes_file_path, edges_file_path, trips_file_path, mode, verbose):
    nodes = NodeFileParser( nodes_file_path ).read()
    edges = NetFileParser( edges_file_path, mode ).read()
    trips = TripsFileParser( trips_file_path ).read()

    return cls(nodes, edges, trips, mode, verbose)

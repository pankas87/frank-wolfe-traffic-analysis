import math
from decimal import *

class StreetEdge:
  def __init__(self, tail_node, head_node, capacity, length, fftt, b, power, mode = 'user-balance' ):
    self.x         = [0] * 1024
    self.y         = [0] * 1024
    self.tail_node = tail_node
    self.head_node = head_node
    self.capacity  = capacity
    self.length    = length
    self.fftt      = fftt
    self.tt        = []
    self.b         = b
    self.power     = power
    self.mode      = mode
    self.label     = str( tail_node ) + '-' + str( head_node )

  def add_traffic(self, vehicles, n):
    while( len( self.x ) <= ( n + 1 ) ):
      self.x.append(0)

    self.x[n] += vehicles

  def add_traffic_change(self, vehicles, n):
    while( len( self.y ) <= ( n + 1 ) ):
      self.y.append(0)
    
    self.y[n] += vehicles

  def get_traffic(self, n):
    return self.x[n]

  def get_traffic_change(self, n):
    return self.y[n]

  def calculate_alpha_equation(self, n, alpha):
    x         = self.x[n]
    y         = self.y[n]
    b         = self.b
    capacity  = self.capacity
    power     = self.power
    fftt      = self.fftt
    flow      = x + ( float( alpha ) * ( y - x ) )
    result    = (y - x) * ( fftt ) * ( 1 + ( b * ( ( flow / capacity ) ** power ) ) )
    
    return Decimal( result )

  def convergence_function(self, n):
    x_1 = self.x[ n ]
    x_2 = self.x[ n + 1 ]

    if( x_1 == 0.0 ):
      return 0
    else:
      return Decimal( math.fabs( x_2 - x_1 ) / math.fabs( x_1 ) )

  def performance_function(self, n, truncate_to_integer = False):
    if( self.mode == 'user-balance' ):
      performance = self.user_balance_performance_function( n, truncate_to_integer )
    elif( self.mode == 'system-balance' ):
      performance = self.system_balance_performance_function( n, truncate_to_integer )    

    return performance

  def user_balance_performance_function(self, n, truncate_to_integer):
    x            = self.x[n]
    b            = self.b
    capacity     = self.capacity
    power        = self.power
    fftt         = self.fftt
    performance  = ( fftt ) * ( 1 + ( b * ( ( x / capacity ) ** power ) ) )

    self.tt.append( performance )

    return int( round( performance, 0 ) ) if truncate_to_integer else performance

  def system_balance_performance_function(self, n, truncate_to_integer):
    x            = self.x[n]
    b            = self.b
    capacity     = self.capacity
    power        = self.power
    fftt         = self.fftt

    performance  = self.user_balance_performance_function( n, False )
    performance += ( x * ( fftt * ( ( b * power ) / ( capacity ** power ) ) * ( x * ( 1.0 / power ) ) ) )

    self.tt.append( performance )
    
    return int( round( performance, 0 ) ) if truncate_to_integer else performance

  def get_traffic_congestion(self, n):
    return self.x[ n ] / self.capacity

  @classmethod
  def from_file_line(cls, line, mode):
    items = line.split( '\t' )

    del items[ 0 ]
    del items[ len(items) - 1 ]

    tail_node   = int( items[ 0 ] )
    head_node   = int( items[ 1 ] )
    capacity    = float( items[ 2 ] )
    length      = float( items[ 3 ] )
    fftt        = float( items[ 4 ] )
    b           = float( items[ 5 ] )
    power       = float( items[ 6 ] )

    return cls( tail_node, head_node, capacity, length, fftt, b, power, mode )

  @classmethod
  def from_results_file_line(cls, line):
    items     = line.split(',')
    tail_node = int( items[ 1 ] )
    head_node = int( items[ 2 ] )
    x         = float( items[ 3 ] )
    capacity  = float( items[ 5 ] )
    fftt      = float( items[ 7 ] )
    b         = float( items[ 8 ] )
    power     = float( items[ 9 ] )

    edge = cls( tail_node, head_node, capacity, None, fftt, b, power )
    edge.add_traffic( x, 0 )

    return edge
import math
from decimal import *

class StreetEdge:
  def __init__(self, tail_node, head_node, capacity, length, fftt, b, power ):
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
    x         = Decimal( self.x[n] )
    y         = Decimal( self.y[n] )
    b         = Decimal( self.b )
    capacity  = Decimal( self.capacity )
    power     = Decimal( self.power )
    fftt      = Decimal( self.fftt )
    flow      = x + ( alpha * ( y - x ) )
    result    = (y - x) * ( fftt ) * ( 1 + ( b * ( ( flow / capacity ) ** power ) ) )
    
    return Decimal( result )

  def convergence_function(self, n):
    x_1 = Decimal( self.x[ n ] )
    x_2 = Decimal( self.x[ n + 1 ] )

    if( x_1 == Decimal( 0.0 ) ):
      return 0
    else:
      return Decimal( math.fabs( x_2 - x_1 ) / math.fabs( x_1 ) )

  def performance_function(self, n, truncate_to_integer = False):
    x            = self.x[n]
    b            = self.b
    capacity     = self.capacity
    power        = self.power
    fftt         = self.fftt
    performance  = ( fftt ) * ( 1 + ( b * ( ( x / capacity ) ** power ) ) )
    
    self.tt.append( performance )

    return int( round( performance, 0 ) ) if truncate_to_integer else performance

  @classmethod
  def from_file_line(cls, line):
    items = line.split( '\t' )

    del items[ 0 ]
    del items[ len(items) - 1 ]

    tail_node   = int( items[0] )
    head_node   = int( items[1] )
    capacity    = float( items[2] )
    length      = float( items[3] )
    fftt        = float( items[4] )
    b           = float( items[5] )
    power       = float( items[6] )

    return cls( tail_node, head_node, capacity, length, fftt, b, power )
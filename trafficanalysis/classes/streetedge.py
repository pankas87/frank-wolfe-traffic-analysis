class StreetEdge:
  x = [0]
  y = []

  def __init__(self, tail_node, head_node, capacity, length, fftt, b, power ):
    self.tail_node   = tail_node
    self.head_node   = head_node
    self.capacity    = capacity
    self.length      = length
    self.fftt        = fftt
    self.b           = b
    self.power       = power
    self.label       = str( tail_node ) + '-' + str( head_node )

  def add_traffic(self, vehicles, n):
    if( n == len( self.x ) ):
      self.x.append(0)

    self.x[n] += vehicles

  def get_traffic(self, n):
    return self.x[n]

  def add_traffic_change(self, vehicles, n):
    if( n == len( self.y ) ):
      self.y.append(0)

    self.y[n] += vehicles

  def get_traffic_change(self, n):
    return self.y[n]

  def calculate_alpha_equation(self, n, alpha):
    x         = self.x[n]
    y         = self.y[n]
    b         = self.b
    capacity  = self.capacity
    power     = self.power
    fftt      = self.fftt
    flow      = x + ( alpha * ( y - x ) )
    result    = (y - x) * ( fftt ) * ( 1 + ( b * ( ( flow / capacity ) ** power ) ) )
    
    return result

  def performance_function(self, n, truncate_to_integer = False):
    x           = self.x[n]
    b           = self.b
    capacity    = self.capacity
    power       = self.power
    fftt        = self.fftt
    performance = ( fftt ) * ( 1 + ( b * ( ( x / capacity ) ** power ) ) )

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
class StreetEdge:
  vehicle_trips_sum = 0

  def __init__(self, tail_node, head_node, capacity, length, fftt, b, power, speed_limit, toll, link_type):
    self.tail_node   = tail_node
    self.head_node   = head_node
    self.capacity    = capacity
    self.length      = length
    self.fftt        = fftt
    self.b           = b
    self.power       = power
    self.speed_limit = speed_limit
    self.toll        = toll
    self.link_type   = link_type
    self.label       = str(tail_node) + '-' + str(head_node)

  def add_vehicle_trips(number_of_trips):
    vehicle_trips_sum += float( number_of_trips )
    return self

  @classmethod
  def from_file_line(cls, line):
    items = line.split( '\t' )

    del items[ 0 ]
    del items[ len(items) - 1 ]

    tail_node   = int( items[0] )
    head_node   = int( items[1] )
    capacity    = int( items[2] )
    length      = float( items[3] )
    fftt        = float( items[4] )
    b           = float( items[5] )
    power       = int( items[6] )
    speed_limit = int( items[7] )
    toll        = int( items[8] )
    link_type   = int( items[9] )

    return cls( tail_node, head_node, capacity, length, fftt, b, power, speed_limit, toll, link_type )
class StreetEdge:
  def __init__(self, tail_node, head_node, capacity, length, fftt, b, speed_limit, toll, link, type):
    self.tail_node   = tail_node
    self.head_node   = head_node
    self.capacity    = capacity
    self.length      = length
    self.fftt        = fftt
    self.b           = b
    self.speed_limit = speed_limit
    self.toll        = toll
    self.link        = link
    self.type        = type

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
    speed_limit = int( items[6] )
    toll        = int( items[7] )
    link        = int( items[8] )
    type        = int( items[9] )            

    return cls( tail_node, head_node, capacity, length, fftt, b, speed_limit, toll, link, type )
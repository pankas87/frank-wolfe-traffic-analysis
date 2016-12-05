from .streetedge import StreetEdge

class NetFileParser:
  STARTING_LINE = 7

  def __init__(self, path):
    self.path = path
    self.fp = open( path, 'r' )

  def read(self):
    edges = []

    for i, line in enumerate(self.fp):
      if( i >= self.STARTING_LINE ):
        edges.append( StreetEdge.from_file_line( line ) )

    return edges

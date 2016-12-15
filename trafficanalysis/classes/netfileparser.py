from .streetedge import StreetEdge

class NetFileParser:
  STARTING_LINE = 7

  def __init__(self, path, mode='user-balance'):
    self.mode = mode
    self.path = path
    self.fp = open( path, 'r' )

  def read(self):
    collection   = {}

    for i, line in enumerate(self.fp):
      if( i >= self.STARTING_LINE ):
        edge = StreetEdge.from_file_line( line, self.mode )
        collection[ edge.label ] = edge

    return collection

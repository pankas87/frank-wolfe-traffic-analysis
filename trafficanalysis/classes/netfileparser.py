import collections as coll
from .streetedge import StreetEdge

class NetFileParser:
  STARTING_LINE = 7

  def __init__(self, path):
    self.path = path
    self.fp = open( path, 'r' )

  def read(self):
    collection   = coll.OrderedDict()

    for i, line in enumerate(self.fp):
      if( i >= self.STARTING_LINE ):
        edge = StreetEdge.from_file_line( line )
        collection[ edge.label ] = edge

    return collection

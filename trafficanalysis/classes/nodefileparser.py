import collections
from .streetnode import StreetNode

class NodeFileParser:
  STARTING_LINE = 1

  def __init__(self, path):
    self.path = path
    self.fp = open( path, 'r' )

  def read(self):
    nodes = collections.OrderedDict()

    for i, line in enumerate(self.fp):
      if( i >= self.STARTING_LINE ):
        node = StreetNode.from_file_line( line )
        nodes[ node.label ] = node

    return nodes

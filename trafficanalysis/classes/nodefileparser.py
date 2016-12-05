from .streetnode import StreetNode

class NodeFileParser:
  STARTING_LINE = 1

  def __init__(self, path):
    self.path = path
    self.fp = open( path, 'r' )

  def read(self):
    nodes = []

    for i, line in enumerate(self.fp):
      if( i >= self.STARTING_LINE ):
        nodes.append( StreetNode.from_file_line( line ) )

    return nodes

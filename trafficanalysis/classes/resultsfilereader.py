from .streetedge import StreetEdge

class ResultsFileReader:

  STARTING_LINE = 1

  def __init__(self, path):
    self.path = path
    self.fp   = open( path, 'r' )

  def read(self):
    collection = {}

    for i, line in enumerate( self.fp ):
      if( i >= self.STARTING_LINE ):
        edge = StreetEdge.from_results_file_line( line )
        collection[ edge.label ] = edge

    return collection
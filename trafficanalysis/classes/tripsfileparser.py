import re
import collections as coll
from .nodetrip import NodeTrip

class TripsFileParser:
  destination_line_regex = re.compile( "[\d+:\d+\.\d+;]+" )

  def __init__(self, path):
    self.path = path
    self.fp = open( path, 'r' )

  def read(self):
    origin_node  = None
    collection   = {}
    i            = 1

    for line in self.fp:
      line = line.replace(' ', '')

      line_type    = self.line_type( line )
      
      if( line_type == 'origin' ):
        origin_node = self.get_origin_from_line( line )
      elif( line_type == 'destinations' ):
        destinations = self.get_destinations_from_line( line )

        for dest_string in destinations:
          dest_array     = dest_string.split(':')
          dest_node     = int( dest_array[0] )
          vehicles      = float( dest_array[1] )

          collection[i] =  NodeTrip( origin_node, dest_node, vehicles )
          i += 1

    return collection

  def line_type(self, line):
    if( line.find('Origin') != -1 ):
      return 'origin'
    elif( self.destination_line_regex.match( line ) ):
      return 'destinations'
    else:
      return None

  def get_origin_from_line(self, line):
    return int( line.replace('Origin', '') )

  def get_destinations_from_line(self, line):
    return filter( lambda x: x != '\n', line.split(';') )

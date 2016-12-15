import os
import datetime

class Results:
  def __init__(self, edges, mode = 'user-balance'):
    self.edges               = edges
    self.mode                = mode
    self.startng_time_string = datetime.datetime.now().strftime( "%Y-%m-%d  %H:%M"  )

  def save(self, n):
    fp = self.get_file( self.get_dir(), n )
    
    fp.write( 'edge, tail_node, head_node, x, y, capacity, tt, fftt, b, power\n' )

    i = 1

    for key, edge in self.edges.iteritems():
      fp.write( str(i) + ', ' )
      fp.write( str( edge.tail_node ) + ', ' )
      fp.write( str( edge.head_node ) + ', ' )
      fp.write( str( edge.x[ n ] ) + ', ' )
      fp.write( str( edge.y[ n ] ) + ', ' )
      fp.write( str( edge.capacity ) + ', ' )
      fp.write( str( edge.tt[ n ] ) + ', ' )
      fp.write( str( edge.fftt ) + ', ' )
      fp.write( str( edge.b ) + ', ' )
      fp.write( str( edge.power ) )
      fp.write( '\r\n' )
      i += 1

    fp.close()

  def get_dir(self):
    dir = 'results/original-' + self.mode + ' - ' + self.startng_time_string + '/'
    if( not os.path.isdir( dir ) ):
      os.makedirs( dir )

    return dir

  def get_file(self, dir, n):
    file = 'iteration-' + str( n ) + '.csv'
    fp   = open( dir + file, 'w' )

    return fp
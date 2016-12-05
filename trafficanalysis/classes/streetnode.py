class StreetNode:
  def __init__(self, number, x, y):
    self.number = number
    self.x   = x
    self.y   = y

  @classmethod
  def from_file_line(cls, line):
    items = line.split( '\t' )
    
    del items[ len(items) - 1 ]
    
    number, x, y = map( int, items )
    
    return cls( number, x, y )



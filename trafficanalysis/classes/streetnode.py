class StreetNode:
  def __init__(self, label, x, y):
    self.label  = label
    self.x      = x
    self.y      = y

  @classmethod
  def from_file_line(cls, line):
    items = line.split( '\t' )
    
    del items[ len(items) - 1 ]
    
    number, x, y = map( int, items )
    
    return cls( number, x, y )



import datetime

class Logs:
  def __init__(self, mode = 'user-equilibrium'):
    self.mode      = mode
    self.LOGS_FILE = 'logs/convergence-results - ' self.mode + ' - ' + datetime.datetime.now().strftime( "%Y-%m-%d  %H:%M"  ) + '.txt'
    pass

  def log(self, n, alpha, f_alpha, convergence_sum):
    fp   = open( self.LOGS_FILE, 'a' )
    date = datetime.datetime.now().strftime( "%d %b %Y %H:%M:%S"  )
    fp.write( date + '\t' + 'n: ' + str( n ) + '\t\t' + 'alpha: ' + str( alpha[ n ] ) + '\t\t' + 'f_alpha: ' + str( f_alpha[ n ] ) + '\t\t' + 'convergence sum: ' + str( convergence_sum[ n ] ) + '\n' )
    fp.close()
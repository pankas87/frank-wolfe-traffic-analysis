import trafficanalysis as ta

nodes_file_path    = 'ChicagoSketch.node'
results_file_paths = []

results_file_paths.append( 'final results/user-balance-iteration-230.csv' )
results_file_paths.append( 'final results/system-balance-iteration-196.csv' )
results_file_paths.append( 'final results/original-user-balance-iteration-43.csv' )
results_file_paths.append( 'final results/original-system-balance-iteration-43.csv' )

for results_file in results_file_paths:
  print results_file
  results = ta.ResultsGraph.from_files( nodes_file_path, results_file ).render()
import trafficanalysis as ta

nodes_file_path    = 'ChicagoSketch.node'
results_file_paths = []

results_file_paths.append( 'results/user-balance - 2016-12-14  02:21/iteration-203.csv' )
results_file_paths.append( 'results/system-balance - 2016-12-14  11:56/iteration-163.csv' )
results_file_paths.append( 'results/original-user-balance - 2016-12-14  16:52/iteration-43.csv' )
results_file_paths.append( 'results/original-system-balance - 2016-12-14  17:22/iteration-43.csv' )

for results_file in results_file_paths:
  print results_file
  results = ta.ResultsGraph.from_files( nodes_file_path, results_file ).render()
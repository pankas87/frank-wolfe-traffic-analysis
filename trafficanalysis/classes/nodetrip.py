import collections

class NodeTrip:
  start_node       = ''
  end_node         = ''
  vehicle_trips    = 0.0
  path             = collections.OrderedDict()

  def __init__(self, start_node, end_node, vehicle_trips):
    self.start_node       = start_node
    self.end_node         = end_node
    self.vehicle_trips    = vehicle_trips
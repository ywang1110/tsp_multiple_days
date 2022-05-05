#!/usr/bin/env python3
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import sys
import math

# Number of vehicles
NUM_VEHICLES = 1

# Day 0 - Start at 8:00am at Location 1 (index 0)
# Day 0 - End at 4:00pm at Location 2 (index 1)
# Day 1 - Start at 6:00am at Location 3 (index 2)
# Day 1 - End at 6:00pm at Location 4 (index 3)
# Day 2 - Start at 10:00am at Location 5 (index 4)
# Day 2 - End at 2:00pm at Location 6 (index 5)
NUM_DAYS = 3
one_day = 86400
one_hour = 3600
one_minute = 60

NUM_VISITS = 32 * NUM_VEHICLES

# 8am, 6am, 10am, then repeat
MORNINGS = [
  28800, # 8am
  21600, # 6am
  36000, # 10am
] * (NUM_DAYS // 3 + 1)

# 4pm, 6pm, 2pm, then repeat
EVENINGS = [
  57600, # 4pm
  64800, # 6pm
  50400, # 2pm
] * (NUM_DAYS // 3 + 1)

################# Matrix



################# Time Windows
Windows = []
## Add START/ENDS
for v in range(NUM_VEHICLES):
    for d in range(NUM_DAYS):
        morning = MORNINGS[d] + d * one_day
        Windows.append([morning, morning])
    for d in range(NUM_DAYS):
        evening = EVENINGS[d] + d * one_day
        Windows.append([evening, evening])
## Add LOCATIONS
Windows += [24200, 59600], [24200, 59600], [24200, 59600], [24200, 59600],
        [24200, 59600], [24200, 59600], [24200, 59600], [24200, 59600],
        [24200, 59600], [24200, 59600], [24200, 59600], [24200, 59600],
        [24200, 59600], [24200, 59600], [24200, 59600], [24200, 59600],
        [24200, 59600], [24200, 59600], [24200, 59600], [24200, 59600],
        [24200, 59600], [24200, 59600], [24200, 59600], [24200, 59600],
        [24200, 59600], [24200, 59600], [24200, 59600], [24200, 59600],
        [24200, 59600], [24200, 59600], [24200, 59600], [24200, 59600],
        [24200, 59600], [24200, 59600], [24200, 59600], [24200, 59600],
        [24200, 59600], [24200, 59600], [24200, 59600], [24200, 59600]

################# Durations
Durations = []
## Add START/ENDS
for v in range(NUM_VEHICLES):
    for d in range(NUM_DAYS):
        Windows.append(0) # start
    for d in range(NUM_DAYS):
        Windows.append(0) # end
## Add LOCATIONS
Durations += 900, 900, 900, 900, 900, 900, 900, 900, 900, 900,
        900, 900, 900, 900, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800,
        1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 3600,
        3600, 3600, 3600, 3600, 3600, 3600

assert len(Durations) == len(Windows)

################# Penalties
max_int = one_day * NUM_DAYS

Penalties = []
for v in range(NUM_VEHICLES):
    for d in range(NUM_DAYS):
        Windows.append(max_int) # start
    for d in range(NUM_DAYS):
        Windows.append(max_int) # end


Penalties += 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000

assert len(Penalties) == len(Windows)

START_NODES = []
for node in range(0, NUM_DAYS):
  START_NODES.append(node * 2)

END_NODES = []
for node in range(0, NUM_DAYS):
  END_NODES.append(node * 2 + 1)

REGULAR_NODES = []
for node in range(NUM_DAYS * 2, len(Matrix)):
  REGULAR_NODES.append(node)

def transit_callback(from_index, to_index):

  # Returns the travel time plus service time between the two nodes.
  # Convert from routing variable Index to time matrix NodeIndex.
  from_node = manager.IndexToNode(from_index)
  to_node = manager.IndexToNode(to_index)

  return Matrix[from_node][to_node] + Durations[from_node]

# Create the routing index manager.
# Start Depot is the index of the start of the first day i.e. 0.
# End Depot is the index of the end of the last day i.e. (2*NUM_DAYS - 1).
manager = pywrapcp.RoutingIndexManager(len(Matrix), NUM_VEHICLES, [0], [2*NUM_DAYS-1])

# Create Routing Model.
# use precaching on OR-Tools side.  So Much Faster
model_parameters = pywrapcp.DefaultRoutingModelParameters()
model_parameters.max_callback_cache_size = len(Matrix) * len(Matrix)
routing = pywrapcp.RoutingModel(manager, model_parameters)
#routing = pywrapcp.RoutingModel(manager)

# Register the Transit Callback.
transit_callback_index = routing.RegisterTransitCallback(transit_callback)

# Set the arc cost evaluator for all vehicles
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# Add Time Windows constraint.
routing.AddDimension(
  transit_callback_index,
  86400 * NUM_DAYS, # An upper bound for slack (the wait times at the locations).
  86400 * NUM_DAYS, # An upper bound for the total time over each vehicle's route.
  False, # Determine whether the cumulative variable is set to zero at the start of the vehicle's route.
  'Time')
time_dimension = routing.GetDimensionOrDie('Time')

# Allow all non-start and non-end nodes to be droppable.
#for node in range(len(START_NODES) + len(END_NODES), len(Matrix)):
for node in range(0, len(Matrix)):
    if manager. node == 0 or node == 2*NUM_DAYS-1:
        continue
    else:
        routing.AddDisjunction([manager.NodeToIndex(node)], Penalties[node])

# Add time window constraints for all regular nodes.
for location_index, time_window in enumerate(Windows):
  if location_index in REGULAR_NODES:
    #print(f"location: {location_index}, TW:{time_window}")
    index = manager.NodeToIndex(location_index)
    # Add the range between the start of the first day and the end of the last day
    time_dimension.CumulVar(index).SetRange(0, 86400 * NUM_DAYS)

    for Day in range(NUM_DAYS):
      day_start = Day * one_day
      day_end = day_start + one_day
      working_start = Windows[Day * 2][0]
      working_end =  Windows[Day * 2 + 1][0]
      #print(f"day {Day}: [{day_start}, {day_end}], Working:[{working_start}, {working_end}]")
      # Remove the range between the start of the day and the start of work
      time_dimension.CumulVar(index).RemoveInterval(day_start, working_start)
      # Remove the range between the start of the day and the start of location
      time_dimension.CumulVar(index).RemoveInterval(day_start, day_start + time_window[0])
      # Remove the range between the end of work and the end of the day
      time_dimension.CumulVar(index).RemoveInterval(working_end, day_end)
      # Remove the range between the end of location and the end of the day
      time_dimension.CumulVar(index).RemoveInterval(day_start + time_window[1], day_end)


## Add time window constraints for start and end nodes.
## TODO: This also needs to be done for each additional day
#index = routing.Start(0)
#time_dimension.CumulVar(index).SetRange(Windows[0][0],Windows[0][1])
#index = routing.End(0)
#time_dimension.CumulVar(index).SetRange(
#  Windows[1][0] + ((NUM_DAYS - 1) * 86400),
#  Windows[1][1] + ((NUM_DAYS - 1) * 86400))

for i in range(0,5):
    if i == 0:
        index = routing.Start(0)
    elif i == 5:
        index = routing.End(0)
    else:
        index = manager.NodeToIndex(i);
    time_dimension.CumulVar(index).SetRange(Windows[i][0],Windows[i][1])


# Instantiate route start and end times to produce feasible times
routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.Start(0)))
routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(0)))

# Setting first solution heuristic.
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.ALL_UNPERFORMED)
        #routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

# Setting local search metaheuristics:
search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
search_parameters.time_limit.seconds = 5
search_parameters.log_search = False

# Solve the problem
solution = routing.SolveWithParameters(search_parameters)

if not solution:
    print("No solution found !")
    sys.exit(1)

# Print the results
print(f"Objective: {solution.ObjectiveValue()}")

# Return the dropped locations
dropped = []
for node in range(routing.Size()):
  if routing.IsStart(node) or routing.IsEnd(node):
    continue
  if solution.Value(routing.NextVar(node)) == node:
    dropped.append(manager.IndexToNode(node))
print(f"droped: {dropped}")

def time2date(time):
  "convert time in second to [day, hour, minute, seconds]"
  days = time // one_day
  hours = (time - days*one_day) // one_hour
  minutes = (time - days*one_day - hours*one_hour) // one_minute
  seconds =  time - days*one_day - hours*one_hour - minutes*one_minute
  return [days, hours, minutes, seconds]

# Return the scheduled locations
index = routing.Start(0)
plan_output = 'Route for vehicle 0:\n'
while not routing.IsEnd(index):
  plan_output += f'{manager.IndexToNode(index)} '
  time = time_dimension.CumulVar(index)
  tw_min = solution.Min(time)
  [days, hours, minutes, seconds] = time2date(tw_min)
  plan_output += f'[{days}d {hours}:{minutes}:{seconds};'
  tw_max = solution.Max(time)
  [days, hours, minutes, seconds] = time2date(tw_max)
  plan_output += f'{days}d {hours}:{minutes}:{seconds}] -> '
  index = solution.Value(routing.NextVar(index))
  if manager.IndexToNode(index) < 2*NUM_DAYS and manager.IndexToNode(index) & 1 == 0:
      plan_output += '\n\n'
time = time_dimension.CumulVar(index)
tw_min = solution.Min(time)
[days, hours, minutes, seconds] = time2date(tw_min)
plan_output += f'[{days}d {hours}:{minutes}:{seconds};'
tw_max = solution.Max(time)
[days, hours, minutes, seconds] = time2date(tw_max)
plan_output += f'{days}d {hours}:{minutes}:{seconds}]'
print(plan_output)

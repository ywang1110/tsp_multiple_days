# TSP over multiple days

I am using Google OR-Tools to optimize the routing of a single vehicle over the span of a several day.

I am aiming to:
- Be able to specify the number of days over which to optimize routing.
- Be able to specify the start location and end location for each day.
- Be able to specify the start time and end time for each day.

I have a set of 40 locations. For every day I want to include in my range of days for optimization, I prepend the start and end location to the matrix. So if I want to optimize for two days, I would have a total of 44 locations in my matrix.

I want to allow location to be dropped if there is no feasible solution - in fact I expect this to be the case fairly often.

For example, if I was providing data for two days, if would look something like

```
[...]

NUM_DAYS = 2

Matrix = [[start day 1], [end day 1], [start day 2], [end day 2], [location], [location], ... ]

# Day 1 - Start at 8:00am at Location 1
# Day 1 - End at 4:00pm at Location 2
# Day 2 - Start at 6:00am at Location 3
# Day 2 - End at 6:00pm at Location 4
Windows = [[28800, 28800], [57600, 57600], [21600, 21600], [64800, 64800], [0, 86400], [0, 86400], [0, 86400], ... ]

[...]
```

If I were providing data for three days, if would look something like

```
[...]

NUM_DAYS = 3

Matrix = [[start day 1], [end day 1], [start day 2], [end day 2], [start day 3], [end day 3], [location], [location], ... ]

# Day 1 - Start at 8:00am at Location 1
# Day 1 - End at 4:00pm at Location 2
# Day 2 - Start at 6:00am at Location 3
# Day 2 - End at 6:00pm at Location 4
# Day 3 - Start at 10:00am at Location 5
# Day 3 - End at 2:00pm at Location 6
Windows = [[28800, 28800], [57600, 57600], [21600, 21600], [64800, 64800], [36000, 36000], [50400, 50400], [0, 86400], [0, 86400], [0, 86400], ... ]

[...]
```

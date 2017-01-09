# Route-Planner

The program runs on the commandline like this:
python route.py [start-city] [end-city] [routing-option] [routing-algorithm]

where:
 start-city and end-city are the cities we need a route between.
 routing-option is one of:
  -"segments" finds a route with the fewest number of \turns" (i.e. edges of the graph)
  -"distance" finds a route with the shortest total distance
  -"time" finds the fastest route, for a car that always travels at the speed limit
  -"scenic" finds the route having the least possible distance spent on highways (which we define as roads with speed limits 55 mph or         greater)
 routing-algorithm is one of:
  -"bfs" uses breadth-first search
  -"dfs" uses depth-firrst search
  -"ids" uses iterative deepening search
  -"astar" uses A* search, with a suitable heuristic function
  

BFS algorithm - 
Breadth First Search:
1.Append start city to fringe
2.pop the last element and make it the new parent
3.the node to be explored is the last element in the parent
4.Add this node to the list of visited states
5.For each sucessor of node
    -if the succ is a goal state add it to the parent list and return it to the main function
    -if it is not the goal state add it to the path traversal list along with the parent
    -if the sucessor isnt in visited AND isnt in the parent AND the path isnt in fringe add the path to the fringe
6.repeat 2-5 as long as fringe is not empty

DFS algorithm -
1.Append start city to fringe
2.pop the first element and make it the new parent
3.the node to be explored is the last element in the parent
4.Add this node to the list of visited states
5.For each sucessor of node
    -if the succ is a goal state add it to the parent list and return it to the main function
    -if it is not the goal state add it to the path traversal list along with the parent
    -if the sucessor isnt in visited AND isnt in the parent AND the path isnt in fringe add the path to the fringe
6.repeat 2-5 as long as fringe is not empty

IDS algorithm - 
Iterative Depth Search:
1.Append start city to fringe, set iteration depth to 1
2.pop the first element and make it the new parent
3.IF the length of the parent is smaller than the iteration level
4.the node to be explored is the last element in the parent
5.Add this node to the list of visited states
6.For each sucessor of node
    -if the succ is a goal state add it to the parent list and return it to the main function
    -if it is not the goal state add it to the path traversal list along with the parent
    -if the sucessor isnt in visited AND isnt in the parent AND the path isnt in fringe add the path to the fringe
7.repeat 2-7 as long as fringe is not empty while increasing the iteration depth by 1

A star search - 
1.Append start city to fringe
2.Sort the fringe based on heuristic value in asceding order.
2.pop the first element and make it the new parent
3.the node to be explored is the last element in the parent
4.Add this node to the list of visited states
5.For each sucessor of node
    -if the succ is a goal state add it to the parent list and return it to the main function
    -if it is not the goal state add it to the path traversal list along with the parent
    -if the succesor is already there in fringe with greater value, then update the fringe with least succesor value. 
    -if the sucessor isnt in visited AND isnt in the parent AND the path isnt in fringe add the 

Some interesting facts:

astar seems to works best for each routing option as it is giving us the optimal solution. As far as bfs, dfs, and ids are concerened, it doesn't matter what the routing option is. They give the solution which they encounter first; it might not be the optimal path.

dfs is fastest in terms of computation time. It took 2.35 secs as compared to bfs which took 4.6 secs, ids which took 2.9 secs and astar which took 16 secs to find the route between 'Bloomington,_Indiana' and 'Chicago,_Illinois'
     
ids takes least amount of memory. We are considering the memory as length of fringe/elements in fringe after your seaarch has stopped. For given set of start and end cities - 'Bloomington,_Indiana' and 'Chicago,_Illinois', length of the fringe  for ids is - 254 while it is 1307 for dfs, 6742 for bfs and A*

When routing option is distance - I have used haversine formula for calculating the direct distance between cities based on its GPS co-ordinates as heuristic. It never overestimates as the physical distance can be at least equal to haversine distance.
    
When the option is time -  I have used haversine distance divided by the max speed on the edge between cities. It gives us time as a heuristic value. This again never overestimates as haversine distance never overestimates divided by the max speed will always give the least time it will take to reach the goal
    
When the option is segments - the heuristic value I used is 0. This value I added to number of nodes visited so far gives us the heuristic function.
    
When the option is scenic -  heuristic I used is the haversine distance divided by maximum speed of scenic route which 55.
The logic behind choosing the heuristic was, if at the node had the scenice route existed, then time taken to reach destination would at least be distance over max speed of scenic route.

Skagway,_Alaska is the furthest from Bloomington with distance = 2525.56718271 miles. get_farthest_city_from_bloomington() function is used. The function calculated the haversine distance for each city from Bloomington using longitudes and latitudes. The largest is returned.

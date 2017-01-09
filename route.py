'''
Created on Sep 25, 2016

@authors: Mihir Thatte, Rohit Dandona, Rahul Velayuthan


Abstraction used:
Start State: The start city as given by the user
Goal State: The end city given by the user
Sucessor function: For any given city return all the cities/highway intersections its connected to
State Space: considered each city/highway intersection as a node and the connection to another city/highway 
Edge Weights: a. Segments : 1 b. Distance : the distance between the cities/intersection [calculated by haversine formula] c. 
Time : used time = distance / speed d. Scenic : Distance/speed[=55] 
'''

import time
import math
from operator import itemgetter
import sys

goal_Nodes=[]
    
def getDistanceByCoordinates(lat1,lon1,lat2,lon2):
    radius = 3961 #// Radius of the earth in miles
    dLat = deg2rad(float(lat2)-float(lat1)) # // deg2rad below
    dLon = deg2rad(float(lon2)-float(lon1)) 
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(float(lat1))) * math.cos(deg2rad(float(lat2))) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
    distanceBetween = radius * c # // Distance in miles
    return distanceBetween

# The distance is calculated using haversine formula which I found on - 
# Ref - http://www.movable-type.co.uk/scripts/latlong.html website. It gives us the distance between cities based on its GPS co-ordinates. 

def getMax(dis_list):
    return max(dis_list)

def get_farthest_city_from_bloomington(cities): # used for calculting question 5
    dis = {}
    d = []
    for details in cities:
        eclidean = getDistanceByCoordinates('39.165325', '-86.5263857', details[1], details[2])
        dis[eclidean] = details[0]
        d.append(eclidean)

    max_dis = getMax(d)
    print "City: ",dis[max_dis]
    print "Distance: ", max_dis

def deg2rad(deg):
    return deg * (math.pi/180)

def getLatLongOf(city):
    for each in cities:
        if each[0]==city:
            return each[1],each[2]


def read(name):
    f=open(name,'r')
    linecount=sum(1 for line in f) #get number of cities NOTE : check if EOF is there and us eit in the while loop
    #linecount=10
    count=0
    fileList=[]
    f.seek(0,0) #to find count we travel to the end of the file return to starty
    while count<linecount:
        linetext=f.readline().rstrip('\n').rstrip('\r') #strip '/n' from the line
        data=linetext.split(" ") #generate three elements
        #print data
        fileList.append(data) #add it to the final list
        count+=1
    f.close()
    return fileList

def create_BiRoads(): # it creates bi directional graph
    for each in roads:
        distance = float(each[2])
        if distance==0:
            # no road exists
            pass
        try:
            speed =float(each[3]) 
        except ValueError: 
            speed = 75.0
            each[3]=75.0 # max speed in US          
        if speed==0:
            speed=75.0
            each[3]=75.0 # max speed on highway
        if distance==0:
            pass # no path exists between cities
        time=distance/speed
        each.append(str(time))
        BiRoads.append(each)
        temp=[]
        temp.append(each[1])
        temp.append(each[0])
        temp.append(each[2])
        temp.append(each[3])
        temp.append(each[4])
        temp.append(str(time))
        BiRoads.append(temp)


def successor(city):
    succesorNodes =[]
    for eachRoad in BiRoads:
        if eachRoad[0]==city:
            succesorNodes.append(eachRoad[1])
    return succesorNodes

def heurostic_for_scenic(parent,city):
    actualDistance = heurostic_for_Distance(parent,city)
    return float(actualDistance/55)
    

def heurostic_for_Time(parent,city):
    city1 = getLatLongOf(parent)
    city2 = getLatLongOf(city)
    if city1==None: #highway junction
        dist = searchBiRoadsDistance(parent, city)
        if dist[0]>0:
            return dist[0]/dist[2] #as it is a junction consider the distance given in the file
    if city2==None: #highway junction
        dist1 = searchBiRoadsDistance(parent, city)
        if dist1[0]>0:
            return dist1[0]/dist1[2] #as it is a junction consider the distance given in the file
    value = getDistanceByCoordinates(city1[0],city1[1],city2[0],city2[1])
    maxSpeed = searchBiRoadsDistance(parent,city)
    hValue = float(value/maxSpeed[2])
    return hValue
        

def heurostic_for_Distance(parent,city):
    city1 = getLatLongOf(parent)
    city2 = getLatLongOf(city)
    if city1==None: #highway junction
        dist = searchBiRoadsDistance(parent, city)
        if dist[0]>0:
            return dist[0] #as it is a junction consider the distance given in the file
    if city2==None: #highway junction
        dist1 = searchBiRoadsDistance(parent, city)
        if dist1[0]>0:
            return dist1[0] #as it is a junction consider the distance given in the file
    hValue = getDistanceByCoordinates(city1[0],city1[1],city2[0],city2[1])
    return math.floor(hValue)
    
def is_goal(city, end_city):
    if city==end_city:
        return True


def searchBiRoadsDistance(city1, city2):
    for row in BiRoads:
        if row[0]==city1 and row[1]==city2:
            return float(row[2]), float(row[5]),float(row[3])
    else:
        return 0
 
 
def timeSoFar(parent): # returns time taken to travel so far
    i=0
    totalTime=0.0
    while(i<len(parent)-1):
        time = searchBiRoadsDistance(parent[i],parent[i+1])
        totalTime = totalTime+ time[1]
        i+=1
    return totalTime

def costSoFar(parent): # returns distance travelled so far
    i=0
    totaldistance=0
    while(i<len(parent)-1):
        distance = searchBiRoadsDistance(parent[i],parent[i+1])
        totaldistance = totaldistance+ distance[0]
        i+=1
    return totaldistance

def nodesSoFar(parent):
    return len(parent)


def solve_Bfs(start_city,end_city):
    fringe = []
    closed = []
    fringe.append([start_city])
    while (len(fringe)>0):
        parent = fringe.pop(0)
        node=parent[-1]
        closed.append(node)
        for s in successor(node):
            if (is_goal(s, end_city)):
                parent.append(s)
                return parent
            path = list(parent)
            path.append(s)
            if(s not in closed)and(s not in parent) and (path not in fringe):
                fringe.append(path)
                

def solve_Dfs(start_city,end_city):
    fringe = []
    closed = []
    fringe.append([start_city])
    while (len(fringe) > 0):
        parent = fringe.pop()
        node = parent[-1]
        closed.append(node)
        for s in successor(node):
            if (is_goal(s, end_city)):
                parent.append(s)
                return parent
            path = list(parent)
            path.append(s)
            if(s not in closed)and(s not in parent) and (path not in fringe):
                fringe.append(path)
        

def solve_Ids(start_city,end_city):
    Idepth = 1
    found = False
    while(not found): #to stop infinite loop if there's no goal solution
        fringe=[]
        closed = []
        fringe.append([start_city])
        while(len(fringe)>0):
                parent=fringe.pop()
                if(len(parent)<=Idepth):
                    node =parent[-1]
                    closed.append(node)
                    for s in successor(node):
                        if (is_goal(s, end_city)):
                            parent.append(s)
                            return parent
                        path = list(parent)
                        path.append(s)
                        if (s not in closed) and (s not in parent) and (path not in fringe):
                            fringe.append(path)
        Idepth+=1
    else:
        return False


def solve_Astar(start_city,end_city,routing_option):
    closed=[]
    if routing_option =='distance':
        fringe = [[0,start_city]]
        while(len(fringe)>0):
            fringe =sorted(fringe,key=itemgetter(0))
            parent = fringe.pop(0)
            node=parent[-1]
            closed.append(node)
            for s in successor(node):
                if (is_goal(s, end_city)):
                    parent.append(s)
                    return parent
                path=list(parent[1:])
                path.append(s)
                hValue = heurostic_for_Distance(node, s) + costSoFar(path)
                path.insert(0,hValue)
                if (s not in parent) and (s not in closed):
                    fringe.append(path)
                    
    elif routing_option=='time':
        fringe = [[0,start_city]]
        while(len(fringe)>0):
            fringe =sorted(fringe,key=itemgetter(0))
            parent = fringe.pop(0)
            node=parent[-1]
            closed.append(node)
            for s in successor(node):
                if (is_goal(s, end_city)):
                    parent.append(s)
                    return parent
                path=list(parent[1:])
                path.append(s)
                #print s
                hValue = heurostic_for_Time(node, s) + timeSoFar(path)
                path.insert(0,hValue)
                if (s not in parent) and (s not in closed) and (path not in fringe):
                    fringe.append(path)
                        
                            
    elif routing_option=='segments':
        fringe = [[0,start_city]]
        while(len(fringe)>0):
            fringe =sorted(fringe,key=itemgetter(0))
            parent = fringe.pop(0)
            node=parent[-1]
            closed.append(node)
            for s in successor(node):
                if (is_goal(s, end_city)):
                    parent.append(s)
                    return parent
                path=list(parent[1:])
                path.append(s)
                #print s
                hValue = nodesSoFar(path)
                path.insert(0,hValue)
                if (s not in parent) and (s not in closed) and (path not in fringe):
                    fringe.append(path)      
    elif routing_option=='scenic':
        fringe = [[0,start_city]]
        while(len(fringe)>0):
            fringe =sorted(fringe,key=itemgetter(0),reverse=True)
            parent = fringe.pop(0)
            node=parent[-1]
            closed.append(node)
            for s in successor(node):
                if (is_goal(s, end_city)):
                    parent.append(s)
                    return parent
                path=list(parent[1:])
                path.append(s)
                hValue = heurostic_for_scenic(node, s)+timeSoFar(path)
                path.insert(0,hValue)
                if (s not in parent) and (s not in closed) and (path not in fringe):
                    fringe.append(path)

start_city = sys.argv[1]
end_city = sys.argv[2]
routing_option = sys.argv[3]
routing_algo =sys.argv[4]

cities = read('city-gps.txt') # reads city-gps file into list
roads= read('road-segments.txt') # reads road=segments file into list
BiRoads=[]
create_BiRoads()

#BiRoads = [city1, city2, distance, speed, HighwayName, time]

def take_Highways(output): #to find name of the highways between start and end city
    i=0
    highway=[]
    while(i<len(output)-1):
        for each in BiRoads:
            if each[0]==output[i] and each[1]==output[i+1]:
                highway.append(each[4])
        i+=1
    return highway
            

def display(output,highways):
    for i in range(0,len(output)-1):
        print "from    "+output[i] + "    take highway ==>  "+ highways[i] +"    you will reach    " +output[i+1]
        
def display_path(output): 
    for each in output:
        print each,



if routing_algo == 'bfs':
    output = solve_Bfs(start_city, end_city)
    print "Total distance to reach your destination is -", 
    print costSoFar(output)
    print " "
    print "Total time to reach your destination is -", 
    print timeSoFar(output)
    print " "
    highways = take_Highways(output)
    print "start from "+start_city
    display(output,highways)
    print ""
    print " you have reached your destination :)  " + end_city
    print ""
    print costSoFar(output),
    print timeSoFar(output),
    display_path(output)

elif routing_algo =='dfs':
    output = solve_Dfs(start_city,end_city)
    print "Total distance to reach your destination is -", 
    print costSoFar(output)
    print " "
    print "Total time to reach your destination is -", 
    print timeSoFar(output)
    print " "
    highways = take_Highways(output)
    print "start from "+start_city
    display(output,highways)
    print ""
    print " you have reached your destination :)  " + end_city
    print ""
    print costSoFar(output),
    print timeSoFar(output),
    display_path(output)
    
    
elif routing_algo=='ids':
    output= solve_Ids(start_city,end_city)
    print "Total distance to reach your destination is -", 
    print costSoFar(output)
    print " "
    print "Total time to reach your destination is -", 
    print timeSoFar(output)
    print " "
    highways = take_Highways(output)
    print "start from "+start_city
    display(output,highways)
    print ""
    print " you have reached your destination :)  " + end_city
    print ""
    print costSoFar(output),
    print timeSoFar(output),
    display_path(output)
    
elif routing_algo == 'astar':
    output =  solve_Astar(start_city,end_city,routing_option)
    print "Total distance to reach your destination is -", 
    print costSoFar(output[1:])
    print " "
    print "Total time to reach your destination is -", 
    print timeSoFar(output[1:])
    print " "
    highways = take_Highways(output[1:])
    print "start from "+start_city
    display(output[1:],highways)
    print ""
    print " you have reached your destination :)  " + end_city
    print ""
    print costSoFar(output[1:]),
    print timeSoFar(output[1:]),
    display_path(output[1:])
    
else:
    print"Sorry!, Your fourth choice of input was incorrect select only from the following four - "
    print "bfs"
    print "dfs"
    print "ids"
    print "astar"

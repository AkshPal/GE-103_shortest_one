#-------------------------------------------------------------------------------------------------------------#
#                                   | A BRIEF ABOUT THE PROJECT AND THE CODE |                                #
#-------------------------------------------------------------------------------------------------------------#

'''Our project aims at providing the shortest path between any two places in IIT Ropar campus. map_iitrpr is the
collection in which all places and their connecting places are place along with the distance between them. All 
this information is stored in the form of a dictionary. runner_code is main function which takes map,starting 
place and destination place as parameters.Then the plot function plots all the places with distance between them
and shows which one will be the shortest path to be taken for reaching from starting place to destination place. '''



#-------------------------------------------------------------------------------------------------------------#
#                                   | All the Imports that are needed in the project|                         #
'''the following library imports are only used to generate a window to display the graph in a user-friendly form.
The dijkstra algorithm implementation is a naive code and does not use any of the following library.'''
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx
import map_iitrpr,map_transit_iitrpr
#-------------------------------------------------------------------------------------------------------------#



#-------------------------------------------------------------------------------------------------------------#
#                          | FUNCTION TO FIND SHORTEST PATH BY DIJKSTRA'S ALGORITHM |                         #
#-------------------------------------------------------------------------------------------------------------#

'''The given below function by the name runner_code is the function which finds the shortest path between the two
places.'''

def runner_code(graph,start,target):
    ''' Multiple lists are made like value_dic,previous_point. Value_dic is the dictionary which stores the min.
    distance to each place till destination is reached. previous_point stores the place from which the present 
    place is reached via the shortest path. To get the shortest path, first 0 value is assigned and a very large 
    value is assigned to all the other points. Then a point is considered and the  all the points connecting to it
    are checked then the distance between them takes place of the very large value assigned to that point/place 
    in the value_dic. Then same procedure is followed for the other points and distance value that is assigned in 
    value_dic is the sum of distances from the starting point. In last the distance assigned to the destination is
    returned as the shortest path distance. Also the previous_point dictionary is used to get the path. This is 
    done by making a variable and making it equal to destination, then a loop is made to run till that variable 
    becomes equal to starting place and that variable is assigned new place which is taken from the previous_point
    dictionary.
    '''
    
    # This is the very large value that is initially assigned to places except starting point. #
    very_large_value = 1000000000
    
    point_considered=graph
    
    # We make the dictionary to store the distance to each point #
    value_dic = {}
    
    # The below loop assigns 0 to starting point and large value to all other places. #
    for i in graph:
        # Checks if i in given map is the staring point or not.
        if i==(start):
            value_dic[i]=0
        else:
            value_dic[i]=very_large_value
            
    # We make this dictionary to store the place from which we reach the present place via the shortest path. #
    previous_point = {}
    
    # This list is the list in which the places via which we reach destination as shortest path is stored.#
    path_taken = []
    
    # The below loops runs untill all the points in point_considered are vanished. #
    while point_considered:
        
        # Min_value_point is the next point to which we have to move. This one has the storest distance than others. #
        min_value_point = None
        
        # This loop considered every point in the map given. #
        for points in point_considered:
            if min_value_point==None:
                min_value_point = points
                
                # The below condition is to check which point is to be taken as min_value_point. If the present point
                # has less than distance value as compared to min_value_point then the present point is made min_value_pt.#
            elif value_dic[points]<value_dic[min_value_point]:
                min_value_point = points
           
            # The below variable is the points to which min_value_point is connected along with distance between them.
            # This is in form of dictionary items.#
            available_point_path = point_considered[min_value_point].items()
            
            # Then we run in loop for the points we get in above available_point_path. Here next_point is next point 
            #to move to and i is the distance between them.#
            for next_point,i in available_point_path:
                # Condition to see if the total distance to next point is less or more then the distance to it through
                #some other path. If it is less then new distance value is assigned to it. 
                if i+value_dic[min_value_point]<value_dic[next_point]:
                    value_dic[next_point]=i+value_dic[min_value_point]
                    
                    # We put the previous point in the dictionary we created for it.#
                    previous_point[next_point] = min_value_point
                    
                    
        # To remove that min_value_point from the map given so that elements in graph are reduced.#            
        point_considered.pop(min_value_point)
        
        
    # We make a variable and get is value that is destination point.#       
    final_point = target
    
    # The below loop will run untill the variable made not becomes the starting point.#
    while final_point!=start:
        path_taken.append(final_point)
        # The final_point is changed to previous point of present point once every time loop runs.#
        final_point = previous_point[final_point]
    print(value_dic[target])
    newList = (path_taken + [start])
    newList.reverse()
    #reversing the list so that we can output the correct ordered path
    print(newList)
    return newList,value_dic[target]


def graphIt(graph,route,mapName):
    '''this function takes argument of graph or the map of the place where the algorithm is finding shortest routes on, also we take 
    route as an argument that is returned by the algorithm, and output a weighted graph of the whole map with the route highlighted. 
    We use the two imported libraries i.e. matplotlib and networkx in this function only.This function has been bootstraped from the 
    official documentation of the networkx library to display the graph window and then edited as per need of this project. '''
    G = nx.Graph()
    #initiating a networkx graph
    for i in graph:
        for j in graph[i]:
            '''this nested for loop adds element to the networkx weighted graph(G).'''
            G.add_edge(i, j, weight=graph[i][j])#adding nodes from the map into the graph with their edge weight. 

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]#these are two arguments that the library needs to produce a graph screen, these two variables came in the documentation code.

    # positions for all nodes - seed argument is given to avoid randomness of the point everytime we run the program.
    if mapName == "IIT Ropar Main Campus | map is not to scale":
        seedCount = 6
    else:
        seedCount = 7
    pos = nx.spring_layout(G,seed=seedCount)
    # nodes - drawing the points in the graph.
    nx.draw_networkx_nodes(G, pos, node_size=1000, alpha=0.5)

    # edges - drawing the edges on the graph.
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=3)
    nx.draw_networkx_edges(
        G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed",#style arguments for the graph are listed here.
    )

    # node labels - point names are given onto the graph by this line of code.
    nx.draw_networkx_labels(G, pos, font_size=8,font_family="sans-serif", font_color="white")
    
    # edge weight labels - display and style of the edge weights is controlled by this line.
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels,font_size=5)
    plt.figure(1)

    ax = plt.gca()#defining the axes

    ax.text(-1.098,-1.189, route , style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10}) #displaying the shortest route on the graph.

    ax.margins(0.1)#0.08

    plt.axis("off")#disable the visibility of the axes.
    plt.tight_layout()#stretching the graph to fit the screen.
    plt.title(mapName)


def output(map,start,end,mapName,mapvar):
    '''this function uses all the above functions and returns the desired path and graph. We take 4 arguments in this function,i.e. 
    map: the place where we search for routes
    start: starting point of the route
    end: destination of the search
    mapName: name of the place'''
    route,distance = runner_code(map.real, start, end) #we define route and distance that are returned from the runner_code function
    x = []#we initialize x and y coordinate empty arrays.
    y = []#these coordinates are used in highlighting the route points.
    for i in route:
        #filling the route points in the arrays so as to highlight those specfic points.
        x.append(map.coordinates[i][0])
        y.append(map.coordinates[i][1])
    Route = "Shortest Distance : " + str(distance) + "m\n" #converting the route returned from ruuner_code into a string so as to display
                                                           #on the graph.
    for j in route:
        Route += j
        Route+= "-->"#appending arrows in the Route for a better user experience.
    Route = Route[:len(Route)-3]#removing the last arrow added in the Route.
    plt.scatter(x, y, color="black", alpha=1, s=1000)#plotting the highlighting points.
    plt.scatter(-0.025,0.017,c="red",alpha=0.5,s=2000**2)#plotting the red background.
    graphIt(map.graph,Route,mapName)#plotting the weighted graph using networkx and matplotlib.
    plt.figure(2)
    plt.imshow(mapvar)
    plt.show()



main_iitrpr = mpimg.imread('assets/map_iitrpr.png')
transit_iitrpr = mpimg.imread('assets/map_transit_iitrpr.png')
map_input = input("where do you want to go IIT(main/transit) campus : ")#choice between main campus or transit campus
if map_input == "main campus": 
    map = map_iitrpr
    mapName = "IIT Ropar Main Campus | map is not to scale"#this is basically the title of the matplotlib window.
    mapvar = main_iitrpr
else:
    map = map_transit_iitrpr
    mapName = "IIT Ropar Transit Campus | map is not scale"
    mapvar = transit_iitrpr

start_input = input("what is the starting point of your journey : ")#input for the starting point.
end_input = input("what is your destination : ")#input for end point.
print("\nlets find out the shortest route for your journey\n......  ")




output(map,start_input,end_input,mapName,mapvar)#executing the combing function on the given input.
# output(map_iitrpr,"mess","chenab","IIT Ropar Main Campus | map is not to scale")#executing the combing function on the given input.

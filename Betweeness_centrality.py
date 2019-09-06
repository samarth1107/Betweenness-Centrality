#!/usr/bin/env python3

"""
Made by 
Samarth Chauhan
2018410
B-3
"""
import ast
import re
import itertools
from collections import defaultdict

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "samarth"
    email = "samarth1107@gmail.com"
    roll_num = "2018410"

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """
        #to initilize vertices
        self.vertices = vertices  
        #to initilize edges 
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))        
        self.edges    = ordered_edges  
        
        #to validate if name,roll,email,vertices and edges are entered correctly
        self.validate()

        #to make graph in dictionary form that dictionary is adjacentnode
        self.create_adjacent(self.edges)        
       
    def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

    def min_dist(self, start_node, end_node):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''
        #here both these list are used to keep check on the explored and visited node of graph
        explored=[]
        visiting_list=[start_node]
        #initilising queue 
        queue_list=[start_node]
        #this will store every level of searching and initilized root level at 1
        level_dict={}        
        level_dict[start_node]=1        
        
        #while loop will conttinue till it founds empty list of queue
        while (queue_list!=[]):            
            
            #adding node that will be explore in the upcoming steps
            explored.append(queue_list[0])
            #to get adjacent and connected node to first node in queue list
            neighbour=self.adjacentnode[queue_list[0]]

            for adjacent_node in neighbour:
                
                #if node is not visited then it will add to visiting list
                if adjacent_node not in visiting_list:
                    
                    #adding node to queue to explore later
                    queue_list.append(adjacent_node)        
                    #adding visiting list
                    visiting_list.append(adjacent_node)
                    #to update level dictionary
                    level_dict[adjacent_node]=level_dict[queue_list[0]]+1
            
            #first in first out (FIFO) concept here removing first element in queue
            del queue_list[0]
        
        return level_dict[end_node]

    def create_adjacent(self, data):
        """
        Creates dictionary with the help of edges 

        Args:
            edges

        Returns:
            Dictionary where value will be connecting node to node in key
        """
        #to make graph 
        self.adjacentnode=defaultdict(set) 
        for node1, node2 in data:
            self.adjacentnode[node1].add(node2)      
            self.adjacentnode[node2].add(node1)
        
    def all_shortest_paths(self, start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """
        #to get shortest distance 
        distance=self.min_dist(start_node,end_node)

        #to get path which has the length of distance or min distance
        return self.all_paths(start_node,end_node,distance)
        
    def all_paths(self, node, destination, dist, path=[]):
        """
        Finds all paths from node to destination with length = dist

        Args:
            node: Node to find path from
            destination: Node to reach
            dist: Allowed distance of path
            path: path already traversed

        Returns:
            List of path, where each path is list ending on destination

            Returns None if there no paths
        """
        #to add every node so that we will enter again that path
        path=path+[node]
        
        #condition to stop recurrsion 
        if node == destination:
            return [path]
        
        pathslist = []
        
        #enter in the connecting node to start node
        for element in self.adjacentnode[node]:
            #if path is not visited then we enter and call again function
            if element not in path:
                newpaths = self.all_paths(element,destination,dist,path)
                
                for newpath in newpaths:
                    #to check of the length of path is equal to min distance
                    if len(newpath)==dist:
                        pathslist.append(newpath)
        
        return pathslist

    def betweenness_centrality(self, node):
        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """       

        vertice_len=len(self.vertices)
        value=[]

        #outter loop that will help to make pairs of node
        for num in range(0,(vertice_len)):
            #to check if in making pair we don't get node for which we are calculating SBC
            if self.vertices[num]!=node:
                #inner loop that will help to make pairs of node
                for num2 in range(num+1,vertice_len):
                    Y=0
                    #to check if in making pair we don't get node for which we are calculating SBC
                    if self.vertices[num2]!=node:                        
                        #to get all path with and without node that is consider in the loop cycle
                        X=len(self.all_shortest_paths(self.vertices[num],self.vertices[num2]))                                                                      
                        #to check if node is present in the path
                        for shortpath in self.all_shortest_paths(self.vertices[num],self.vertices[num2]):
                            if node in shortpath:
                                Y+=1
                        
                        value.append(Y/X)
                       
        sum=0                
        #calulating the sum of Y/X stored in value list 
        for n in range(0,len(value)):
            #sum will BC at the last step of loop
            sum+=value[n]

        #in this step i am making BC into SBC
        return (sum*2)/((vertice_len-1)*(vertice_len-2))
        
    def top_k_betweenness_centrality(self):
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            List a integer, denoting top k nodes based on betweenness
            centrality.
        """
        value=[]
        for node in self.vertices:
            value.append(self.betweenness_centrality(node))

        #initilizing max variable
        max=value[0]
        
        #block to find max of SBC 
        SBC={}
        for num in range(0,len(value)):
            SBC[self.vertices[num]]=value[num]
            if value[num]>=max:
                max=value[num]
      
        #this will make list of vertices and its SBC value in increasing order
        sortedSBC=sorted(SBC.items(),key=lambda t:t[1])

        #to make final list that contain top K vertices according to max from previous block
        finalSBC=[]
        for num in range(0,len(sortedSBC)):           
            if sortedSBC[num][1]==max:
                finalSBC.append(sortedSBC[num][0])
            
          

        return finalSBC
            

if __name__ == "__main__":

    #example
    #vertices = [1, 2, 3, 4, 5, 6]
    #edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (3, 6), (4, 5), (4, 6)]
    
    
    #list to store vertices
    vertices=input("Enter vertices in format like [1, 2, 6] : \n")    
    vertices=ast.literal_eval(vertices)
    
    #list to store edges
    edges=input("Enter edges in format like [(1,2),(1,3)] : \n")
    edges=ast.literal_eval(edges)   

    #graph is instance of class Graph
    graph = Graph(vertices, edges)

    #printing of output
    print("Top node according to betweeness centrality : ")
    for node in graph.top_k_betweenness_centrality():
        print (node,"   ",end=" ")
    
    
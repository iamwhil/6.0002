# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest

from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: The graphs nodes represent each building in this problem.  The edges 
# represent the paths between the buildings.  The distances are represented
# in WeightedEdges.  These are edges that have the total_distance and 
# outdoor_distance properties.  When they are added to the graph, the weighted
# edges are a list in a dictionary with the nodes (buildings) as the keys.
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    # Create the empty digraph.
    g = Digraph()
    
    #Creating a node look up dictionary, so that 2 nodes are not created with the name 'a' that look the same
    # but do not set off the duplicate warnings.
    nodes = {} 
    
    print("Loading map from file...")
    loaded_data= []
    with open(map_filename, 'r') as f:
        loaded_data = f.read()
        
    # Split the loaded data at the newlines.
    loaded_data = loaded_data.split("\n")
    for path in loaded_data:
        if not path == "": # Avoid any blank lines.
            source, destination, total_dist, outdoor_dist = path.split(' ')
            # Check if we've already made a node for the source and destination
            if not source in nodes.keys():
                nodes[source] = Node(source)
            if not destination in nodes.keys():
                nodes[destination] = Node(destination)
                
            # If the nodes are not in the nodes list, add them    
            if not nodes[source] in g.nodes:
                g.add_node(nodes[source])
            if not nodes[destination] in g.nodes:
                g.add_node(nodes[destination])
                
            g.add_edge(WeightedEdge(nodes[source], nodes[destination], total_dist, outdoor_dist))
    return g
        
 
# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
# print(load_map("test_map.txt"))
#est Path using Optimized Search Method
#
# Problem 3: Finding the Shor
# Problem 3a: Objective function
# What is the objective function for this problem? What are the constraints?
# Answer:
# The objective function here is to find the shortest possible distance between two nodes.
# Additionally, the constraints that bound the problem are a maximum time spent out doors.
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # Add the starting node to our path
    path = [path[0] + [start], path[1], path[2]]
    #best_dist = path[1]
    #print("max_dist_outdoors", max_dist_outdoors)
    # If the start is the end point return the path
    if start == end:
        return path
    
    if start == Node('32'):
        for edge in digraph.get_edges_for_node(start):
            print(str(edge))
    # For each of the nodes edges, explore that path.
    for edge in digraph.get_edges_for_node(start):
        if not (edge.get_destination() in path[0]): # Avoid cycles.
            path[1] = path[1] + edge.get_total_distance()
            path[2] = path[2] + edge.get_outdoor_distance()
            if edge.get_destination() == Node('56'):
                print("Destination", edge.get_destination())
                print("{PATH IS:", path)
            if best_path == None or best_dist == None or (path[2] <= max_dist_outdoors and path[1] <= best_dist):
                new_path = get_best_path(digraph, edge.get_destination(), end, path, max_dist_outdoors, best_dist, best_path)
                if new_path != None:
                    best_path = new_path
                    best_dist = new_path[1]
        else:
            if False:
                print("Already vistited ", start)
    
    return best_path
#    path = [path[0] + [start], path[1], path[2]]
#    print("CURRENT PATH", path)
#    if start == end:
#        return path
#    for edge in digraph.get_edges_for_node(start):
#        if edge.get_destination() not in path[0]: #avoid cycles
#            if best_path == None or len(path[0]) < len(best_path):
#                newPath = get_best_path(digraph, edge.get_destination(), end, path, max_dist_outdoors, best_dist,
#                  best_path)
#                if newPath != None:
#                    best_path = newPath
#        else:
#            print('Already visited', edge.get_destination())
#            
#    return best_path 


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    start_node = Node(start)
    destination_node = Node(end)
    if (start_node in digraph.nodes and destination_node in digraph.nodes):
        best_path = get_best_path(digraph, start_node, destination_node, [[], 0, 0], max_dist_outdoors, None, None)
    if best_path == None or best_path[1] > max_total_dist or best_path[2] > max_dist_outdoors:
        raise ValueError
    else:
        list_of_buildings = []
        for node in best_path[0]:
            list_of_buildings.append(str(node))
        return list_of_buildings


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")
        #self.graph = load_map("test_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        #self._test_path(expectedPath=['1', '7'])
        self._test_path(expectedPath=['32', '56'])

#    def test_path_no_outdoors(self):
#        self._test_path(
#            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

#    def test_path_multi_step(self):
#        self._test_path(expectedPath=['2', '3', '7', '9'])
#
#    def test_path_multi_step_no_outdoors(self):
#        self._test_path(
#            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)
#
#    def test_path_multi_step2(self):
#        self._test_path(expectedPath=['1', '4', '12', '32'])
#
#    def test_path_multi_step_no_outdoors2(self):
#        self._test_path(
#            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
#            outdoor_dist=0)
#
#    def test_impossible_path1(self):
#        self._test_impossible_path('8', '50', outdoor_dist=0)
#
#    def test_impossible_path2(self):
#        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()

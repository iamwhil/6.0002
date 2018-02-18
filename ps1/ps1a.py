###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    
    cow_dict = {}
    
    with open(filename, 'r') as f:
        lines = list(f)
    
    for line in lines:
        line = line.replace("\n", '')
        cow_data = line.split(',')
        cow_dict[cow_data[0]] = int(cow_data[1])
    
    return cow_dict

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    returned_cows = [] # List of list of returned cows.
    cows_copy = [] #We will copy the sorted cows into a list so they can be iterated over.

    #Sorting the cows by their weight.
    sorted_cows = sorted(cows, key=cows.get, reverse=True) 

    # Go through the cows_copy building lists of cows to return.
    while len(sorted_cows) > 0:
    	cow_batch = [] # Cows to return this trip. 
    	total_weight = 0 # Running weight of the cows.
    	for i in range(len(sorted_cows)):
    		if cows[sorted_cows[i]] <= limit - total_weight:
    			cow_batch.append(sorted_cows[i])
    			total_weight += cows[sorted_cows[i]]
    	returned_cows.append(cow_batch)
    	for cow in cow_batch:
    		if cow in sorted_cows:
    			sorted_cows.remove(cow) # Remove the cows in the batch from the sorted list.
    return(returned_cows)

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    num_trips = len(cows) # Number of trips that will need to be taken
    returned_cows = []
    for partition in get_partitions(cows):
    	max_weight = 0 # Find the max weight for the partition.
    	for cow_batch in partition:
    		# Ideally I would like to break from this loop and go to the
    		# next partition if the total_batch_weight > limit.
    		total_batch_weight = 0
    		for cow in cow_batch:
    			total_batch_weight += cows[cow]
    		if total_batch_weight > max_weight:
    			max_weight = total_batch_weight
	    	if max_weight > limit:
	    		break

    	if (len(partition) < num_trips) and (max_weight <= limit):
    		returned_cows = partition
    		num_trips = len(partition)
        
    return returned_cows
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # Load the cows, only do this once. 
    cows = load_cows('ps1_cow_data.txt')

    # run and print time to run our greedy cow transport function.
    tn = time.time()
    greedy_cows = greedy_cow_transport(cows, 10)
    print("Greedy cow time: {0:.5f}".format(time.time() - tn))

    # Run and print time to run our brute force cow transport function.
    tn = time.time()
    brute_cows = brute_force_cow_transport(cows, 10)
    print("Brute force time: {0:.5f}".format(time.time() - tn))

    print("Greedy cow trips: ", len(greedy_cows))
    print("Brute force cow trips: ", len(brute_cows))

compare_cow_transport_algorithms()

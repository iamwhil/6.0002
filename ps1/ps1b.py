###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Whil Piavis
# Collaborators: None
# Time: Too Long?
# Author: charz, cdenise
# Notes: The dp_make_weight function is supposed to be recursive via the problem descriptoin.
# However if you make it simply return an integer, the quantity of each of the eggs is completely lost.
# To rectify this we could make a second function with a recursive call, but that is not what was asked.
# So instead I simply return the set, a dictionary, of the eggs that will be shipped back.

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: an optimal set of eggs.
    """
   
    # Check the memoization first.
    if target_weight in memo.keys():
        return memo[target_weight]
    
    # If the target_weight is not in the memo build its optimal set.
    optimal_set = {}
    
    # If the target_weight is an egg weight return the optimal set, and set the memo.
    if target_weight in egg_weights:
        optimal_set[target_weight] = 1
        memo[target_weight] = optimal_set
        return optimal_set
    
    # If the target weight is not an egg weight, find the largest egg in the set that fits, 
    # subtract it from the target weight and find the optimal set for the remaining_weight
    if target_weight >= egg_weights[-1]:
        remaining_weight = target_weight - egg_weights[-1]
        optimal_set = combine_sets(dp_make_weight(egg_weights, egg_weights[-1], memo), dp_make_weight(egg_weights, remaining_weight, memo))
        memo[target_weight] = optimal_set
    else:
        optimal_set = combine_sets(optimal_set, dp_make_weight(egg_weights[0:-1], target_weight, memo))
        memo[target_weight] = optimal_set
    return optimal_set
        
def combine_sets(s1, s2):
    """
    Combines 2 sets of egg choices.
    
    eg: {1: 1, 5: 2, 10: 0, 25: 0} + {1: 1, 5: 0, 10: 2, 25: 4} = {1: 2, 5: 2, 10: 2, 25: 4}
    """
    combined_set = {}
    # Iterate through the first set of keys.
    for key in s1.keys():
        if key in s2.keys():
            combined_set[key] = s1[key] + s2[key]
        else:
            combined_set[key] = s1[key]
    # Iterate through the second set of keys.
    for key in s2.keys():
        if key in s1.keys():
            combined_set[key] = s1[key] + s2[key]
        else:
            combined_set[key] = s2[key]
    
    return combined_set

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
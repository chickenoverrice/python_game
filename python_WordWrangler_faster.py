#http://www.codeskulptor.org/#user40_x2cwxuQAJrbZuoz.py
"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
codeskulptor.set_timeout(100)


WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    ans = []
    for item in list1:
        ans.append(item)
    temp = []
    for idx in range(len(list1)-1):
        if ans[idx] == ans[idx+1]:
            temp.append(idx)
    for idx_t in range((len(temp)-1),-1,-1):
        ans.pop(temp[idx_t])
    #print temp
    #print ans
    return ans
#remove_duplicates([1,2,2,2,3,4,5,7,9])                     

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
#    ans = []
#    if len(list1) < len(list2):
#        for item in list1:
#            if item in list2:
#                ans.append(item)
#    else:
#        for item in list2:
#            if item in list1:
#                ans.append(item)
    ans = []
    idx1 = 0
    idx2 = 0
    while idx1<len(list1) and idx2<len(list2):
        if list1[idx1]<list2[idx2]:
            idx1 += 1        
        elif list1[idx1]==list2[idx2]:
            ans.append(list1[idx1])
            idx1 += 1
            idx2 += 1
        elif list1[idx1]>list2[idx2]:
            idx2 += 1
            
    #print ans   
    return ans
#intersect([2,3,4,5],[1,2,3,5,9,10])
# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """ 
    ans = []
    idx1 = 0
    idx2 = 0
    if len(list1) > len(list2):
        temp = list1
        list1 = list2
        list2 = temp
    while idx1 < len(list1) and idx2 < len(list2):
        if list1[idx1] < list2[idx2]:
            ans.append(list1[idx1])
            idx1 += 1
        else:
            ans.append(list2[idx2])
            idx2 += 1
    if idx1 < len(list1):
        ans.extend(list1[idx1:])
    if idx2 < len(list2):
        ans.extend(list2[idx2:])
    #print ans                  
    return ans
#merge([4,5],[1,2,3])                

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    else:
        left = merge_sort(list1[:len(list1)/2])
        right = merge_sort(list1[len(list1)/2:])
        ans = merge(left, right)
    #print ans
    return ans
#a = merge_sort([7,4,6,3,1,2,10,23,45,15,78,101,63,27])
#print a
# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == "":
        return [""]
    else:
        first = word[0]
        rest = word[1:]
        new_list = [first]
        rest = gen_all_strings(rest)
        if first != "":
            for item in rest:
                if item != "":
                    for idx in range(len(item)+1):
                        temp = item[:idx]+first+item[idx:]
                        new_list.append(temp)   
            new_list.extend(list(rest))            
    #print new_list
    return new_list

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    dict_file = urllib2.urlopen(codeskulptor.file2url(filename))
    ans = []
    for item in dict_file.readlines():
        ans.append(item[:-1])
    return ans

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()

    
    

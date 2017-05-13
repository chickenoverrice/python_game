#http://www.codeskulptor.org/#user40_Pr2t3Pg6M4Wkq7O.py
"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster



######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    min_dist = (float('inf'),-1,-1)
    temp = ()
    for idx1 in range(len(cluster_list)):
        for idx2 in range(len(cluster_list)):
            if idx1 != idx2:
                temp = pair_distance(cluster_list,idx1, idx2)
                if temp[0] < min_dist[0]:
                    min_dist = temp
    #print min_dist
    return min_dist



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    temp_list = []
    for item in cluster_list:
        temp_list.append(item.copy())    
    temp_list.sort(key = lambda cluster: cluster.horiz_center())
    min_dist = ()
    if len(temp_list)<=3:
        min_dist = slow_closest_pair(temp_list)
        #print temp_list
#        if min_dist[1] != -1 and min_dist[2] != -1:
#            cidx1 = cluster_list.index(temp_list[min_dist[1]])
#            cidx2 = cluster_list.index(temp_list[min_dist[2]])
#            temp_lst = [min_dist[0],min(cidx1,cidx2),max(cidx1,cidx2)]
#            min_dist = tuple(temp_lst) 
        #print min_dist    
        return min_dist
    else:
        l_list = temp_list[:len(temp_list)/2]
        r_list = temp_list[len(temp_list)/2:]
        temp1 = fast_closest_pair(l_list)
        temp2 = fast_closest_pair(r_list)
        if temp1[0]<temp2[0]:
            min_dist = temp1
        else:
            min_point = [temp2[0],(temp2[1]+len(temp_list)/2),(temp2[2]+len(temp_list)/2)]
            min_dist = tuple(min_point)    
        mid_xcoor = (temp_list[len(temp_list)/2-1].horiz_center()+temp_list[len(temp_list)/2].horiz_center())/2
        temp3 = closest_pair_strip(temp_list,mid_xcoor,min_dist[0])
        if temp3[0]<min_dist[0]:
            min_dist = temp3
    #print min_dist
    return min_dist


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    min_dist = (float('inf'), -1, -1)
    temp = ()
    select = []
    for item in cluster_list:
        if math.fabs(item.horiz_center()-horiz_center) < half_width:
            select.append(item)
    select.sort(key = lambda cluster: cluster.vert_center()) 
    for idx1 in range(len(select)-1):
        for idx2 in range(idx1+1, (min((idx1+3),(len(select)-1))+1) ,1):
            temp = pair_distance(select, idx1, idx2)
            if temp[0] < min_dist[0]:
                min_dist = temp
    #print min_dist   
    if min_dist[1] != -1 and min_dist[2] != -1:
        cidx1 = cluster_list.index(select[min_dist[1]])
        cidx2 = cluster_list.index(select[min_dist[2]])
        temp_lst = [min_dist[0],min(cidx1,cidx2),max(cidx1,cidx2)]
        min_dist = tuple(temp_lst)
    return min_dist
            
#slow_closest_pair([alg_cluster.Cluster(set([]), 0.32, 0.16, 1, 0), alg_cluster.Cluster(set([]), 0.39, 0.4, 1, 0), alg_cluster.Cluster(set([]), 0.54, 0.8, 1, 0), alg_cluster.Cluster(set([]), 0.61, 0.8, 1, 0), alg_cluster.Cluster(set([]), 0.76, 0.94, 1, 0)])
#fast_closest_pair([alg_cluster.Cluster(set([]), 0.32, 0.16, 1, 0), alg_cluster.Cluster(set([]), 0.39, 0.4, 1, 0)])
#fast_closest_pair([alg_cluster.Cluster(set([]), 0.32, 0.16, 1, 0), alg_cluster.Cluster(set([]), 0.39, 0.4, 1, 0), alg_cluster.Cluster(set([]), 0.54, 0.8, 1, 0), alg_cluster.Cluster(set([]), 0.61, 0.8, 1, 0), alg_cluster.Cluster(set([]), 0.76, 0.94, 1, 0)])    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    return []


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
            
    return []


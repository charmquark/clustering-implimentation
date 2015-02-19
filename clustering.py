# -*- coding: utf-8 -*- 
import codecs
import string
import math
import random
import argparse

def read_data(filename):
    """ return list of points from file with structure like
    (name, [x, y, q, r]), where x, y, q, r are some integers """
    data = []
    with codecs.open(filename, encoding='utf-8') as f:
        next(f) # skip first line
        for line in f:
            line_strip = string.replace(line, '\r\n', '')
            components = line_strip.split('\t')
            name = components[0]
            coords = [int(i) for i in components[1:]]
            data.append((name, coords))
    return data

def clean_data(data):
    """ put the given data into dictionary with key: editors' name and value: the points
        assuming given data is in the format [('haa',[1,2,3,5....]), ...)]
        return a list conists of a dictionary and data withouth editor username
     """
    data_dict={}
    clean_data = []
    for item in data:
        data_dict[item[0]] = item[1]
        clean_data.append(item[1])
    return [clean_data, data_dict]

def standardize(data):
    """ convert every value x in data to log(x+1) """
    std_data = []
    for entry in data:
        pts = entry[1]
        log_pts = [math.log(p+1) for p in pts]
        std_data.append((pts[0], log_pts))
    return std_data

def random_centers_from_limit(k_clusters, dimentions, limit):
    """Do not use this for now. need limit, which is the range we get from data"""
    k = k_clusters
    d = dimentions
    centers = []
    random.seed(27945)      # seed the random
    for i in range(k):
        center = []
        for i in range(d):   #d = 4 if given 4D data
            r = random.random()
            center.append(r * limit)
        centers.append(center)
    return centers

def random_centers_from_data(k, data):
    """ generate random centers with given data 
        assuming given data is in the format [('haa',[1,2,3,5....]), ...)]
    """
    index = len(data)
    #random.seed(78902)     # seed is not used
    centers =[] 
    for i in range(k): # number of ranges
        rand = random.randint(1, index)    # generate random number in the range of 1 to the length of the data
        center =[]
        for j in range(len(data[0][1])): # the dimension of the data      
            center.append(data[rand-1][1][j])
        centers.append(center)
    return centers

def gen_new_centers(clusters):
    """ return a list of new cluster centers 
        given the current clusters dictionary (currently without their id)
    """
    centers =[]
    for key, values in clusters.iteritems():
        num_points = len(values)     # number of points in data
        d = len(values[0])   #dimension of the data
        cluster_sum=[0] * d
        for i in range(num_points):     # each point within the cluster
            for j in range(d):                   # each dimension of each point
                cluster_sum[j] += value[i][j]
        for each_sum in cluster_sum:
            centers.append[each_sum/num_points]
        centers.append(centers)
    return centers

def gen_clusters (centers, data):
    """ returned data format, when k = 3: [([1,2,3,4],[2,2,3,4],[3,2,3,4],....),[],[]]"""
    k = len(centers)
    result = [()] * k
    dict = {}
    for i, center in enumerate(centers):
        dict[i] = center      
        result[i]
    for point in data:       # number of points
        assignment = min_squared_euclidean_dist(centers, point[1])
        index = get_key(dict, assignment)
        result[index].append(point)
    return result

def get_key(dict, value):
    """ helper function getting key fiven a value for a dictionary.
        This is faster
     """
    for index, point in dict.iteritems():
        if point == value:
            return index

def min_squared_euclidean_dist(centers, point):
    """ return the assignment for the point given several centers as choices"""
    min_dist = float("infinity")
    cur_dist = 0
    for center in centers:
        for i in range(len(center)):
            cur_dist += (center[i] - point[i])**2
        if cur_dist < min_dist:           
            min_dist = cur_dist
            assignment = center 
    return assignment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--clusters', type= int, required=True, help='Input the number of clusters')
    parser.add_argument('-f', '--filename', required=True, help='Input file name')
    #parser.add_argument('-m','-method', required = False, help = 'Choose the method for initializing the cluster centers')

    args = parser.parse_args()
    k = args.clusters
    filename = args.filename

    # do something with choosing a cluster centers initialization method

    # the following are for debugging, eventually we gonna have one function to call from main 
    # and run until it converge

    # readfile 
    data = read_data(filename)
   # standadize data
    data = standardize(data)

    # clean data, not necessary
    #data = process_data(data)
    #data_clean = data[0]
    #data_dict = data[1]

    # generating initial centers from random points from data
    centers = random_centers_from_data(k,data)  
    # for test purpse, test initial center
    for center in centers:
        print "the initial random center is:{0}, \n".format(center)

    # calculating and form some clusters with the centers
    clusters = gen_clusters(centers, data)

    # do sometthing with SSE

    # generating the new centers
    centers = gen_new_centers(clusters)
    # assigne the each point to the closest new centers 




if __name__ == '__main__':
    main()


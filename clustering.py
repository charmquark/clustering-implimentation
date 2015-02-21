import codecs
import string
import math
import random
import argparse
import sys

class Center(object):
    """docstring for Center"""
    def __init__(self, location):
        super(Center, self).__init__()
        self.location = location
        self.points = []

    def __repr__(self):
        # undo log_2(x+1)
        unlogged_loc = [2**(i-1) for i in self.location]
        return "<Center> at {0}".format(self.location)


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

def standardize(data):
    """ convert every value x in data to log(x+1) """
    std_data = []
    for entry in data:
        pts = entry[1]
        log_pts = [math.log(p+1)/math.log(2) for p in pts]
        std_data.append((entry[0], log_pts))
    return std_data

def random_centers_from_data(k, data):
    """ generate random centers with given data 
        assuming given data is in the format [('haa',[1,2,3,5....]), ...)]
    """
    index = len(data)
    random.seed(123)
    centers = [] 
    for i in range(k): # number of ranges
        rand = random.randint(1, index)    # generate random number in the range of 1 to the length of the data
        point = data[rand]
        center = Center(point[1])
        centers.append(center)
    return centers

def move_centers(centers):
    """ given a list of centers, move each center based on where the average 
    of the points assigned to it lies """
    for center in centers:
        avg = [0] * len(center.location)
        for point in center.points:
            for i, elem in enumerate(point[1]):
                avg[i] += elem
        if len(center.points) > 0:
            avg = [i/len(center.points) for i in avg]
            center.location = avg

def gen_clusters(centers, data):
    """ returned data format, when k = 3: [([1,2,3,4],[2,2,3,4],[3,2,3,4],....),[],[]]"""
    k = len(centers)
    for point in data:       # number of points
        assignment = min_squared_euclidean_dist(centers, point[1])
        # print result[index]
        assignment.points.append(point)

def min_squared_euclidean_dist(centers, point):
    """ return the assignment for the point given several centers as choices"""
    min_dist = float("infinity")
    assignment = None
    for center in centers:
        cur_dist = 0
        for i in range(len(center.location)):
            cur_dist += (center.location[i] - point[i])**2
        if cur_dist < min_dist:           
            min_dist = cur_dist
            assignment = center 
    return assignment

def sse(centers):
    """ compute sum of squares error for data """
    sse = 0
    for center in centers:
        for point in center.points:
            p = point[1]
            for i in range(len(p)):
                sse += (center.location[i] - p[i])**2
    return sse

def kmeans(data, k):
    """ run k-means algorithm """
    centers = random_centers_from_data(k, data)
    gen_clusters(centers, data)
    sse_val = float("infinity")
    iter_num = 1
    while True:
        move_centers(centers)
        all_points = []
        for center in centers:
            all_points.extend(center.points)
            center.points = []
        gen_clusters(centers, all_points)
        new_sse = sse(centers)
        print "SSE before iteration {0}: {1}, after: {2}".format(iter_num, sse_val, new_sse)
        assert new_sse <= sse_val
        if new_sse == sse_val:
            return centers
        sse_val = new_sse
        iter_num += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--clusters', type= int, required=True, help='Input the number of clusters')
    parser.add_argument('-f', '--filename', required=True, help='Input file name')
    # parser.add_argument('-m','-method', required = False, help = 'Choose the method for initializing the cluster centers')

    args = parser.parse_args()
    k = args.clusters
    filename = args.filename

    # read file 
    data = standardize(read_data(filename))
    clusters = kmeans(data, k)
    for center in clusters:
        print center
        for point in center.points:
            sys.stdout.write(point[0] + ', ')
        print "\n"

if __name__ == '__main__':
    main()


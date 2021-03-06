import codecs
import string
import math
import random
import argparse
import sys

"""
clustering2.py by Brian Charous and Yawen Chen
An implementation of k-means clustering technique
PART2 uses normalize_row to normalize data without calculating the log.
To compile: clustering.py -k (number of clusters) -f (filename) -i (initialization method: either random or distance, default is random) 
For example: 
                     python clustering2.py -k 5 -f wiki.txt -i random
                     python clustering2.py -k 5 -f wiki.txt -i random 
                    python clustering2.py -k 5 -f wiki.txt -i distance 
                    python clustering2.py -k 5 -f wiki.txt  #default method is random -

"""
class Center(object):
    """class for the centroid of a cluster"""
    def __init__(self, location):
        super(Center, self).__init__()
        self.location = location
        self.points = []

    def __repr__(self):
        return "<Center> at {0}, {1} items".format(self.location, len(self.points))

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

def normalize_rows(data):
    """ normalize the row with the method: -dividing each row by the Euclidean magnitude of the row """
    normalized_data = []
    for item in data:
        point = item[1]
        magnitude = 0
        norm_row = []
        for d in range(len(point)):  # get the magnitude of this row
            magnitude += (point[d] **2)
        magnitude = math.sqrt(magnitude) # square root of the sum of squared values 
        for i in range (len(point)):    # normalize row
            norm_row.append(point[i]/magnitude)
        normalized_data.append ((item[0], norm_row))
    return normalized_data


def random_centers_from_data(k, data):
    """ generate random centers with given data 
        assuming given data is in the format [('haa',[1,2,3,5....]), ...)]
    """
    index = len(data)
    random.seed(123)
    centers = [] 
    for i in range(k): # number of ranges
        rand = random.randint(0, index-1)    # generate random number in the range of 1 to the length of the data
        point = data[rand]
        center = Center(point[1])
        centers.append(center)
    return centers

def distanced_centers_from_data(k, data):
    """ initialize centers by choosing a random point, 
    then choosing the furthest away point from the current starting points """
    centers = []
    random.seed(123)
    first_p = data[random.randint(0, len(data)-1)]
    first = Center(first_p[1])
    centers.append(first)
    for i in range(k-1):
        max_dist = 0
        new_center_p = None
        for point in data:
            total_distance = 0
            p = point[1]
            for center in centers:
                for i in range(len(p)):
                    total_distance += (center.location[i] - p[i])**2
            if total_distance > max_dist:
                max_dist = total_distance
                new_center_p = point
        new_center = Center(new_center_p[1])
        centers.append(new_center)
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
            # deal with empty cluster in a sec
            avg = [i/len(center.points) for i in avg]
            center.location = avg

def distance(center, point):
    dist = 0
    for i in range(len(point)):
        dist += (center.location[i] - p[i])**2
    return dist

def gen_clusters(centers, data):
    k = len(centers)
    for center in centers:
        center.points = []
    for point in data:
        assignment = min_squared_euclidean_dist(centers, point[1])
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

def point_furthest_from_center(centers):
    """ find the point furthest away from its center and the center
    to which it corresponds """
    max_dist = 0
    return_pt = None
    return_center = None
    for c in centers:
        for j, point in enumerate(c.points):
            p = point[1]
            dist = 0
            for i in range(len(point)):
                dist += (c.location[i] - p[i])**2
            if dist > max_dist:
                max_dist = dist
                return_pt = c.points[j]
                return_center = c
    return (return_center, return_pt)

def kmeans(data, k, init_method):
    """ run k-means algorithm"""
    if init_method:
        if init_method == 'random':
            centers = random_centers_from_data(k, data)
        elif init_method == 'distance':
            centers = distanced_centers_from_data(k, data)
        else:
            print "'Error: {0}' is not a valid initilization technique. Please choose from random or distance".format(init_method)
            sys.exit(1)
    else:
        centers = random_centers_from_data(k, data)
    gen_clusters(centers, data)
    sse_val = float("infinity")
    iter_num = 1
    while True:
        move_centers(centers)
        before_sse = sse(centers)
        gen_clusters(centers, data)

        # deal with empty clusters
        empty_centers = False
        while True:
            for center in centers:
                if len(center.points) == 0:
                    # empty center
                    empty_centers = True
                    # get furthest away point, reassign empty center's location
                    remove_c, new_pt = point_furthest_from_center(centers)
                    center.location = new_pt[1]
                    gen_clusters(centers, data)
                    empty_centers = False
            if not empty_centers:
                break

        new_sse = sse(centers)
        print "SSE before, after iteration {0}: {1}, {2}".format(iter_num, before_sse, new_sse)
        assert new_sse <= before_sse
        if new_sse == sse_val:
            return centers
        sse_val = new_sse
        iter_num += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--clusters', type= int, required=True, help='Number of clusters')
    parser.add_argument('-f', '--filename', required=True, help='Data file name')
    parser.add_argument('-i','--init_method', required = False, help = 'Techniqure to choose initial cluster centers. Choices are random or distance')
    args = parser.parse_args()
    k = args.clusters
    filename = args.filename
    init_method = args.init_method

    # read file 
    data = normalize_rows(read_data(filename))
    print "data set up!"
    clusters = kmeans(data, k, init_method)

    for center in clusters:
        print center
              
if __name__ == '__main__':
    main()


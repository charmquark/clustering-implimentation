import codecs
import string
import math
import random

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
        log_pts = [math.log(p+1) for p in pts]
        std_data.append((pts[0], log_pts))
    return std_data


def random_centers(k_clusters, dimentions):
''' Using random method to generate cluster center
    Return a list of k centers with d dimentions
'''
    k = k_clusters
    d = dimentions
    clusters = []
    random.seed(27945)      #seed the random
    for i in range(k):
        center = []
        for i in range(d):  #d = 4 if given 4D data
            r = random.random()
            center.append(r)
        clusters.append(center)
    return clusters

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--clusters', type= int, required=True, help='Input the number of clusters')
    parser.add_argument('-f', '--filename', required=True, help='Input file name')
    #parser.add_argument('-m','-method', required = False, help = 'Choose the method for initializing the cluster centers')

    args = parser.parse_args()
    k = args.clusters
    #if args.method = 2:
        #print "Implimentation coming soon"      
    cluster_centers = random_center(k, 4)

if __name__ == '__main__':
    main()
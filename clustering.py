import codecs
import string
import math

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

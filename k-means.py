from parse import *
import random
import sys


# intiates the random instances as the center of the clusters
def randompick(instances, seed):
    random.seed(seed)

    #I don't really know why I am choosing 10
    k = 10
    randoms = [random.randrange(len(instances)) for _ in range(k)]

    #making the list of centroids from the random indexes
    centroids = []
    for i in range (len(instances)):
        for num in randoms:
            if i == num:
                centroids.append(instances[i])


    return centroids


#using Generalized Jaccard Distance as the distance function
# read about it at https://en.wikipedia.org/wiki/Jaccard_index#Generalized_Jaccard_similarity_and_distance
# looks like what we want maybeeeeeeesssss!

def genjaccard(I1, I2):


    #getting dictionaries
    dic1 = I1[1]
    dic2 = I2[1]

    #finding the denominator and numerator
    union = 0
    inter = 0
    # taking max of attributes that appear in both, and adding all values that are only in d1, Also finding intersection by taking min over attributes that are
    # in both
    for key1 in dic1.keys():

        if key1 in dic2.keys():
            #print('key: ',key1, '   dic1 value: ',dic1[key1],' dic2 value: ',dic2[key1],'     max: ', max(dic1[key1],dic2[key1]) ,'union: ', union)

            union = union + max(dic1[key1],dic2[key1])
            inter = inter + min(dic1[key1],dic2[key1])

        else:
            union = union + dic1[key1]


    # taking all values that are only in d2 adding to union
    for key2 in dic2.keys():
        if key2 not in dic1.keys():
            union = union + dic2[key2]



    distance = 1 - (inter/union)

    return distance






def main():

    seed = sys.argv[1]

    parser = parse()
    instances = parser.read()

    centroids = randompick(instances, seed)

    





main()
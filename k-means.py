from parse import *
import random
import sys


#cluster class where we assign instances to clusters...not completely sure this will necessery but might make it easier
class clusters:

    def __init__(self,k,centroids):

        self.k = k

        self.clustdic = {}
        for center in centroids:
            self.clustdic[center] = []

    def __str__(self):

        string=""
        count = 0
        for key, value in self.clustdic.items():
            count = count + 1
            string = string + "cluster" + str(count) + "\ncenter instance: \n"+ str(key) + "\ninstances in cluster: \n\n"
            for instance in value:
                string = string + str(instance.name) + '\n'
            string = string + "\n\n\n"

        return string


    #reassigns a new centroid to cluster so that then we can recalulate cluster
    def newcentroid(self,mean, oldmean):

        self.clustdic[mean] = self.clustdic.pop(oldmean)
        self.clustdic[mean] = []


################################################################################################


# intiates the random instances as the centers of the clusters
def randompick(instances, seed,k):
    random.seed(seed)

    #I don't really know why I am choosing 10

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
    dic1 = I1.words
    dic2 = I2.words

    #finding the denominator and numerator
    union = 0
    inter = 0
    # taking max of attributes that appear in both, and adding all values that are only in d1, Also finding intersection by taking min over attributes that
    #  are in both
    for key1 in dic1.keys():

        if key1 in dic2.keys():


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




#assigns an instance a cluster based on the smallest distance
def assigncluster(instance,clusters):

    possible = []
    centroids = clusters.clustdic.keys()
    #all distances to each centroid
    for center in centroids:

        distance = genjaccard(center,instance)
        possible.append([center,distance])

    #adding the instance to cluster with smallest distance

    pair = min(possible, key=lambda x: x[1])
    clusters.clustdic[pair[0]].append(instance)

#reassigns centroid by recalculating mean
def recalcmean(cluster):

    #new centroid is a dictonary of words with means as values
    newcentroid = {}

    #adding all words in the cluster to new centroid
    for inst in cluster:
        for word, num in inst.words.items():
            if word not in newcentroid.keys():
                newcentroid[word] = num
            else:
                newcentroid[word] =+ num

    #dividing all values by number of instances
    for word in newcentroid.keys():
        newcentroid[word] = newcentroid[word]/len(cluster)

    new = instance("newmean",newcentroid)

    return new

#checks to see if mean has moved if no then we know we are done
def isStable(oldmeans, newmeans,iteration):

    #looping through the clusters if they are identical then return true
    #doing this by adding 1 to count if vectors are the same, if all vectors are the same return true
    if iteration != 0:
        count = 0
        total = 0
        for old in oldmeans:
            for new in newmeans:
                for key1, value1 in old.words.items():
                    for key2, value2 in new.words.items():
                        total += 1
                        if key1 == key2:
                            if value1 == value2:
                                count += 1

        if count == total:
            return True
        return False

    return False


def main():

    #parsing data
    seed = sys.argv[1]
    parser = parse()
    instances = parser.read()


    ##############initial run #####################
    #randomly sets centroids, and makes the clusters object which will be changed on ever iteration of recalculating the means
    centroids = randompick(instances, seed,10)

    clst = clusters(10,centroids)

    # assigns each instance to a cluster
    for instance in instances:
        assigncluster(instance,clst)

    #just to start the while loop
    count = 0
    oldlist=[]
    newlist=[]
    ###################all runs after but before stabilized##########################

    while isStable(oldlist,newlist,count) == False:

        for centroid,cluster in clst.clustdic.items():

            oldlist=[]
            newlist=[]
            newcentroid = recalcmean(cluster)

            newlist.append(newcentroid)
            oldlist.append(centroid)

            clst.newcentroid(newcentroid, centroid)

        for instance in instances:
            assigncluster(instance,clst)


        print(clst)


main()
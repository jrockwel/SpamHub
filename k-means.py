from parse import *
import random
import sys


#cluster class where we assign instances to clusters, and start new iterations...not completely sure this will necessery but might make it easier

class clst:

    def __init__(self,clusternumber,centroid):


        self.iteration = 0
        self.clustnum = clusternumber
        self.centroid = centroid
        self.instances = []

    def __str__(self):

        string = ""
        string = string +"\ncluster number: "+str(self.clustnum)+'\niteration: '+str(self.iteration) + "\ncentroid:\n" + str(self.centroid) + "\ncontains:\n\n"
        for instance in self.instances:
            string = string + '\n' + instance.name

        string = string + "\n\n\n"

        return string



    def addinstance(self,instance):

        self.instances.append(instance)


    def newiteration(self,newcentroid):

        self.centroid = newcentroid
        self.instances = []
        self.iteration += 1




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
                instances[i].iscent = True
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
def assigncluster(instance,centroids,clusters):



    possible = []
    #all distances to each centroid
    for center in centroids:

        distance = genjaccard(center,instance)
        possible.append([center,distance])

    #adding the instance to cluster with smallest distance

    pair = min(possible, key=lambda x: x[1])

    for cluster in clusters:
        if pair[0].name == cluster.centroid.name:
            cluster.instances.append(instance)


#reassigns centroid by recalculating mean
def recalcmean(cluster):

    #new centroid is a dictonary of words with means as values
    newcentroid = {}

    #adding all words in the cluster to new centroid
    for inst in cluster.instances:
        for word, num in inst.words.items():
            if word not in newcentroid.keys():
                newcentroid[word] = num
            else:
                newcentroid[word] =+ num

    #dividing all values by number of instances
    for word in newcentroid.keys():
        newcentroid[word] = newcentroid[word]/len(cluster.instances)

    new = instance('mean centroid ' + str(cluster.clustnum), newcentroid,True)

    return new

#checks to see if mean has moved if no then we know we are done
def isStable(newmeans, oldmeans,iteration):

    #looping through the clusters if they are identical then return true
    #doing this by adding 1 to count if vectors are the same, if all vectors are the same return true
    if iteration != 0:
        count = 0
        total = 0
        #taking a single centroid
        for i in range(len(oldmeans)):
            # single word, and count in old version
            for oldword, oldcount in oldmeans[i].words.items():
                #getting total length of centroid
                total += 1
                #finding oldword in new dic if it exists
                if oldword in newmeans[i].words.keys():
                    # if values are within a little range then add one to count
                    newvalue = newmeans[i].words[oldword]
                    distance = abs(oldcount - newvalue)
                    if distance < .01:
                        count += 1


        if count == total:
            return True
        return False

    return False


def main():

    #parsing data
    seed = sys.argv[1]
    k = int(sys.argv[2])
    parser = parse()
    instances = parser.read()


    ##############initial run #####################
    #randomly sets centroids, and makes the clusters object which will be changed on ever iteration of recalculating the means
    oldcentroids = randompick(instances, seed,k)

    #making the clusters in a list
    clusters = []
    for i in range(len(oldcentroids)):
        clusters.append(clst(i,oldcentroids[i]))

    # assigns each instance to a cluster
    for instance in instances:
        assigncluster(instance,oldcentroids,clusters)

    newcentroids = []

    for cluster in clusters:
        print(cluster)


    #just to start the while loop

    ###################all runs after but before stabilized##########################
    #while we haven't stabelized keep running
    while isStable(newcentroids,oldcentroids,clusters[0].iteration) != True:

        oldcentroids = []
        newcentroids=[]
        #recalculate the mean for each cluster, and re assign that mean as the new centroid
        #we make the two lists above so we can do the comparsion to see if stable
        for cluster in clusters:
            oldcentroids.append(cluster.centroid)
            new = recalcmean(cluster)
            newcentroids.append(new)
            cluster.newiteration(new)

        #readd all the instances too the clusters with their new centroids
        for instance in instances:
            assigncluster(instance,newcentroids,clusters)

        for cluster in clusters:
            print(cluster)




main()
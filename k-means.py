from parse import *
import random
import sys
import os
import math


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


def cosine(inst1,inst2):

    vector1 = inst1.words
    vector2 = inst2.words

    numerator = 0
    d1 = 0
    d2 = 0
    for i in range (len(vector1)):
        numerator += (vector1[i]*vector2[i])
        d1 += math.sqrt((vector1[i]*vector1[i]))
        d2 += math.sqrt((vector2[i]*vector2[i]))

    denom = d1 *d2

    return (1 - (numerator/denom))



#assigns an instance a cluster based on the smallest distance
def assigncluster(instance,centroids,clusters,format):



    possible = []
    #all distances to each centroid
    for center in centroids:

        if format == "j":
            distance = genjaccard(center,instance)
        else:
            distance = cosine(center,instance)
        possible.append([center,distance])

    #adding the instance to cluster with smallest distance

    pair = min(possible, key=lambda x: x[1])

    for cluster in clusters:
        if pair[0].name == cluster.centroid.name:
            cluster.instances.append(instance)


#reassigns centroid by recalculating mean
def recalcmean(cluster, format):

    #new centroid is a dictonary of words with means as values
    if format == 'j':
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

    else:

        meanvector = [0 for _ in range(len(cluster.instances[0].words))]

        for i in range(len(meanvector)):
            for inst in cluster.instances:
                words = inst.words
                meanvector[i] += words[i]

        for i in range (len(meanvector)):
            meanvector[i] = meanvector[i]/len(cluster.instances)

        new = instance('mean centroid ' + str(cluster.clustnum), meanvector,True)

        print(new)

    return new

#checks to see if mean has moved if no then we know we are done
def isStable(newmeans, oldmeans,iteration):

    #looping through the clusters if they are identical then return true
    #doing this by adding 1 to count if vectors are the same, if all vectors are the same return true
    if iteration != 0:
        #setting counters for number of centriods with unchanged means
        numcluster = len(newmeans)
        check = 0
        #taking a single centroid
        for i in range(len(oldmeans)):
            #setting counter for unchanged values and words
            total = 0
            count = 0
            # single word, and count in old version
            for oldword, oldcount in oldmeans[i].words.items():
                #getting total length of centroid
                total += 1
                #finding oldword in new dic if it exists
                if oldword in newmeans[i].words.keys():
                    # if values are within a little range then add one to count
                    newvalue = newmeans[i].words[oldword]
                    if newvalue == oldcount:
                        count += 1
                        #print(total,count)

            #if nothing has changed in words, and values that centroid is good
            if count == total:
                check += 1
        if check == numcluster:
            return True
    return False


#makes a folder to put cluster documents in
def makenewclusterfolder(seed, k):

    path ='seed_' +  str(seed) + "_k_" + str(k)

    if os.path.isdir(path):
        print("Folder already exists!")
    else:
        os.makedirs(path)

    return path

# writes cluster documents
def writeclusterdoc(clusters, folderpath):

    for i in range (len(clusters)):
        clustnum = clusters[i].clustnum
        filename = str(folderpath) + '/clusternumber_' + str(clustnum) + ".txt"
        file = open(filename, 'w')
        file.write("cluster number: " + str(clustnum) + "\n\n\nFiles in cluster: \n\n\n")
        for instance in clusters[i].instances:
            file_to_write = 'fake_data/'+ str(instance.name)
            towrite = open(file_to_write)
            string = towrite.read()
            file.write(string)
            file.write("\n\n\n\n")


def main():

    #parsing data
    seed = sys.argv[1]
    k = int(sys.argv[2])
    format = sys.argv[3]
    parser = parse()
    instances = parser.read(format)

    # if we our using sparse tfidf vectors then we gotta do a extra step
    if format == 'tfidf':
        instances = parser.all_tfidf(instances)



    ##############initial run #####################
    #randomly sets centroids, and makes the clusters object which will be changed on ever iteration of recalculating the means
    oldcentroids = randompick(instances, seed,k)

    #making the clusters in a list
    clusters = []
    for i in range(len(oldcentroids)):
        clusters.append(clst(i,oldcentroids[i]))

    # assigns each instance to a cluster
    for instance in instances:
        assigncluster(instance,oldcentroids,clusters,format)

    newcentroids = []

    for cluster in clusters:
        print(cluster)


    #just to start the while loop

    ###################all runs after but before stabilized##########################
    #while we haven't stabelized keep running
    while clusters[0].iteration < 20:
        print('\n',clusters[0].iteration,'\n')
        oldcentroids = []
        newcentroids=[]
        #recalculate the mean for each cluster, and re assign that mean as the new centroid
        #we make the two lists above so we can do the comparsion to see if stable
        for cluster in clusters:
            #weeding out the case where the centroid is the only thing in the cluster
            if len(cluster.instances) != 0 :
                oldcentroids.append(cluster.centroid)
                new = recalcmean(cluster,format)
                newcentroids.append(new)
                cluster.newiteration(new)
            # if the centroid is the only thing in the cluster, then keep that cluster and change the others
            else:
                cluster.newiteration(cluster.centroid)
                newcentroids.append(cluster.centroid)

        #readd all the instances too the clusters with their new centroids
        for instance in instances:
            assigncluster(instance,newcentroids,clusters,format)

        for cluster in clusters:
            print(cluster)

    #####after we have clusters add files to their own documents
    path = makenewclusterfolder(seed,k)
    writeclusterdoc(clusters,path)



main()
from parse2 import *
import random
import sys
import os
import math


#cluster class where we assign instances to clusters, and start new iterations...not completely sure this will necessery but might make it easier

class clust:

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

    randoms = random.sample(range(len(instances)),k)

    #making the list of centroids from the random indexes
    centroids = []
    for i in range (len(instances)):
        for num in randoms:
            if i == num:
                centroids.append(instances[i])


    return centroids



def euclid(inst1,inst2):

    vector1 = inst1.words
    vector2 = inst2.words

    tosqrt = 0
    for i in range (len(vector1)):

        tosqrt += (vector1[i]-vector2[i])*(vector1[i]-vector2[i])

    return math.sqrt(tosqrt)


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

    if denom != 0:
        return (1 - (numerator/denom))
    else:
        return 10000000000


def assigncluster(instance,clusters,distfunc):

    possible = []
    #all distances to each centroid
    for cluster in clusters:
        center = cluster.centroid
        if distfunc == "cosine":
            distance = cosine(center,instance)
        else:
            distance = euclid(center,instance)
        possible.append([center,distance])

    #adding the instance to cluster with smallest distance

    pair = min(possible, key=lambda x: x[1])

    for cluster in clusters:
        if pair[0].name == cluster.centroid.name:
            cluster.instances.append(instance)


def recalcmean(cluster):

    meanvector = [0 for _ in range(len(cluster.instances[0].words))]

    for i in range(len(meanvector)):
        for inst in cluster.instances:
            words = inst.words
            meanvector[i] += words[i]

    for i in range(len(meanvector)):
        meanvector[i] = meanvector[i] / len(cluster.instances)

    new = instance('mean centroid ' + str(cluster.clustnum), meanvector,None)


    return new




#makes a folder to put cluster documents in
def makenewclusterfolder(seed, k,dirc,distfunc):

    path =dirc + '_seed_' +  str(seed) + "_k_" + str(k) + '_distance_' + str(distfunc)

    if os.path.isdir(path):
        print("Folder already exists!")
    else:
        os.makedirs(path)

    return path

# writes cluster documents
def writeclusterdoc(clusters,folderpath,dirc):

    for i in range (len(clusters)):
        clustnum = clusters[i].clustnum
        filename = str(folderpath) + '/clusternumber_' + str(clustnum) + ".txt"
        file = open(filename, 'w')
        file.write("cluster number: " + str(clustnum) + "\n\n\nFiles in cluster: \n\n\n")
        for instance in clusters[i].instances:
            file_to_write = dirc +'/'+ str(instance.name)
            towrite = open(file_to_write)
            string = towrite.read()
            file.write(string)
            file.write("\n\n\n\n")


# makes contin_table for Rand index: https://en.wikipedia.org/wiki/Rand_index
def contin_table (clusters,instances,subjects):

    # make dictonary for clusters given on website
    orig_clusters = {}
    for instance in instances:
        for subject in subjects:
            if subject == instance.subject:
                try:
                    orig_clusters[subject].append(instance)
                except KeyError:
                    orig_clusters[subject] =[instance]



    #making contin_table
    table = [[0 for _ in range(len(subjects)+1)]for _ in range(len(subjects)+1)]

    #comparing all clusters
    for i in range(len(clusters)):
        index_count = 0
        for subject, orgininsts in orig_clusters.items():
            makeinsts = clusters[i].instances
            intersect_count = 0

            #comparing all instances between the 2 clusters
            for orginst in orgininsts:
                for madeinst in makeinsts:
                    if orginst == madeinst:
                        intersect_count += 1

            table[index_count][i] = intersect_count
            index_count += 1


    for i in range(len(table)-1):
        a = 0
        b = 0
        for j in range(len(table)-1):
            a += table[i][j]
            b += table[j][i]

        table[i][len(table)-1] = a
        table[len(table)-1][i] = b

    return table


# computes ARI for this type of clustering
def ARI(table,n):

    index = 0
    sum_a = 0
    sum_b = 0
    for i in range(len(table)-1):
        for j in range(len(table)-1):
            sum_a += choose(table[i][len(table)-1],2)
            sum_b += choose(table[len(table)-1][j],2)
            index += choose(table[i][j],2)

    expected_index = (sum_a*sum_b)/(choose(n,2))
    max_index = (sum_a+sum_b)/2

    return (index - expected_index)/(max_index-expected_index)


#choose to compute rand
def choose(n,r):
    
    f = math.factorial
    if (n-r)>=0:
        return f(n) // f(r) // f(n-r)
    else:
        return 0



def main():

    #arguments
    direc = sys.argv[1]
    seed = int(sys.argv[2])
    k = int(sys.argv[3])
    distfunc = sys.argv[4]


    #getting data
    parse = parser()
    instances, subjects = parse.parse(direc)

    #the inital centroids
    centroids = randompick(instances,seed,k)


    #making cluster objects
    clusters = []
    count = 0
    for centroid in centroids:
        clusters.append(clust(count, centroid))
        count += 1


    #intial assigning instances
    for instance in instances:
        assigncluster(instance,clusters,distfunc)



    while clusters[0].iteration < 30:

        print(clusters[0].iteration)

        for cluster in clusters:
            if len(cluster.instances) != 0:
                newcent = recalcmean(cluster)
                cluster.newiteration(newcent)
            else:
                cluster.newiteration(cluster.centroid)

        for instance in instances:
            assigncluster(instance,clusters,distfunc)


    for cluster in clusters:
        print(cluster)



    path = makenewclusterfolder(seed, k, direc, distfunc)
    writeclusterdoc(clusters, path, direc)
    con_table = contin_table(clusters,instances,subjects)
    ari = ARI(con_table,len(instances))

    print("ARI: ",ari)



main()



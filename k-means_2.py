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
        string = string +"\ncluster number: "+str(self.clustnum)+'\niteration: '+str(self.iteration) + "\ncentroid: " + str(self.centroid) + "\ncontains:\n\n"
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


class clusts:

    def __init__(self,clusters):

        self.clusters = clusters


    def intra_cluster_variance(self):

        sum = 0
        for cluster in self.clusters:
            cenvec = cluster.centroid.words
            for inst in cluster.instances:
                vector = inst.words
                for i in range(len(vector)):
                    sum += ((vector[i] - cenvec[i]) * (vector[i] - cenvec[i]))

        self.intrasum = sum


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

    v1 = inst1.words
    v2 = inst2.words

    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return 1 - (sumxy/math.sqrt(sumxx*sumyy))


def assigncluster(instance,clusters,distfunc):

    flag = 0
    for cluster in clusters:
        if instance.name == cluster.centroid.name:
            flag += 1
            cluster.instances.append(instance)

    if flag == 0:
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

    new = instance('mean centroid ' + str(cluster.clustnum), meanvector,None,False)


    return new




#makes a folder to put cluster documents in
def makenewclusterfolder(seed, k,dirc,distfunc):

    path =dirc + '_seed_' +  str(seed) + "_k_" + str(k) + '_distance_' + str(distfunc)

    if os.path.isdir(path):
        print("Folder already exists!")
    else:
        os.makedirs(path)

    return path


def clust_overview(clusters,folderpath,direc, seed, k, distfunc,vectype, ari,subjects):

    dic = {}
    for cluster in clusters:
        dic[cluster] = []
        for inst in cluster.instances:
            dic[cluster].append([inst.name,inst.subject])


    filename = str(folderpath) + '/overview.txt'
    file = open(filename, 'w')
    file.write("Dataset:  " + str(direc) + '\n')
    file.write('seed: ' + str(seed) + '\n')
    if subjects != None and k != 'minvar':
        file.write('number of clusters: ' + str(len(subjects)) + '\n')
    if k == 'minvar':
        file.write('number of clusters: ' + str(len(clusters)) + '\n')
    else:
        file.write('number of clusters: ' + str(k) + '\n')
    file.write('distance function: ' + str(distfunc) + '\n')
    file.write('document vector type: ' + str(vectype) + '\n')
    file.write('ARI (if applicable):' + str(ari) + '\n\n\n')
    for cluster in clusters:
        pairs = dic[cluster]
        file.write('cluster number ' + str(cluster.clustnum) + ':\n')
        file.write('doc name\t\t\t\tlabel(if applicable)\n\n')
        for pair in pairs:
            file.write(str(pair[0]) +"\t\t\t" + str(pair[1]) + '\n')
        file.write('\n\n##########################################################\n')







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


    expected_index = (sum_a*sum_b)
    expected_index = expected_index/choose(n,2)
    max_index = (sum_a+sum_b)
    max_index = max_index/2

    print(index, max_index, expected_index)

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
    k = sys.argv[3]
    distfunc = sys.argv[4]
    vectype = sys.argv[5]


    #getting data
    parse = parser()
    instances, subjects = parse.parse(vectype,direc)

    if direc != "poemsgen" and direc!='smallpoems':
        subjects = None

    #the inital centroids
    if k == 'same':
        centroids = randompick(instances, seed, len(subjects))

        # making cluster objects
        clusters = []
        count = 0
        for centroid in centroids:
            clusters.append(clust(count, centroid))
            count += 1

        # intial assigning instances
        for instance in instances:
            assigncluster(instance, clusters, distfunc)

        for cluster in clusters:
            print(cluster)

        while clusters[0].iteration < 20:

            for cluster in clusters:
                newcent = recalcmean(cluster)
                cluster.newiteration(newcent)

            for instance in instances:
                assigncluster(instance, clusters, distfunc)

            for cluster in clusters:
                print(cluster)


        path = makenewclusterfolder(seed, k, direc, distfunc)

        if subjects != None and len(subjects) == len(clusters):
            con_table = contin_table(clusters, instances, subjects)
            ari = ARI(con_table, len(instances))
            print("ARI: ", ari)

        else:
            ari = None

        clust_overview(clusters, path, direc, seed, k, distfunc, vectype, ari, subjects)
        writeclusterdoc(clusters, path, direc)

    if k == 'minvar':

        cluster_k_pair = []

        for i in range (2,(len(instances)-1)//2):

            centroids = randompick(instances, seed, i)

            # making cluster objects
            clusters = []
            count = 0
            for centroid in centroids:
                clusters.append(clust(count, centroid))
                count += 1

            # intial assigning instances
            for instance in instances:
                assigncluster(instance, clusters, distfunc)

            for cluster in clusters:
                print(cluster)

            while clusters[0].iteration < 20:

                for cluster in clusters:
                    newcent = recalcmean(cluster)
                    cluster.newiteration(newcent)

                for instance in instances:
                    assigncluster(instance, clusters, distfunc)

            clustk = clusts(clusters)
            clustk.intra_cluster_variance()
            cluster_k_pair.append([clustk,clustk.intrasum])


        for i in range (1,len(cluster_k_pair)):
            difference = abs(cluster_k_pair[i-1][1] - cluster_k_pair[i][1])
            cluster_k_pair[i].append(difference)


        cluster_k_pair= cluster_k_pair[1:]
        for pair in cluster_k_pair:
            print(pair)
        right_clust = max(cluster_k_pair, key= lambda x: x[2])


        clusters = right_clust[0].clusters

        path = makenewclusterfolder(seed, k, direc, distfunc)

        if subjects != None and len(subjects) == len(clusters):
            con_table = contin_table(clusters, instances, subjects)
            ari = ARI(con_table, len(instances))
            print("ARI: ", ari)

        else:
            ari = None

        clust_overview(clusters, path, direc, seed, k, distfunc, vectype, ari, subjects)
        writeclusterdoc(clusters, path, direc)


    else:

        centroids = randompick(instances, seed, int(k))

        #making cluster objects
        clusters = []
        count = 0
        for centroid in centroids:
            clusters.append(clust(count, centroid))
            count += 1


        #intial assigning instances
        for instance in instances:
            assigncluster(instance,clusters,distfunc)

        for cluster in clusters:
            print(cluster)



        while clusters[0].iteration < 20:


            for cluster in clusters:
                newcent = recalcmean(cluster)
                cluster.newiteration(newcent)


            for instance in instances:
                assigncluster(instance,clusters,distfunc)


            for cluster in clusters:
                print(cluster)


        totclusters = clusts(clusters)
        totclusters.intra_cluster_variance()

        path = makenewclusterfolder(seed, k, direc, distfunc)

        if subjects != None and len(subjects) == len(clusters):
            con_table = contin_table(clusters,instances,subjects)
            ari = ARI(con_table,len(instances))
            print("ARI: ", ari)

        else:
            ari = None

        clust_overview(clusters, path, direc, seed, k, distfunc,vectype, ari,subjects)
        writeclusterdoc(clusters, path, direc)



main()



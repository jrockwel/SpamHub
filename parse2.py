import os
import StemmingUtil
import string
import math
import gensim.models.doc2vec


class instance:

    def __init__(self,name,list,subject):

        self.name = name
        self.words = list
        self.subject = subject


    def __str__(self):

        return "filename: " +  self.name + "\n" + "words dictionary: " + str(self.words) + "\n\n"

    def __eq__(self, other):

        return self.name == other.name

    def __ne__(self, other):

        if self.name != other.name:

            return True

        return False

class parser:

    def __init__(self):

        pass


    def parse(self,direc):

        # gets list of file names
        files = os.listdir(direc)

        # MY computer is fucked so I had to do this
        if ".DS_Store" in files:
            files.remove(".DS_Store")

        translator = str.maketrans("", "", string.punctuation)
        stopwords = open("stopwords.txt")
        stopwords = stopwords.read().splitlines()

        totalwords = []
        totalfiles = []
        subjects = []
        total = len(files)
        count1 = 0
        for filename in files:

            count1 = count1 + 1
            file = open(direc + '/' + filename)
            dirttext = file.read().split()
            subject = dirttext[0]
            subjects.append(subject)
            dirttext = dirttext[3:len(dirttext)-1]
            # clean that &*%$#@!
            for i in range(len(dirttext)):
                dirttext[i] = dirttext[i].lower()
                dirttext[i] = dirttext[i].translate(translator)
            #rinsed = dirttext
                # goodbye stopwords
            for stopword in stopwords:
                if stopword in dirttext:
                    dirttext.remove(stopword)
            rinsed = dirttext

            # using adams stemming thing
            done = StemmingUtil.createStems(rinsed)
            done = (filename,done,subject)

            totalfiles.append(done)

            for word in done[1]:
                totalwords.append(word)

            print(count1/total)

        totalwords = list(set(totalwords))
        subjects = list(set(subjects))

        instances = self.all_tfidf(totalfiles,totalwords)


        return instances, subjects



    def all_tfidf(self,totalfiles,totalwords):

        instances=[]
        total = len(totalfiles)
        count = 0
        for instance in totalfiles:
            count += 1
            newinst = self.tfidf_vector(totalfiles,instance,totalwords)

            print(count/total)
            instances.append(newinst)


        return instances


    def tfidf_vector(self, totalfiles, inst, allwords):

        vector = []

        for word in allwords:
            score = self.tfidf_score(word, inst[1], totalfiles)
            vector.append(score)

        newinst = instance(inst[0], vector,inst[2])

        return newinst

    def tfidf_score(self, term, words, totalfiles):

        tf = self.tf_calc(term, words)
        idf = self.idf_calc(term, totalfiles)

        return tf * idf

    def tf_calc(self, term, words):

        count = 0
        for word in words:
            if word == term:
                count += 1
        return count

    def idf_calc(self, term, totalfiles):

        N = len(totalfiles)
        d = 0

        for instance in totalfiles:
            if term in instance[1]:
                d += 1

        return math.log(N / d)





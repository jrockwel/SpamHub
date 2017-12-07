import os
import StemmingUtil
import string
import math
import gensim


class instance:

    def __init__(self,name,list,subject, isdata):

        self.name = name
        self.words = list
        self.subject = subject
        self.isdata = isdata


    def __str__(self):

        string = "filename: " +  self.name + "\n" + "words dictionary: " + str(self.words) + "\n"


        if self.subject != None:

            string = string + 'subject: ' + str(self.subject)

        return string

    def __eq__(self, other):

        return self.name == other.name

    def __ne__(self, other):

        if self.name != other.name:

            return True

        return False

class parser:

    def __init__(self):

        pass


    def parse(self,type,direc):

        if type == "tfidf":

            instances, subjects = self.parse_tfidf(direc)

        if type == "doc2vec":

            instances, subjects = self.parse_doc2vec(direc)

        return instances, subjects

    def parse_doc2vec(self,direc):

        # gets list of file names
        files = os.listdir(direc)

        # MY computer is fucked so I had to do this
        if ".DS_Store" in files:
            files.remove(".DS_Store")
        translator = str.maketrans("", "", string.punctuation)


        if direc == "smallpoems" or direc == "poemsgen":


            tovecpoems=[]
            sub_title_pair = {}
            subjects = []
            for filename in files:

                file = open(direc + "/" + filename)
                list1 = file.read().split(sep= "\n")
                subject = list1[0].split(" ",1)[0]

                poem = list1[3:]
                poem = ''.join(poem)
                poem = poem.split()
                list(filter(lambda a: a != '', poem))
                for i in range (len(poem)):
                    poem[i] = poem[i].lower()
                    poem[i] = poem[i].replace('\t','').replace('\n','')
                    poem[i] = poem[i].translate(translator)


                tovecpoem = gensim.models.doc2vec.LabeledSentence(words = poem, tags = [filename])
                tovecpoems.append(tovecpoem)
                sub_title_pair[filename] = subject
                subjects.append(subject)

            learner = gensim.models.doc2vec.Doc2Vec(tovecpoems, size=3, iter=100)
            vectors = learner.docvecs

            instances = []

            for i in range(len(vectors)):
                title = vectors.index_to_doctag(i)
                inst = instance(title, vectors[i], sub_title_pair[title], True)

                instances.append(inst)

            subjects = list(set(subjects))
            return instances, subjects

        else:
            tovecpoems = []
            for filename in files:
                file = open(direc + "/" + filename)
                text = file.read().split()
                tovec = gensim.models.doc2vec.LabeledSentence(words = text, tags = [filename])
                tovecpoems.append(tovec)


            learner = gensim.models.doc2vec.Doc2Vec(tovecpoems,size=3, iter=1000)
            vectors = learner.docvecs

            instances = []

            for i in range(len(vectors)):
                title = vectors.index_to_doctag(i)
                inst = instance(title,vectors[i],None,True)

                instances.append(inst)

            return instances, None



    def parse_tfidf(self,direc):

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
            if direc == "smallpoems" or direc == "poemsgen":
                subject = dirttext[0]
                subjects.append(subject)
                dirttext = dirttext[3:len(dirttext)-1]
            # clean that &*%$#@!
            for i in range(len(dirttext)):
                dirttext[i] = dirttext[i].lower()
                dirttext[i] = dirttext[i].translate(translator)


                # goodbye stopwords
            for stopword in stopwords:
                if stopword in dirttext:
                    dirttext.remove(stopword)
            rinsed = dirttext

            # using adams stemming thing
            done = StemmingUtil.createStems(rinsed)
            if direc == "smallpoems" or direc == "poemsgen":
                done = (filename,done,subject)
            else:
                done = (filename, done, None)
            totalfiles.append(done)

            for word in done[1]:
                totalwords.append(word)

            print(count1/total)


        totalwords = list(set(totalwords))
        subjects = list(set(subjects))


        instances = self.all_tfidf(totalfiles,totalwords)

        if direc == "smallpoems" or direc == "poemsgen":

            return instances, subjects
        else:
            return instances, None



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

        newinst = instance(inst[0], vector,inst[2],True)

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





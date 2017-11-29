import os
import StemmingUtil
import string
import math

###My Idea and the way it seems to work online is to have each instance be a vector of the total number of words seen in all instances, with number of times
###that word appears as the value of that words index. But there are way to many emails for this and a vector is gunna by way to big. Can we using dictonaries
### as instances with keys as words, and values as wordcounts? Then when we do k-means if a word isn't in the dictonary with give a a really big distance in
###that dimension.


#....yea i tried the first way first and it took for evvvverrr...the second is way faster

class instance:

    def __init__(self,name,dict,iscent):

        self.name = name
        self.words = dict
        self.iscent = iscent

    def __str__(self):

        return "filename: " +  self.name + "\n" + "words dictionary: " + str(self.words) + "\n\n"


class parse:

    def __init__(self):

        pass



    def read(self,format):
        #makes each instance a dictonary as explained above
        # cleans emails of punctuation and uses same NLP module we used in hw 5 we gunna have to figure out later how to convert them back, or we could just keep
        # the filename with the instance to know which one it actually is in the end (ill do that for now)



        # gets list of file names
        files = os.listdir("fake_data")

        # MY computer is fucked so I had to do this
        if ".DS_Store" in files:
            files.remove(".DS_Store")

        totalnum = len(files)

        translator = str.maketrans("", "", string.punctuation)
        stopwords = open("stopwords.txt")
        stopwords = stopwords.read().splitlines()
        # will later turn this into total words

        #
        totalfiles = []
        count1 = 0
        for filename in files:

            count1 = count1 + 1
            file = open('fake_data/' + filename)
            # print(filename)
            dirttext = file.read().split()
            rinsed = []

            # clean that &*%$#@!
            for i in range(len(dirttext)):
                dirttext[i] = dirttext[i].lower()
                dirttext[i] = dirttext[i].translate(translator)

                # goodbye stopwords
                for j in range(len(stopwords)):
                    flag = 0
                    if stopwords[j] == dirttext[i]:
                        flag = 1
                if flag == 0:
                    rinsed.append(dirttext[i])

            # using adams stemming thing
            done = StemmingUtil.createStems(rinsed)
            #jaccard format

            instance = self.jacformat(done,filename)
            totalfiles.append(instance)

            percent = count1/totalnum
            print(percent)



        return totalfiles

            ###There are a lot of emails that are either in their entirety or partly just a long string of captial letters and numbers and crap
            ###These should probably all go into the same key value pair because they are don't actually mean anything to us, and are a distict type of thing
            ### in themselves so I try to weed them out first just by saying if any word is longer than 25 charcters throw it all in the same thing

    #for jaccard distance k-means we use a dictonary
    def jacformat(self,done,filename):
            #making the actual instance now
            dic = {}

            # checking for crazy ones
            getrideof=[]
            for word in done:
                dic["large-stuff"] = 0
                if len(word) > 20:
                    dic["large-stuff"] += 1
                    getrideof.append(word)

            ####################################

            # throwing out all the long stuff
            new = []
            for word in done:
                if word not in getrideof:
                    new.append(word)

            # looking at each word that isn't crazy
            if len(new) != 0:
                for word in new:
                    # add it if its not in dictonary
                    if word not in dic.keys():
                        count = 0
                        # finding how many times its repeated and setting that as the value
                        for i in range(len(new)):
                            if word == new[i]:
                                count += 1
                        dic[word] = count

            #instance is tuple of filname and dictionary
            return instance(filename, dic,False)


    # can create vectors using tf-idf(but we gotta go back to those big old sparse vectors...), then us k-means on these vectors with cosine distance too...
    # maybe this will get better results
    # https://en.wikipedia.org/wiki/Tf%E2%80%93idf

    def all_tfidf(self,totalfiles):

        vectors=[]
        allwords = self.getallwords(totalfiles)

        for instance in totalfiles:

            newinst = self.tfidf_vector(totalfiles,instance,allwords)
            vectors.append(newinst)
            print(newinst)


        return vectors

    def getallwords(self,totalfiles):

        allwords=[]

        for instance in totalfiles:
            keys = instance.words.keys()
            for word in keys:
                allwords.append(word)

        allwords = list(set(allwords))

        return allwords


    def tfidf_vector(self,totalfiles,inst,allwords):

        vector = []

        for word in allwords:
            score = self.tfidf_score(word,inst.words,totalfiles)
            vector.append(score)

        newinst = instance(inst.name,vector,False)

        return newinst


    def tfidf_score(self,term,words,totalfiles):

        tf = self.tf_calc(term,words)
        idf = self.idf_calc(term,totalfiles)

        return tf*idf


    def tf_calc(self,term,words):


        try:
            return words[term]

        except KeyError:
            return 0

    def idf_calc(self,term,totalfiles):

        N = len(totalfiles)
        d = 0

        for instance in totalfiles:
            if term in instance.words.keys():
                d += 1

        return math.log(N/d)


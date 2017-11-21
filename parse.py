import os
import StemmingUtil
import string

###My Idea and the way it seems to work online is to have each instance be a vector of the total number of words seen in all instances, with number of times
###that word appears as the value of that words index. But there are way to many emails for this and a vector is gunna by way to big. Can we using dictonaries
### as instances with keys as words, and values as wordcounts? Then when we do k-means if a word isn't in the dictonary with give a a really big distance in
###that dimension.


#....yea i tried the first way first and it took for evvvverrr...the second is way faster




class data:

    def __init__(self):

        pass



    def read(self):
        # makes a huge list of all of the words
        # takes every email and makes it into a list of words
        # cleans emails of punctuation and uses same NLP module we used in hw 5 we gunna have to figure out later how to convert them back, or we could just keep
        # keep the filename with the instance to know which one it actually is in the end (ill do that for now)



        # gets list of file names
        files = os.listdir("emails")

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
            file = open('emails/' + filename)
            # print(filename)
            dirttext = file.read().split()
            rinsed = []

            # clean that shit!
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
            #making the actual instance now
            dic = {}
            # looking at each word
            for word in done:
                # add it if its not in dictonary
                if word not in dic.keys():
                    count = 0
                    # finding how many times its repeated and setting that as the value
                    for i in range(len(done)):
                        if word == done[i]:
                            count += 1
                    dic[word] = count

            #instance is tuple of filname and dictionary
            inst = (filename,dic)
            totalfiles.append(inst)


            # dammmnnnn there are a lot of fuckin emails
            per = count1 / totalnum
            print(per)




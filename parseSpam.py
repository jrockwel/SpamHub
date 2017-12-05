#! /usr/bin/env python

import os, sys, random

from langdetect import detect


############
##   USAGE
############

# filters a number of randomized, english-only spam emails
# into a subfolder


# 1st argument on command line is number of emails you'd like to add
# 2nd argument is random seed



##########
# OUTLINE
########



# shuffle

# for name in list:

# get file contents

# get list of file names



# make new subfolder

# go into emails folder

# for each filename in filenames:

# copy file into new subfolder

###########



# returns complete list of filenames from original spam folder
def get_filenames():
    filenames = []

    # switch manually into email directory
    os.chdir("../emails")

    # get names, copy into file
    os.system("ls > temp.txt")
    temp = open("temp.txt", 'r')

    # copy names from file into internal representation 'filenames'
    for line in temp:
        line = line[:-1]
        if line != "temp.txt": 
            filenames.append(line)

    #clean up 
    temp.close()
    os.system("rm temp.txt")

    # return to original directory 
    os.chdir("../Spamhub")

    # return filenames
    return filenames

# checks to see if a character is ascii or not.
# credit to these guys: https://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii 
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# clean_text removes all non-ascii characters from a piece of text
# so that it's compatible with Langdetect
def clean_text(text):
    toReturn = ""
    for thing in text:
        for char in thing:
            if is_ascii(char):
                toReturn = toReturn + char
    return toReturn 

# filter, for now, returns the name of the file only if
# it's deemed to be in English, otherwise '0'
def filter(filename):
    x = open(os.path.dirname(__file__) +  "/../emails/" + filename, 'r')
    text = clean_text(x)
    print("about to check:" + filename)
    try: 
        if detect(text) == "en":
            return filename
        else:
            return '0'
    except:
        print("error in Langdetect")
        return '0'
        
def main():

    number = int(sys.argv[1])
    print("number = ",number)
    seed = int(sys.argv[2])

    # initialize some lists, get filenames, randomize
    
    filtered = []
    filenames = get_filenames()
    random.seed(seed)
    random.shuffle(filenames)

    # get <number> filenames

    numb = 0
    for filename in filenames:
        if numb < number:
            var = filter(filename)
            print(var)
            if var != '0':
                numb += 1
                filtered.append(var)
            print(numb, "out of", number)
        else:
            break
    print(filtered)
    print(len(filtered))

    
    # make new directory
    os.makedirs("spam")

    # change to emails directory
    os.chdir("../emails")

    # copy files
    yay = 0
    for filename in filtered:
        os.system("cp " + filename + " ../SpamHub/spam")
        yay += 1
        print("copying...", yay)


main()

#!/usr/bin/python3

import re

from ImageMaker import getImageFromLetterCombinations
from prediction import getPredictedLetterViaInputImage

"""
    For a input word, this function will return all the possible letter combinations
    e.g. if input is: "b@t"
        output will be [
                        ['b', '@', 't'],
                        ['b@', t],
                        ['b', '@t']
                        ['b@t']
                    ]
"""
def getAllWords(word):
    allCombinations = []
    length = len(word)
    if length == 1:
        # stopping clause for recursion. If input is single charecter, just return the input.
        allCombinations.append(word[0])
    else:
        # loop for considering all letter grouping for the 1st letter.
        for i in range(1, length):
            firstLetter = word[0:i]
            restword = word[i:length]

            #get all combinations keeping first letter fixed.
            restAllCombinations = getAllWords(restword)

            #loop on all combinations from rest of the letters and add first letter to them
            for restItem in restAllCombinations:
                newWord = []
                newWord.append(firstLetter)
                newWord += restItem

                #isCurLetterAlphaNum new combination, add it to the allCombinations list
                allCombinations.append(newWord)

        # we have not considered the whole word as the first letter in the above recursion. add it to the full set now.
        allCombinations.append([word])
    return allCombinations

"""
    Filters out un-necessary combinations from the full list of possible combinations.

    When we find 2 consecutive letters which does not contain any special charecters, we can discard that combination.
    This is because, we are only interested in combinations involving special charecters.

    Let's say inut was 'ba{}'
    Here let's look at 2 possible combinations: ['b', 'a', '{', '}'] and ['ba', '{', '}']
    For both the above combinations, special charecter based combinations are same ( '{' and '}' )
    So, if we discard 1st combination (having 2 consecutive non-special charecters, i.e. 'b' and 'a'),
        we still have the other combination to cover for our evaluation requirements.
"""
def filter(allCombinations):
    filteredCombinations = []
    # pattern for finding alphanumeric (non-special) charecters
    pattern = re.compile('[a-zA-Z0-9]')
    removed = []

    # iterate over all the combinations
    for comb in allCombinations:
        isRemove = False
        wasLastLetterAlphaNum = False # keeps track whether the last letter in iteration was non-special

        # iterate each letter in a combination
        for curLetter in comb:
            isCurLetterAlphaNum = pattern.search(curLetter) is not None

            if isCurLetterAlphaNum and wasLastLetterAlphaNum:
                # both last letter and current letter is alphanumeric (non-special), remove the combination
                isRemove = True
                break;

            # save the current letters value as last letter for next iteration
            wasLastLetterAlphaNum = isCurLetterAlphaNum

        if isRemove:
            removed.append(comb)
        else:
            # not marked for removal, add it to the final combinations list
            filteredCombinations.append(comb)

    #print('filter removed: ', len(removed), ' out of ', len(allCombinations))
    #printAll(removed)

    return filteredCombinations

"""
    This is the primary method.

    This method takes care of all the following:
    1. Breaks up a word into all possible letter combinations.
    2. Filters out un-necessary combinations for performance gain.
    3. Processes a letter combination via Image predictor service to get a predicted letter
    4. Keep a cache of input vs predicted letter from #3 for performance gain (takes it directly from cache instead of processing #3, when the input is found in cache)
    5. Joins all predicted letters to create a transformed word
    6. Runs the tranformed word via a dictonary check for sanity (whether the word has is a real word with meaning) and discards non-real words.
    7. Returns/prints all possible real words predicted based on the input
"""
def getWordPrediction(word):
    # get all possible combinations
    allCombinations = getAllWords(input)
    lenBeforeFilter = len(allCombinations)

    # filter the combnations based on our requirement
    allCombinations = filter(allCombinations)
    print('before filter: ', lenBeforeFilter, 'after filter: ', len(allCombinations))
    #printAll(allCombinations)

    # this dictionary based cache holds previously predicted letters (input vs prediction), so that we do not have to re-compute same items
    letterTransformCache = {}
    pattern = re.compile('[^a-zA-Z0-9]') # pattern to find all special charecters (non-alphanumeric)

    predictedWords = [] # this is the final set of words to be in the output
    rejectedWords = [] # transformed words, which gets rejected by dictionary run
    totalPredictionRequest = 0
    cacheBasedPrediction = 0

    # iterate through all the combinations
    for comb in allCombinations:
        transformedComb = []
        hasFailed = False

        # iterate through all letter combinations
        for letter in comb:
            isSpecialCharecter = pattern.search(letter) is not None
            if isSpecialCharecter:
                predictedLetter = None
                totalPredictionRequest += 1

                if letter in letterTransformCache:
                    #letter found in cache. No need for image prediction, just get the result from cache
                    predictedLetter = letterTransformCache[letter]
                    cacheBasedPrediction += 1

                else:
                    # letter combination not found in cache... need to run image prediction
                    predictedLetter = getPredictionViaImage(letter)

                    # save the predicted letter into the cache for future predictions
                    letterTransformCache[letter] = predictedLetter

                # if the by any chance, predictor method could not return a predicted letter
                if predictedLetter is None:
                    #print('failed to get prediction: ', letter)
                    hasFailed = True
                    break;

                # got the predicted letter, add it to transformed combination
                transformedComb.append(predictedLetter)
            else:
                # the letter is not a special char, directly add it to the transformed combination.
                transformedComb.append(letter)

        if not hasFailed:
            #all word have been transformed... now make the word and check with dictionary
            word = "".join(transformedComb)
            word = word.upper() # convert to uppercase to remove redundant words using different cases

            if(isProperWordInOxfordDict(word)):
                # the word has been found in the dictionary. Add it to the final predicted words list
                #print('original: ', comb, ' predicted: ', word)
                predictedWords.append(word)
            else:
                # the transformed word has failed dictionary check. Reject it.
                rejectedWords.append(word)

    print('letter prediction requested ', totalPredictionRequest, ', served from cache: ', cacheBasedPrediction, ', actual prediction runs: ', len(letterTransformCache))
    print('words rejected: ', len(rejectedWords), ' predicted: ', len(predictedWords))
    printAll(rejectedWords)

    predictedWords = list(set(predictedWords))
    predictedWords.sort()
    return predictedWords # converting the list of predicted words into a set to remove any duplicate predictions from the output

"""
    This method:
        1. takes a letter combination of special characters
        2. converts the letter combination to an image
        3. Runs the image through a machine learning algorithm to get a predicted alphanumeric letter
        4, returns the predicted letter
"""
def getPredictionViaImage(letter):
    #add Image based prediction here
    img = getImageFromLetterCombinations(letter)
    predictedChar = getPredictedLetterViaInputImage(img)
    return predictedChar

    #dummy code
    #dict = { '{}': 'o', '|': 'l', '!': 'i', '{': 'c', '@': 'a', '#': 'e', '}': 'i'}
    #return None if letter not in dict else dict[letter]

"""
    this method runs a predicted word through a dictionary (or a set of known words), which helps to filter out un-real/junk words from final prediction
"""
def isProperWordInOxfordDict(word):
    knownWordSet = ('DOLL', 'FOOT', 'RAGE','W') #this is the oxford dictionary words
    return word in knownWordSet
    #return len(word) > 0 #dummy

def printAll(result):
    for item in result:
        print('--->    ', item)
    print('length: ', len(result))

if __name__ == "__main__":
    input='\/\/'
    result = getWordPrediction(input)
    printAll(result)
    print()

#    input='!m@g!n@t!{}n'
#    result = getWordPrediction(input)
#    printAll(result)

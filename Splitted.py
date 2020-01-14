#!/usr/bin/python3

import re

def getAllWords(letters):
    allCombinations = []
    length = len(letters)
    if length == 1:
        allCombinations.append(letters[0])
    else:
        for i in range(1, length):
            curLetters = letters[0:i]
            restLetters = letters[i:length] #recurssion

            restallCombinations = getAllWords(restLetters)
            for restItem in restallCombinations:
                newWord = []
                newWord.append(curLetters)
                newWord += restItem
                allCombinations.append(newWord)
        allCombinations.append([letters])
    return allCombinations

def filter(allCombinations):
    retVal = []
    pattern = re.compile('\W')
    removed = []

    for comb in allCombinations:
        isRemove = False
        lastFound = False
        #isLastLenGT1 = False

        for letter in comb:
            #isLenGT1 = len(letter) > 1
            found = pattern.search(letter) is None

            if found and lastFound:#and (isLenGT1 != isLastLenGT1 or (isLenGT1 and isLastLenGT1)):
                isRemove = True
                break;

            lastFound = found
            #isLastLenGT1 = isLenGT1

        if isRemove:
            removed.append(comb)
        else:
            retVal.append(comb)
    #print('removed: ', len(removed), ' len: ', len(allCombinations))
    #for item in removed:
    #    print(item)

    return retVal

def getWordPrediction(word):
    allCombinations = getAllWords(input)
    lenBeforeFilter = len(allCombinations)

    allCombinations = filter(allCombinations)
    for s in allCombinations:
        print(s)
    print('before filter: ', lenBeforeFilter, 'after filter: ', len(allCombinations))
    #printAll(allCombinations)

    letterTransformCache = {} # this holds previously found letters, so that we do not re-compute same items
    pattern = re.compile('\W')

    predictedWords = []
    rejectedWords = []
    totalPredictionRequest = 0
    cacheBasedPrediction = 0

    for comb in allCombinations:
        transformedComb = []
        hasFailed = False


        for letter in comb:
            if pattern.search(letter) is not None:
                predictedLetter = None
                totalPredictionRequest += 1

                if letter in letterTransformCache:
                    #found in cache, no need for image prediction
                    predictedLetter = letterTransformCache[letter]
                    cacheBasedPrediction += 1

                else:
                    #not found in cache... need to run image prediction
                    predictedLetter = getPredictionViaImage(letter)
                    letterTransformCache[letter] = predictedLetter

                if predictedLetter is None:
                    #print('failed to get prediction: ', letter)
                    hasFailed = True
                    break;

                transformedComb.append(predictedLetter)
            else:
                transformedComb.append(letter)

        if not hasFailed:
            #all letters have been transformed... now make the word and check with dictionary
            word = "".join(transformedComb)

            if(isProperWordInOxfordDict(word)):
                #print('original: ', comb, ' predicted: ', word)
                predictedWords.append(word)
            else:
                rejectedWords.append(word)

    print('letter prediction cache: ', cacheBasedPrediction, ' out of: ', totalPredictionRequest, ' cacheSize: ', len(letterTransformCache))
    print('words rejected: ', len(rejectedWords), ' predicted: ', len(predictedWords))
    #printAll(rejectedWords)

    return set(predictedWords)


def getPredictionViaImage(letter):
    #add Image based prediction here
    
    #dummy code
    dict = { '{}': 'o', '!': 'i', '{': 'c', '@': 'a', '#': 'e', '|_': 'l', '}': 'j'}
    return None if letter not in dict else dict[letter]

def isProperWordInOxfordDict(word):
    knownWordSet = set() #this is the oxford dictionary words
    #return knownWordSet.contains(word)
    return len(word)  #dummy

def printAll(result):
    for item in result:
        print(item)
    print('length: ', len(result))

if __name__ == "__main__":
    input='f{}{}tb@ll'
    result = getWordPrediction(input)
    printAll(result)
    print()

    #input='!m@g!n@t!{}n'
    #result = getWordPrediction(input)
    #printAll(result)

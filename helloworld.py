def convert_to_dictionary(theList):
    newDict = {}
    for i in theList:
        #split into list
        x = i.split(",")
        createList = [x[1], x[2], x[3]]
        newDict.update({x[0]: createList})
    #return value
    return newDict
listOfStrings = ["132,George,Engineering,Admitted", "265,Marie,Science,Admitted", "543,Christina,Engineering,Not Admitted", "311,Dennis,Pharmacy,Admitted", "323,Jerry,Science,Not Admitted"]
print(convert_to_dictionary(listOfStrings))
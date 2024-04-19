def getDifference(text1, text2):
    listText1 = text1.split()
    listText2 = text2.split()

    return " ".join(listText2[len(listText1) :])

def toStr(listin: list):
    tStr = ""
    for one in listin:
        tStr += str(one) + ', '
    tStr = tStr[:-2]
    return tStr

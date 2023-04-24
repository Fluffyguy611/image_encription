def splitLine(line, n):
    while len(line[n:n+12]) < 12:
        line += "0"
    tempL = line[n:n + 6]
    tempR = line[n + 6:n + 12:]
    return tempL, tempR


def readimage():
    with open('img2.pbm', "rb") as image:
        imageBytesArray = []
        lines = image.readlines()

        imageBytes = lines[3:]
        for line in imageBytes:
            line = str(line)
            line = line[2:-1]
            line = line.split('\\n')[0]
            imageBytesArray.append(line)
    return {'img': imageBytesArray, 'header': lines[:3]}


def showImage(header, array):
    f = open('cipherimg.pbm', 'wb')
    for line in header:
        f.write(line)
    for row in array:
        newLine = (''.join([str(byte) for byte in row[:-2]]) + '\n').encode()
        f.write(newLine)
    f.close()


def IVboxIT(lftmsg, rgtmsg):
    leftIVbox = IVbox[:6]
    rightIVbox = IVbox[6:]

    tempL = xorStrings(lftmsg, leftIVbox)
    tempR = xorStrings(rgtmsg, rightIVbox)

    return tempL, tempR


def xorStrings(str1, str2):
    return "".join([str(ord(a) ^ ord(b)) for a, b in zip(str1, str2)])


def cipherLoop(number_of_rounds):
    for i in range(1, number_of_rounds):
        MiniDES(Llist, Rlist, i)
        #MiniDESreversed(Llist, Rlist, i)


def MiniDES(Llist, Rlist, i):
    L = Llist[i-1]
    R = Rlist[i-1]

    keyOfR = [R[int(char)] for char in permutation]
    keyOfR = ''.join(keyOfR)
    temp_key = list(key[0:i])

    temp_key.insert(0, key[i:])
    i_key = ''.join(temp_key)

    xoredKey = xorStrings(keyOfR, i_key)

    lValue = int(xoredKey[:4], 2)
    rValue = int(xoredKey[4:], 2)

    tempF1 = s_box1[lValue]
    tempF2 = s_box2[rValue]

    connectedF = tempF1 + tempF2

    funct = xorStrings(L, connectedF)

    Rlist[i] = funct
    Llist[i] = Rlist[i-1]
    Llist[i+1] = funct


if __name__ == '__main__':
    image = readimage()
    message = image['img']
    key = "01011010"
    permutation = "04323541"
    IVbox = '111011010010'

    s_box1 = "101 010 001 110 011 100 111 000 001 100 110 010 000 111 101 011".split(" ")
    s_box2 = "100 000 110 101 111 001 011 010 101 011 000 111 110 010 001 100".split(" ")

    number_of_rounds = 8

    result = []

    for line in message:
        one_line = ''
        for n in range(0, len(line) - 1, 12):
            tempL, tempR = splitLine(line, n)
            # Uncomment next line to make it CBC
            #tempL, tempR = IVboxIT(tempL, tempR)
            Llist = [0 for i in range(number_of_rounds + 1)]
            Rlist = [0 for i in range(number_of_rounds + 1)]
            Llist[0] = tempL
            Rlist[0] = tempR
            cipherLoop(number_of_rounds)
            outputLine = Llist[-1] + Rlist[-3]
            IVbox = Llist[-1] + Rlist[-3]
            one_line += outputLine
        result.append(one_line)

    showImage(image['header'], result)

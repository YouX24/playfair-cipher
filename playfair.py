# Yousae Xiong
# CS 276-001

# creates matrix with key
def createEncryptionMatrix(k):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    matrix = []
    innerArray = []

    for c in k:
        if (c == 'i' or c == 'j') and alphabet[ord(c) - ord('a')] != "":
            alphabet[ord('i') - ord('a')] = ''
            alphabet[ord('j') - ord('a')] = ''
            innerArray.append(c)
        elif alphabet[ord(c) - ord('a')] != '':
            alphabet[ord(c) - ord('a')] = ''
            innerArray.append(c)
        if len(innerArray) == 5:
            matrix.append(innerArray)
            innerArray = []

    for c in alphabet:
        if c == 'i' or c == 'j':
            innerArray.append(c)
            alphabet[ord('i') - ord('a')] = ''
            alphabet[ord('j') - ord('a')] = ''
        elif c != '':
            innerArray.append(c)
            alphabet[ord(c) - ord('a')] = ''
        if len(innerArray) == 5:
            matrix.append(innerArray)
            innerArray = []

    return matrix


# prepare plaintext before it can be used in encryption
def prepare(pt):
    alphabetSet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
    prepared = []
    i = 0
    numOfDummy = 0
    prev = ""
    lettersOnly = []
    for c in pt.lower():
        if c in alphabetSet:
            lettersOnly.append(c)

    lettersPT = "".join(lettersOnly)

    while i < len(lettersPT):
        if lettersPT[i] == prev:
            prepared.append('x')
            numOfDummy += 1
            prev = ""
        else:
            prepared.append(lettersPT[i])
            if (i + 1 + numOfDummy) % 2 == 0:
                prev = ""
            else:
                prev = lettersPT[i]
            i += 1

    if len(prepared) % 2 != 0:
        prepared.append('x')

    return "".join(prepared)


# remove special characters, spaces, etc
def prepareKey(k):
    alphabetSet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
    lettersOnly = []
    for c in k.lower():
        if c in alphabetSet:
            lettersOnly.append(c)
    return "".join(lettersOnly)


def createLetterMap(matrix):
    letterMap = {}
    # map letter to its position in the table [row, col]
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            letter = matrix[row][col]
            letterMap[letter] = [row, col]
    return letterMap


def shiftRight(r, c, matrix):
    if c == 4:
        return matrix[r][0]
    else:
        return matrix[r][c + 1]


def shiftLeft(r, c, matrix):
    if c == 0:
        return matrix[r][4]
    else:
        return matrix[r][c - 1]


def shiftDown(r, c, matrix):
    if r == 4:
        return matrix[0][c]
    else:
        return matrix[r+1][c]


def shiftUp(r, c, matrix):
    if r == 0:
        return matrix[4][c]
    else:
        return matrix[r-1][c]


def swap(r, c, matrix):
    return matrix[r][c]


def encrypt(pt, matrix, lmap):
    result = []

    i = 0
    while i < len(pt):
        c1 = pt[i]
        c2 = pt[i+1]
        c1Row = lmap[c1][0]
        c1Col = lmap[c1][1]
        c2Row = lmap[c2][0]
        c2Col = lmap[c2][1]

        if c1Row == c2Row:
            result.append(shiftRight(c1Row, c1Col, matrix))
            result.append(shiftRight(c2Row, c2Col, matrix))
        elif c1Col == c2Col:
            result.append(shiftDown(c1Row, c1Col, matrix))
            result.append(shiftDown(c2Row, c2Col, matrix))
        else:
            result.append(swap(c1Row, c2Col, matrix))
            result.append(swap(c2Row, c1Col, matrix))

        i += 2

    return "".join(result)


def decrypt(ct, matrix, lmap):
    result = []
    i = 0
    while i < len(ct):
        c1 = ct[i]
        c2 = ct[i + 1]
        c1Row = lmap[c1][0]
        c1Col = lmap[c1][1]
        c2Row = lmap[c2][0]
        c2Col = lmap[c2][1]

        if c1Row == c2Row:
            result.append(shiftLeft(c1Row, c1Col, matrix))
            result.append(shiftLeft(c2Row, c2Col, matrix))
        elif c1Col == c2Col:
            result.append(shiftUp(c1Row, c1Col, matrix))
            result.append(shiftUp(c2Row, c2Col, matrix))
        else:
            result.append(swap(c1Row, c2Col, matrix))
            result.append(swap(c2Row, c1Col, matrix))

        i += 2

    return "".join(result)


def encryptOnly():
    key = input("Enter a key: ")
    message = input("Enter your message / plaintext: ")
    preparedKey = prepareKey(key)
    encryptionMatrix = createEncryptionMatrix(preparedKey)
    letterCoordinates = createLetterMap(encryptionMatrix)
    preparedPT = prepare(message)
    encryptMessage = encrypt(preparedPT, encryptionMatrix, letterCoordinates)
    print("Encrypted Message:", encryptMessage)


def decryptOnly():
    key = input("Enter the key used: ")
    encryptedMessage = input("Enter the ciphertext: ")
    preparedKey = prepareKey(key)
    encryptionMatrix = createEncryptionMatrix(preparedKey)
    letterCoordinates = createLetterMap(encryptionMatrix)
    decryptedMessage = decrypt(encryptedMessage.lower(), encryptionMatrix, letterCoordinates)
    print("Decrypted Message:", decryptedMessage)


def encryptAndDecrypt():
    key = input("Enter a key: ")
    message = input("Enter your message / plaintext: ")
    preparedKey = prepareKey(key)
    encryptionMatrix = createEncryptionMatrix(preparedKey)
    letterCoordinates = createLetterMap(encryptionMatrix)
    preparedPT = prepare(message)
    encryptMessage = encrypt(preparedPT, encryptionMatrix, letterCoordinates)
    decryptedMessage = decrypt(encryptMessage, encryptionMatrix, letterCoordinates)
    print("Encrypted Message:", encryptMessage)
    print("Decrypted Message:", decryptedMessage)


def selection():
    print("Enter a number 1-3 to select an option.")
    print("1. Encrypt a plaintext")
    print("2. Decrypt a ciphertext")
    print("3. Encrypt and Decrypt")
    option = input()
    if int(option) == 1:
        encryptOnly()
    elif int(option) == 2:
        decryptOnly()
    elif int(option) == 3:
        encryptAndDecrypt()
    else:
        selection()


selection()

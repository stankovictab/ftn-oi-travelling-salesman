import numpy as np
import math

SHOW_TABLE = True  # Da li da prikaze tabelu sa rutama i cenama
ALGO = 2  # 0 - bruteForce, 1 - nearestNeighbour, 2 - hungarian, 3........ TODO:

priceMatrix = np.array(
    [
        [999, 2, 3, 1, 4],
        [1, 999, 2, 3, 4],
        [3, 1, 999, 4, 2],
        [4, 3, 2, 999, 1],
        [2, 3, 4, 1, 999],
    ]
)
# priceMatrix = np.array([[999, 1, 2], [4, 999, 5], [9, 2, 999]])
print("------------------------")
print("Input price matrix:")
print(priceMatrix)
dimension = priceMatrix.shape[0]
stack = []
memoryIndex = 0
mask = np.zeros((dimension, dimension))

if ALGO == 0:
    memoryList = list(np.zeros((math.factorial(dimension), 2)))
elif ALGO == 1:
    memoryList = list(np.zeros((dimension, 2)))
elif ALGO == 2:
    memoryList = []  # Ne koristi
elif ALGO == 3:
    2 + 2  # TODO:


print("There are", math.factorial(dimension), "possible routes.")


def generatePermutations(lst):
    # If lst is empty then there are no permutations
    if len(lst) == 0:
        return []
    # If there is only one element in lst then, only
    # one permutation is possible
    if len(lst) == 1:
        return [lst]
    # Find the permutations for lst if there are
    # more than 1 characters
    l = []  # empty list that will store current permutation
    # Iterate the input(lst) and calculate the permutation
    for i in range(len(lst)):
        m = lst[i]
        # Extract lst[i] or m from the list.  remLst is
        # remaining list
        remLst = lst[:i] + lst[i + 1 :]
        # Generating all permutations where m is first
        # element
        for p in generatePermutations(remLst):
            l.append([m] + p)
    return l  # l je lista listi


def calcCost(route):
    # print(route)
    totalCost = 0
    for index, value in enumerate(route):
        if index != dimension:
            row = int(route[index])
            col = int(route[index + 1])
            totalCost += priceMatrix[row, col]
    # print("Total cost for route", route, "is:", totalCost)
    return totalCost


def bruteForce():
    permutations = generatePermutations(list(range(dimension)))
    for p in permutations:
        p.append(p[0])
    print("--------------------------")
    print("Writing permutations to memoryList, calculating costs and appending cost...")
    for index, l in enumerate(memoryList):
        memoryList[index] = permutations[index]
        cost = calcCost(memoryList[index])
        memoryList[index].append(cost)
    print("--------------------------")
    minPrice = math.inf
    print("Calculating minPrice...")
    for l in memoryList:
        if l[-1] < minPrice:
            minPrice = l[-1]
    if SHOW_TABLE == True:
        print("--------------------------")
        print("memoryList :")
        for l in memoryList:
            print(l)
    print("--------------------------")
    print("Optimal routes are :")
    for index, l in enumerate(memoryList):
        if minPrice == memoryList[index][-1]:
            print(
                "Route:",
                memoryList[index][:-1],  # Do poslednjeg
                "with price",
                memoryList[index][-1],
            )
    return


def nnNewRow(beginning, row):
    memoryList[beginning].append(row)
    mask[:, row] = 1
    minVal = math.inf
    minValCol = -1
    for col in range(dimension):
        if priceMatrix[row][col] < minVal:
            if mask[row, col] == 0:
                minVal = priceMatrix[row][col]
                minValCol = col
    if minValCol == -1:
        return
    nnNewRow(beginning, minValCol)
    return


def nearestNeighbour():
    global mask
    # TODO: Sta ako u redu ima npr 2 minimalna elementa - da li je bitno koji se uzima?
    for row in range(dimension):
        memoryList[row] = [row]
        mask[:, row] = 1
        # Za svaki red se pravi tacno jedna ruta
        minVal = math.inf
        minValCol = -1
        for col in range(dimension):
            if priceMatrix[row][col] < minVal:
                if mask[row, col] == 0:
                    minVal = priceMatrix[row][col]
                    minValCol = col
        if minValCol == -1:
            return
        nnNewRow(row, minValCol)  # minValCol ce biti novi row
        mask = np.zeros((dimension, dimension))
    for index, l in enumerate(memoryList):
        memoryList[index].append(memoryList[index][0])
    for index, l in enumerate(memoryList):
        cost = calcCost(memoryList[index])
        memoryList[index].append(cost)
    print("--------------------------")
    print("Optimal routes are :")
    for index, l in enumerate(memoryList):
        print(
            "From",
            memoryList[index][0],
            ": ",
            memoryList[index][:-1],
            "with price",
            memoryList[index][-1],
        )


def rowReduction():
    global priceMatrix
    for x in range(dimension):
        minValue = math.inf
        for y in range(dimension):
            if priceMatrix[x, y] < minValue:
                minValue = priceMatrix[x, y]
        for y in range(dimension):
            if priceMatrix[x, y] == 999:
                continue
            priceMatrix[x, y] -= minValue

    print("-------------------")
    print("Row Reduced:")
    for i in priceMatrix:
        print(i)
    return


def columnReduction():
    global priceMatrix
    for x in range(dimension):
        minValue = math.inf
        for y in range(dimension):
            if priceMatrix[y, x] < minValue:
                minValue = priceMatrix[y, x]
        for y in range(dimension):
            if priceMatrix[y, x] == 999:
                continue
            priceMatrix[y, x] -= minValue

    print("-------------------")
    print("Column Reduced:")
    for i in priceMatrix:
        print(i)
    return


def hungarian():
    rowReduction()
    columnReduction()
    return


if ALGO == 0:
    bruteForce()
elif ALGO == 1:
    nearestNeighbour()
elif ALGO == 2:
    hungarian()


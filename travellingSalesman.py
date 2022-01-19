import numpy as np
import math

SHOW_TABLE = True  # Da li da prikaze tabelu sa rutama i cenama

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


print(priceMatrix)
dimension = priceMatrix.shape[0]
stack = []
memoryIndex = 0
mask = np.zeros((dimension, dimension))
memoryList = list(np.zeros((math.factorial(dimension), 2)))
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
    totalCost = 0
    for index, value in enumerate(route):
        if index != dimension:
            row = int(route[index])
            col = int(route[index + 1])
            totalCost += priceMatrix[row, col]
    # print("Total cost for route", route, "is:", totalCost)
    return totalCost


def fillMask(row, col):
    global mask
    # Glavna dijagonala
    for i in range(dimension):
        for j in range(dimension):
            if i == j:
                mask[i, j] = 1
    # Plus - Red i Kolona
    mask[:, col] = 1
    mask[row, :] = 1
    # Simetricno po glavnoj dijagonali
    mask[col, row] = 1
    print("Mask")
    print(mask)


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


def nearestNeighbour():
    # TODO: Sta ako u redu ima npr 2 minimalna elementa - da li je bitno koji se uzima?
    for row in range(dimension):
        # Za svaki red se pravi tacno jedna ruta
        minVal = math.inf
        for col in range(dimension):
            if priceMatrix[row][col] < math.inf:
                minVal = priceMatrix[row][col]
                minValCol = col
    # TODO: U masci kolonu postavljamo na 1, ne diramo red (nema potrebe)
    # (ako idemo iz A, celu kolonu A stavimo na 1, nije isto kao pre sto je bilo za brute force)
    # Na kraju samo moramo da skontamo kako da iz poslednjeg cvora ode u prvi,
    # Mada to moze samo u memoryList da se .append(l[0]) kao za brute force ovde, nije to problem

    # TODO: Ispisati sve (optimalne) putanje iz svakog cvora, pa onda od svih njih najbolju (iz bilo kog cvora)
    return


# bruteForce()
nearestNeighbour()

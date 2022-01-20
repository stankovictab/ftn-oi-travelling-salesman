import numpy as np
import math

SHOW_TABLE = True  # Da li da prikaze tabelu sa rutama i cenama
ALGO = 2  # 0 - bruteForce, 1 - nearestNeighbour, 2 - hungarian, 3........ TODO:

# TODO: Uporediti rezultate svih algoritama nad istim priceMatrix

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
priceMatrix = np.array(
    [[999, 25, 75, 45], [35, 999, 150, 25], [35, 40, 999, 15], [65, 75, 130, 999]]
)

print("------------------------")
print("Input price matrix:")
print(priceMatrix)
dimension = priceMatrix.shape[0]
stack = []
memoryIndex = 0
mask = np.zeros((dimension, dimension))
routeMask = np.zeros((dimension, dimension))

if ALGO == 0:
    memoryList = list(np.zeros((math.factorial(dimension), 2)))
elif ALGO == 1:
    memoryList = list(np.zeros((dimension, 2)))
elif ALGO == 2:
    memoryList = []  # Ne koristi
    reducedPriceMatrix = priceMatrix.copy()
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
    print(priceMatrix)
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
    global reducedPriceMatrix
    for x in range(dimension):
        minValue = math.inf
        for y in range(dimension):
            if reducedPriceMatrix[x, y] < minValue:
                minValue = reducedPriceMatrix[x, y]
        for y in range(dimension):
            if reducedPriceMatrix[x, y] == 999:
                continue
            reducedPriceMatrix[x, y] -= minValue

    print("-------------------")
    print("Row Reduced:")
    for i in reducedPriceMatrix:
        print(i)
    return


def columnReduction():
    global reducedPriceMatrix
    for x in range(dimension):
        minValue = math.inf
        for y in range(dimension):
            if reducedPriceMatrix[y, x] < minValue:
                minValue = reducedPriceMatrix[y, x]
        for y in range(dimension):
            if reducedPriceMatrix[y, x] == 999:
                continue
            reducedPriceMatrix[y, x] -= minValue

    print("-------------------")
    print("Column Reduced:")
    for i in reducedPriceMatrix:
        print(i)
    return


def rowZeros():
    print("Started finding row zeros...")
    global reducedPriceMatrix
    global mask
    global routeMask
    for x in range(dimension):
        numOfZeros = 0
        selectedZeroRow = -1
        selectedZeroCol = -1
        for y in range(dimension):
            if reducedPriceMatrix[x, y] == 0:
                # Posto se ne radi provera za vec precrtane
                if mask[x, y] == 0:
                    numOfZeros += 1
                    selectedZeroRow = x
                    selectedZeroCol = y
        print("Num of zeros for row is", numOfZeros)
        if numOfZeros == 1:
            mask[:, selectedZeroCol] += 1  # Inkrementira jer hocemo 2 na presecima
            routeMask[selectedZeroRow, selectedZeroCol] = 1
        for l in reducedPriceMatrix:
            print(l)
        for m in mask:
            print(m)


def columnZeros():
    print("Started finding column zeros...")
    global reducedPriceMatrix
    global mask
    global routeMask
    for x in range(dimension):
        numOfZeros = 0
        selectedZeroRow = -1
        selectedZeroCol = -1
        for y in range(dimension):
            if reducedPriceMatrix[y, x] == 0:
                # Posto se ne radi provera za vec precrtane
                if mask[y, x] == 0:
                    numOfZeros += 1
                    selectedZeroRow = y
                    selectedZeroCol = x
        print("Num of zeros for column is", numOfZeros)
        if numOfZeros == 1:
            mask[selectedZeroRow, :] += 1  # Inkrementira jer hocemo 2 na presecima
            routeMask[selectedZeroRow, selectedZeroCol] = 1
        for l in reducedPriceMatrix:
            print(l)
        for m in mask:
            print(m)


def findMinInBlock():
    print("Finding min in block...")
    minValue = math.inf
    for x in range(dimension):
        for y in range(dimension):
            if mask[x, y] == 0:
                if reducedPriceMatrix[x, y] < minValue:
                    minValue = reducedPriceMatrix[x, y]
    # Ova 2 for-a mogu da se spoje
    print("Updating block...")
    for x in range(dimension):
        for y in range(dimension):
            if mask[x, y] == 0:
                if reducedPriceMatrix[x, y] == 999:
                    continue
                reducedPriceMatrix[x, y] -= minValue
    print("Updating intersection...")
    for x in range(dimension):
        for y in range(dimension):
            if mask[x, y] == 2:
                if reducedPriceMatrix[x, y] == 999:
                    continue
                reducedPriceMatrix[x, y] += minValue
    print("reducedPriceMatrix (from findMinInBlock) :")
    for l in reducedPriceMatrix:
        print(l)
    print("mask (from findMinInBlock) :")
    for l in mask:
        print(l)
    return


def createRouteFromRouteMask():
    route = []
    # Posto je optimalna ruta cicklicna, mozemo krenuti od prvog reda (cvora)
    row = 0
    while True:
        for col in range(dimension):
            if routeMask[row, col] == 1:
                route.append((row, col))
                row = col
                break
        if row == 0:
            break
    print("Created route", route, "from routeMask.")
    newRoute = []
    for i in range(dimension):
        newRoute.append(route[i][0])
    newRoute.append(newRoute[0])
    print("newRoute:", newRoute)
    return newRoute


def hungarian():
    global reducedPriceMatrix
    global mask
    global routeMask

    rowReduction()
    columnReduction()

    mask = np.zeros((dimension, dimension))
    routeMask = np.zeros((dimension, dimension))
    existsZeroInBlock = 1
    while existsZeroInBlock == 1:
        rowZeros()
        columnZeros()

        print("Route Mask:")
        for l in routeMask:
            print(l)

        onesInRowPerRow = []
        for x in range(dimension):
            onesInRow = 0
            for y in range(dimension):
                if routeMask[x, y] == 1:
                    onesInRow += 1
            onesInRowPerRow.append(onesInRow)

        onesInColumnPerColumn = []
        for x in range(dimension):
            onesInColumn = 0
            for y in range(dimension):
                if routeMask[y, x] == 1:
                    onesInColumn += 1
            onesInColumnPerColumn.append(onesInColumn)

        print("Ones from routeMask:")
        print(onesInRowPerRow)
        print(onesInColumnPerColumn)
        # Ako su ove 2 liste pune jedinica, to znaci da u svakom redu i svakoj koloni routeMaske ima tacno jedna jedinica
        # TODO: Uradi na osnovu toga tu proveru za kraj, i return

        # existsZeroInBlock provera
        zerosInBlock = 0
        for x in range(dimension):
            for y in range(dimension):
                if mask[x, y] == 0:
                    if reducedPriceMatrix[x, y] == 0:
                        zerosInBlock += 1
        if zerosInBlock > 0:
            existsZeroInBlock = 1
        else:
            existsZeroInBlock = 0

    findMinInBlock()
    print("-------!!!---------")

    mask = np.zeros((dimension, dimension))
    routeMask = np.zeros((dimension, dimension))
    existsZeroInBlock = 1
    while existsZeroInBlock == 1:
        rowZeros()
        columnZeros()

        print("Route Mask:")
        for l in routeMask:
            print(l)

        onesInRowPerRow = []
        for x in range(dimension):
            onesInRow = 0
            for y in range(dimension):
                if routeMask[x, y] == 1:
                    onesInRow += 1
            onesInRowPerRow.append(onesInRow)

        onesInColumnPerColumn = []
        for x in range(dimension):
            onesInColumn = 0
            for y in range(dimension):
                if routeMask[y, x] == 1:
                    onesInColumn += 1
            onesInColumnPerColumn.append(onesInColumn)

        print("Ones from routeMask:")
        print(onesInRowPerRow)
        print(onesInColumnPerColumn)
        # Ako su ove 2 liste pune jedinica, to znaci da u svakom redu i svakoj koloni routeMaske ima tacno jedna jedinica
        # TODO: Uradi na osnovu toga tu proveru za kraj, i return

        # existsZeroInBlock provera
        zerosInBlock = 0
        for x in range(dimension):
            for y in range(dimension):
                if mask[x, y] == 0:
                    if reducedPriceMatrix[x, y] == 0:
                        zerosInBlock += 1
        if zerosInBlock > 0:
            existsZeroInBlock = 1
        else:
            existsZeroInBlock = 0

    findMinInBlock()
    print("-------!!!---------")

    mask = np.zeros((dimension, dimension))
    routeMask = np.zeros((dimension, dimension))
    existsZeroInBlock = 1
    while existsZeroInBlock == 1:
        rowZeros()
        columnZeros()

        print("Route Mask:")
        for l in routeMask:
            print(l)

        onesInRowPerRow = []
        for x in range(dimension):
            onesInRow = 0
            for y in range(dimension):
                if routeMask[x, y] == 1:
                    onesInRow += 1
            onesInRowPerRow.append(onesInRow)

        onesInColumnPerColumn = []
        for x in range(dimension):
            onesInColumn = 0
            for y in range(dimension):
                if routeMask[y, x] == 1:
                    onesInColumn += 1
            onesInColumnPerColumn.append(onesInColumn)

        print("Ones from routeMask:")
        print(onesInRowPerRow)
        print(onesInColumnPerColumn)
        # Ako su ove 2 liste pune jedinica, to znaci da u svakom redu i svakoj koloni routeMaske ima tacno jedna jedinic
        notOneFlag = 0
        for x in range(dimension):
            if onesInRowPerRow[x] != 1:
                notOneFlag = 1
            if onesInColumnPerColumn[x] != 1:
                notOneFlag = 1
        if notOneFlag == 0:  # Ako ovde udje, ispunjen je uslov za kraj
            route = createRouteFromRouteMask()
            price = calcCost(route)
            print("Algorithm Finished!")
            print("Optimal route is:", route, "with price", price)
            print("The optimal route is cyclical, ")
            return

        # existsZeroInBlock provera
        zerosInBlock = 0
        for x in range(dimension):
            for y in range(dimension):
                if mask[x, y] == 0:
                    if reducedPriceMatrix[x, y] == 0:
                        zerosInBlock += 1
        if zerosInBlock > 0:
            existsZeroInBlock = 1
        else:
            existsZeroInBlock = 0

    # findMinInBlock()
    # print("-------!!!---------")

    return


if ALGO == 0:
    bruteForce()
elif ALGO == 1:
    nearestNeighbour()
elif ALGO == 2:
    hungarian()


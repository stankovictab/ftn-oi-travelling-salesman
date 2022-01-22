from statistics import median
import numpy as np
import math
import random

ALGO = 3  # 0 - Brute Force, 1 - Nearest Neighbour, 2 - Hungarian, 3 - Genetic Algorithm
SHOW_TABLE = True  # Da li da prikaze tabelu sa rutama i cenama u Brute Force algoritmu
POPULATION_SIZE = 8  # Broj jedinki u GA, povecace se do sledeceg mnozioca cetvorke
ITERATIONS = 20  # Broj iteracija koje ce GA izvrsiti
MUTATION_RATE = 0.2  # Verovatnoca da ce se dete mutirati u GA

# TODO: Uporediti rezultate svih algoritama nad istim priceMatrix

# Random primer iz glave
priceMatrix = np.array(
    [
        [999, 2, 3, 1, 4],
        [1, 999, 2, 3, 4],
        [3, 1, 999, 4, 2],
        [4, 3, 2, 999, 1],
        [2, 3, 4, 1, 999],
    ]
)
# Brute Force nasao optimalnu sa cenom 8
# Hungarian kaze da ima vise optimalnih ruta i staje
# GA ima u poslednjoj populaciji dosta cena 8, tako da konvergira

# priceMatrix = np.array([[999, 1, 2], [4, 999, 5], [9, 2, 999]])
# Hungarian radi - [0, 2, 1, 0] with price 8
# GA uvek konvergira u 8

# Hungarian primer sa indijskog snimka
priceMatrix = np.array(
    [[999, 25, 75, 45], [35, 999, 150, 25], [35, 40, 999, 15], [65, 75, 130, 999]]
)
# Hungarian radi - [0, 2, 3, 1, 0] with price 200

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
    # Ne koristi memoryList
    reducedPriceMatrix = priceMatrix.copy()
    multipleOptimalRoutesFlag = 0
elif ALGO == 3:
    # Postavljanje POPULATION_SIZE na mnozilac cetvorke, jer ce se deliti sa 2 za roditelje,
    # i onda taj broj opet mora biti deljiv sa 2, jer moramo da imamo paran broj roditelja
    if POPULATION_SIZE < 4:
        POPULATION_SIZE = 4
    # Postavljanje na paran
    if POPULATION_SIZE % 2 != 0:
        POPULATION_SIZE += 1
    # Postavljanje na deljiv sa 4
    if POPULATION_SIZE % 4 != 0:
        POPULATION_SIZE += 2
    print("Popsize:", POPULATION_SIZE)
    population = list(np.zeros((POPULATION_SIZE, 1)))


print("There are", math.factorial(dimension), "possible routes.")


# Third party metoda za generisanje permutacija liste
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
    # print(priceMatrix)
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


def multipleOptimalRouteCheck():
    global multipleOptimalRoutesFlag
    global reducedPriceMatrix
    # Row Check
    zeroCountPerRow = []
    zeroCountPerColumn = []
    for x in range(dimension):
        zeroCount = 0
        for y in range(dimension):
            if reducedPriceMatrix[x, y] == 0:
                if mask[x, y] == 0:
                    zeroCount += 1
        zeroCountPerRow.append(zeroCount)
    # Column Check
    for x in range(dimension):
        zeroCount = 0
        for y in range(dimension):
            if reducedPriceMatrix[y, x] == 0:
                if mask[y, x] == 0:
                    zeroCount += 1
        zeroCountPerColumn.append(zeroCount)
    # Ako imamo neki red ili kolonu koja ima tacno 1 nulu, to znaci da postoji jedna optimalna putanja, pa vracamo flag na ok stanje
    # U suprotnom ostavljamo raise-ovan flag
    multipleOptimalRoutesFlag = 1
    for i in range(dimension):
        if zeroCountPerRow[i] == 1:
            multipleOptimalRoutesFlag = 0
        if zeroCountPerColumn[i] == 1:
            multipleOptimalRoutesFlag = 0
    # TODO: Obrisati ako se skapira, tako da se ne radi grananje i backtracking za proveru iz svih mogucih nula
    if multipleOptimalRoutesFlag == 1:
        print("There exist multiple optimal solutions, the algorithm will stop.")
        return False
    print("zeroCountPerRow:", zeroCountPerRow)
    print("zeroCountPerColumn:", zeroCountPerColumn)
    return


def rowZeros():
    print("Started finding row zeros...")
    global reducedPriceMatrix
    global mask
    global routeMask
    global multipleOptimalRoutesFlag
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
        if numOfZeros >= 2 and multipleOptimalRoutesFlag == 1:
            # TODO: Mislim da je isto? Uzima poslednji sacuvan selectedZero..., to moze, ne mora bas prvi.
            mask[:, selectedZeroCol] += 1  # Inkrementira jer hocemo 2 na presecima
            routeMask[selectedZeroRow, selectedZeroCol] = 1
            # Vracamo flag, da ne uzme sledeci put kada ima 2 nule u redu poslednju, nego da nastavi standardan postupak
            multipleOptimalRoutesFlag = 0
            # Drugu nulu (odnosno sve ostale nule) u redu isto moramo da obelezimo u masci
            # da ne bi imali dve jedinice u istom redu u routeMask na kraju
            for col in range(dimension):
                if reducedPriceMatrix[selectedZeroRow, col] == 0:
                    if mask[selectedZeroRow, col] == 0:
                        # Ne sme += 1 jer ce to postaviti 2 na onu selektovanu nulu, a 2 nam je intersection, a 1 je ok da bude
                        mask[selectedZeroRow, col] = 1
        # TODO: Slucaj za vise optimalnih ruta
        # kada prodje ovaj if gore (bitno) da radi if multipleOptimalRoutesFlag == 1
        # (mislim da mora provera i da je numOfZeros razlicito od 0, dakle bar 2 nule u redu, da moze da izabere)
        # ako jeste, onda override-uj ovo sto je u gornjem if-u na prvu nulu u tom redu, na primer
        # ovo isto i za column treba (mada mozda i ne?) TODO:
        for l in reducedPriceMatrix:
            print(l)
        for m in mask:
            print(m)


def columnZeros():
    print("Started finding column zeros...")
    global reducedPriceMatrix
    global mask
    global routeMask
    global multipleOptimalRoutesFlag
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
    print(route)
    newRoute = []
    for i in range(dimension):
        newRoute.append(route[i][0])
    newRoute.append(newRoute[0])
    print("Created route", newRoute, "from routeMask.")
    return newRoute


def hungarian():
    global reducedPriceMatrix
    global mask
    global routeMask

    rowReduction()
    columnReduction()
    while True:
        mask = np.zeros((dimension, dimension))
        routeMask = np.zeros((dimension, dimension))
        existsZeroInBlock = 1
        while existsZeroInBlock == 1:
            if multipleOptimalRouteCheck() == False:
                return
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
                print(
                    "The optimal route is cyclical, so the choice of the first node doesn't matter."
                )
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
        findMinInBlock()
        print("-------!!!---------")


def initializePopulation():
    global population
    print("Initializing population...")
    for index, l in enumerate(population):
        shuffled = list(range(dimension))  # Od 0 do dimension
        random.shuffle(shuffled)
        # Posto shuffle kreira float64, konvertovanje u int
        for place, i in enumerate(shuffled):
            shuffled[place] = int(shuffled[place])
        population[index] = shuffled
        # Mora da se vrati u isti cvor
        # population[index].append(population[index][0])
    for l in population:
        print(l)
    print("--------------------")
    return


def calculateFitness(organisms):
    print("Calculating fitness...")
    for index, j in enumerate(organisms):
        # Vracanje u isti cvor
        # Stoji ovde a ne u initializePopulation() jer se koristi za odredjivanje fitness-a za decu
        organisms[index].append(organisms[index][0])
        organisms[index].append(calcCost(j))
        print(organisms[index])
    print("--------------------")
    return organisms


def selection():
    print("Selecting parents...")
    prices = []
    for index, j in enumerate(population):
        prices.append(population[index][-1])
    # print(prices)
    m = median(prices)
    # print("m:", m)
    selectedParents = []
    i = 0
    for index, j in enumerate(population):
        if population[index][-1] < m:
            selectedParents.append(population[index])
            i += 1
    # Posto uslov < median moze da da manje od POPULATION_SIZE / 2 elemenata, a nama treba bas toliko,
    # dodajemo elemente koji imaju cenu tacno m
    # print(len(selectedParents))
    if len(selectedParents) < (POPULATION_SIZE / 2):
        for index, j in enumerate(population):
            if population[index][-1] == m:
                selectedParents.append(population[index])
            if len(selectedParents) == (POPULATION_SIZE / 2):
                break
    for sp in selectedParents:
        print(sp)
    print("--------------------")
    return selectedParents


def crossover(selectedParents):
    children = []
    for i in range(len(selectedParents)):
        # Svaki par roditelja pravi par dece
        if i % 2 != 0:
            continue
        parentOne = selectedParents[i][:-2]
        parentTwo = selectedParents[i + 1][:-2]
        print("parentOne", parentOne)
        print("parentTwo", parentTwo)
        # Algoritam ukrstanja :
        # Prva polovina cvorova iz prvog roditelja se kopira,
        # pa se iz drugog roditelja redom uzimaju cvorovi koji su ostali.
        # Isto se radi i za drugu polovinu prvog roditelja, za kreiranje drugog deteta.
        # Ovime se odrzava validnost rute.
        copyLength = len(parentOne) // 2
        if len(parentOne) % 2 == 0:
            # Da za 4 ide do 1, a za 5 ide do 2
            copyLength -= 1
        childOne = parentOne[: copyLength + 1]
        childTwo = parentOne[copyLength + 1 :]
        print("Created children:")
        for (index, elem) in enumerate(parentTwo):
            if parentTwo[index] not in childOne:
                childOne.append(parentTwo[index])
            if parentTwo[index] not in childTwo:
                childTwo.append(parentTwo[index])
        print("childOne:", childOne)
        print("childTwo:", childTwo)
        children.append(childOne)
        children.append(childTwo)
        # TODO: dodaj ponovo prvi element na kraj
    print("children:")
    for c in children:
        print(c)
    print("--------------------")
    return children


def mutate(children):
    print("Mutating children...")
    for i in range(len(children)):  # Za svako dete
        if random.random() < MUTATION_RATE:
            print("Mutation occured on child", i + 1)
            # Mutacija je zamena cvorova na random mestima
            pos1 = random.randint(0, dimension - 1)
            pos2 = random.randint(0, dimension - 1)
            children[i][pos1], children[i][pos2] = children[i][pos2], children[i][pos1]
    for c in children:
        print(c)
    print("--------------------")
    return children


def ga():
    global population
    # Inicijalizacija populacije na POPULATION_SIZE jedinki
    initializePopulation()
    # Odredjivanje fitness-a za svaku jedinku
    # Ovo se radi samo jednom, jer ce u sledecoj iteraciji population vec imati cene
    population = calculateFitness(population)
    for _ in range(ITERATIONS):
        print("\n|||||||||||||||||||||||||||\n")
        # Selekcija se vrsi na osnovu fitness-a, uzima se polovina populacije koja ima najmanje cene
        selectedParents = selection()
        # Ta polovina (roditelji) ostaju, i kreiraju isto toliko dece, ukrstanjem
        children = crossover(selectedParents)
        # Deca se mutiraju i odredjuje im se prilagodjenost (cena)
        children = mutate(children)
        children = calculateFitness(children)
        # Pravljenje nove populacije za sledecu iteraciju
        population = selectedParents + children
        print("Population at the end of iteration:")
        for p in population:
            print(p)
    minPrice = math.inf
    minPriceRoute = []
    for index, l in enumerate(population):
        if population[index][-1] <= minPrice:
            minPrice = population[index][-1]
            minPriceRoute = population[index][:-1]
    print("The price that the algorithm convergated into is", minPrice)
    print("The last route found with that price is:", minPriceRoute)

    # TODO: Problem kod ovog algoritma je sto su i ukrstanje i mutacija random, sto ne doprinosi do poboljsanja rada algoritma,
    # odnosno deca nece nuzno oznacavati priblizavanje optimalnoj ruti, vec samo nekoj novoj.
    # Zbog toga mozemo da belezimo "najbolju rutu do sad", i mozda gledati da li je ona ostala u poslednjoj populaciji.

    # TODO: Spomeni algoritam roja
    #
    return


if ALGO == 0:
    bruteForce()
elif ALGO == 1:
    nearestNeighbour()
elif ALGO == 2:
    hungarian()
elif ALGO == 3:
    ga()


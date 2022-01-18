from asyncio import run_coroutine_threadsafe
from operator import contains
import numpy as np
import math

# priceMatrix = np.array([[999, 1, 2], [4, 999, 1], [3, 2, 999]])
priceMatrix = np.array(
    [
        [999, 2, 3, 1, 4],
        [1, 999, 2, 3, 4],
        [3, 1, 999, 4, 2],
        [4, 3, 2, 999, 1],
        [2, 3, 4, 1, 999],
    ]
)

# [999, 1, 2]
# [4, 999, 1]
# [3, 2, 999]

# treba da ide od nazad i da nadje poslednji element koji nije bio na prvo mesto u steku i njega da stavi kao prvi
# nadje 1 i doda na prvo mesto
#

# krece od nazad i proverava da li se trenutna pozicija nalazi u memoriji na prvom mestu, ako se ne nalazi ne dodajemo odmah
# nego ide dalje i proverava za sledeci element, sve dok ne naidje na poslednji moguci element
# napraviti proveru, ako je red isti kao element na prethodnom mestu, nemoj taj da dodajes

#
#
#

# -----------------
# Krece od pocetka
# Gleda da li je trenutni element 999, ako jeste, preskaci
# Gleda da li je trenutni element u matrici (po indeksu) bio na stackPosition mestu u memoriji
# Kada nadjemo prvog koji nije, stavljamo ga na stackPosition mesto u steku i u memoriji
# Inkrementujemo stackPosition (jer sada gledamo za drugo mesto)
# Krecemo ponovo od pocetka (bitno) (ovo je iteracija)
# Gledamo da li je trenutni element u istom redu kao bilo koji element u steku trenutno
# 	Ako jeste, preskacemo ga
# 	Ako nije, dodaj ga u stek i u memoriju
# Ponavljaj postupak dok ne napunimo dimension mesto u steku
# Tada smo zavrsili, update-ovali smo u memoriji, i sada na osnovu toga preko neke funkcije (calcCost([a1,a2,...])) kojoj dajemo taj route racunamo totalCost za tu rutu, i upisujemo u memoriju
#
# TODO: Da prvo implementiramo ovo gore, pa da onda tek vidimo za ostale slucajeve
#

print(priceMatrix)

dimension = priceMatrix.shape[0]
dimension = 5

# stack = np.zeros(
#     (dimension, 2)
# )  # Stack za pravljenje rute, elementi su indeksi matrice
# stack = stack - 1
# print(stack)
stack = []
firstRow = -1
memoryIndex = 0
mask = np.zeros((dimension, dimension))
maskStack = []
maskStack.append(mask.copy())  # Prva maska je uvek puna nula, ne menja se
# memory je python lista jer mora da ima u sebi listu uredjenih parova za 1. elem.
# memory = [[]]
memory = np.zeros((math.factorial(dimension), 2))  # TODO: routesAndPrices
memoryList = list(memory)
# memoryList[0] = [
#     ((0, 1), (1, 0), (2, 0)),
#     8,
# ]  # (0,1),(1,0),(2,0) - pozicije elemenata, 3 - cena
# memoryList[0][0] = (2, 3)
# tuple je immutable, mora list(tuple), pa izmene, pa tuple(list) za u memory
# print("Memory list:")
# for x in memoryList:
#     print(x)

# print(memory)
print("There are", memory.shape[0], "possible routes.")


def calcCost(stack):
    totalCost = 0
    for value in stack:
        row = int(value[0])
        col = int(value[1])
        totalCost += priceMatrix[row, col]
    print("Total cost for route", stack, "is:", totalCost)
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


def grananje(row, col):
    global mask
    print("Usao u grananje")
    stack.append((row, col))
    print("Stack:", stack)
    print("Mask")
    print(mask)
    print("Row, col:", row, col)

    print("Napunio masku po", row, col)
    fillMask(row, col)

    zeroCounter = 0
    (lastZeroX, lastZeroY) = (-1, -1)
    for x in range(dimension):
        for y in range(dimension):
            if mask[x, y] == 0:
                zeroCounter += 1
                lastZeroX = x
                lastZeroY = y
    print("ZERO TEST:")
    print("Broj nula:", zeroCounter)
    print("Koordinate poslednje nule:", lastZeroX, lastZeroY)
    if zeroCounter == 1:
        print("JEDNA NULA! KRAJ!")
        stack.append((lastZeroX, lastZeroY))
        print("Stack")
        print(stack)
        fillStackIntoMemory()
        # TODO: Ovde verovatno treba da se pop-uje iz maskStack-a?
        maskStack.pop()
        mask = maskStack[-1].copy()
        return
    # TODO: OVDE SE VRATI NA 2 4, STO I TREBA, ALI TREBA DA SE RESETUJE MASKA NA PRVOBITNO STANJE
    # TAKO DA ILI NEKI STEK MASKI ILI POCNI IZ POCETKA ALI OBELEZI GDE SI BIO,
    # ALI TO ONDA MORA OD NAZAD?
    for indexAsCol, zero in enumerate(mask[col, :]):
        # col, indexAsCol je pozicija trenutne nule
        print("Trenutan element maske je:", col, indexAsCol)
        print("Mask")
        print(mask)
        if mask[col, indexAsCol] == 0:
            # if zero == 0:
            # print(indexAsCol)
            if indexAsCol == firstRow:
                print("NE SME OVAJ!")
                print("Masked 1 on", col, indexAsCol)
                mask[col, indexAsCol] = 1
                continue
            maskStack.append(mask.copy())
            grananje(col, indexAsCol)


def fillStackIntoMemory():
    global stack
    global memoryList
    global memoryIndex
    print("Calculating cost...")
    totalCost = calcCost(stack)
    stack.append(totalCost)
    memoryList[memoryIndex] = stack
    memoryIndex += 1
    # print("Memory List:")
    # for x in memoryList:
    #     print(x)
    # TODO: Ovde ne sme ceo stek da se resetuje, mora do onog do kojeg se vracamo
    # kako to da znamo? da brojimo nule u redu, odnosno opcije za grananje?
    # pa kao ako ih ima vise da zna da se vrati tu?
    stack = []


def bruteForce(priceMatrix):
    # totalCost = 0
    # stackPosition = 0
    global firstRow
    global mask
    global maskStack
    for row in range(dimension):  # reversed(range(dimension))
        for col in range(dimension):  # reversed(range(dimension))
            if len(maskStack) != 1:
                print("GRESKA! U maskStack postoji vise od jedne maske.")
                return (False, False)
            # Resetovanje maske na sve nule, svaki put kada se uzme novi prvi element
            mask = maskStack[0].copy()
            firstRow = row  # pamti red odakle je poceo
            if priceMatrix[row, col] == 999:
                continue
            print("Stack:", stack)
            stack.append((row, col))
            print("Stack:", stack)
            # Punimo masku po glavnoj dijagonali, krstu i simetricnoj celiji
            fillMask(row, col)
            # Sad gledamo onaj red koji je bio od selektovanog kolona
            # Biramo prvi slobodan koji :
            #    - Je u masci 0
            #    - Zadovoljava da je njegova kolona razlicita od prve
            for indexAsCol, zero in enumerate(mask[col, :]):
                # col, indexAsCol je pozicija trenutne nule
                if zero == 0:
                    # print(indexAsCol)
                    if indexAsCol == firstRow:
                        print("NE SME OVAJ!")
                        print("Masked 1 on", col, indexAsCol)
                        mask[col, indexAsCol] = 1
                        continue
                    maskStack.append(mask.copy())
                    grananje(col, indexAsCol)
            print("-----------------------")
            # ako je u poslednjem redu ostala samo jedna nula, to oznacava kraj, i onda ovaj drugi uslov ne vazi

            # (maska se resetuje na svaku novu rutu)
            # (moramo da koristimo memoriju za grananje)
            # (svaki put kad u redu vidi vise nula, on mora da radi proveru u memoriji da vidi da li je to nesto vec bilo iskorisceno)
            # (problem sa tim je sto moze da uzme i to iskorisceno ako kasnije ponovo postoji grananje)

            # provera nova
            # red iz kojeg je krenuo je row
            # ako je krenuo iz tog row, on ne sme da se vrati u tu istu ali kolonu
            # i onda ne sme da se vrati u tu ili bilo koju drugu kolonu u kojoj je vec bio
    #         # TODO: Provera da li je selektovani bio na stackPosition mestu u memoriji
    #         if row in stack[:, 0]:
    #             continue
    #         stack[stackPosition, 0] = row
    #         stack[stackPosition, 1] = col
    #         stackPosition += 1
    #         print("Stack Pos", stackPosition)
    #         if stackPosition == dimension:
    #             # Dosli smo do kraja
    #             rowToInsert = list(stack)
    #             rowToInsert.append(rowToInsert[0])
    #             rowToInsert.append(calcCost(stack))
    #             memoryList[memoryIndex] = rowToInsert
    #             print("Memory List:")
    #             for x in memoryList:
    #                 print(x)
    #             memoryIndex += 1
    #             break

    #         print("Added", row, col, "to the stack.")
    #         print(stack)

    # minimumIndex = 0
    # print("Najmanja cena puta je:", memoryList[minimumIndex][-1])
    print("Memory List:")
    for x in memoryList:
        print(x)
    return (False, False)


(route, totalCost) = bruteForce(priceMatrix)
print(route, totalCost)

from asyncio import run_coroutine_threadsafe
import numpy as np
import math

priceMatrix = np.array([[999, 1, 2], [4, 999, 1], [3, 2, 999]])

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
# dimension = 5

stack = np.zeros(
    (dimension, 2)
)  # Stack za pravljenje rute, elementi su indeksi matrice
stack = stack - 1
print(stack)
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


def calcCost(array):
    totalCost = 0
    for (index, value) in enumerate(array):
        print(value)
        row = int(value[0])
        col = int(value[1])
        totalCost += priceMatrix[row, col]
    return totalCost


def bruteForce(priceMatrix):
    totalCost = 0
    stackPosition = 0
    memoryIndex = 0
    for row in range(dimension):  # reversed(range(dimension))
        for col in range(dimension):  # reversed(range(dimension))
            # pamti red kao djoka
            if priceMatrix[row, col] == 999:
                continue
            # puni masku po glavnoj dijagonali, krstu i simetricnom
            # sad gledamo onaj red koji je bio od selektovanog kolona
            # u tom redu biramo sledeci koji selektujemo
            # biramo prvi slobodan koji :
            #    je u masci 0
            #    zadovoljava da je njegova kolona razlicita od djoke
            # ako je u poslednjem redu ostala samo jedna nula, to oznacava kraj, i onda ovaj drugi uslov (djoka) ne vazi

            # (maska se resetuje na svaku novu rutu)
            # (moramo da koristimo memoriju za grananje)
            # (svaki put kad u redu vidi vise nula, on mora da radi proveru u memoriji da vidi da li je to nesto vec bilo iskorisceno)
            # (problem sa tim je sto moze da uzme i to iskorisceno ako kasnije ponovo postoji grananje)

            # provera nova
            # red iz kojeg je krenuo je row
            # ako je krenuo iz tog row, on ne sme da se vrati u tu istu ali kolonu
            # i onda ne sme da se vrati u tu ili bilo koju drugu kolonu u kojoj je vec bio
            # TODO: Provera da li je selektovani bio na stackPosition mestu u memoriji
            if row in stack[:, 0]:
                continue
            stack[stackPosition, 0] = row
            stack[stackPosition, 1] = col
            stackPosition += 1
            print("Stack Pos", stackPosition)
            if stackPosition == dimension:
                # Dosli smo do kraja
                rowToInsert = list(stack)
                rowToInsert.append(rowToInsert[0])
                rowToInsert.append(calcCost(stack))
                memoryList[memoryIndex] = rowToInsert
                print("Memory List:")
                for x in memoryList:
                    print(x)
                memoryIndex += 1
                break

            print("Added", row, col, "to the stack.")
            print(stack)

    minimumIndex = 0
    print("Najmanja cena puta je:", memoryList[minimumIndex][-1])
    return (False, False)


(route, totalCost) = bruteForce(priceMatrix)
print(route, totalCost)

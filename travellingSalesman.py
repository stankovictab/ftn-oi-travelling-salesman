import numpy as np

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


print(priceMatrix)

dimension = priceMatrix.shape[0]

stack = []  # Stack za pravljenje rute, elementi su indeksi matrice


def bruteForce(priceMatrix):
    totalPrice = 0
    routesAndPrices = []
    for row in reversed(range(dimension)):
        for col in reversed(range(dimension)):
            # print(row, col)

            if priceMatrix[row, col] != 999:
                stack.append((row, col))
                totalPrice += priceMatrix[row, col]
    print(stack)
    print(totalPrice)

    return (False, False)


(route, totalPrice) = bruteForce(priceMatrix)
print(route, totalPrice)

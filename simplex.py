import numpy as np
import warnings

warnings.simplefilter(action="ignore", category=DeprecationWarning)  # Za cast u list()
np.set_printoptions(suppress=True)  # Brise eksponencijalnu notaciju brojeva

# Implementiran je Simplex algoritam za kriterijum optimalnosti tipa maksimum,
# odnosno za nalazenje sto vece vrednosti u problemu (maksimalan prihod, na primer)

# Primer 1
# Koeficijenti parametara funkcije kriterijuma optimalnosti, zajedno sa koeficijentima dodatnih promenljivih (0)
costFunctionCoeffs = np.array([6, 14, 13, 0, 0])
# Koeficijenti parametara ogranicenja tipa nejednakosti, zajedno sa koeficijentima dodatnih promenljivih, podrazumeva se oblik <=
constraintCoeffs = np.matrix([[0.5, 2, 1, 1, 0], [1, 2, 4, 0, 1]])
# Slobodni koeficijenti u ogranicenjima, odnosno vrednosti desno od <=
freeCoeffs = np.array([[24], [60]])

# Primer 2
# costFunctionCoeffs = np.array([2, 1.5, 0, 0])
# constraintCoeffs = np.matrix([[6, 3, 1, 0], [75, 100, 0, 1]])
# freeCoeffs = np.array([[1200], [25000]])

# Primer 3
# costFunctionCoeffs = np.array([1, 2, 3, 0, 0, 0])
# constraintCoeffs = np.matrix(
#     [[1, 2, 3, 1, 0, 0], [2, 3, 1, 0, 1, 0], [4, 5, 6, 0, 0, 1]]
# )
# freeCoeffs = np.array([[100], [200], [250]])


def pvt(table, nonbaseVariables, nonbaseVariableIndexes):
    print("Calling pvt 💫")
    print(np.round(table, 2))
    omega = table[0, 1:-2]
    belowOmega = table[1:, 1:-2]
    print("omega:", omega)
    print("belowOmega:")
    print(belowOmega)
    print("nonbaseVariables:", nonbaseVariables)
    print("nonbaseVariableIndexes:", nonbaseVariableIndexes)
    jCandidatesA = []
    jCandidatesB = []
    jCandidatesC = []
    for (index, val) in enumerate(nonbaseVariableIndexes):
        print("val:", val)
        constraintColumn = constraintCoeffs[:, val]
        print("constraintColumn:", constraintColumn)
        print("nonbaseVariables[index]:", nonbaseVariables[index])
        jCandidate = omega.dot(constraintColumn) - nonbaseVariables[index]
        print("jCandidate:", jCandidate)
        jCandidatesA.append(jCandidate)
        jCandidatesB.append(constraintColumn)
        jCandidatesC.append(val)
    print("jCandidates:")
    print(jCandidatesA)
    print(jCandidatesB)
    print(jCandidatesC)
    # Uslov za kraj algoritma
    flag = 0
    for candidate in jCandidatesA:
        if candidate < 0:
            flag = 1
    if flag == 0:
        return (False, False)
    minJCandidateA = jCandidatesA[0]
    minJCandidateIndex = 0
    for (index, candidate) in enumerate(jCandidatesA):
        if minJCandidateA > candidate:
            minJCandidateA = candidate
            minJCandidateIndex = index
    # minJCandidate = min(jCandidates)  # Ovo radi iako je jCandidates obfuskiran
    minJCandidateValue = minJCandidateA
    minJCandidateArray = jCandidatesB[minJCandidateIndex]
    minJCandidateCoeffsIndex = jCandidatesC[minJCandidateIndex]
    print("minJCandidateValue:", minJCandidateValue)
    print("minJCandidateArray:", minJCandidateArray)
    print("minJCandidateCoeffsIndex:", minJCandidateCoeffsIndex)
    # Ubacivanje pivot kolone
    table[0, -1] = minJCandidateValue
    # Mora cast u list jer je table[1:, -1] dimenzija (2,) a ovo (2,1)
    table[1:, -1] = list(belowOmega.dot(minJCandidateArray))
    # Odredjivanje pivot elementa i pivot reda
    minElements = []
    for index in range(constraintCoeffs.shape[0]):
        divisor = table[1:, -2]
        divider = table[1:, -1]
        division = divisor[index] / divider[index]
        minElements.append((division, index + 1))
    print("minElements:", minElements)
    (minElement, pivotRow) = min(minElements)
    print("minElement & pivotRow :", minElement, pivotRow)
    pivotElem = table[pivotRow, -1]
    print("pivotElem =", pivotElem)
    # Update prve kolone
    table[pivotRow, 0] = minJCandidateCoeffsIndex
    print("Updated first column with", minJCandidateCoeffsIndex)
    print(np.round(table, 2))
    return (pivotRow, pivotElem)


def reset(table):
    print("Original:", costFunctionCoeffs)
    baseVariables = []
    baseVariableIndexes = []
    nonbaseVariables = []
    nonbaseVariableIndexes = []
    for (index, val) in enumerate(costFunctionCoeffs):
        if index in table[1:, 0]:
            baseVariables.append(val)
            baseVariableIndexes.append(index)
        else:
            nonbaseVariables.append(val)
            nonbaseVariableIndexes.append(index)
    print("baseVariables: ", baseVariables)
    print("baseVariableIndexes: ", baseVariableIndexes)
    print("nonbaseVariables: ", nonbaseVariables)
    print("nonbaseVariableIndexes: ", nonbaseVariableIndexes)
    return (
        baseVariables,
        baseVariableIndexes,
        nonbaseVariables,
        nonbaseVariableIndexes,
    )


def updateTable(table, pivotRow, pivotElem):
    print("🔱 Updating table...")
    # Izmena svih elemenata osim pivot reda, on mora na kraju da ne utice na ostale
    for row in range(constraintCoeffs.shape[0] + 1):
        # Column do + 2 jer pivot kolonu menjamo na poseban nacin
        for column in range(1, constraintCoeffs.shape[0] + 2):
            if row == pivotRow:
                continue
            appropRow = table[pivotRow, column]
            appropCol = table[row, -1]
            table[row, column] = table[row, column] - (
                appropRow * appropCol / pivotElem
            )
    # Izmena pivot reda
    for row in range(constraintCoeffs.shape[0] + 1):
        # Column do + 2 jer pivot kolonu menjamo na poseban nacin
        for column in range(1, constraintCoeffs.shape[0] + 2):
            if row == pivotRow:
                table[row, column] = table[row, column] / pivotElem


def simplexMax(costFunctionCoeffs, constraintCoeffs, freeCoeffs):
    # Inicijalno punjenje table-a
    table = np.zeros((constraintCoeffs.shape[0] + 1, constraintCoeffs.shape[0] + 3))
    print("Starting table:")
    print(table)
    # Punjenje prve kolone
    baseVariableIndexes = []
    # Posto su u costFunctionCoeffs svi koeficijenti nebaznih promenljivih razliciti od nule, mozemo uzeti za bazne na pocetku indekse tih nula
    for (index, val) in enumerate(costFunctionCoeffs):
        if val == 0:
            baseVariableIndexes.append(index)
    print("baseVariableIndexes:", baseVariableIndexes)
    table[1:, 0] = baseVariableIndexes
    baseVariables = np.zeros((1, len(baseVariableIndexes)))
    for (index, indexValue) in enumerate(baseVariableIndexes):
        baseVariables[0, index] = costFunctionCoeffs[indexValue]
    print("🎇 baseVariables: ", baseVariables)  # baseVariables je Cb

    # baseVariables ce se inicijalizovati na 0 koliko god ih ima
    # B je deo constraintCoeffs matrice od kolone prvog baseVariableIndex-a do kraja
    BMatrixInv = np.linalg.inv(constraintCoeffs[:, baseVariableIndexes[0] :])
    print("BMatrixInv Inserted: ")
    print(BMatrixInv)
    table[1:, 1:-2] = BMatrixInv
    # XMatrix je b nadvuceno
    XMatrix = BMatrixInv.dot(freeCoeffs)
    print("XMatrix: ")
    print(XMatrix)
    # Mora cast u list jer je table[1:, -2] dimenzija (2,) a ovo (2,1)
    table[1:, -2] = list(XMatrix)

    omega = baseVariables.dot(BMatrixInv)
    print("omega:", omega)
    table[0, 1:-2] = omega[0, :]  # Zapravo celo omega
    print("XMatrix:")
    print(XMatrix)
    Cbb = baseVariables.dot(XMatrix)
    print("Cbb: ")
    print(Cbb)
    table[0, -2] = Cbb

    print("Finished inserting!")
    print(np.round(table, 2))

    # Reset i dobavljanje nonbaseVariables i nonbaseVariableIndexes, ovde se stvaraju
    (
        baseVariables,
        baseVariableIndexes,
        nonbaseVariables,
        nonbaseVariableIndexes,
    ) = reset(table)

    while True:
        # Mislim da mora ovaj redosled da se odrzi
        # Racunanje pivot kolone, pivot elementa i update prve kolone
        (pivotRow, pivotElem) = pvt(table, nonbaseVariables, nonbaseVariableIndexes)
        if pivotRow == False:
            print(np.round(table, 2))
            print("Simplex algorithm finished. 🏁")
            print("The result is: ", table[0, -2])
            return
        (
            baseVariables,
            baseVariableIndexes,
            nonbaseVariables,
            nonbaseVariableIndexes,
        ) = reset(table)
        # Update-ovanje svih elemenata osim prve i poslednje kolone
        # Racunanje na osnovu pivotRow, pivotCol (iz tabele direktno) i pivotElem
        updateTable(table, pivotRow, pivotElem)
        print(np.round(table, 2))


simplexMax(costFunctionCoeffs, constraintCoeffs, freeCoeffs)

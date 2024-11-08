def sortIncreasingCol(L):
    if L == []:
        return L
    rows, cols = len(L), len(L[0])
    result = [[] for i in range(rows)]
    colList = []
    for col in range(cols):
        colList = [L[row][col] for row in range(rows)]
        colList.sort()
        print(colList)
        for i in range(len(colList)):
            result[i].append(colList[i])
    return result

L = [[2, 4, 6, -1],
[1, 0, 3, 9],
[17, -5, 9, 4]]

print(sortIncreasingCol(L))
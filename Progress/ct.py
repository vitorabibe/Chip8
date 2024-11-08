import copy
def ct10(L):
    M = copy.copy(L)
    N = copy.deepcopy(L)
    M[0] = L[1] * L[1][0]
    M[0][1]*= 2
    D = [L[1]] * L[1][0]
    D[0][0] += 3
    for x in (L, N, D):
        print(x)
    return M
L = [[1],[2]]
print(ct10(L))
print(L)
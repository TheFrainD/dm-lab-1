def symmetric_difference(A, B):
    A = list(A)
    B = list(B)
    result = []

    for element in A:
        if element not in B:
            result.append(element)
    for element in B:
        if element not in A:
            result.append(element)
    
    sorted(result)
    return set(result)

def union(A, B):
    A = list(A)
    B = list(B)
    result = B.copy()

    for i in A:
        k = True
        for j in B:
            if i == j:
                k = False
        if k == True:
            result.append(i)

    return set(result)
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

    for element in A:
        if element not in B:
            result.append(element)

    return set(result)

def crossing(A, B):
    A = list(A)
    B = list(B)
    result = []

    for element in A:
        if element in A and element in B:
            result.append(element)

    return set(result)

def difference(A, B):
    A = list(A)
    B = list(B)
    result = []

    for element in A:
        if element not in B:
            result.append(element)

    sorted(result)
    return set(result)
def bin_add_4(a, b):
    """Add two four bit binary numbers.
    Most significant bit first.

    Inputs
    ------
    a : iterable of bool
    b : iterable of bool

    Returns
    -------
    list of bool
    """
    res = [int(bool(x)) for x in a]
    add = [int(bool(x)) for x in b]
    for _ in range(4):
        for k in range(4):
            res[k] ^= add[k]
            add[k] = add[k + 1] & res[k + 1] if k < 3 else 0
    return res

def bin_add_4(a, b):
    """Add two four bit binary numbers.
    Least significant bit first.

    Inputs
    ------
    a : str
    b : str

    Returns
    -------
    str
    """
    res = [int(bool(int(x))) for x in a]
    add = [int(bool(int(x))) for x in b]
    tmp = [0 for _ in range(4)]
    for _ in range(5):
        tmp[1:] = [x & y for x, y in zip(res[:-1], add[:-1])]
        res[:] = [x ^ y for x, y in zip(res, add)]
        add = [x for x in tmp]
    return "".join(str(x) for x in res)

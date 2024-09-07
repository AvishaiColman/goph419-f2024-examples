def bin_add_4(a, b):
    """Add two four bit binary numbers.
    Most significant bit first.

    Inputs
    ------
    a : iterable[bool]
    b : iterable[bool]

    Returns
    -------
    list[bool]
    """
    res = [int(bool(x)) for x in a]
    add = [int(bool(x)) for x in b]
    for _ in range(4):
        for k in range(4):
            res[k] ^= add[k]
            add[k] = add[k + 1] & res[k + 1] if k < 3 else 0
    return res


def bin_value(a):
    """Return the value of a list of bits.
    Most significant bit first.

    Inputs
    ------
    a : iterable[bool]

    Returns
    -------
    int
    """
    val = 0
    dig = 2 ** (len(a) - 1)
    for x in a:
        val += bool(x) * dig
        dig //= 2
    return val


def get_dec2bin_dict():
    """Populate a dict with binary representations
    of decimal digits.

    Returns
    -------
    dict
        Keys are decimal digits (as single character strings)
        and values are four bit lists of binary digits.
    """
    bin = [0, 0, 0, 0]
    one = [0, 0, 0, 1]
    dec2bin = dict()
    for k in range(10):
        dec2bin[str(k)] = bin
        bin = bin_add_4(bin, one)
    return dec2bin


_dec2bin = get_dec2bin_dict()


def dec2bin_array(s):
    """Initialize array of binary representations
    from a string of decimal digits.

    Inputs
    ------
    s : str
        String of decimal digits.

    Returns
    -------
    list[list[bool]]
    """
    return [_dec2bin[x] for x in s]


def floor_div_2(a):
    """Floor divide a binary number by 2,
    chopping fractional portion.

    Inputs
    ------
    a : list[bool]

    Returns
    -------
    list[bool]
    """
    res = [0 for _ in range(len(a))]
    res[1:] = a[:-1]
    return res

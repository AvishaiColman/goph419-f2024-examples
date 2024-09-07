from goph419.binary import (
    bin_add_4,
    bin_value,
    get_dec2bin_dict,
)


def main():
    a = [1, 1, 1, 1]
    b = [0, 0, 0, 1]
    print(f"  {a}: {bin_value(a)}")
    print(f"+ {b}: {bin_value(b)}")

    c = bin_add_4(a, b)
    print(f"= {c}: {bin_value(c)}")
    print(f"      expected: {(bin_value(a) + bin_value(b)) % 16}")

    dec2bin = get_dec2bin_dict()
    print(dec2bin)


if __name__ == "__main__":
    main()

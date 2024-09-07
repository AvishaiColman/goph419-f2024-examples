from goph419.binary import (
    bin_add_4,
    bin_value,
    dec2bin_array,
)


def main():
    a = [1, 1, 1, 1]
    b = [0, 0, 0, 1]
    print(f"  {a}: {bin_value(a)}")
    print(f"+ {b}: {bin_value(b)}")

    c = bin_add_4(a, b)
    print(f"= {c}: {bin_value(c)}")
    print(f"      expected: {(bin_value(a) + bin_value(b)) % 16}")

    print()

    d = "42"
    print(f"{d}:\n{dec2bin_array(d)}")


if __name__ == "__main__":
    main()

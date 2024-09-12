"""Example showing conversion of an unsigned integer
to a 32-bit binary representation.
"""

from goph419.binary import (
    binary_int32_big,
    binary_int32_lit,
)


def main():
    # decimal (base-10) integer input
    a = 173

    print(f"Convert {a} to 32-bit binary:")
    print(f"  Big endian: {binary_int32_big(a)}")
    print(f"Litte endian: {binary_int32_lit(a)}")

    print()

    # binary (base-2) integer input
    a = 0b100011011100

    print(f"Convert 0b{a:b} = {a} to 32-bit binary:")
    print(f"  Big endian: {binary_int32_big(a)}")
    print(f"Litte endian: {binary_int32_lit(a)}")

    print()

    # octal (base-8) integer input
    a = 0o716311

    print(f"Convert 0o{a:o} = {a} to 32-bit binary:")
    print(f"  Big endian: {binary_int32_big(a)}")
    print(f"Litte endian: {binary_int32_lit(a)}")

    print()

    # hexadecimal (base-16) integer input
    # commonly used for 24-bit RGB color ("true color") entry
    # where each pair of hexadecimal digits
    # can represent numbers from 0 to 255
    # and there are 256*256*256 = (2**8)**3 = 2**24
    # possible colors
    # e.g.  0x00 = 0
    #       0x0A = 10
    #       0xAA = 170
    #       0xFF = 255
    #       0xFF0000 = red
    #       0x00FF00 = green
    #       0x0000FF = blue
    #       0x000000 = black
    #       0xFFFFFF = white
    #       0x00FFFF = cyan
    #       0xFFFF00 = yellow
    #       0xFF00FF = magenta
    a = 0xEBDCC2

    print(f"Convert 0x{a:X} = {a} to 32-bit binary:")
    print(f"  Big endian: {binary_int32_big(a)}")
    print(f"Litte endian: {binary_int32_lit(a)}")


if __name__ == "__main__":
    main()

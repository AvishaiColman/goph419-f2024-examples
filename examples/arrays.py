import numpy as np

from goph419.linalg import forward_substitution


def main():
    A = np.array(
        [[8e5, 0, 0, 0], [-8e5, 2e6, 0, 0], [0, -2e6, 8e6, 0], [0, 0, -8e6, 2e7]]
    )
    b = np.array([1.0, 2.0, 3.0, 4.0])

    print("solving A * x = b")
    print(f"A: {A}")
    print(f"b: {b}")

    x_np = np.linalg.solve(A, b)
    x_for = forward_substitution(A, b)
    print(f"x_np: {x_np}")
    print(f"x_for: {x_for}")


if __name__ == "__main__":
    main()

import numpy as np


def forward_substitution(a, b):
    """Solve a lower triangular system a * x = b
    for x given a and b.

    Parameters
    ----------
    a : array_like, shape=(M, M)
        The coefficient matrix, in lower triangular form.
    b : array_like, shape=(M, ) or (M, N)
        The right-hand side vector. Can solve for multiple
        right-hand sides if b is 2 dimensional.

    Returns
    -------
    x : numpy.ndarray, shape=(M, ) or (M, N)
        The solution vector(s). Will match the shape of b.

    Notes
    -----
    Assume that a is in lower triangular form and that all
    values above the main diagonal are 0. These values are not
    used in the algorithm, so other information can be safely
    stored there without affecting output.
    """
    a = np.array(a, dtype="float64")
    b = np.array(b, dtype="float64")
    a_shape = a.shape
    M = a_shape[0]
    if len(a_shape) != 2:
        raise ValueError(
            f"coefficient matrix has dimension {len(a_shape)}, should be 2."
        )
    if M != a_shape[1]:
        raise ValueError(f"a has shape {a_shape}, should be square.")
    b_shape = b.shape
    if len(b_shape) < 1 or len(b_shape) > 2:
        raise ValueError(f"b has dimension {len(b_shape)}, should be 1 or 2.")
    if M != b_shape[0]:
        raise ValueError(
            f"b has leading dimension {b_shape[0]}, should match leading dimension of a which is {M}"
        )
    b_one_d = len(b_shape) == 1
    # convert b to (M, 1) for one dimensional b
    # we will put it back to one dimensional later
    if b_one_d:
        b = np.reshape(b, (M, 1))
    # forward substitution algorithm
    x = np.zeros_like(b)
    for k, a_row in enumerate(a):
        x[k, :] = (b[k, :] - a[k, :k] @ x[:k, :]) / a[k, k]
    # tidy up output shape
    if b_one_d:
        x = x.flatten()
    return x


def backward_substitution(a, b):
    """Solve an upper triangular system a * x = b
    for x given a and b.

    Parameters
    ----------
    a : array_like, shape=(M, M)
        The coefficient matrix, in upper triangular form.
    b : array_like, shape=(M, ) or (M, N)
        The right-hand side vector. Can solve for multiple
        right-hand sides if b is 2 dimensional.

    Returns
    -------
    x : numpy.ndarray, shape=(M, ) or (M, N)
        The solution vector(s). Will match the shape of b.

    Notes
    -----
    Assume that a is in upper triangular form and that all
    values below the main diagonal are 0. These values are not
    used in the algorithm, so other information can be safely
    stored there without affecting output.
    """
    a = np.array(a, dtype="float64")
    b = np.array(b, dtype="float64")
    a_shape = a.shape
    M = a_shape[0]
    if len(a_shape) != 2:
        raise ValueError(
            f"coefficient matrix has dimension {len(a_shape)}, should be 2."
        )
    if M != a_shape[1]:
        raise ValueError(f"a has shape {a_shape}, should be square.")
    b_shape = b.shape
    if len(b_shape) < 1 or len(b_shape) > 2:
        raise ValueError(f"b has dimension {len(b_shape)}, should be 1 or 2.")
    if M != b_shape[0]:
        raise ValueError(
            f"b has leading dimension {b_shape[0]}, should match leading dimension of a which is {M}"
        )
    b_one_d = len(b_shape) == 1
    # convert b to (M, 1) for one dimensional b
    # we will put it back to one dimensional later
    if b_one_d:
        b = np.reshape(b, (M, 1))
    # backward substitution algorithm
    x = np.zeros_like(b)
    for k in range(-1, -(M + 1), -1):
        x[k, :] = (b[k, :] - a[k, (k + 1) :] @ x[(k + 1) :, :]) / a[k, k]
    # tidy up output shape
    if b_one_d:
        x = x.flatten()
    return x

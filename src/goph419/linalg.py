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


def gauss_solve(a, b):
    """Solve a well-posed system a * x = b
    for x given a and b using the Gaussian Elimination algorithm.

    Parameters
    ----------
    a : array_like, shape=(M, M)
        The coefficient matrix, must be full rank, det(a) != 0.
    b : array_like, shape=(M, ) or (M, N)
        The right-hand side vector. Can solve for multiple
        right-hand sides if b is 2 dimensional.

    Returns
    -------
    x : numpy.ndarray, shape=(M, ) or (M, N)
        The solution vector(s). Will match the shape of b.

    Notes
    -----
    Assume that matrix a has full rank.
    Using naive GE, we do not check for zeros in pivot positions.
    """
    # making a copy of the input arrays,
    # so that we do not overwrite their values
    a = np.array(a, dtype="float64")
    b = np.array(b, dtype="float64")
    # check for valid input
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
    # form the augmented matrix
    aug = np.hstack([a, b])
    # forward elimination algorithm
    for k, _ in enumerate(aug):
        kp1 = k + 1
        # perform row pivoting
        k_max = np.argwhere(np.abs(aug[k:, k]) == np.max(np.abs(aug[k:, k])))[0, 0]
        if k_max:
            aug[k, :], aug[k + k_max, :] = aug[k + k_max, :].copy(), aug[k, :].copy()
        # calculate elimination coefficients below the pivot
        aug[kp1:, k] /= aug[k, k]
        # subtract correction to eliminate below the pivot
        aug[kp1:, kp1:] -= aug[kp1:, k:kp1] @ aug[k:kp1, kp1:]
    # perform backward substitution
    x = backward_substitution(aug[:, :M], aug[:, M:])
    # tidy up output shape
    if b_one_d:
        x = x.flatten()
    return x

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
    Using GE with partial pivoting, i.e. row pivoting only.
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
    p_row = np.arange(M)  # for tracking row pivots
    q_col = np.arange(M)  # for tracking column pivots
    # forward elimination algorithm
    for k, _ in enumerate(aug):
        kp1 = k + 1
        # perform row and column pivoting
        k_row, k_col = np.argwhere(
            np.abs(aug[k:, k:M]) == np.max(np.abs(aug[k:, k:M]))
        )[0, :]
        if k_row:
            swap = k + k_row
            aug[(k, swap), :] = aug[(swap, k), :]
            p_row[k], p_row[swap] = p_row[swap], p_row[k]
        if k_col:
            swap = k + k_col
            aug[:, (k, swap)] = aug[:, (swap, k)]
            q_col[k], q_col[swap] = q_col[swap], q_col[k]
        # calculate elimination coefficients below the pivot
        aug[kp1:, k] /= aug[k, k]
        # subtract correction to eliminate below the pivot
        aug[kp1:, kp1:] -= aug[kp1:, k:kp1] @ aug[k:kp1, kp1:]
    # perform backward substitution
    x = backward_substitution(aug[:, :M], aug[:, M:])
    # tidy up output
    x = x[q_col, :]  # put output in correct order, after column pivots
    if b_one_d:
        x = x.flatten()
    return x


def lu_factor(a, overwrite_a=False):
    """Factor a non-singular square matrix a
    into p, q, l, and u matrices such that p*a*q = l*u.
    Uses the Gaussian elimination algorithm with complete pivoting.

    Parameters
    ----------
    a : array_like, shape=(M, M)
        The coefficient matrix, must be full rank, det(a) != 0.
    overwrite_a : bool, default=False
        Flag for whether to overwrite a with the lu matrix.

    Returns
    -------
    lu : numpy.ndarray, shape=(M, M)
        The l and u matrices in compact storage,
        with l in the lower triangle (below main diagonal)
        and u in in the upper triangle (at and above main diagonal).
    pq : numpy.ndarray, shape=(2, M)
        The p and q matrices in compact storage,
        with the first row containing row pivot vector p
        and the second row containing column pivot vector q.

    Notes
    -----
    Assume that matrix a has full rank.
    To separate the l and u matrices,
    create an identity matrix and copy the values below
    the main diagonal in lu to create l,
    and create a matrix of zeros and copy the values at
    and above the main diagonal in lu to create u.
    To create the p and q matrices,
    create an identity matrix and rearrange rows
    in the order given by pq[0, :] to create p
    and create an identity matrix and rearrange columns
    in the order given by pq[1, :] to create q.
    """
    # make a copy or rename the input array
    lu = a if overwrite_a else np.array(a, dtype="float64")
    # check for valid input
    shape = lu.shape
    M = shape[0]
    if len(shape) != 2:
        raise ValueError(f"a has dimension {len(shape)}, should be 2.")
    if M != shape[1]:
        raise ValueError(f"a has shape {shape}, should be square.")
    # initialize pivot array
    pq = np.vstack([np.arange(M), np.arange(M)])
    # forward elimination algorithm
    for k, _ in enumerate(lu):
        kp1 = k + 1
        # perform row and column pivoting
        row, col = np.argwhere(np.abs(lu[k:, k:]) == np.max(np.abs(lu[k:, k:])))[0, :]
        if row:
            swap = k + row
            lu[(k, swap), :] = lu[(swap, k), :]
            pq[0, k], pq[0, swap] = pq[0, swap], pq[0, k]
        if col:
            swap = k + col
            lu[:, (k, swap)] = lu[:, (swap, k)]
            pq[1, k], pq[1, swap] = pq[1, swap], pq[1, k]
        # eliminate below the pivot
        lu[kp1:, k] /= lu[k, k]
        lu[kp1:, kp1:] -= lu[kp1:, k:kp1] @ lu[k:kp1, kp1:]
    # TODO: tidy up output
    return lu, pq

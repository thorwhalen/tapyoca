import numpy as np

def cosine_similarity(u, v, *, cartesian_product=False):
    """
    Computes the cosine similarity between two vectors or arrays of vectors.

    If both inputs are 1D vectors, returns a float.
    If one or both inputs are 2D arrays, returns either a 1D array (row-wise)
    or a 2D array (cartesian product of rows) depending on the cartesian_product flag.

    Behavior for row-wise (cartesian_product=False):
      - If both arrays have the same number of rows, compares row i of u to row i of v.
      - If one array has only 1 row, it is broadcast against each row of the other array.
        (Returns a 1D array of length k, where k is the number of rows in the multi-row array.)

    Args:
        u (array-like): A single vector (1D) or a 2D array (k1 x n),
                        where each row is a separate vector.
        v (array-like): A single vector (1D) or a 2D array (k2 x n).
        cartesian_product (bool, optional):
            - If False (default), the function compares rows in a one-to-one fashion (u[i] vs. v[i]),
              **except** if one array has exactly 1 row and the other has multiple rows, in which case
              that single row is broadcast to all rows of the other array.
            - If True, computes the similarity for every combination of rows
              (results in a 2D array of shape (k1, k2)).

    Returns:
        float or np.ndarray:
            - A float if both u and v are 1D vectors.
            - A 1D numpy array if either u or v is 2D and cartesian_product=False.
            - A 2D numpy array if cartesian_product=True.

    Raises:
        ValueError:
            - If the number of columns in u and v do not match.
            - If cartesian_product=False, both arrays have multiple rows but differ in row count.

    Examples
    --------

    Case 1: Both are single 1D vectors

    >>> u1d = [2, 0]
    >>> v1d = [2, 0]
    >>> cosine_similarity(u1d, v1d)
    1.0

    Case 2: Single 1D vector vs. a 2D array (row-wise broadcast)

    >>> import numpy as np
    >>> M1 = np.array([
    ...     [2, 0],
    ...     [0, 2],
    ...     [2, 2]
    ... ])
    >>> cosine_similarity(u1d, M1)  # doctest: +ELLIPSIS
    array([1.        , 0.        , 0.70710678...])

    Case 3: Two 2D arrays of different row lengths, cartesian_product=False (raises ValueError)

    >>> M2_different = np.array([
    ...     [0, 2],
    ...     [2, 2]
    ... ])
    >>> # Expect a ValueError because M1 has 3 rows and M2_different has 2 rows
    >>> cosine_similarity(M1, M2_different, cartesian_product=False)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: For row-wise comparison, u and v must have the same number of rows...

    Case 4: Two 2D arrays of the same number of rows, cartesian_product=False

    >>> M2 = np.array([
    ...     [0, 2],
    ...     [2, 0],
    ...     [2, 2]
    ... ])
    >>> cosine_similarity(M1, M2, cartesian_product=False)
    array([0., 0., 1.])

    Case 5: Two 2D arrays of the same size, `cartesian_product=True`
    (computes every combination of rows => 3 x 3)

    >>> res5 = cosine_similarity(M1, M2, cartesian_product=True)
    >>> np.round(res5, 3)  # doctest: +NORMALIZE_WHITESPACE
    array([[0.   , 1.   , 0.707],
           [1.   , 0.   , 0.707],
           [0.707, 0.707, 1.   ]])
    """
    # Convert inputs to numpy arrays
    u = np.asarray(u)
    v = np.asarray(v)

    # --------------- CASE 1: Both are single 1D vectors ---------------
    if u.ndim == 1 and v.ndim == 1:
        if u.shape[0] != v.shape[0]:
            raise ValueError("Vectors u and v must have the same dimension.")
        dot_uv = np.dot(u, v)
        norm_u = np.linalg.norm(u)
        norm_v = np.linalg.norm(v)
        return dot_uv / (norm_u * norm_v)

    # --------------- CASE 2: At least one is 2D; ensure both are 2D ---------------
    if u.ndim == 1:  # shape (n,) -> (1, n)
        u = u[np.newaxis, :]
    if v.ndim == 1:  # shape (n,) -> (1, n)
        v = v[np.newaxis, :]

    k1, n1 = u.shape
    k2, n2 = v.shape

    # Check that columns (vector dimension) match
    if n1 != n2:
        raise ValueError(
            f"Inconsistent dimensions: u has {n1} columns, v has {n2} columns."
        )

    # --------------- CARTESIAN PRODUCT ---------------
    if cartesian_product:
        # (k1 x k2) dot products
        dot_uv = u @ v.T  # shape (k1, k2)
        norm_u = np.linalg.norm(u, axis=1)  # shape (k1,)
        norm_v = np.linalg.norm(v, axis=1)  # shape (k2,)
        # Outer product of norms => shape (k1, k2)
        denom = np.outer(norm_u, norm_v)
        return dot_uv / denom

    # --------------- ROW-WISE (NOT CARTESIAN) ---------------
    # 1) If one array has a single row (k=1), broadcast it against each row of the other
    if k1 == 1 and k2 > 1:
        # Broadcast u's single row against each row in v
        dot_uv = np.sum(u[0] * v, axis=1)  # shape (k2,)
        norm_u = np.linalg.norm(u[0])  # scalar
        norm_v = np.linalg.norm(v, axis=1)  # shape (k2,)
        return dot_uv / (norm_u * norm_v)

    if k2 == 1 and k1 > 1:
        # Broadcast v's single row against each row in u
        dot_uv = np.sum(u * v[0], axis=1)  # shape (k1,)
        norm_u = np.linalg.norm(u, axis=1)  # shape (k1,)
        norm_v = np.linalg.norm(v[0])  # scalar
        return dot_uv / (norm_u * norm_v)

    # 2) Otherwise, require the same number of rows
    if k1 != k2:
        raise ValueError(
            f"For row-wise comparison, u and v must have the same number of rows. "
            f"(u has {k1}, v has {k2})"
        )
    dot_uv = np.sum(u * v, axis=1)  # shape (k1,)
    norm_u = np.linalg.norm(u, axis=1)
    norm_v = np.linalg.norm(v, axis=1)
    return dot_uv / (norm_u * norm_v)

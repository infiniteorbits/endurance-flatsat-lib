"""General functions used to manipulate string commands from candump"""


def split_string(s: int, keys: list[int]) -> str:
    """
    Splits a binary representation of a given integer into segments of specified lengths.

    Args:
        s (int): The integer to be split. It is first converted into a binary string.
        keys (list of int): A list of integers specifying the lengths
        of each segment to split the binary string into.

    Returns:
        str: A space-separated string where each segment corresponds
        to the binary split as specified by `keys`.

    Raises:
        ValueError: If the total length of the keys exceeds the binary string length.

    Example:
        split_string(12345, [8, 3, 8, 3, 1, 6])
        # Returns '00000000 000 00110001 110 1 100001'

    Notes:
        - The input integer `s` is padded to 29 bits (as specified by "0>29b" format).
        - The function is typically used for decoding and parsing binary fields from CAN bus IDs.
    """
    # Convert the integer s to a zero-padded 29-bit binary string
    s = format(s, "0>29b")  # type: ignore
    start = 0
    result = []

    # Split the binary string into sections based on keys
    for key in keys:
        result.append(s[start : start + key])  # type: ignore
        start += key

    return " ".join(result)

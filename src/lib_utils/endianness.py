def convert_big_to_little_endian(bit_message: str) -> str:
    """
    Converts a bit message from big-endian to little-endian format.

    Args:
        bit_message (str): A string of bits separated by spaces, representing octets in big-endian order.

    Returns:
        str: The bit message converted to little-endian format, with spaces between octets.
    """
    # Split the input message into a list of 8-bit groups (octets)
    octets: list[str] = bit_message.strip().split()

    # Validate that each octet is exactly 8 bits and contains only '0' or '1'
    if not all(len(octet) == 8 and set(octet).issubset({"0", "1"}) for octet in octets):
        raise ValueError("Input must be a space-separated string of valid 8-bit binary numbers.")

    # Reverse the order of the octets for little-endian format
    reversed_octets: list[str] = octets[::-1]

    # Join the reversed octets with spaces
    return " ".join(reversed_octets)
from lib_utils.exception import ApidParameterError

"""This module is making correspondance betweens ids and systems related to the ICD"""

# Define all dictionaries
lookup_tables = {
    "transfer_type": {
        "Telecommand": 2,
        "Telemetry": 3,
        "Get Block": 5,
        "Set Block": 4,
        "Unsolicited Telemetry": 1,
        "Time Synchronisation": 0,
    },
    "set_block_frame_type": {
        "Set Block Request": 0,
        "SB Acknowledge": 2,
        "SB Negative Acknowledge": 4,
        "Transfer": 1,
        "Abort": 3,
        "Status Request": 6,
        "Report": 7,
    },
    "system": {
        "OBC": 32,
        "Radio A": 64,
        "Radio B": 65,
        "Radio C": 66,
        "Radio D": 67,
    },
    "apid": {
        "Mission A": 10,
        "Mission B": 11,
        "GNC A": 30,
        "GNC B": 31,
        "Far Camera A": 40,
        "Far Camera B": 41,
        "Near Camera A": 50,
        "Near Camera B": 51,
        "Near Camera C": 52,
    },
    "sequence flags": {
        "First packet of sequence": 1,
        "Continuation packet": 0,
        "Last packet of sequence": 2,
        "Standalone packet": 3,
    },
}


# Generalized function to look up values in dictionaries
def lookup_value(keyword: str, binary_value: int) -> str:
    """
    Looks up a human-readable value corresponding to a
    binary representation in a specified lookup table.

    Args:
        keyword (str): The name of the lookup table to search,
        case-insensitive. Example keywords include
                       "transfer_type", "set_block_frame_type", "system",
                         "apid", or "sequence flags".
        binary_value (int): The binary value to look up in the specified dictionary.

    Returns:
        str: The corresponding human-readable key if found, or a message indicating either an
             unrecognized binary value or an invalid keyword.

    Raises:
        TypeError: If binary_value is not an integer.
        KeyError: If the keyword does not match any available lookup tables.

    Example:
        lookup_value('transfer_type', 2)  # Returns 'Telecommand'
    """
    # Fetch the correct dictionary using the keyword
    lookup_table = lookup_tables.get(keyword.lower())

    if lookup_table:
        for key, bits in lookup_table.items():
            if int(bits) == binary_value:
                return key
        return "Unrecognized " + keyword.capitalize()

    return "Invalid keyword provided"


def get_apid_number(apid_name: str) -> int:
    """
    Returns the APID number corresponding to the given name, tolerating variations in case and spaces.

    Args:
        apid_name (str): The name of the APID to look up.

    Returns:
        int: The APID number if found.

    Raises:
        ApidParameterError: If the APID name is not found in the lookup table.
    """
    # Normalize user input: remove spaces and convert to lowercase
    normalized_apid_name = apid_name.strip().lower().replace(" ", "")

    # Create a normalized version of the dictionary for lookup
    normalized_lookup = {
        key.strip().lower().replace(" ", ""): value for key, value in lookup_tables["apid"].items()
    }

    # Look up the APID number in the normalized dictionary
    apid_number = normalized_lookup.get(normalized_apid_name)

    if apid_number is None:
        raise ApidParameterError(f"APID '{apid_name}' not found.")

    print(f"The APID number for '{apid_name}' is {apid_number}.")
    return apid_number

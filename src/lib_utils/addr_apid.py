from dataclasses import dataclass, field

from lib_utils.exception import ApidParameterError


@dataclass
class LookupTable:
    """
    Represents a lookup table with a mapping of human-readable keys to binary values.
    """

    name: str
    table: dict[str, int] = field(default_factory=dict)

    def lookup_value(self, binary_value: int) -> str:
        """
        Look up a human-readable value corresponding to a binary representation.

        Args:
            binary_value (int): The binary value to look up.

        Returns:
            str: The corresponding human-readable key if found.

        Raises:
            ValueError: If the binary value is not recognized.
        """
        for key, value in self.table.items():
            if value == binary_value:
                return key
        raise ValueError(f"Unrecognized value {binary_value} in {self.name} lookup table.")


@dataclass
class LookupTables:
    """
    Contains all lookup tables as dataclass instances.
    """

    transfer_type: LookupTable = field(
        default_factory=lambda: LookupTable(
            name="transfer_type",
            table={
                "Telecommand": 2,
                "Telemetry": 3,
                "Get Block": 5,
                "Set Block": 4,
                "Unsolicited Telemetry": 1,
                "Time Synchronisation": 0,
            },
        )
    )
    set_block_frame_type: LookupTable = field(
        default_factory=lambda: LookupTable(
            name="set_block_frame_type",
            table={
                "Set Block Request": 0,
                "SB Acknowledge": 2,
                "SB Negative Acknowledge": 4,
                "Transfer": 1,
                "Abort": 3,
                "Status Request": 6,
                "Report": 7,
            },
        )
    )
    system: LookupTable = field(
        default_factory=lambda: LookupTable(
            name="system",
            table={
                "OBC": 32,
                "Radio A": 64,
                "Radio B": 65,
                "Radio C": 66,
                "Radio D": 67,
            },
        )
    )
    apid: LookupTable = field(
        default_factory=lambda: LookupTable(
            name="apid",
            table={
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
        )
    )
    sequence_flags: LookupTable = field(
        default_factory=lambda: LookupTable(
            name="sequence_flags",
            table={
                "First packet of sequence": 1,
                "Continuation packet": 0,
                "Last packet of sequence": 2,
                "Standalone packet": 3,
            },
        )
    )


# Initialize the lookup tables
lookup_tables = LookupTables()


# Generalized function to look up values in dataclasses
def lookup_value(keyword: str, binary_value: int) -> str:
    """
    Generalized function to look up a value in a specified lookup table.

    Args:
        keyword (str): The name of the lookup table.
        binary_value (int): The binary value to look up.

    Returns:
        str: The corresponding human-readable value.
    """
    table = getattr(lookup_tables, keyword.lower(), None)
    if table and isinstance(table, LookupTable):
        try:
            return table.lookup_value(binary_value)  # type: ignore
        except ValueError as e:
            return str(e)
    return f"Invalid keyword '{keyword}'."


def get_apid_number(apid_name: str) -> int:
    """
    Returns the APID number corresponding to a given name.

    Args:
        apid_name (str): The name of the APID.

    Returns:
        int: The corresponding APID number.

    Raises:
        ApidParameterError: If the APID name is not found.
    """
    normalized_name = apid_name.strip().lower().replace(" ", "")
    normalized_lookup = {
        key.strip().lower().replace(" ", ""): value for key, value in lookup_tables.apid.table.items()
    }
    apid_number = normalized_lookup.get(normalized_name)
    if apid_number is None:
        raise ApidParameterError(f"APID '{apid_name}' not found.")
    return apid_number

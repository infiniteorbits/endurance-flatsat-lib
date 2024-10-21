"""This module processes the first message data from CAN bus dumps."""

from typing import Any, Optional

from lib_utils.addr_apid import lookup_value


def process_first_message_data(line: str, doplot: bool = True) -> Optional[dict[str, Any]]:
    """
    Process the first message data from a CAN bus dump line.

    This function parses the first message in a CAN bus dump line,
    extracting relevant information such as
    the version number, TM/TC type, APID (Application Process Identifier), sequence flags, and more.
    It also has an option to print the parsed data if `doplot` is set to True.

    Args:
    line (str): A string containing the CAN bus message.
                The message is expected to be in binary format
                (as a string of 1s and 0s) and follows the standard packet structure.
                The function extracts fields by shifting and masking bits.

    doplot (bool, optional): A flag to indicate whether to print the parsed data for debugging or
                             visualization purposes. Default is True.

    Returns:
    dict or None: A dictionary containing the parsed fields from the CAN bus message if successful,
                  or None if the message is invalid or an error occurs.

    Parsed fields in the dictionary:
        - "prefix": First 8 bits of the message, used as a prefix.
        - "version_number": Version number (3 bits).
        - "type_tmtc": Type of message (TM or TC).
        - "str_type": Human-readable string for TM/TC type.
        - "data_field_header_flag": Data field header flag (1 bit).
        - "apid": Application Process Identifier (11 bits).
        - "apid_sys": System identifier corresponding to the APID (from lookup table).
        - "grouping_flags": Grouping flags (2 bits), representing the sequence flags.
        - "Sequence flag": Human-readable sequence flag (from lookup table).
        - "source_sequence_count": Source sequence count (14 bits).
        - "packet_length": Length of the packet (16 bits).
        - "counter": Message counter (7 bits).
        - "fsb": First Segment Bit (1 bit), whether the message is the first in a sequence.

    Raises:
        ValueError: If the line cannot be parsed as a binary integer.
        IndexError: If the line does not contain enough data to be parsed.
    """
    try:
        # Split the line into parts
        parts = line.split(None, 3)
        if len(parts) < 3:
            return None

        bytes_data = int(parts[3].replace(" ", "").replace("\n", ""), 2)

        if len(line.replace(" ", "").replace("\n", "")) < 8**2:
            return None

        prefix = bytes_data >> 56  # 8 bits
        version_number = (bytes_data >> 53) & 0x7  # 3 bits
        type_tmtc = (bytes_data >> 52) & 0x1  # 1 bit

        if type_tmtc == 0:
            str_type = "TM"
        elif type_tmtc == 1:
            str_type = "TC"
        else:
            str_type = "ERROR TmTc type"

        data_field_header_flag = (bytes_data >> 51) & 0x1  # 1 bit
        apid = (bytes_data >> 40) & 0x7FF  # 11 bits (0x7FF = 2047)
        grouping_flags = (bytes_data >> 38) & 0x3  # 2 bits (0x3 = 3)
        source_sequence_count = (bytes_data >> 24) & 0x3FFF  # 14 bits (0x3FFF = 16383)
        packet_length = (bytes_data >> 8) & 0xFFFF  # 16 bits (0xFFFF = 65535)
        counter = (bytes_data >> 1) & 0x7F  # 7 bits (0x7F = 127)
        fsb = bytes_data & 0x1  # 1 bit

        res_dict = {
            "prefix": prefix,
            "version_number": version_number,
            "type_tmtc": type_tmtc,
            "str_type": str_type,
            "data_field_header_flag": data_field_header_flag,
            "apid": apid,
            "apid_sys": lookup_value("apid", apid),
            "grouping_flags": grouping_flags,
            "Sequence flag": lookup_value("sequence flags", grouping_flags),
            "source_sequence_count": source_sequence_count,
            "packet_length": packet_length,
            "counter": counter,
            "fsb": fsb,
        }

        if doplot:
            print(
                f"Packet Header: (type: {str_type}, Apid: {apid}({lookup_value('apid', apid)}), "
                f"Sequence flag: {lookup_value('sequence flags', grouping_flags)}, "
                f"source_sequence_count: {source_sequence_count}, packet_length: {packet_length}, "
                f"counter: {counter})"
            )
        return res_dict

    except (ValueError, IndexError) as e:
        print(f"Erreur lors du traitement des données: {e}")
        return None

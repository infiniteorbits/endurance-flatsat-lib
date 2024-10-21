"""This module decommutes the CAN ID hexadecimal values from the candump command"""

from typing import Any, Optional

from candump_utils.utils import split_string
from lib_utils.addr_apid import lookup_value


def write_candump_line(line: str, doplot: bool = True) -> Optional[tuple[dict[str, Any], bool]]:
    """
    Parses a single CAN dump line, extracts relevant information from the CAN ID,
    and optionally prints the parsed data in a structured format.

    Args:
        line (str): A string representing a single line from the candump output. It is expected
                    to contain at least three parts: a timestamp,
                    CAN ID in hexadecimal, and CAN data.
        doplot (bool): If True, prints the parsed CAN ID information. Default is True.

    Returns:
        tuple:
            - can_info (dict): A dictionary containing extracted fields from the CAN ID:
                - to_addr (int): The destination address (8 bits).
                - to_apid (str): The system name corresponding to the destination address.
                - set_block (int): The block type associated with the transfer (3 bits).
                - sb_type (str): The transfer type name based on the set_block.
                - from_addr (int): The source address (8 bits).
                - from_apid (str): The system name corresponding to the source address.
                - set_block_request (int): The frame type of the set block request (3 bits).
                - sbr_type (str): The set block frame type name.
                - if_done (int): Whether the operation is marked as done (1 bit).
                - block_to_transfert (int): Remaining 6 bits representing the block to transfer.
            - supervisor (bool): A flag indicating if the line corresponds
                to a supervisor message (CAN ID = 1824).

    Raises:
        IndexError: If the line is not correctly formatted or does not contain enough parts.
        ValueError: If there is an issue converting the CAN ID from hexadecimal to an integer.

    Example:
        line = '123456789 ABCDEF01 [8] 00 00 00 00 00 00 00 00'
        can_info, supervisor = write_candump_line(line)

    Notes:
        - This function extracts and processes specific parts of the
            CAN ID based on bitwise operations,
          where the CAN ID is divided into fields according to the satellite communication protocol.
        - If `doplot` is True, the function prints the parsed information in a readable format.
        - The function handles and returns None if the line is malformed or missing necessary data.
    """
    supervisor = False
    try:
        # Split the line into parts
        parts = line.split(None, 3)
        if len(parts) < 3:
            return None

        can_id = int(parts[1], 16)

        can_parsed = split_string(can_id, [8, 3, 8, 3, 1, 6])

        if can_id == 1824:
            supervisor = True

        can_info = {
            "to_addr": (can_id >> 21) & 0xFF,  # 8 bits
            "to_apid": lookup_value("system", (can_id >> 21) & 0xFF),
            "set_block": (can_id >> 18) & 0x7,  # 3 bits
            "sb_type": lookup_value("transfer_type", (can_id >> 18) & 0x7),
            "from_addr": (can_id >> 10) & 0xFF,  # 8 bits
            "from_apid": lookup_value("system", (can_id >> 10) & 0xFF),
            "set_block_request": (can_id >> 7) & 0x7,  # 3 bits
            "sbr_type": lookup_value("set_block_frame_type", (can_id >> 7) & 0x7),
            "if_done": (can_id >> 6) & 0x1,  # 1 bit
            "block_to_transfert": can_id & 0x3F,  # 6 bits restants
        }

        if doplot:
            print(
                f"Raw_ID:{can_parsed},\n"
                f"CAN_ID: (to: {can_info['to_addr']}({can_info['to_apid']}), "
                f"set_block: {can_info['set_block']}({can_info['sb_type']}), "
                f"from: {can_info['from_addr']}({can_info['from_apid']}), "
                f"set_block_request: {can_info['set_block_request']}({can_info['sbr_type']}), "
                f"if_done: {can_info['if_done']}, "
                f"block_to_transfert: {can_info['block_to_transfert']})"
            )

        return can_info, supervisor

    except (IndexError, ValueError):
        # Handling cases where input data might be missing or malformed
        return None

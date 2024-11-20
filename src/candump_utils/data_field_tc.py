"""
Module for processing data fields from candump telemetry.

This module contains utility functions to process the data field of a CAN telemetry line.
"""

from typing import Any, Optional


def process_data_field_tc(line: str, doplot: bool = True) -> Optional[dict[str, Any]]:
    """
    Parses a CAN telemetry line to extract fields such as the PUS version number,
    acknowledgement flags, service type ID, message subtype ID, and source ID.

    Args:
        line (str): A string representing a single telemetry line from the candump output.
                    The line must have at least three parts and the third
                    part should be the data field in binary format.
        doplot (bool): If True, prints the extracted values for
                        PUS service type, subtype, and acknowledgment flags.

    Returns:
        dict: A dictionary with the following keys:
            - 'tc_packet_pus_version_number' (int): PUS version number (4 bits).
            - 'acknowledgements_flags' (int): Acknowledgement flags (4 bits).
            - 'service_type_id' (int): Service type ID (8 bits).
            - 'message_subtype_id' (int): Message subtype ID (8 bits).
            - 'source_id' (int): Source ID (16 bits).
        None: Returns None if the line format is invalid or if an error occurs during processing.

    Example:
        line = "123456789 1FFFFFFF [8] 01010101 11001100 00000000 10101010"
        process_data_field_tc(line)

    Raises:
        ValueError: If there is an issue converting the data field to binary.
        IndexError: If the line doesn't contain enough parts.
    """
    try:
        # Split the line into parts
        parts = line.split(None, 3)
        if len(parts) < 3:
            return None

        # Remove spaces and newlines from the data field, take first 40 bits, and convert to integer
        bytes_data = int(parts[3].replace(" ", "").replace("\n", "")[0:40], 2)

        # Extract the individual fields from the 40-bit data field
        tc_packet_pus_version_number = (bytes_data >> 36) & 0xF  # 4 bits
        acknowledgements_flags = (bytes_data >> 32) & 0xF  # 4 bits
        service_type_id = (bytes_data >> 24) & 0xFF  # 8 bits
        message_subtype_id = (bytes_data >> 16) & 0xFF  # 8 bits
        source_id = bytes_data & 0xFFFF  # 16 bits

        res_dict = {
            "tc_packet_pus_version_number": tc_packet_pus_version_number,
            "acknowledgements_flags": acknowledgements_flags,
            "service_type_id": service_type_id,
            "message_subtype_id": message_subtype_id,
            "source_id": source_id,
        }

        # If doplot is True, print the parsed values
        if doplot:
            print(
                f"DATA FIELD : (AckFlags: {acknowledgements_flags}, "
                f"PUS_Type: {service_type_id}, PUS_Sub_Type: {message_subtype_id})"
                f"TC_PUS_version: {tc_packet_pus_version_number}"
            )

        return res_dict

    except (ValueError, IndexError) as e:
        # Print the error message if any exception occurs
        print(f"Error during data processing: {e}")
        return None

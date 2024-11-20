"""
Module for processing telemetry data fields from candump telemetry.

This module contains utility functions to process the data field of a telemetry message (TM).
"""

from typing import Any, Optional


def process_data_field_tm(line: str, doplot: bool = True) -> Optional[dict[str, Any]]:
    """
    Parses a CAN telemetry line to extract fields such as the PUS version number,
    spacecraft time reference status, service type ID, message subtype ID, and other fields.

    Args:
        line (str): A string representing a single telemetry line from the candump output.
                    The line must have at least three parts and the third part
                    should be the data field in binary format.
        doplot (bool): If True, prints the extracted values for PUS service type and subtype.

    Returns:
        dict: A dictionary with the following keys:
            - 'tm_packet_pus_version_number' (int): PUS version number (4 bits).
            - 'spacecraft_time_reference_status' (int): Spacecraft time reference status (4 bits).
            - 'service_type_id' (int): Service type ID (8 bits).
            - 'message_subtype_id' (int): Message subtype ID (8 bits).
            - 'message_type_counter' (int): Message type counter (16 bits).
            - 'destination_id' (int): Destination ID (16 bits).
        None: Returns None if the line format is invalid or if an error occurs during processing.

    Example:
        line = "123456789 1FFFFFFF [8] 01010101 11001100 00000000 10101010"
        process_data_field_tm(line)

    Raises:
        ValueError: If there is an issue converting the data field to binary.
        IndexError: If the line doesn't contain enough parts.
    """
    try:
        # Split the line into parts
        parts = line.split(None, 3)
        if len(parts) < 3:
            return None

        # Remove spaces and newlines from the data field and convert it to an integer
        bytes_data = int(parts[3].replace(" ", "").replace("\n", ""), 2)

        # Extract individual fields from the data
        tm_packet_pus_version_number = (bytes_data >> 60) & 0xF  # 4 bits
        spacecraft_time_reference_status = (bytes_data >> 56) & 0xF  # 4 bits
        service_type_id = (bytes_data >> 48) & 0xFF  # 8 bits
        message_subtype_id = (bytes_data >> 40) & 0xFF  # 8 bits
        message_type_counter = (bytes_data >> 24) & 0xFFFF  # 16 bits
        destination_id = (bytes_data >> 8) & 0xFFFF  # 16 bits
        #:TODO: Time not treated yet

        res_dict = {
            "tm_packet_pus_version_number": tm_packet_pus_version_number,
            "spacecraft_time_reference_status": spacecraft_time_reference_status,
            "service_type_id": service_type_id,
            "message_subtype_id": message_subtype_id,
            "message_type_counter": message_type_counter,
            "destination_id": destination_id,
        }

        # If doplot is True, print the extracted values for PUS type and subtype
        if doplot:
            print(
                f"DATA FIELD : (PUS_Type: {service_type_id},"
                f"PUS_Sub_Type: {message_subtype_id}),"
                f"TM_Counter: {message_type_counter},"
                f"Destination_ID: {destination_id},"
                f"TM_PUS_version: {tm_packet_pus_version_number}"
            )

        return res_dict

    except (ValueError, IndexError) as e:
        # Print an error message if an exception occurs
        print(f"Error during data processing: {e}")
        return None

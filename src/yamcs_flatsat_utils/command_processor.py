import os
import struct
from binascii import hexlify
from collections.abc import Callable
from typing import Any, Optional, Union

import pandas as pd
from yamcs.client import ContainerSubscription, ParameterSubscription, VerificationConfig  # type: ignore
from yamcs.tmtc.model import ContainerData, IssuedCommand  # type: ignore

from lib_utils.addr_apid import get_apid_number
from lib_utils.config import create_table, get_project_root, process_pas_table_and_merge, read_config
from lib_utils.exception import IssuingCommandError
from yamcs_flatsat_utils.yamcs_interface import YamcsInterface

FIELDS = ["ccf", "cdf", "pas"]


def get_cname(ccf_type: int = 0, ccf_stype: int = 0) -> str:
    """
    Retrieve the CCF_CNAME based on CCF_TYPE and CCF_STYPE from a CSV file.

    Args:
    dat_file (str): The path to the CSV file containing the data.
    ccf_type (int): The type to search for.
    ccf_stype (int): The subtype to search for.

    Returns:
    str: The CCF_CNAME if a match is found, otherwise an empty string.
    """
    config = read_config({"Submodule": ["name", "commit"]})
    expected_commit = config["Submodule.commit"]
    dat_file = f"ccf_table_{expected_commit}.dat"


    # Lire le fichier CSV dans un DataFrame
    path_df = os.path.join(get_project_root(), "etc/config/", dat_file)
    df = pd.read_csv(path_df, sep="\t")

    # Filtrer les résultats en fonction de CCF_TYPE et CCF_STYPE
    result = df[(df["CCF_TYPE"] == ccf_type) & (df["CCF_STYPE"] == ccf_stype)]

    # Retourner le nom correspondant s'il existe, sinon une chaîne vide
    return result.iloc[0]["CCF_CNAME"] if not result.empty else ""


def get_cparameters(ccf_type: int = 0, ccf_stype: int = 0) -> Optional[list[str]]:
    """
    Retrieve the CCF_CNAME based on CCF_TYPE and CCF_STYPE from a CSV file.

    Args:
    dat_file (str): The path to the CSV file containing the data.
    ccf_type (int): The type to search for.
    ccf_stype (int): The subtype to search for.

    Returns:
    str: The CCF_CNAME if a match is found, otherwise an empty string.
    """

    name = get_cname(ccf_type, ccf_stype)

    config = read_config({"Submodule": ["name", "commit"]})
    expected_commit = config["Submodule.commit"]
    dat_file = f"cdf_table_{expected_commit}.dat"

    # Lire le fichier CSV dans un DataFrame
    path_df = os.path.join(get_project_root(), "etc/config/", dat_file)
    df = pd.read_csv(path_df, sep="\t")

    # Filtrer les résultats en fonction de CCF_TYPE et CCF_STYPE
    result = df[(df["CDF_CNAME"] == name)]

    if result.value_counts().count() == 0:
        return None

    return list(result.CDF_PNAME.to_dict().values())


class CommandProcessor:
    """
    Command processing abstraction, using YamcsInterface to interact with the Yamcs system.
    Provides a unified method for issuing and monitoring commands.
    """

    def __init__(self, interface: YamcsInterface) -> None:
        """
        Initialize the CommandProcessor with a Yamcs client instance.

        Args:
            interface (YamcsInterface): An instance of YamcsClient to interact with Yamcs.
        """
        self.processor = interface.get_processor()
        self.listen_to_command_history()
        self.table_command = [create_table(field) for field in FIELDS]  # type: ignore
        process_pas_table_and_merge(do_write=True)

    def issue_command_yamcs(
        self,
        apid: str,
        tc_type: int,
        tc_stype: int,
        args: Optional[tuple[Any, ...]] = None,
        ackflags: int = 0,
        monitor: bool = True,
        acknowledgment: Optional[str] = None,
        disable_verification: bool = False,
    ) -> IssuedCommand:
        """
        Send a command with parameters for PUS commands, verification, and monitoring.

        Args:
            apid (str): Application Process ID for PUS commands.
            tc_type (int): Type of the PUS telecommand.
            tc_stype (int): Subtype of the PUS telecommand.
            args (tuple, optional): A tuple of arguments to map to parameter names.
            ackflags (int, optional): Acknowledgment flags for the PUS command.
            monitor (bool, optional): If True, monitor the command completion (default: True).
            acknowledgment (str, optional): Name of the acknowledgment to wait for.
            disable_verification (bool, optional): If True, disable all verification checks (default: False).

        Returns:
            IssuedCommand: The issued command object.
        """

        # Initialize args to empty tuple if None is passed
        args = args or ()

        # Special case: tc_type=17 and tc_stype=1 have no arguments
        if tc_type == 17 and tc_stype == 1:
            if args:
                raise ValueError("Telecommand type 17, subtype 1 does not accept arguments.")
            tc_args = {}
        else:
            # Retrieve parameter names based on tc_type and tc_stype
            parameter_names = get_cparameters(tc_type, tc_stype)
            if not parameter_names:
                raise ValueError(f"No parameters found for type={tc_type}, subtype={tc_stype}")

            # Validate that the number of arguments matches the number of parameters
            if len(parameter_names) != len(args):
                raise ValueError(
                    f"Mismatch: {len(parameter_names)} parameters, but {len(args)} arguments provided."
                )

            # Map arguments to parameter names
            tc_args = dict(zip(parameter_names, args, strict=False))

        # Command setup
        apid_number = get_apid_number(apid)
        command_name = "/MIB/" + get_cname(ccf_type=tc_type, ccf_stype=tc_stype)

        # Set up verification configuration
        verification = VerificationConfig()
        if disable_verification:
            print("Verification Disabled")
            verification.disable()

        try:
            # Issue the base command
            base_command = self.processor.issue_command(
                command_name,
                args=tc_args,
                dry_run=True,
            )

            # Extract PUS data and issue the PUS command
            pus_data = base_command.binary[11:]
            pus_tc = self.processor.issue_command(
                "/TEST/PUS_TC",
                args={
                    "apid": apid_number,
                    "type": tc_type,
                    "subtype": tc_stype,
                    "ackflags": ackflags,
                    "data": pus_data,
                },
                verification=verification,
            )

            # Monitor acknowledgment if specified
            if acknowledgment:
                ack = pus_tc.await_acknowledgment(acknowledgment)
                print(f"Acknowledgment status: {ack.status}")

            # Monitor command completion if requested
            if monitor:
                pus_tc.await_complete()
                if not pus_tc.is_success():
                    print(f"Command failed: {pus_tc.error}")

        except IssuingCommandError as e:
            print(f"Error issuing command: {e}")
            return None

        return pus_tc

    def listen_to_command_history(self) -> ParameterSubscription:
        """
        Listen for updates to the command history and print them when received.
        """

        def tc_callback(rec):  # type: ignore
            print("Command history update:", rec)

        self.processor.create_command_history_subscription(tc_callback)

    def listen_to_telemetry(self, parameter_list: list[str]) -> ParameterSubscription:
        """
        Subscribe to telemetry updates for specified parameters.

        Args:
            parameter_list (list): List of telemetry parameters to subscribe to.
            callback (function): Function to call when telemetry data is received.
        """

        def tm_callback(delivery) -> None:  # type: ignore
            for parameter in delivery.parameters:
                print("Telemetry received:", parameter)

        return self.processor.create_parameter_subscription(parameter_list, tm_callback)

    def receive_container_updates(
        self,
        containers: Union[str, list[str]],
        callback: Optional[Callable[[ContainerData], None]] = None,
    ) -> ContainerSubscription:
        """
        Subscribes to specified containers and processes updates using a callback function.

        Args:
            containers (list of str): A list of container paths to subscribe to. Defaults to
        ['/YSS/SIMULATOR/FlightData', '/YSS/SIMULATOR/Power'] if not provided.
            callback (function): The function to call when data is received. Defaults to printing
        the generation time and hex representation of the packet.

        Example:
        ```
        receive_container_updates(processor)
        ```

        or with a custom callback:
        ```
        receive_container_updates(processor, callback=my_custom_callback)
        ```
        """

        def default_callback(packet):  # type: ignore
            hexpacket = hexlify(packet.binary).decode("ascii")
            print(packet.generation_time, ":", hexpacket)

        # Use the provided callback or the default one if not specified
        self.processor.create_container_subscription(
            containers=containers,
            on_data=callback or default_callback,
        )

    def receive_callbacks_tm_20_1(self) -> None:
        """Shows how to receive callbacks on packet updates."""

        def parse_packet(packet: Any) -> None:
            """Parse the packet starting from [160:-16], extract parameters and their values."""
            # Extract binary data excluding the first 160 bits and last 16 bits (checksum)
            binary_data = packet.binary[20:-2]
            hexpacket = hexlify(binary_data).decode("ascii")
            print(packet.generation_time, ":", hexpacket)

            # Read the first byte to determine the number of parameters
            num_parameters = binary_data[0]
            print(f"Number of parameters: {num_parameters}")

            # Initial offset after reading num_parameters
            offset = 1
            parameters = []

            for _ in range(num_parameters):
                # Extract PARAMETER_ID (32 bits)
                parameter_id = struct.unpack_from(">I", binary_data, offset=offset)[0]
                offset += 4  # Move past the 4 bytes of PARAMETER_ID

                mdb = process_pas_table_and_merge(do_write=False)

                # Look up the name and size from `my_mdb` DataFrame
                name_row = mdb[mdb["ID"] == parameter_id]
                if not name_row.empty:
                    name = name_row.iloc[0]["Name"]
                    size_bits = name_row.iloc[0]["Size (Bits)"]
                    size_bytes = size_bits // 8  # Convert bits to bytes
                else:
                    name = "Unknown"
                    size_bytes = 4  # Default to 4 bytes if size is unknown

                # Extract the value based on size
                if size_bytes == 1:
                    value = struct.unpack_from(">B", binary_data, offset=offset)[0]  # Unsigned byte
                elif size_bytes == 2:
                    value = struct.unpack_from(">H", binary_data, offset=offset)[0]  # Unsigned short
                elif size_bytes == 4:
                    value = struct.unpack_from(">I", binary_data, offset=offset)[0]  # Unsigned int
                elif size_bytes == 8:
                    value = struct.unpack_from(">Q", binary_data, offset=offset)[0]  # Unsigned long long
                else:
                    value = "Unsupported size"

                offset += size_bytes  # Move past the value's size
                parameters.append((parameter_id, name, value))

            # Display the parameters with their values
            for param_id, name, value in parameters:
                print(f"PARAMETER_ID: {param_id}, Name: {name}, Value: {value}")

        # Subscribe to container updates
        self.receive_container_updates(
            containers=["/MIB/ENY_PAR00265"],
            callback=parse_packet,
        )

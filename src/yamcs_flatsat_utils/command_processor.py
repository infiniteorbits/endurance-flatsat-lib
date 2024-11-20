import os
from binascii import hexlify
from collections.abc import Callable
from typing import Optional, Union

import pandas as pd
from yamcs.client import ContainerSubscription, ParameterSubscription, VerificationConfig  # type: ignore
from yamcs.tmtc.model import ContainerData, IssuedCommand  # type: ignore

from lib_utils.addr_apid import get_apid_number
from lib_utils.config import create_commands, get_project_root, read_config
from yamcs_flatsat_utils.yamcs_interface import YamcsInterface


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
    dat_file = f"tc_table_{expected_commit}.dat"

    # Lire le fichier CSV dans un DataFrame
    path_df = os.path.join(get_project_root(), "etc/config/", dat_file)
    df = pd.read_csv(path_df, sep="\t")

    # Filtrer les résultats en fonction de CCF_TYPE et CCF_STYPE
    result = df[(df["CCF_TYPE"] == ccf_type) & (df["CCF_STYPE"] == ccf_stype)]

    # Retourner le nom correspondant s'il existe, sinon une chaîne vide
    return result.iloc[0]["CCF_CNAME"] if not result.empty else ""


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
        create_commands()  # That command creates etc/config/tc_tables.dat

    def issue_command_yamcs(
        self,
        apid: str,
        tc_type: int,
        tc_stype: int,
        tc_args: Optional[dict[str, str]] = None,
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
            tc_args (dict, optional): Command arguments (default: None).
            ackflags (int, optional): Acknowledgment flags for the PUS command.
            monitor (bool, optional): If True, monitor the command completion (default: True).
            acknowledgment (str, optional): Name of the acknowledgment to wait for (e.g., "Acknowledge_Sent").
            disable_verification (bool): If True, disable all verification checks (default: False).
            custom_verification (VerificationConfig, optional): Custom verification configuration.
            dry_run (bool): If True, only simulate the command without sending it.

        Returns:
            IssuedCommand: The issued command object.
        """
        tc_args = tc_args or {}
        apid_number = get_apid_number(apid)
        command_name = "/MIB/" + get_cname(ccf_type=tc_type, ccf_stype=tc_stype)

        # Set up verification configuration
        verification = VerificationConfig()
        if disable_verification:
            print("Verification Disabled")
            verification.disable()

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

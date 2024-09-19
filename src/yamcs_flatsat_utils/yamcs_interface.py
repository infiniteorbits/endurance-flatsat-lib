from binascii import hexlify
from collections.abc import Callable
from typing import Optional

from yamcs.client import (  # type: ignore
    CommandConnection,
    CommandHistorySubscription,
    ContainerSubscription,
    ParameterSubscription,
    YamcsClient,
)
from yamcs.tmtc.model import IssuedCommand  # type: ignore


class YamcsInterface:
    """
    Interface for interacting with Yamcs system, providing methods to send commands and
    subscribe to telemetry and command history.
    """

    def __init__(self, host: str, instance: str, processor_name: str) -> None:
        """
        Initialize the Yamcs client and processor.

        Args:
            host (str): The Yamcs host (e.g., "localhost:8090").
            instance (str): The Yamcs instance (e.g., "simulator").
            processor_name (str): The name of the processor (e.g., "realtime").
        """
        self.client = YamcsClient(host)
        self.processor = self.client.get_processor(instance, processor_name)

    def issue_command(
        self, command_name: str, args: Optional[dict[str, str]] = None, verification: Optional[object] = None
    ) -> IssuedCommand:
        """
        Send a command through Yamcs.

        Args:
            command_name (str): The name of the command to issue.
            args (dict, optional): Command arguments (default: None).
            verification (VerificationConfig, optional): Optional verification configuration (default: None).

        Returns:
            The issued command object.
        """
        if args is None:
            args = {}

        return self.processor.issue_command(command_name, args=args, verification=verification)

    def create_command_connection(self) -> CommandConnection:
        """
        Create a connection for issuing commands.

        Returns:
            A command connection object.
        """
        return self.processor.create_command_connection()

    def create_command_history_subscription(
        self, callback: Callable[[object], None]
    ) -> CommandHistorySubscription:
        """
        Subscribe to command history updates.

        Args:
            callback (function): Function to call when command history updates are received.
        """
        self.processor.create_command_history_subscription(on_data=callback)

    def create_parameter_subscription(
        self, parameter_list: list[str], callback: Callable[[object], None]
    ) -> ParameterSubscription:
        """
        Subscribe to telemetry parameter updates.

        Args:
            parameter_list (list): List of telemetry parameters to subscribe to.
            callback (function): Function to call when telemetry updates are received.
        """
        return self.processor.create_parameter_subscription(parameter_list, on_data=callback)

    def receive_callbacks(
        self, containers: list[str], callback: Optional[Callable[[object], None]] = None
    ) -> ContainerSubscription:
        """
        General method to subscribe to packet updates and handle callbacks.

        Args:
            containers (list): List of container paths to subscribe to.
            callback (function, optional): A custom function to handle packet data.
                                            If None, a default function is used that prints hex data.
        """

        def default_print_data(packet) -> None:  # type: ignore
            """
            Default callback function to print packet data as hex.

            Args:
                packet: The packet object received from the subscription.
            """
            hexpacket = hexlify(packet.binary).decode("ascii")
            print(f"Packet generated at {packet.generation_time}: {hexpacket}")

        # If no custom callback is provided, use the default print function
        if callback is None:
            callback = default_print_data

        return self.processor.create_container_subscription(containers=containers, on_data=callback)

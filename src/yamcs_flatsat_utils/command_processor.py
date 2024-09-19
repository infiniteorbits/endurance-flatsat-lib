from yamcs.client import ParameterSubscription, VerificationConfig  # type: ignore
from yamcs.tmtc.model import IssuedCommand  # type: ignore

from yamcs_flatsat_utils.yamcs_interface import YamcsInterface


class CommandProcessor:
    """
    Command processing abstraction, using YamcsInterface to interact with the Yamcs system.
    Provides higher-level methods for issuing and monitoring commands.
    """

    def __init__(self, yamcs_interface: YamcsInterface) -> None:
        """
        Initialize the CommandProcessor with a YamcsInterface instance.

        Args:
            yamcs_interface (YamcsInterface): An instance of YamcsInterface to interact with Yamcs.
        """
        self.yamcs_interface = yamcs_interface

    def issue_command(self, command_name: str, args: dict[str, str] | None) -> IssuedCommand:
        """
        Send a basic command.

        Args:
            command_name (str): The name of the command to issue.
            args (dict, optional): Command arguments (default: None).

        Returns:
            The issued command object.
        """
        command = self.yamcs_interface.issue_command(command_name, args=args)
        print("Command issued:", command)
        return command

    def issue_command_modify_verification(
        self,
        command_name: str,
        args: dict[str, str] | None,
    ) -> IssuedCommand:
        """
        Send a command with modified verification configuration.

        Args:
            command_name (str): The name of the command to issue.
            args (dict, optional): Command arguments (default: None).

        Returns:
            The issued command object with modified verification.
        """
        verification = VerificationConfig()
        verification.disable("Started")
        verification.modify_check_window("Queued", 1, 5)

        command = self.yamcs_interface.issue_command(command_name, args=args, verification=verification)
        print("Command with modified verification issued:", command)
        return command

    def issue_command_no_verification(self, command_name: str, args: dict[str, str] | None) -> IssuedCommand:
        """
        Send a command without any verification checks.

        Args:
            command_name (str): The name of the command to issue.
            args (dict, optional): Command arguments (default: None).

        Returns:
            The issued command object without verification.
        """
        verification = VerificationConfig()
        verification.disable()

        command = self.yamcs_interface.issue_command(command_name, args=args, verification=verification)
        print("Command without verification issued:", command)
        return command

    def monitor_command(
        self,
        command_name: str,
        args: dict[str, str] | None,
        success_command_name: str,
        success_args: dict[str, str] | None,
    ) -> None:
        """
        Monitor the completion of a command and optionally issue another command if the first succeeds.

        Args:
            command_name (str): The name of the command to issue and monitor.
            args (dict, optional): Command arguments (default: None).
            success_command_name (str, optional): Command to issue if the first command is successful.
            success_args (dict, optional): Arguments for the success command (default: None).
        """
        conn = self.yamcs_interface.create_command_connection()

        command1 = conn.issue(command_name, args=args)
        command1.await_complete()

        if command1.is_success() and success_command_name:
            conn.issue(success_command_name, args=success_args)
        else:
            print("Command failed:", command1.error)

    def monitor_acknowledgment(
        self,
        command_name: list[str],
        args: dict[str, str] | None,
        acknowledgment_type: str = "Acknowledge_Sent",
    ) -> None:
        """
        Monitor the acknowledgment status of a command.

        Args:
            command_name (str): The name of the command to monitor.
            args (dict, optional): Command arguments (default: None).
            acknowledgment_type (str, optional): The acknowledgment type \
                to wait for (default: "Acknowledge_Sent").
        """
        conn = self.yamcs_interface.create_command_connection()

        command = conn.issue(command_name, args=args)
        ack = command.await_acknowledgment(acknowledgment_type)
        print("Acknowledgment received:", ack.status)

    def listen_to_command_history(self) -> ParameterSubscription:
        """
        Listen for updates to the command history and print them when received.
        """

        def tc_callback(rec):  # type: ignore
            print("Command history update:", rec)

        self.yamcs_interface.create_command_history_subscription(tc_callback)

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

        return self.yamcs_interface.create_parameter_subscription(parameter_list, tm_callback)

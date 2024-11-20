from lib_utils.exception import MdbParameterError
from yamcs_flatsat_utils.yamcs_interface import YamcsInterface


class YamcsMDBInterface:
    """
    Extended Yamcs interface for interacting with the Mission Database (MDB).
    Inherits from YamcsInterface and provides methods for querying space systems, parameters, and commands.
    """

    def __init__(self, interface: YamcsInterface) -> None:
        """
        Initialize the CommandProcessor with a Yamcs client instance.

        Args:
            interface (YamcsInterface): An instance of YamcsClient to interact with Yamcs.
        """
        self.mdb = interface.get_mdb()

    def print_space_systems(self) -> None:
        """
        Print all space systems available in the Mission Database (MDB).

        A space system is a hierarchical grouping of parameters, commands, and other data structures,
        typically organized by mission or subsystem.
        """
        for space_system in self.mdb.list_space_systems():
            print(space_system)

    def print_parameters(self, parameter_type: str = "float") -> None:
        """
        Print all parameters of a specific type from the MDB.

        Args:
            parameter_type (str): The type of the parameters to retrieve (default: "float").
                                  Other types can be used such as "int", "string", etc.
        """
        for parameter in self.mdb.list_parameters(parameter_type=parameter_type):
            print(parameter)

    def print_commands(self) -> None:
        """
        Print all commands available in the MDB.

        Commands represent actions that can be issued to a spacecraft or a simulator,
        and are part of the mission database.
        """
        for command in self.mdb.list_commands():
            print(command)

    def find_parameter(self, parameter_name: str) -> None:
        """
        Find and print details of a specific parameter by its name or alias.

        This method searches the MDB for a parameter and prints its details.
        The parameter can be identified by its fully qualified name (e.g., "/YSS/SIMULATOR/BatteryVoltage2")
        or by an alias (e.g., "MDB:OPS Name/SIMULATOR_BatteryVoltage2").

        Args:
            parameter_name (str): The fully qualified name or alias of the parameter.

        Example:
            find_parameter("/YSS/SIMULATOR/BatteryVoltage2")
            find_parameter("MDB:OPS Name/SIMULATOR_BatteryVoltage2")
        """
        try:
            # Attempt to retrieve by fully qualified name
            parameter = self.mdb.get_parameter(parameter_name)
            print(f"Parameter found via qualified name: {parameter}")
        except MdbParameterError as e:
            print(f"Error finding parameter via qualified name: {e}")

        try:
            # Attempt to retrieve by alias if not found by qualified name
            parameter = self.mdb.get_parameter(parameter_name)
            print(f"Parameter found via alias: {parameter}")
        except MdbParameterError as e:
            print(f"Error finding parameter via alias: {e}")

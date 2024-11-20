import warnings
from typing import Optional

from yamcs.client import ArchiveClient, MDBClient, ProcessorClient, YamcsClient  # type: ignore

from lib_utils.config import read_config
from lib_utils.exception import YamcsInterfaceError
from lib_utils.warning import YamcsInterfaceWarning


class YamcsInterface:
    """
    Interface for managing the connection and interaction with the Yamcs system.
    Provides methods to access the processor, MDB, and archive.
    """

    def __init__(
        self, host: Optional[str] = None, instance: Optional[str] = None, processor: Optional[str] = None
    ) -> None:
        """
        Initialize the Yamcs client and processor.

        Args:
            host (str): The Yamcs host (e.g., "localhost:8090").
            instance (str): The Yamcs instance (e.g., "simulator").
            processor (str): The mode of the processor (e.g., "realtime").
        """
        if host and instance and processor:
            warnings.warn(
                f"Creating {instance} instance on {host} host, in {processor} processor",
                YamcsInterfaceWarning,
            )
            self.client = YamcsClient(host)
            self.instance = instance
            self.processor = processor
        elif not host and not instance and not processor:
            default_interface_parameters = read_config({"Interface": ["host", "instance", "processor"]})
            self.instance = default_interface_parameters["Interface.instance"]
            self.host = default_interface_parameters["Interface.host"]
            self.processor = default_interface_parameters["Interface.processor"]

            warnings.warn(
                f"Creating default Yamcs instance: '{self.instance}' on host '{self.host}' "
                f"using processor '{self.processor}'",
                YamcsInterfaceWarning,
            )

            self.client = YamcsClient(self.host)
        else:
            raise YamcsInterfaceError(
                "Parameters 'host', 'instance', and 'processor' should all be defined or all be None."
            )

    def get_processor(self) -> ProcessorClient:
        """
        Get the Yamcs processor associated with the current instance.

        Returns:
            object: The Yamcs processor object.
        """
        return self.client.get_processor(instance=self.instance, processor=self.processor)

    def get_mdb(self) -> MDBClient:
        """
        Get the Mission Database (MDB) associated with the current instance.

        Returns:
            object: The MDB object.
        """
        return self.client.get_mdb(instance=self.instance)

    def get_archive(self) -> ArchiveClient:
        """
        Get the Archive service associated with the current instance.

        Returns:
            object: The Archive object.
        """
        return self.client.get_archive(instance=self.instance)

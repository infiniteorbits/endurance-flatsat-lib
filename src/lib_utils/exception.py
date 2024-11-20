class MdbParameterError(Exception):
    """
    Raised in mdb_utils when the parameter is not found
    """


class YamcsInterfaceError(Exception):
    """
    Raised in yamcs_interface when the interfaces parameters are partially given
    """


class ApidParameterError(Exception):
    """
    Raised in addr_apid when the Apid is not found
    """

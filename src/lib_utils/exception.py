class MdbParameterError(Exception):
    """
    Raised in mdb_utils when the parameter is not found
    """


class YamcsInterfaceError(Warning):
    """
    Raised in yamcs_interface when the interfaces parameters are partially given
    """

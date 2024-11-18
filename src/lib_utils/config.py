import configparser
import os
from pathlib import Path
from typing import Optional

import pandas as pd

ccf_fields = [
    "CCF_CNAME",
    "CCF_DESCR",
    "CCF_DESCR2",
    "CCF_CTYPE",
    "CCF_CRITICAL",
    "CCF_PKTID",
    "CCF_TYPE",
    "CCF_STYPE",
    "CCF_APID",
    "CCF_NPARS",
    "CCF_PLAN",
    "CCF_EXEC",
    "CCF_ILSCOPE",
    "CCF_ILSTAGE",
    "CCF_SUBSYS",
    "CCF_HIPRI",
    "CCF_MAPID",
    "CCF_DEFSET",
    "CCF_RAPID",
    "CCF_ACK",
    "CCF_SUBSCHEDID",
]


def get_project_root() -> Path:
    """get_project_root _summary_

    Returns
    -------
        _description_
    """
    current_path = Path.cwd()
    for parent in current_path.parents:
        if parent.name == "endurance-flatsat-lib":
            return parent
    return current_path


def create_config() -> None:
    """_summary_"""
    config = configparser.ConfigParser()

    # Add sections and key-value pairs
    config["Interface"] = {"host": "localhost:8090", "instance": "myproject", "processor": "realtime"}

    # Define the path to the configuration file in the 'src' directory of the project
    repo_root = get_project_root()
    config_path = os.path.join(repo_root, "etc/config/config.ini")

    # Write the configuration to the file
    with open(config_path, "w", encoding="utf-8") as configfile:
        config.write(configfile)


def read_config(requested_values: Optional[dict] = None) -> dict[str, str]:  # type: ignore
    """
    Reads specified values from a configuration file or prints the entire file if no values are requested.

    Args:
        requested_values (dict, optional): A dictionary where the keys are section names
        and the values are lists of keys to retrieve.
        If None, the entire configuration file is printed.

    Returns:
        dict: A dictionary with the requested configuration values,
        or an empty dictionary if the entire file is printed.
    """
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Define the path to the configuration file in the 'src' directory of the project
    repo_root = get_project_root()
    config_path = os.path.join(repo_root, "etc/config/config.ini")
    # Read the configuration file
    config.read(config_path)

    # If no specific values are requested, print the entire configuration file
    if requested_values is None:
        for section in config.sections():
            print(f"[{section}]")
            for key, value in config.items(section):
                print(f"{key} = {value}")
        return {}

    # Initialize a dictionary to store the retrieved values
    config_values = {}

    # Loop through the requested sections and keys to retrieve values
    for section, keys in requested_values.items():
        for key in keys:
            try:
                # Attempt to get the value for the key in the specified section
                value = config.get(section, key)
                config_values[f"{section}.{key}"] = value
            except (configparser.NoSectionError, configparser.NoOptionError):
                # If the section or key does not exist, you can decide how to handle it
                print(f"Warning: Section '{section}' or key '{key}' not found in the configuration file.")

    return config_values


def create_commands(path: Optional[str] = None) -> None:
    """Function to create correspondance to TC names and pus type"""

    repo_root = get_project_root()

    if path is None:
        ccf_path = repo_root.joinpath("endurance-flight-software/mdb/ccf.dat")
        mdb = pd.read_table(ccf_path, names=ccf_fields, sep="\t")

    else:
        mdb = pd.read_table(path, names=ccf_fields, sep="\t")

    mdb = mdb.dropna(axis=1)
    config_path = repo_root.joinpath("etc/config/tc_table.dat")
    mdb.to_csv(config_path, sep="\t", index=False)

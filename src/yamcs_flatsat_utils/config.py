import configparser
import os
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """get_project_root _summary_

    Returns
    -------
        _description_
    """
    return Path(__file__).parent.parent


def create_config() -> None:
    """_summary_"""
    config = configparser.ConfigParser()

    # Add sections and key-value pairs
    config["Interface"] = {"host": "localhost:8090", "instance": "myproject", "mode": "realtime"}

    # Define the path to the configuration file in the 'src' directory of the project
    repo_root = get_project_root()
    config_path = os.path.join(repo_root, "config.ini")

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
    config_path = os.path.join(repo_root, "config.ini")
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

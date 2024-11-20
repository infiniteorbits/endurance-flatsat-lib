import configparser
import os
import subprocess
from pathlib import Path
from typing import Optional

import pandas as pd


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
    config["Submodule"] = {
        "name": "endurance-flight-software-csw",
        "commit": "3b78dfb94a62796e93abc943db47c63c04389b2e",
    }

    # Define the path to the configuration file in the 'src' directory of the project
    repo_root = get_project_root()
    config_path = os.path.join(repo_root, "config.ini")

    # Write the configuration to the file
    with open(config_path, "w", encoding="utf-8") as configfile:
        config.write(configfile)


def read_config(requested_values: Optional[dict] = None) -> dict[str, str]:  # type: ignore
    """
    Reads specified values from a configuration file or
    prints the entire file if no values are requested.

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


def create_commands(path: Optional[str] = None) -> None:
    """
    Creates a correspondence table for TC names and PUS types.
    The table's filename includes the SHA1 of the submodule commit.

    Parameters
    ----------
    path : Optional[str]
        Custom path to the CCF data file. If not provided, uses the default path
        derived from the submodule and configuration.
    """
    repo_root = get_project_root()
    config = read_config({"Submodule": ["name", "commit"]})

    submodule_name = config["Submodule.name"]
    expected_commit = config["Submodule.commit"]
    submodule_path = repo_root / submodule_name

    # Validate submodule path and commit
    if not submodule_path.exists() or not submodule_path.is_dir():
        raise FileNotFoundError(f"Submodule path does not exist: {submodule_path}")

    current_commit = get_submodule_commit(submodule_path)
    if current_commit != expected_commit:
        raise ValueError(f"Submodule commit mismatch. Expected: {expected_commit}, Found: {current_commit}")

    # Name of the TC table file with the commit SHA1
    tc_table_name = f"tc_table_{current_commit}.dat"
    tc_table_path = repo_root / "etc" / "config" / tc_table_name

    # Check if the table already exists
    if tc_table_path.exists():
        print(f"TC table already exists: {tc_table_path}")
        return

    # Determine the path to the CCF file
    if path is None:  # noqa: SIM108
        ccf_path = submodule_path / "mdb" / "ccf.dat"
    else:
        ccf_path = Path(path)

    if not ccf_path.exists():
        raise FileNotFoundError(f"CCF file not found at: {ccf_path}")

    ccf_fields = get_fields("ccf")

    # Read and process the CCF data
    print(f"Reading CCF data from: {ccf_path}")
    mdb = pd.read_table(ccf_path, names=ccf_fields, sep="\t").dropna(axis=1)

    # Save the processed data with the commit SHA1 in the filename
    tc_table_path.parent.mkdir(parents=True, exist_ok=True)
    mdb.to_csv(tc_table_path, sep="\t", index=False)

    print(f"TC table created at: {tc_table_path}")


def get_submodule_commit(submodule_path: Path) -> str:
    """
    Retrieves the current commit hash of the specified submodule.

    Parameters
    ----------
    submodule_path : Path
        The path to the submodule directory.

    Returns
    -------
    str
        The commit hash of the submodule.
    """
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=submodule_path, text=True).strip()
        return commit
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to retrieve the commit for the submodule: {submodule_path}") from e


def get_fields(name: str) -> list[str]:
    """
    Reads a list of fields from a configuration file located in the 'etc/config' directory.

    Parameters
    ----------
    name : str
        The base name of the field file (e.g., "ccf" will look for "ccf_fields.ini").

    Returns
    -------
    list[str]
        A list of fields specified in the configuration file.

    Raises
    ------
    FileNotFoundError
        If the configuration file does not exist.
    RuntimeError
        If the configuration file is malformed or missing the 'fields' key.
    """
    repo_root = get_project_root()
    config_dir = repo_root / "etc" / "config"
    config_file = config_dir / f"{name}_fields.ini"

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        fields = config.get(f"{name.upper()}_FIELDS", "fields").split(", ")
        return fields
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        raise RuntimeError(
            f"Failed to load fields from {config_file}."
            f"Ensure it contains a '{name.upper()}_FIELDS' section with a 'fields' key."
        ) from e

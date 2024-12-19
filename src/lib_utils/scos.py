import csv

from yamcs.client import YamcsClient  # type: ignore


def process_pcf_file(
    parameter_id: str,
    input_file: str,
    output_file: str,
    yamcs_host: str = "localhost:8090",
    yamcs_instance: str = "myproject",
) -> None:
    """
    Modifies a PCF file by replacing column values based on enum mappings from a Yamcs parameter.

    :param parameter_id: The parameter ID to fetch enum values from (e.g., "/MIB/JCTD0022").
    :param input_file: Path to the input PCF file.
    :param output_file: Path to save the modified PCF file.
    :param yamcs_host: (Optional) The host and port of the Yamcs server (default: "localhost:8090").
    :param yamcs_instance: (Optional) The Yamcs instance name (default: "myproject").
    """
    # Connect to Yamcs and fetch parameter details
    client = YamcsClient(yamcs_host)
    mdb = client.get_mdb(instance=yamcs_instance)
    para_id = mdb.get_parameter(parameter_id)
    print(para_id)

    # Create a mapping from enum labels to values
    hk_id = {ev.label: ev.value for ev in para_id.enum_values}
    print(hk_id)

    # Process the input file and write to the output file
    with (
        open(input_file, "r", encoding="utf-8") as infile,
        open(output_file, "w", newline="\n", encoding="utf-8") as outfile,
    ):
        reader = csv.reader(infile, delimiter="\t")
        writer = csv.writer(outfile, delimiter="\t", lineterminator="\n")
        for row in reader:
            if row[1] in hk_id:
                row[2] = hk_id[row[1]]
            writer.writerow(row)

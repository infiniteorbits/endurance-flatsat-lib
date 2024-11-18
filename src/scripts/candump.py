import sys

from candump_utils.can_id import write_candump_line
from candump_utils.data_field_tc import process_data_field_tc
from candump_utils.data_field_tm import process_data_field_tm
from candump_utils.packet_header import process_first_message_data


def decode_can_ts() -> None:
    """main _summary_

    Raises
    ------
    ValueError
        _description_
    """
    cpt = 0
    for line in sys.stdin:
        line = line.strip()
        print("#-----------------------------------------------------------#")
        print(line)

        # Call write_candump_line for each line
        can_id, supervisor = write_candump_line(line)  # type: ignore
        sbr = can_id["sbr_type"]

        if supervisor:
            print("/**-------------------------SUPERVISOR-------------------------**/")
            continue

        # For the first line, process the first message and get the length
        if (sbr == "Set Block Request") & (can_id["sb_type"] != "Unsolicited Telemetry"):
            packet_header = process_first_message_data(line)
            tmtc = packet_header["str_type"]  # type: ignore

        # For the second line, process the TM data field
        elif sbr == "Transfer":
            if tmtc == "TM":
                if cpt == 0:
                    process_data_field_tm(line)
                    cpt += 1
            elif tmtc == "TC":
                if cpt == 0:
                    process_data_field_tc(line)
                    cpt += 1
            else:
                raise ValueError
        else:
            cpt = 0

        print("#-----------------------------------------------------------#\n")


def main() -> None:
    """main _summary_"""
    decode_can_ts()


if __name__ == "__main__":
    main()

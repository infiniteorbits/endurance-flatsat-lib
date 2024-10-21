import sys

from candump_utils.can_id import write_candump_line
from candump_utils.data_field_tc import process_data_field_tc
from candump_utils.data_field_tm import process_data_field_tm
from candump_utils.packet_header import process_first_message_data

cpt = 0

for line in sys.stdin:
    line = line.strip()
    print("#-----------------------------------------------------------#")
    print(line)

    # Call write_candump_line for each line
    can_id, supervisor = write_candump_line(line)
    sbr = can_id["sbr_type"]

    if supervisor:
        print("/**-------------------------SUPERVISOR-------------------------**/")
        continue

    # For the first line, process the first message and get the length
    if sbr == "Set Block Request":
        x, _ = write_candump_line(line, doplot=False)
        nb_blocks = int(x["block_to_transfert"])

        packet_header = process_first_message_data(line)
        tmtc = packet_header["str_type"]

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

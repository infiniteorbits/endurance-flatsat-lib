# Yamcs-client

All of these examples run against a simulation that is used to develop and demo Yamcs. This setup is linked to a simple simulator which emits TM in the form of CCSDS packets and accepts a few telecommands as well.
## Force APID

Issue command is from basis with command name, without choosing the apid, or the ackflags. See how to do instead

```python
from yamcs.client import YamcsClient
import struct


client = YamcsClient("localhost:8090")
processor = client.get_processor("myproject", "realtime")

command = processor.issue_command("/MIB/JCC45006", args={"JCPD0009": 3, "JCPD0010": "EiPrRe"}, dry_run=True)

print(f"MIB cmd binary:  {command.binary.hex()}")
raw_tc = processor.issue_command("/TEST/RAW_TC", args={"data": command.binary})

print(f"raw_cmd binary:  {raw_tc.binary.hex()}")

pus_data = command.binary[11:]
pus_tc = processor.issue_command("/TEST/PUS_TC", args={"apid": 1, "type": 5, "subtype": 5, "ackflags": 0, "data": pus_data})

print(f"pus_cmd binary:  {pus_tc.binary.hex()}")

#make a writable copy
pus_data = bytearray(command.binary[11:])
struct.pack_into('>H', pus_data, 0, 0xABCD)
pus_tc = processor.issue_command("/TEST/PUS_TC", args={"apid": 1, "type": 5, "subtype": 5, "ackflags": 0, "data": pus_data})
print(f"modified binary: {pus_tc.binary.hex()}")
```


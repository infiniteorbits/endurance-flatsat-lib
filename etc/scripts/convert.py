import binascii
import os
import struct


def convert_elf_to_bin(elf_file, output_bin):
    """convert_elf_to_bin _summary_

    Parameters
    ----------
    elf_file
        _description_
    output_bin
        _description_
    """
    # Step 1: Read the ELF file and write the binary content directly
    try:
        with open(elf_file, "rb") as elf, open(output_bin, "wb") as bin_out:
            data = elf.read()
            bin_out.write(data)
        print(f"[OBJCOPY] Conversion complete: {output_bin}")
    except OSError as e:
        print(f"Error reading or writing files: {e}")
        return

    # Step 2: Add header and process the binary for packaging
    try:
        with open(output_bin, "r+b") as f:
            size = os.path.getsize(output_bin)
            data = f.read(size)
            crc = binascii.crc32(data) & 0xFFFFFFFF

            # Write header (magic number, size, CRC)
            f.seek(0)
            f.write(struct.pack("<L", 0x4E4F454C))  # Magic number
            f.write(struct.pack("<L", size))  # Size
            f.write(struct.pack("<L", crc))  # CRC

            # Write the original data again after the header
            f.write(data)

            # Expand to multiple of 1536 bytes
            remainder = (size + 12) % 1536
            if remainder != 0:
                f.write(bytes([0] * (1536 - remainder)))

        print("Packaging complete.")
    except OSError as e:
        print(f"Error during file processing: {e}")


# Example usage:
# convert_elf_to_bin("mission_sw_v_0_2.elf", "csw-FS.bin")

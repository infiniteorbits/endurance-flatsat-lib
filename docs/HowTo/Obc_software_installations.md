# OBC Software Installations
## Setup Instructions

This is split into two steps:  
1. First, GRMON3 and FlashPro5 need to be set up so we can communicate with the board.  
2. After that, the RTEMS SDK can be set up.

---

## GRMON3 Setup

GRMON3 can be downloaded from Cobham Gaisler's webpage (username and password are attached to the hardware license key): [GRMON3 Download](https://www.gaisler.com/index.php/downloads/debug-tools).

Follow the installation guide in the GRMON3 documentation. Don’t forget to set up the Sentinel license key driver.

### Installation 
Follow these steps to install GRMON. Detailed information can be found further down. 
1. **Extract** the archive 
2. **Install** the Sentinel LDK Runtime (GRMON Pro version) 
3. **Install** the Java runtime environment 11 
4. *Optionally* install third-party drivers for the debug interfaces. 
5. *Optionally* setup the path for shared libraries (Linux only) 
6. *Optionally* add GRMON to the environment variable PATH

Once it works, the bin folder should be added to your system's `PATH` variable. For example, if you extract it under `/home/buildbot/grmon-pro-3.2.17`, you can add this to your `~/.profile` or `~/.bashrc` (depending on your distribution):

```bash
PATH="$PATH:/home/buildbot/grmon-pro-3.2.17/linux/bin64"
```

---

## FlashPro5 Setup

To use the FlashPro5 programmer, you need to add a rule to `udev` so that it can be used without root privileges. On Ubuntu, this can be done by following these steps:

1. Create a file `/etc/udev/rules.d/99-FlashPro5.rules` with the following two lines:

```bash
SUBSYSTEM=="usb",DRIVERS=="ftdi_sio",ATTRS{interface}=="FlashPro5",RUN+="/bin/sh -c 'echo -n %k >/sys/bus/usb/drivers/ftdi_sio/unbind'"
SUBSYSTEM=="usb",ATTR{idProduct}=="2008",ATTR{idVendor}=="1514",MODE="0660",GROUP="20",SYMLINK+="FlashPro5"
```

**Note**: You will need root privileges to create this file.

2. Execute the following commands:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

**Note**: If you still can’t use the FlashPro5 programmer without root privileges, you may need to unplug and replug the programmer.

Once the FlashPro5 programmer can be used with normal user privileges, its serial number has to be determined. Without it, GRMON3 will just select the first FTDI-based serial device it can find. To retrieve the serial number, execute the following command:

```bash
grmon -ftdi -jtaglist
```

You should get output similar to this:

```
GRMON debug monitor v3.2.13 64-bit pro version  
Copyright (C) 2021 Cobham Gaisler - All rights reserved.  
For latest updates, go to http://www.gaisler.com/  
Comments or bug-reports to support@gaisler.com  

NUM  NAME                SERIAL  
1)   SKY-EGSE-LINK2 A    0621-000017A  
2)   SKY-EGSE-LINK2 B    0621-000017B  
3)   PicoSkyDebugSPI A   FT61L0YQA  
4)   PicoSkyDebugSPI B   FT61L0YQB  
5)   FlashPro5 A         01541KRT  
```

Use `-jtagcable <num>`, or `-jtagserial <sn>`, to select the cable. Even though the device can be selected by number, it should ideally be selected only by serial, as numbers can change depending on the number of devices connected to the PC.

Based on the above output, you can use the FlashPro5 programmer with the following command:

```bash
grmon -ftdi -jtagserial 01541KRT
```

---

## Installation Guide for Skylabs NANOhpm-OBC

### 1. Download and Extract Application Code

- Download `NANO_hpm_application_code.zip` from [CSWxIO/OBC&SkyLabs Information](https://drive.google.com/drive/folders/1oFkO6h9tL5cpfq3l_QFWWIBa1U-LH-5j).
- Unzip the file to your desired location.

### 2. Install RTEMS SDK

- Extract `rtems-noel-1.0.4-2022-07-05-14-00-toolchain-ubuntu-22.04.tar.bz2` to your home folder. You can find it here: [Nano-HPM-zip](https://drive.google.com/file/d/1Ny_-3nRZRY5-i6MD_pVNblY0_wXvLkzy/view?usp=drive_link).
- Add its bin folder to the system `PATH` variable. For example, if you extracted it under `/home/buildbot/rtems-noel-1.0.4`, you can add the following to your `~/.profile` or `~/.bashrc`:

```bash
PATH="$PATH:/home/buildbot/rtems-noel-1.0.4/bin"
```

**Note**: The RTEMS SDK from the Gaisler webpage supports only 4 UART devices without interrupts. Skylabs' variant of the RTEMS SDK is rebuilt to support 6 UART devices with interrupts.

### 3. Add Path to Profile

Add the following line to your `.profile` file to ensure the SDK is always available:

```bash
if [ -d "$HOME/path/to/rtems-noel-1.0.4/bin/" ]; then
    PATH="$PATH:$HOME/path/to/rtems-noel-1.0.4/bin"
fi
```

### 4. Install Required Dependencies

Install the `device-tree-compiler` package:

```bash
sudo apt-get install device-tree-compiler
```

### 5. Build the Software Application

- Navigate to the `hpm-riscv` folder in the extracted application code.
- Run one of the following commands to build the project:

  ```bash
  make TARGET=Debug all
  ```

  or

  ```bash
  make TARGET=Release all
  ```

- A folder (`Debug` or `Release`) should be generated, containing the application binaries.

### Useful Guides

- [How to flash the Mission OBC] (insert link here)

- - -
## Critical software installation on RAM OBC

1.  `grmon -ftdi -jtagcable 7 -ucli 5 (Select the appropriate JTAG cable, ucli 5 redirects the uart to the terminal for prints)`
2.  `load mission_sw_v_0_1.elf (loads the elf into RAM)`
3.  `dtb hpm-riscv.dtb (Selects the DTB to use)`
4.  `dtb load (loads the DTB into the stack)`
5.  `run`
## Critical software installation on Flash memory

1.  `grmon -ftdi -jtagcable 7 -ucli 5 (Select the appropriate JTAG cable, ucli 5 redirects the uart to the terminal for prints)`
2.  `load mission_sw_v_0_1.elf (loads the elf into RAM)`
3.  `dtb hpm-riscv.dtb (Selects the DTB to use)`
4.  `dtb load (loads the DTB into the stack)`
5.  `run`

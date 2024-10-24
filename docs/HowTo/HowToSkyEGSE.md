# How to install Skylab GUI

## Introduction

skyEGSE-GUI application enables user immediate out of the box control, monitor and management of any SkyLabs equipment. skyEGSE-GUI application is a graphical user interface developed on top of powerful NANOsky CMM SDK Application Library module. Application establish connection with target equipment via skyEGSE-LINK2 or skyEGSE-comm, and provides features as:

- Equipment general status overview
- Equipment real-time TM monitoring in charts and export function
- Provides TC for controlling all equipment functions
- Downloading equipment logs
- Equipment parameterisation
- Equipment FW upgrade function
- Execution of customised TM/TC

- - -
## Installation

1. Download the zip file from [cloud-skylab](https://cloud.skylabs.si/d/s/ysb1MxxZKMflwU8uLduIYSGHEK1AV7x5/FQV0Oh0CMYNqj7eimEeY1jbh-j3OUsqz-cb1A3az1bws).
2. Make the script executable:
   ```bash
   chmod u+x skyEGSE-GUI-start.sh
   ```
3. Run the script with superuser privileges:
   ```bash
   sudo bash skyEGSE-GUI-start.sh
   ```
4. **Connect** to the OBC.
5. In *Settings/Options/Can Stack*:
   1. Enable *Can-TS*.
   2. Enable *Can-Open*.
   3. Set *Can-TS address* to `0x7f`.
   4. Enable *Auto switch bus*.
   5. Enable *Auto detect devices*.
6. Click on *nano HPM OBC*.
7. Go to the *Control* tab.
8. Select the *Mass Memory Read/Write* tab.
9. In *Address*, choose *NAND with EDAC*.
10. Check *[ ] from file* for writing.
11. Select the binary file to use.
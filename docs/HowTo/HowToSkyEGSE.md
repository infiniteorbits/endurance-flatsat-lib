# How to Install and Configure skyEGSE-GUI for Skylab Equipment

### Introduction

The **skyEGSE-GUI** application provides an out-of-the-box solution for the control, monitoring, and management of any SkyLabs equipment. This GUI, developed on top of the powerful **NANOsky CMM SDK Application Library module**, enables connection to target equipment via **skyEGSE-LINK2** or **skyEGSE-comm** and includes features such as:

- Equipment status overview
- Real-time telemetry (TM) monitoring with charting and export options
- Telecommand (TC) capabilities for full equipment control
- Log download functionality
- Equipment parameter configuration
- Firmware upgrade support
- Execution of custom TM/TC sequences

---

### Part 1: Installing flight software on flash

#### Installation Steps

1. **Download** the installation zip file from [cloud-skylab](https://cloud.skylabs.si/d/s/ysb1MxxZKMflwU8uLduIYSGHEK1AV7x5/FQV0Oh0CMYNqj7eimEeY1jbh-j3OUsqz-cb1A3az1bws).
2. **Make the installation script executable** by running:
   `chmod u+x skyEGSE-GUI-start.sh`
3. **Run the script with superuser privileges**:
   `sudo bash skyEGSE-GUI-start.sh`
4. **Connect** to the Onboard Computer (OBC).
5. In **Settings > Options > Can Stack**:
   - Enable *Can-TS*.
   - Enable *Can-Open*.
   - Set *Can-TS address* to `0x7f`.
   - Enable *Auto switch bus*.
   - Enable *Auto detect devices*.
6. Select *nano HPM OBC*.
7. Navigate to the **Control** tab.
8. In **Mass Memory Read/Write**, choose:
   - *Address*: Select *NAND with EDAC*.
   - *Write Option*: Check the box for *[ ] from file*.
9. **Choose the binary file** for installation.

---

## Part 2: Managing the NANOhpm-OBC Supervisor Heartbeat

### Context

The **NANOhpm-OBC** contains an application core executing mission-specific functions and a supervisor monitoring the application’s status. These components operate independently as distinct nodes on the CANbus. By default, the supervisor sends a heartbeat signal at 1 Hz, which is helpful for testing but can be disabled for in-flight operations to prevent dependency on the supervisor.

The following guide explains how to disable and enable the NANOhpm-OBC supervisor heartbeat.

### Disabling the Heartbeat

1. **Connect to the NANOhpm-OBC** using **skyEGSE-link2**.
2. Right-click on the OBC icon in the right-hand panel and select **HPM-SM > Emergency Mode** to set the OBC to emergency mode. Power consumption should reduce to around 250 mA.
3. **Verify** the emergency mode by refreshing parameters on the dashboard.
4. In the **Parameters** panel, set:
   - *Redundancy master address* to 0
   - *Receive period* to 0
   - *Transmit period* to 0
5. **Send settings** to both the primary and secondary devices.
6. **Reset the supervisor** by right-clicking on the NANOhpm-OBC icon and selecting **HPM-SM > Software Reset**.

After this, the supervisor should stop sending heartbeat signals on the CANbus.

> **Note:** The skyEGSE-GUI may experience connection issues after this change. To reconnect to the NANOhpm, perform **two power cycles** to re-establish detection.

### Enabling the Heartbeat

To re-enable the heartbeat, repeat the previous steps for disabling, but set the following parameters:

1. **Set the OBC to emergency mode**.
2. Update parameters on the dashboard.
3. In the **Parameters** panel, set:
   - *Redundancy master address*: 0 (default)
   - *Receive period*: 0 (default)
   - *Transmit period*: 2000 (default)
4. **Send settings** to both the primary and secondary devices.
5. **Reset the software**.

The heartbeat signal should resume, and any GUI connection instability should resolve.

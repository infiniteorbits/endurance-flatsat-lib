# Yamcs-interface

*Requirements: Java and Maven*

1. Navigate to the yamcs-io directory.
2. Run the following command to install dependencies and compile:

```
mvn install
```
- - -
## ygw-io
*Requirements: Rust*

1. Navigate to the ygw-io directory.
2. Use Cargo to build the project:

```
cargo build
```
- - -
## ygw-can-ts
*Requirements: Rust*

1. Navigate to the ygw-io directory.
2. Use Cargo to build the project:

```
cargo build
```
- - -
## Running
## Set up Can

If you want to use a real CAN interface (instead of a virtual one like `vcan0`), you can follow these steps:

1. **Bring up the CAN interface** (replace `can0` with your actual CAN device name):
   ```bash
   sudo ip link set can0 up type can bitrate 500000
   ```

   In this example, the bitrate is set to 500 kbps. Adjust the bitrate as needed for your setup.

2. **Capture and display CAN messages on the real CAN interface**:
   ```bash
   candump can0
   ```

Make sure your CAN interface (`can0`) is properly connected to a CAN network and the appropriate bitrate is configured to match the network.
- - -
## Run Yamcs interface

To start both the Yamcs server and the gateway, execute the following scripts in the root directory:

```
./start-yamcs.sh
./start-ygw.sh
```


---

# Yamcs-based Checkout System for Infinite Orbits Endurance Mission

*Required* : rust, jdk, libudev-dev

This repository contains the necessary configuration and code for running the Yamcs-based checkout system for the Infinite Orbits Endurance mission.

## Directory Overview

- **yamcs-io**  
  Contains the Yamcs configuration for Infinite Orbits. The configuration files are located in `src/main/yamcs`. The Yamcs version is specified in `pom.xml` and is retrieved from the public Maven repository. The configuration also integrates `yamcs-mqtt` and `yamcs-ygw` links, which are non-standard and also pulled from Maven.

- **ygw-can-ts**  
  A Rust implementation of the CAN-TS protocol. Once completed, this will be published on crates.io and used as an external dependency.

- **ygw-io**  
  Yamcs gateway configuration for Infinite Orbits, which utilizes the `ygw-can-ts` library to implement a mission-specific link. It pulls the Yamcs gateway framework from crates.io.

- **drawings**  
  Contains system diagrams, including the one shown above.

## Compiling

### yamcs-io
*Requirements: Java, Maven*

1. Navigate to the `yamcs-io` directory.
2. Install dependencies and compile the project by running:
   ```bash
   mvn install
   ```

### ygw-io
*Requirements: Rust*

1. Navigate to the `ygw-io` directory.
2. Build the project using Cargo:
   ```bash
   cargo build
   ```

### ygw-can-ts
*Requirements: Rust*

1. Navigate to the `ygw-can-ts` directory.
2. Build the project using Cargo:
   ```bash
   cargo build
   ```

## Running the System

### Starting the Yamcs Server and Gateway

To start the Yamcs server and the gateway, run the following scripts from the root directory:

```bash
./start-yamcs.sh
./start-ygw.sh
```

### Setting Up the CAN Interface

If you want to use a physical CAN interface instead of a virtual one (like `vcan0`), follow these steps:

1. **Activate the CAN Interface**  
   Replace `can0` with your actual CAN device name. Set the bitrate according to your network:
   ```bash
   sudo ip link set can0 up type can bitrate 10000
   ```

2. **Monitor CAN Traffic**  
   To display CAN messages on your CAN interface:
   ```bash
   candump can0
   ```

Make sure your CAN interface is correctly connected to a CAN network, and the bitrate matches your setup.

## Configure Radio in yamcs
In the folder ygw-io :

### VCAN

```
tcp_addr:
  host: 0.0.0.0
  port: 7897


can_ts_links:
 - name: RADIO_A
   can_ts_device: vcan0
   # own CAN-TS address
   addr: 1
   # address where the TC are sent to
   # note that messages are accepted from everywhere
   obc_addr: 0
 - name: RADIO_B
   can_ts_device: vcan0
   obc_addr: 1
   addr: 0   
```

### Can

```yaml
can_ts_links:
 - name: RADIO_A
   can_ts_device: can0
   # own CAN-TS address
   addr: 20
   # address where the TC are sent to
   # note that messages are accepted from everywhere
   obc_addr: 0
```
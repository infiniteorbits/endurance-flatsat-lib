# How to Set Up and Test a New MDB in Yamcs

This guide will walk you through integrating SCOS2000-based Mission Database (MDB) files with Yamcs. For additional reference, see the [SCOS2k manual](https://ia903400.us.archive.org/11/items/manualzilla-id-5725182/5725182.pdf).

---

## Prerequisites:

### Install Maven

Yamcs uses Maven for dependency management and to run the server. To install Maven, follow the instructions for your operating system:

1. **Ubuntu/Debian**:
   ```bash
   sudo apt update
   sudo apt install maven
   ```

2. **macOS** (with Homebrew):
   ```bash
   brew install maven
   ```

3. **Windows**: Download [Maven](https://maven.apache.org/download.cgi), extract it, and add the `bin` directory to your PATH.

Verify the installation:
   ```bash
   mvn -version
   ```

### Install Java 17

You can install Java 17 with the following command:
```sudo apt install openjdk-17-jdk```

If you have more than one Java version installed, you can pick the one you want to use with the following command:
```sudo update-alternatives --config java```

---

## Project Structure for MDB Integration

Clone the Yamcs quick start repo"
```git clone https://github.com/yamcs/quickstart.git myproject```

For more information, refer to the [Yamcs Getting Started guide](https://yamcs.org/getting-started).

Make sure your project has the following organization for smooth MDB integration with Yamcs:

```
myproject/
|-- README.md
|-- pom.xml
|-- simulator.py
|-- src
|   `-- main
|       |-- java
|       |   `-- com
|       |       `-- example
|       |           `-- myproject
|       |               |-- MyCommandPostprocessor.java
|       |               `-- MyPacketPreprocessor.java
|       `-- yamcs
|           |-- etc
|           |   |-- processor.yaml
|           |   |-- yamcs.myproject.yaml
|           |   `-- yamcs.yaml
|           `-- mdb
|               `-- xtce.xml
`-- testdata.ccsds
```

---

### Steps to Add a New MDB

1. **Place the MDB Files**  
   Copy your MDB files into `myproject/src/main/yamcs/mdb`.

2. **Configure Yamcs for MIB Loading**  
   Edit `myproject/src/main/yamcs/etc/yamcs.myproject.yaml` to specify the MIB loader in the `mdb` section:

   ```yaml
   mdb:
      - type: "org.yamcs.scos2k.MibLoader"
        args:
           path: "mdb/Scos2k_v0_2"
           TM:
             vblParamLengthBytes: 1
             typeOffset: 7
             subTypeOffset: 8
             pus1DataOffset: 20
           TC:
             vblParamLengthBytes: 0
   ```

3. **Add the Dependency**  
   In `myproject/pom.xml`, add the SCOS2k dependency in the `<dependencies>` section:

   ```xml
   <dependency>
      <groupId>org.yamcs</groupId>
      <artifactId>yamcs-scos2k</artifactId>
      <version>0.4.1</version>
   </dependency>
   ```

4. **Run Yamcs**  
   From your project directory, start Yamcs with Maven:

   ```bash
   cd myproject/
   mvn yamcs:run
   ```
# SSH Connection to FlatSat PC
## Introduction

This How To explains how to connect your computer (**client**) to the FlatSat PC (**server**) via SSH connection.

**Note:** currently, SSH connection is only supported if the client is on the same network as the server.

---

## Steps to configure the SSH connection on the client

1. **Instal OpenSSH:** to install the OpenSSH client application, run the following command:
```bash
sudo apt install openssh-client
```

2. **Generate SSH key:** to generate an SSH key, run the following command and follow the instructions (if you already have an SSH key, jump to the next step):
```bash
ssh-keygen -t rsa
```
This command  will generate a public key and a private key which will be stored in the ```~/.ssh/``` folder.

3. **Copy the public key to the FlatSat PC server:** to copy your key to the FlatSat PC, run the following command:
```bash
ssh-copy-id infinite-orbits@192.168.1.10
```
If this is the first time you try to connect to the server via SSH, you will need to enter the server password for the infinite-orbits user. If this is successful, from this point forward, you will not need to enter the password again.

---

## Connect to the server
If you already configured OpenSSH on the client and already copied the public key to the server, you just need to enter the following command to connect to the server:
```bash
ssh infinite-orbits@192.168.1.10
```
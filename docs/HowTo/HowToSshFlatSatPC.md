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
- - -
## Summary: Using the SSH `config` File

The `~/.ssh/config` file simplifies and automates SSH connections by allowing you to configure host-specific settings. Here's an overview of how to use it effectively:

---

### **Basic SSH Configuration Structure**

```ssh
Host <alias>
    HostName <address_or_IP>
    User <username>
    Port <port_number>
    IdentityFile <path_to_private_key>
```

- **Host**: Alias used in SSH commands.
- **HostName**: Host address or IP.
- **User**: Username for the connection.
- **Port**: (Optional) Port to use (default: 22).
- **IdentityFile**: (Optional) Path to the private key.

---

### **Complete Example**

```ssh
Host myserver
    HostName 192.168.1.100
    User romain
    Port 2222
    IdentityFile ~/.ssh/id_rsa_myserver
```

Simplified connection:

```bash
ssh myserver
```

---

### **Advanced Configuration**

- **Configure multiple hosts with patterns**:
    
    ```ssh
    Host *.example.com
        User romain
        IdentityFile ~/.ssh/id_rsa_example
    ```
    
- **Use a proxy jump**:
    
    ```ssh
    Host internal-host
        HostName 10.0.0.5
        User romain
        ProxyJump jumphost
    ```
    

---

### **Useful Commands**

- **Test the configuration**:
    
    ```bash
    ssh -T myserver
    ```
    
- **Reload the SSH agent**:
    
    ```bash
    ssh-add ~/.ssh/id_rsa
    ```
    

---

By setting up a well-configured `config` file, you can avoid specifying connection details every time you use SSH.

## SFTP connection to the Flatsat

In **Files**, select **Other Location**, and in **enter the server address...** :

```
sftp://<user>@192.168.1.10
```

## VNC connection to the Flatsat

### Summary: Using Remmina for Remote Desktop on Ubuntu

Remmina is a remote desktop client that supports various protocols, including VNC, RDP, SSH, and more. Here's a guide to set up and use Remmina for remote desktop access.

---

#### **1. Install Remmina**

To install Remmina and its plugins on Ubuntu:

```bash
sudo apt update
sudo apt install remmina remmina-plugin-rdp remmina-plugin-vnc
```

---

#### **2. Launch Remmina**

- Open Remmina from the application menu or by running:
    
    ```bash
    remmina
    ```
    

---

#### **3. Set Up a Remote Desktop Connection**

1. **Create a New Connection**:
    
    - Click the "New Connection Profile" button.
    - Fill in the required fields:
        - **Name**: Name your connection.
        - **Protocol**: Choose the appropriate protocol (e.g., RDP, VNC, SSH).
        - **Server**: Enter the remote server's IP or hostname.
        - **Username**: Enter the remote user’s username.
        - **Password**: (Optional) Save the password for automatic login.
2. **Customize Connection Settings**:
    
    - Adjust options like resolution, color depth, and security settings based on your needs.
3. **Save and Connect**:
    
    - Save the profile and double-click to connect.

---

#### **4. Using SSH Tunnels (Optional)**

To secure your connection, you can tunnel it over SSH:

- Enable **SSH Tunnel** in the connection settings.
- Provide the SSH server address, username, and password.

---

#### **5. Manage and Edit Connections**

- **View saved connections** in the main window.
- **Edit existing profiles** by right-clicking and selecting "Edit."
- **Delete profiles** if no longer needed.

---

Remmina offers a simple and flexible way to access remote desktops across different protocols, making it a great tool for managing multiple remote connections.
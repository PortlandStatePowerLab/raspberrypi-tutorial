# raspberrypi-tutorial
General description of setting up a Raspberry Pi for project development.
## Headless Setup
A Headless setup means you don't need to use a moniotor to setup the raspberry pi. Setting up a raspberry pi from scratch is detailed [headless pi setup](https://desertbot.io/blog/headless-pi-zero-w-wifi-setup-windows). While the setup is specific to windows, each step is applicable to any operating system. I have highlighted the important components, but you should follow the more detailed post for specifics.

- Download [Raspbian Lite](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-03-25/2021-03-04-raspios-buster-armhf-lite.zip)
- Download and install an imagining software. We used [balena etcher](https://www.balena.io/etcher/) referenced in the headless pi setup tutorial.
- Enable SSH by creating a blank ssh file in root folder
- Add Networking Info by creating a wpa_supplicant.conf file in the root directory and filling in the required fields. 
- **No need to install Bonjour** we will just log into the local router to determine raspi ip address.
- Eject disk and boot the raspberry pi
- Log into local router and get raspi ip address
  - Open browser and go to 192.168.0.1 or 192.168.1.1 which are the default router ip address
  - Log in to router dashboard
    - Username: admin
    - Password: password
  - Select wifi devices and record raspi ip address
- SSH into raspi from the terminal using `ssh pi@<ip address>` with password *raspberry*

## Setup Using a Monitor
If you would prefer to use a monitor rather than do a headless setup, the steps are fairly similar.

- Download [Raspbian Lite](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-03-25/2021-03-04-raspios-buster-armhf-lite.zip)
- Download and install an imagining software. We used [balena etcher](https://www.balena.io/etcher/) referenced in the headless pi setup tutorial.
- Insert the SD card into the raspberry pi and connect a monitor via micro USB and a keyboard.
- Use default credentials to get into the pi
  - Username: pi
  - Password: raspebrry
**Enable SSH**
- Open the configuration menu using the command: `sudo raspi-config`
- Use the up and down arrow keys on the keyboard to navigate to option 3, `Interface Options`.
- Select P2 SSH and select yes.
- Exit the menu.
**Find the MAC Address**
The MAC Address is needed in order to register the Rapsberry Pi with PSU's IoT network. The address will be used to register the device with CAT using the Intranet website.
- In the command line, type: `ifconfig`
- Check under `wlan0 ether` and write down the numbers and letters listed.
- Compare this address with the ones listed in our Raspberry Pi document; if it is not already registered, use the link in the doc to do so.
- You will be able to assign a new PSK that will be used for the network connection.
**Add Network Information**
There are several ways to change the network information. You can navigate to `etc/wpa_supplicant` and edit the `wpa_supplicant.conf` file directly, or you can use the configuration menu as described below.
- Open the configuration menu using the command: `sudo raspi-config`
- Navigate to option 1, `System Connection`.
- Select `S1 Wireless LAN`
- Select the country as `US`
- Type in the network name: `PSU-IoT`
- Type in the PSK that is assigned to the pi
- Exit the menu
**SSH Into the Raspberry Pi**
You can remotely SSH into the several ways.
- Open your computer's terminal/command prompt or use something like VSCode's SSH enabled terminal.
- Use either the IP address or the hostname of the pi to login:
  - `ssh pi@[IP address]`
  - `ssh pi@[hostname].local`
- Type in the username and password, if prompted

## Increase Swap memory -- May delete this section
In light of installation issues which I believe stem from lack of RAM on the earlier versions of raspberry pi's or possibly poor memory managment I have found and [article](https://pimylifeup.com/raspberry-pi-swap-file/) that increases the swap memory at the cost of disk space. This is essentially converting disk to slow RAM, but it does appear to aleviate some of the installation issues we have been experiancing. Change the following value within dphys-swapfile:

- CONF_SWAPSIZE=100 -> CONF_SWAPSIZE=1024

```shell
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
sudo reboot
```

## Dependancy Installation
In an effort to make development and debugging easier. All raspberry pi's will install all the dependancies as a base. Copy Paste: `sudo apt update -y && sudo apt upgrade -y && sudo apt-get install -y build-essential wget git pkg-config  cmake python3 python3-dev libssl-dev libmodbus-dev && mkdir ~/temp`

```shell
sudo apt update -y
sudo apt upgrade -y
sudo apt-get install -y build-essential wget git pkg-config  cmake python3 python3-dev libssl-dev libmodbus-dev
mkdir ~/temp
```

### CMake
Copy paste: `cd ~/temp && wget https://github.com/Kitware/CMake/releases/download/v3.18.4/cmake-3.18.4.tar.gz && tar -xf cmake-3.18.4.tar.gz && cd cmake-3.18.4 && cmake . && make && sudo make install `

```shell
cd ~/temp
wget https://github.com/Kitware/CMake/releases/download/v3.18.4/cmake-3.18.4.tar.gz
tar -xf cmake-3.18.4.tar.gz
cd cmake-3.18.4 && cmake . && make && sudo make install
```

### Boost
If the respberry pi supports boost 1.72+ then an apt-get install will be sufficient. `cd ~/temp && wget https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.tar.gz && tar -xf boost_1_76_0.tar.gz && cd boost_1_76_0 && ./bootstrap.sh && ./b2 && sudo ./b2 install`

```shell
cd ~/temp
wget https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.tar.gz
tar -xf boost_1_76_0.tar.gz
cd boost_1_76_0 && ./bootstrap.sh 
./b2 && sudo ./b2 install

```


We have also added the boost python libs to make implementation testing of each of our actors easier. The following installs the required boost libs. `cd ~/temp/boost_1_76_0 && ./bootstrap.sh --with-python=/usr/bin/python3 && sudo ./b2 --with-python install`

```shell
cd ~/temp/boost_1_76_0
./bootstrap.sh --with-python=/usr/bin/python3
sudo ./b2 --with-python install
```
We have also added the boost filesystem libs to make implementation of the server registration easier. 

```shell
cd ~/temp/boost_1_76_0
./bootstrap.sh --with-filesystem
sudo ./b2 --with-filesystem install
```

### XercesC
`cd ~/temp && wget https://ftp.wayne.edu/apache//xerces/c/3/sources/xerces-c-3.2.3.tar.gz && tar -xf xerces-c-3.2.3.tar.gz && cd xerces-c-3.2.3 && ./configure --prefix=/usr && make && sudo make install`

```shell
cd ~/temp
wget https://ftp.wayne.edu/apache//xerces/c/3/sources/xerces-c-3.2.3.tar.gz
tar -xf xerces-c-3.2.3.tar.gz
cd xerces-c-3.2.3 && ./configure --prefix=/usr && make && sudo make install
```

### Clean Up

```shell
cd
rm -rf ~/temp
sudo apt update -y
sudo apt upgrade -y
```

## Serial Port UART Configuration for Pi 4B's
In order to communicate via RS485, we use a specialized Raspi HAT RS-485 Auto-Switching Serial Converter with a MAX485 chip. This requires the use of the raspi's serial communication port. 

Our lives are made easier by the fact that the Pi 4's have 6 UARTs. Therefore, in order to use a HAT via the GPIO pins, all you need to do is edit the port. Change it from `dev/ttyAMA0` to `dev/ttyS0`


## Download a File From the Rapsberry Pi to Computer Using SSH
It is helpful to be able to download files back and forth using SSH. [This website](https://www.raspberrypi.com/documentation/computers/remote-access.html) describes the process both ways.
- To retrieve a file from the pi, use your computer's command prompt to type: `scp pi@[IP address]:[path]/[filename]`
- An example of this: `scp pi@[IP address]:/home/pi/Temperature/temp_data_records.csv`
  - This would copy the `temp_data_records.csv` file to your computer.

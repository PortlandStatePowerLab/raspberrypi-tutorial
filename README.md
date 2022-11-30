# raspberrypi-tutorial
General description of setting up a Raspberry Pi for project development.
## Initial Setup
The official [Raspberry Pi website](https://www.raspberrypi.com/documentation/computers/getting-started.html) offers detailed instructions on setting up a Pi. Another resource for setting up a Pi from scratch is detailed [headless Pi setup](https://desertbot.io/blog/headless-pi-zero-w-wifi-setup-windows). While the setup is specific to Windows, each step is applicable to any operating system. Before getting started, check the the new SD card doesn't have the Raspberry Pi OS already pre-installed. If it does, plug it into the Raspberry Pi and skip the rest of these steps. If it does not have the OS already installed, continue through these steps.

- Download and install the [Raspberry Pi OS imagining software](https://www.raspberrypi.com/software/) from the official website. 
- Once the software is installed, on the main screen, open the "CHOOSE OS" menu.
  - If a desktop environment is desired, select the first option "Raspberry Pi OS".
  - If a non-desktop environment is desired, select "Raspberry Pi OS (other)" then slect "Raspberry Pi OS Lite".
- Open the settings menu with the cog button on the bottom right of the screen.
- Change the following settings:
  - Set the hostname
  - Check the "Enable SSH" box and select "Use password authentication"
  - Set the username and password
  - Add network information to the SSID and Password fields
  - Set locale settings to the correct time zone
- From the main menu, select the "CHOOSE STORAGE" menu and select the SD card.
- Click "WRITE" and eject the SD card when it is complete.
- Place SD card into the Raspberry Pi and boot it by connecting it to a power source.
- If you forget to add these settings during the installation process, they can later be once the Raspberry Pi has the SD card in it. Use the command *sudo raspi-config* and navigate through the window to select the previously mentioned options.

To continue with a Headless (no monitor) Setup:
- Log into local router and get raspi ip address
  - Open browser and go to 192.168.0.1 or 192.168.1.1 which are the default router ip address
  - Log in to router dashboard
    - Username: admin
    - Password: password
  - Select wifi devices and record raspi ip address
- SSH into raspi from the terminal using `ssh pi@<ip address>` with password *raspberry*

Alternative Setup Using a Monitor:
- Plug a mouse and keyboard into the Pi via USB
- Plug a monitor into the Pi via micro HDMI
- Plug the Pi back into power supply and wait for it to boot on its own
- Follow prompts on the screen, if any pop up
- Log into the the Pi using crentials set in the initial setup (username and password)
- In the command line, type `ifconfig`
- Look for `wlan0 ether` MAC address. Write down the series of letters and numbers.
- Use this MAC address to register with CAT so that the Pi can be connected to the PSU-IoT network.
- Once connected to the PSU-IoT network, type `ifconfig` in the command line again and find the current IP address listed under `wlan0`. This will be the address used to ssh into the Pi.

## SSH Into the Pi
There are two ways to ssh into the Pi. One is with the IP address, and the other is with the hostname.
- IP Address: When connected to the PSU-IoT network, the Pi can only be accessed via IP address. 
  - To ssh in, open command prompt on your computer and type: `ssh pi@[IP address]`. For example: `ssh pi@172.30.8.180`. 
  - Enter the Pi's credentials when prompted.
- Hostname: This methond can be used on networks other than the PSU-IoT network. 
  - Open command prompt on your computer and type: `ssh pi@hostname.local`. 
  - Enter Pi's credentails when prompted.

## Increase Swap memory
In light of installation issues which may stem from lack of RAM on the earlier versions of Raspberry Pi's or possibly poor memory managment, this [article](https://pimylifeup.com/raspberry-pi-swap-file/) describes how to increase the swap memory at the cost of disk space. This is essentially converting disk to slow RAM, but it does appear to aleviate some of installation issues that have been encountered. Change the following value within dphys-swapfile:

- CONF_SWAPSIZE=100 -> CONF_SWAPSIZE=1024

```shell
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
sudo reboot
```

## Dependancy Installation
In an effort to make development and debugging easier, all Raspberry Pi's will install all the dependancies as a base. Copy Paste: `sudo apt update -y && sudo apt upgrade -y && sudo apt-get install -y build-essential wget git pkg-config  cmake python3 python3-dev libssl-dev libmodbus-dev && mkdir ~/temp`

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
If the Raspberry Pi supports boost 1.72+ then an apt-get install will be sufficient. `cd ~/temp && wget https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.tar.gz && tar -xf boost_1_76_0.tar.gz && cd boost_1_76_0 && ./bootstrap.sh && ./b2 && sudo ./b2 install`

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
We have also added the boost filesystem libs to make implementation of the server registration easier. `cd ~/temp/boost_1_76_0 && ./bootstrap.sh --with-filesystem && sudo ./b2 --with-filesystem install`

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
sudo rm -rf ~/temp
sudo apt update -y
sudo apt upgrade -y
```

## Serial Port UART Configuration for Pi Zeros
In order to communicate via RS485, we use a specialized Raspi HAT RS-485 Auto-Switching Serial Converter with a MAX485 chip. This requires the use of the raspi's serial communication port. In order to configure the pi to use the correct port (because there are 2, and the one we want to use is, be default, reserved for bluetooth communication) we need to do a few things. 

The first thing is, from the command line via ssh, to `sudo raspi-config` to access the configuration menu. Under "Interface Options," we will go to "Serial Port." In response to the question "Would you like a login shell to be accessible over serial?" we want to say "No." The next question is "Would you like the serial port hardware to be enabled?" and we will select "Yes."

Next, go to your "boot," directory with `cd /boot/` and open the "config.txt," file with nano or vim, like this: `sudo vim config.txt`

Now at the very end of the file add the line:
```bash
dtoverlay=disable-bt
```
and save it. 

Then from the command line enter: `sudo systemctl disable hciuart` and then reboot the raspi with `sudo reboot`

Once the raspi has rebooted, you can check if you were successful with the command `ls -l /dev` and scroll through to find a line that says `serial0 -> ttyAMA0` which confirms that the primary UART on the raspi (serial0) is pointing to the full UART (AMA0)


## Serial Port UART Configuration for Pi 4B's
Our lives are made easier by the fact that the Pi 4's have 6 UARTs. Therefore, in order to use a HAT via the GPIO pins, all you need to do is edit the port. Change it from `dev/ttyAMA0` to `dev/ttyS0` and you're all good :)

## Cloning Github Repository
Once everything is installed and the Pi is setup, the `doe-egot-system` Github repository should be cloned to the Pi.
- Navigate to the pi folder 
- Copy and paste: `git clone https://github.com/PortlandStatePowerLab/doe-egot-system.git`

To navigate Github branches on the Pi:
- Navigate to the doe folder: `cd doe-egot-system`
- Add the build directory: `mkdir build`
- Check what branch you're in: `git branch -a`
  - This will show all the branches and the highlighted one is where you currently are
- To switch to the main branch: `git checkout main`
- To see all commits: `git log`

Use CMake to build:
- In the doe-egot-system, use CMake to get setup for build: `cmake -S . -B build`
  - Make sure you are in the main branch!
  - S is for source (CMake.txt file)
  - B is for build location (which is the build directory)
  - The dot indicates the current directory
  - To stop the build, press `ctrl + C`
 
Use CMake to compile:
- To compile, type: `cmake -- build .` or just `make`

Run and change binary files:
- To run a binary file (usually displayed as a different color than other directoris; files don't end in .txt, .csv, etc): `./name of binary file`
- To switch a binary file to executable or non executable:
  - `chmod -x name`
  - `chmod +x name`







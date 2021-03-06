# raspberrypi-tutorial
General description of setting up a Raspberry Pi for project development.
## Headless Setup
Setting up a raspberry pi from scratch is detailed [headless pi setup](https://desertbot.io/blog/headless-pi-zero-w-wifi-setup-windows). While the setup is specific to windows, each step is applicable to any operating system. I have highlighted the important components, but you should follow the more detailed post for specifics.

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

## Increase Swap memory
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

## Serial Port UART Configuration for Pi Zeros
In order to communicate via RS485, we use a specialized Raspi HAT RS-485 Auto-Switching Serial Converter with a MAX485 chip. This requires the use of the raspi's serial communication port. In order to configure the pi to use the correct port (because there are 2, and the one we want to use is, be default, reserved for bluetooth communication) we need to do a few things. 

The first thing is, from the command line via ssh, to `sudo raspi-config` to access the configuration menu. Under "Interface Options," we will go to "Serial Port." In response to the question "Would you like a login shell to be accessible over serial?" we want to say "No." The next question is "Would you liek the serial port hardware to be enabled?" and we will select "Yes."

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

## CLion IDE Remote Development Instructions for Raspi Zero W 
CLion is JetBrains's C++ IDE. PSU students/staff may access a free educational license, which can be applied for here: https://www.jetbrains.com/community/education/#students

Unfortunately, VSCode's ssh-based remote development system does not support the architecture of the Raspi Zero. CLion's does, however. Here are some instructions for getting it working. This tutorial assumes that you have already done the following:

* Downloaded the CLion IDE
* Performed the initial raspi build steps outlined in the readme [here](https://github.com/EGoT-DCS-CTA2045/EGoT-DCS/tree/ssh-dev) consisting of downloading dependencies onto the raspi. This can be performed by copy pasting the following to the raspi's command line: ```sudo apt-get update -y && sudo apt-get install -y wget pkg-config build-essential git cmake libssl-dev libboost-all-dev -y && sudo apt-get upgrade -y && sudo reboot``` The last command in the list will reboot the pi. Re- login and enter: ```mkdir ~/temp && cd ~/temp && wget https://github.com/Kitware/CMake/releases/download/v3.18.4/cmake-3.18.4.tar.gz && tar -xf cmake-3.18.4.tar.gz && cd cmake-3.18.4 && cmake . && make && sudo make install``` this may take several hours.
* Cloned the ssh-dev repository to the desired directory of your desktop environment. 

Now, in an ssh terminal session, clone the [repository](https://github.com/EGoT-DCS-CTA2045/EGoT-DCS/tree/ssh-dev) to the desired directory of your raspi.  Make sure you are in the correct branch with `git branch -a` to view all branches, and `git checkout <branch>` to switch. Now ```cd``` into the repository. 

Now, on your desktop, open your CLion IDE. Select `File > Open` and navigate to the repository. Select it, and select New Window.

Now you're going to go to `File > Settings > Build, Execution, Deployment`. 

The first thing we need to do is add a toolchain. Select `Toolchains` from the list of Build, Execution, Deployment options. We are going to create a new one. Click the `+` sign in the upper left above the list of Toolchains as shown here:

![InkedCLionPlusToolchain_LI](https://user-images.githubusercontent.com/72573224/114450462-e41f9800-9b8a-11eb-9637-14f6b02a7020.jpg)

From the Dropdown menu that appears, select `Remote Host`. Enter your desired name (such as raspi-dcm). Next to the `Credentials` box, hit the gear-shaped button to open `SSH Configurations`. Select the `+` to add a new one, and enter the ssh credential information for your raspi, as shown here:

![sshConfig](https://user-images.githubusercontent.com/72573224/114450945-80e23580-9b8b-11eb-959a-3ac719b7b906.png)


Hit `Apply` then `OK`. 

Now, CLion will automatically search for a cmake installation. You need to manually select one instead. To the right of the `Cmake:` field, hit the button labeled `...` Now select the directory of your `cmake 3.18` installation. It should be `\usr\local\bin\cmake`. Like so:

![correc_318_bin_tylors](https://user-images.githubusercontent.com/72573224/118702266-902b5300-b7c9-11eb-8510-60ba3de9e47f.png)



Hit `Apply`. 

Now we need to configure CMake. Right under `Toolchains` in the left hand side menu bar, select `CMake`. Hit `+` again, to create a new CMake profile. Name it whatever you want, but it should be related to your toolchain name. Next to build type, you should probably select `Debug` though in the screenshot below I have `Default` selected. The important thing here is that next to `Toolchain` you need to select the toolchain you've just created, as shown here: 

![cmakeChooseToolchain](https://user-images.githubusercontent.com/72573224/114452814-bb4cd200-9b8d-11eb-8195-ae46027cbfa9.png)

For build directory, you can let CLion generate a name automatically, or you can name it yourself. An important thing to remember is that if you've done this before, and already created a build directory, you may need to either select it if you want to continue overwriting it, or create a new one. Whatever directory is listed here will be filled with CMake's build files.

Next thing to do is go to `Build, Execution, Deployment > Deployment` which is nearer the bottom of the left hand side menu (shown below). You're gonna click on the profile whose name matches the name you gave your toolchain. Make sure the SSH configuration information is correct. This is the place where you can accidentally mess stuff up, and probably will. CLion will generate new deployment files, sharing the same name but with different ID's (the long random string next to the name). Messing with these Deployment files causes chaos. 


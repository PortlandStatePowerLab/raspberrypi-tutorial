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

## Dependancy Installation
In an effort to make development and debugging easier. All raspberry pi's will install all the dependancies as a base.

```shell
sudo apt update -y
sudo apt-get install -y build-essential wget git pkg-config  cmake libssl-dev libmodbus-dev
sudo apt upgrade -y
mkdir ~/temp
```

### CMake

```shell
cd ~/temp
wget https://github.com/Kitware/CMake/releases/download/v3.18.4/cmake-3.18.4.tar.gz
tar -xf cmake-3.18.4.tar.gz
cd cmake-3.18.4 && cmake . && make && sudo make install
```

### Boost

```shell
cd ~/temp
wget https://dl.bintray.com/boostorg/release/1.75.0/source/boost_1_75_0.tar.gz
tar -xf boost_1_75_0.tar.gz
cd boost_1_75_0 && ./bootstrap.sh && ./b2 && sudo ./b2 install
```

### XercesC

```shell
cd ~/temp
wget https://mirror.jframeworks.com/apache//xerces/c/3/sources/xerces-c-3.2.3.tar.gz
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

## CLion IDE Remote Development Instructions for Raspi Zero W 
Unfortunately, VSCode's ssh-based remote development system does not support the architecture of the Raspi Zero. CLion's does, however. Here are some instructions for getting it working. This tutorial assumes that you have already done the following:

* Downloaded the CLion IDE
* Performed the initial raspi build steps outlined in the readme [here](https://github.com/EGoT-DCS-CTA2045/EGoT-DCS/tree/ssh-dev) consisting of downloading dependencies onto the raspi. This can be performed by copy pasting the following to the raspi's command line: ```sudo apt-get update -y && sudo apt-get install -y wget pkg-config build-essential git cmake libssl-dev libboost-all-dev -y && sudo apt-get upgrade -y && sudo reboot``` The last command in the list will reboot the pi. Re- login and enter: ```mkdir ~/temp && cd ~/temp && wget https://github.com/Kitware/CMake/releases/download/v3.18.4/cmake-3.18.4.tar.gz && tar -xf cmake-3.18.4.tar.gz && cd cmake-3.18.4 && cmake . && make && sudo make install``` this may take several hours.
* Cloned the ssh-dev repository to the desired directory of your desktop environment. 

Now, in an ssh terminal session, clone the [repository](https://github.com/EGoT-DCS-CTA2045/EGoT-DCS/tree/ssh-dev) to the desired directory of your raspi.  Make sure you are in the correct branch with `git branch -a` to view all branches, and `git checkout <branch>` to switch. Now ```cd``` into the repository. 

Now, on your desktop, open your CLion IDE. Select `File > Open` and navigate to the repository. Select it, and select New Window.

Now you're going to go to `File > Settings > Build, Execution, Deployment`. Now we are ready to configure our remote development system.

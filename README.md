# raspberrypi-tutorial
General description of setting up a Raspberry Pi for project development.


## CLion IDE Remote Development Instructions for Raspi Zero W 
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


Hit `Apply` then `OK`. Now, CLion will automatically search for a cmake installation. You need to manually select one instead. To the right of the `Cmake:` field, hit the button labeled `...`. Now select the directory of your `cmake 3.18` installation. It should be `\home\pi\temp\cmake-3.18.4\bin\cmake`. Hit `Apply`. 


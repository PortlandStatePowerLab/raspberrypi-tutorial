# Errors Nicole encountered while setting up the Raspberry Pis:

## Issues with backup battery pack
The red control board of the backup power supply and battery pack is very important! This [Github page](https://github.com/rcdrones/UPSPACK_V3/blob/master/README_en.md) has detailed information about the board and how to use it. One of the issues that has been encountered is the battery being used up and having issues with recharging it.

To prevent the battery from running out and preserve its life, make sure the little on/off switch on the red control board is OFF at all times that the prototype is not plugged into a water heater. Only switch the board ON when the prototype is about to be plugged into a water heater. If the switch stays ON, it will continue providing power to the Pi until the battery dies.

## Errors with building cmake files
When trying to execute: 
```
$ cmake --build
```
the error message "Error: Could not load cache" popped up. Pulling and recloning the github repository did not fix the issue.
This was fixed by reinstalling all the packages for Cmake and boost. I believe that during the initial setup of the Pi, one of the boost installations did not complete fully.

Similarly, on another Pi, the error message "Could not find a package configuration file proivded by 'boost_filesystem'" popped up. This issue was also resolved by reinstalling boost through the process in the tutorial.


## Errors with connecting a Pi to the PSU-IoT network
Here is a list of things to check if the Pi will not connect to the IoT network:
* Make sure the MAC address is registered and that the correct pre-shared key is being used.
* Check the date and time of the Raspberry Pi! If it is off from the actual date/time (even by a few seconds), it will have trouble with connecting. [You can manually reset the date/time.](https://raspberrytips.com/set-date-time-raspberry-pi/#:~:text=NTP%20is%20enabled%20by%20default,%3AMM%3ASS%27%E2%80%9C.)
* Check the Pi for updates.


## Errors with ssh into Pi
* Make sure the Pi is connected to power.
* Check that the IP address has been typed in correctly (you cannot ssh via hostname on the PSU-IoT network).
* If you still cannot connect, the IP address may have changed. Plug into a monitor to find the new IP address.



# Errors Nicole encountered while setting up the Raspberry Pis:

## Errors with getting cmake to build
When trying to execute: 
```
$ cmake --build
```
the error message "Error: Could not load cache" popped up. Pulling and recloning the github repository did not fix the issue.
This was fixed by reinstalling all the packages for Cmake and boost. I believe that during the initial setup of the Pi, one of the boost installations did not complete fully.

Similarly, on another Pi, the error message "Could not find a package configuration file proivded by 'boost_filesystem'" popped up. This issue was also resolved by reinstalling boost through the process in the tutorial.


## Errors with getting a Pi to connect to the PSU-IoT network

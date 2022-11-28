## References
[Rapsberry Pi Temperature Monitor](https://linuxhint.com/raspberry_pi_temperature_monitor/)
[How to Write Data to a File on the Raspberry Pi](https://www.circuitbasics.com/writing-data-to-files-on-the-raspberry-pi/)

## CPU Temperature Sensor Code and Process
* Either ssh into the Pi or connect the Pi to a monitor, keyboard, and mouse.
* Login to the Pi.
* Navigate to:
``` ~$ ```
* Create a new text file:
``` sudo nano templog.txt ```
* Crfeate and edit the python script:
``` sudo nano tempmon.py ```
* Copy and paste this text for the script:
```
from datetime import datetime

printf “%-15s%5s\n” “TIMESTAMP” “TEMP(degC)”
printf “%20s\n” “**************************”
while true
do 
	file = open(“templog.txt”, “a”)
temp=$(vcgencmd measure_temp | egrep -o ‘[0-9]*\.[0-9]*’)
	file.write(“temp”)
	file.write(datetime.today().strftime(‘%Y-%m-%d %H:%M:%S’)+”\n”)
	printf “%-15s%5s\n” “$timestamp” “$temp”
	sleep 3600
done

```

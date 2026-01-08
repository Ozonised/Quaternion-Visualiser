# Quaternion Visualiser
![](https://github.com/Ozonised/Quaternion-Visualiser/blob/main/orientationPlot.gif)
A python script to visualise orientation from quaternion data sent through serial port.
This script is based on the work done by [Steppe School](https://www.steppeschool.com/).

# How to use?
This script accepts string from the serial port in this format: ```"w, i, j, k"```
- ```w``` is the scalar part of the quaternion
- ```i``` is the i component
- ```j``` is the j component
- ```k``` is the k component

To use the script simply, replace [serial port] with your serial port number, and [baudrate] with the baudrate value on line 97:
```uart_mcu = serial.Serial('[serial port]', [baudrate], parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)```
### For example:
Here is a example on linux:
```uart_mcu = serial.Serial('/dev/ttyACM0', 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)```

### Note:
You might have to install some python packages such as: ```pyquaternion```, and ```matplotlib```.

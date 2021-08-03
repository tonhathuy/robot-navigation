# robot-navigation

## Introduction

## requirement

## Tutorials
-requirement
    <strong>Hardware</strong>

        * Jetson nano
        * RPLIDAR A1M8
        * Arduino Mega 2560
        * 2 motor encoder [GA25-370](https://www.thegioiic.com/products/ga25-370-dong-co-giam-toc-co-encoder-12vdc-130-rpm-truc-4mm)</li>
        * L298N</li>
        * Usb wifi tp link archer T2U


    <strong>Software</strong>

        * jetpack [4.5.1 or 32.3.1](https://developer.nvidia.com/embedded/jetpack)
        * [ROS melodic](http://wiki.ros.org/melodic/Installation/Ubuntu)
-Installation
    - [Setup jenson nano image](./docs/Jetson_nano_image.md)
    - [Setup USB wifi](./docs/rtl8812au.md)
    - [Setup Nox_ws](./docs/nox_ws.md)
    - [Setup Camera_ws](./docs/camera_ws.md)
## Build Nox 
```bash
mkdir -p catkin_ws/src
cd catkin_ws/
catkin_make
source devel/setup.bash
```
## Test Navigation
```bash
ls -l /dev |grep ttyUSB
sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyACM0

roslaunch nox nox_bringup.launch
roslaunch nox nox_slam.launch
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

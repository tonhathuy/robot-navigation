# robot-navigation

## Introduction

## requirement

## Tutorials
- Requirement
- Installation
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

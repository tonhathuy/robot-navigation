# SLAM DOC



## 1. What is RPLIDAR ?

RPLIDAR is a low-cost LIDAR sensor suitable for indoor robotic SLAM application. The produced 2D point cloud data can be used in mapping, localization and object/environment modeling. RPLIDAR will be a great tool using in the research of SLAM (Simultaneous localization and mapping).

- RPLIDAR Application Scenarios:
+ Obstacle detection and avoidance
+ Environment scanning and 3D modeling
+ Multi-touch technology and man-machine interaction
+ Robot simultaneous localization and mapping



## Build Nox 
```bash
mkdir -p catkin_ws/src
cd catkin_ws/
catkin_make
source devel/setup.bash
```
## Test Motor encoder and Rplidar
```bash
sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyACM0

roslaunch nox nox_bringup_with_rviz.launch
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```
## Run Mapping and Navigation
```bash
ls -l /dev |grep ttyUSB
sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyACM0

roslaunch nox nox_bringup.launch
roslaunch nox nox_slam.launch
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```
## Save Static Map
```bash
cd ./Nox_ws/src/nox/map && rosrun map_server map_saver -f map
```

## Run Navigation with Static Map
```bash
roslaunch nox nox_bringup.launch
roslaunch nox nox_map_slam.launch
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```
* Note: rename your Map name in nox_map_slam.launch

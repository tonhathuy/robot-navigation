# Nox ws 

## INSTALL Nox
```bash
sudo apt-get install ros-melodic-robot-state-publisher
sudo apt-get install ros-melodic-joint-state-publisher-gui
sudo -H apt-get install -y ros-melodic-teb-local-planner
sudo apt install ros-melodic-rviz
sudo apt-get install ros-melodic-move-base
sudo apt-get install ros-melodic-dwa-local-planner
```
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

# Camera ws 

## Install package
```bash
pip3 install unidecode playsound
sudo apt-get install -y ros-melodic-usb-cam
```
## Build Camera ws with python3* 
```bash
sudo apt-get install python3-pip python3-yaml
sudo pip3 install rospkg catkin_pkg
sudo apt-get install python-catkin-tools python3-dev
sudo apt install python3-empy

mkdir -p camera_ws/src
cd camera_ws/
catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3.6
source devel/setup.bash
```
* because many package for face detection not on python2 ROS, so I run ROS with python3 
## Run Face Detection 
```bash
roslaunch usb_cam usb_cam-test.launch
```
## Run display camera
```bash
rqt_image_view
```

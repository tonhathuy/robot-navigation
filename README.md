# robot-navigation

## requirement

<strong>Hardware</strong>
<ul>
<li>Jetson nano</li>
<li>RPLIDAR A1M8</li>
<li>Arduino Mega 2560</li>
<li>2 motor encoder [GA25-370](https://www.thegioiic.com/products/ga25-370-dong-co-giam-toc-co-encoder-12vdc-130-rpm-truc-4mm)</li>
<li>L298N</li>
<li>Usb wifi tp link archer T2U</li>

</ul>

<strong>Software</strong>
<ul>
<li>jetpack [4.5.1 or 32.3.1](https://developer.nvidia.com/embedded/jetpack)</li>
<li>[ROS melodic](http://wiki.ros.org/melodic/Installation/Ubuntu)</li>
</ul>
## INSTALL rtl8812au usb wifi
```bash
sudo apt install git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

## INSTALL ALL package
```bash
sudo apt install python-rosdep
rosdep install --from-paths ./src --ignore-src --rosdistro melodic -y
```
## INSTALL Nox
```bash
sudo apt-get install ros-melodic-robot-state-publisher
sudo apt-get install ros-melodic-joint-state-publisher-gui
sudo -H apt-get install -y ros-melodic-teb-local-planner
sudo apt install ros-melodic-rviz
sudo apt-get install ros-melodic-move-base
sudo apt-get install ros-melodic-dwa-local-planner
```
## build Nox 
```bash
mkdir -p catkin_ws/src
cd catkin_ws/
catkin_make
source devel/setup.bash
```

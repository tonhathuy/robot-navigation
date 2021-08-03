# VNC

## Install VNC jetson nano
### 1.Enable the VNC server to start each time you log in
```bash
cd /usr/lib/systemd/user/graphical-session.target.wants
sudo ln -s ../vino-server.service ./.
```
### 2.Configure the VNC server
```bash
gsettings set org.gnome.Vino prompt-enabled false
gsettings set org.gnome.Vino require-encryption false
```
### 3.Set a password to access the VNC server
```bash
gsettings set org.gnome.Vino prompt-enabled false
gsettings set org.gnome.Vino require-encryption false
```
### 4.Reboot the system so that the settings take effect
```bash
sudo reboot
```

## Install VNC service for PC
- [VNC Connect Viewer](https://www.realvnc.com/en/connect/download/viewer/linux/)

## VNC Connecting to Jetson
1.After nano login, you must enter your password to login before the remote service will start automatically
2.View the nano's iP address
```bash
ifconfig
```

## Change resolution display sharing VNC
```bash
nano /etc/X11/xorg.conf 
```
Add at the bottom of the file
```bash
Section "Screen"
   Identifier    "Default Screen"
   Monitor       "Configured Monitor"
   Device        "Tegra0"
   SubSection "Display"
       Depth    24
       Virtual 1280 800 # Modify the resolution by editing these values
   EndSubSection
EndSection
```
Restart takes effect
```bash
sudo reboot
```
## Set static IP

# pirob

1. Download Ubuntu 16.04 LTS Mate

2. Install it and resize the partition

(https://www.bitblokes.de/ubuntu-mate-16-04-lts-auf-dem-raspberry-pi-installieren/)

!!Dont try to SSH from Ubuntu 20.04 to Ubuntu 16.04, its not working!!

3. Install ROS Kinect

(http://wiki.ros.org/kinetic/Installation/Ubuntu)

Do the whole installation, dont forget the enviroment things.

To find available packages, use: 

$ apt-cache search ros-kinetic


Install freenect openni and all the other things for the kinect 360.

(https://newscrewdriver.com/2019/01/26/xbox-360-kinect-and-rtab-map-handheld-3d-environment-scanning/)

But instead of

$ sudo apt install res-kinetic-rtabmap-ros

use:

$ sudo apt-get install ros-kinetic-rtabmap-ros

(https://github.com/introlab/rtabmap_ros)




All together:

sudo apt-get update ; sudo apt-get upgrade ; sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' ; sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 ; sudo apt-get update ;  sudo dpkg --configure -a ; sudo apt-get update ; sudo apt-get install ros-kinetic-desktop-full

echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc ; source ~/.bashrc ; sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential ; sudo apt install python-rosdep ; sudo rosdep init ; rosdep update

sudo apt install freenect ; sudo apt install ros-kinetic-freenect-launch ; sudo apt-get install ros-kinetic-rtabmap-ros

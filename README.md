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




How to use the Cam:

1. SSH to the Raspberry at least two windows ( dont forget not to use Ubuntu 20.04 or 20.10 as local machine )

Start roscore and freenect:

First window:
$ roscore

Second window:
$ roslaunch freenect_launch freenect.launch depth_registration:=true

2. To visualize the Map on you local machine, we have to tell the ROS system where it finds the ROS Master:

$ export ROS_MASTER_URI=http://<host_ip>:11311

$ export ROS_NAMESPACE=rtabmap

3. Run rviz on your local machine:

(https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiB7KL7oPHvAhUvhv0HHe5vCmQQFjAFegQIAhAD&url=http%3A%2F%2Fwww.choitek.com%2Fuploads%2F5%2F0%2F8%2F4%2F50842795%2Fros_kinect.pdf&usg=AOvVaw1pdPztTFnN6UlTh8czUXk3)

$ rosrun rviz rviz

In the rviz options panel on the left, change Global Options > Fixed Frame to camera_link

In rviz add a new PointCloud2. Set its topic to /camera/depth_registered/points 

Wait a few seconds for the point cloud to show up. You may need to rotate the viewport around to see it

4. Create Map on the Raspberry Pi

TODOO

###for mappping try $ rosrun rtabmap_ros rtabmap and subscribe to cloud_map or grid_map topics. 

###try:
https://github.com/introlab/rtabmap_ros/issues/181

###$ roslaunch realsense_camera r200_nodelet_rgbd.launch
###$ roslaunch rtabmap_ros rtabmap.launch rtabmap_args:="--delete_db_on_start" depth_topic:=/camera/depth_registered/sw_registered/image_rect_raw

5. Enable I2C for communication with the Servomotors.

(https://askubuntu.com/questions/1130052/enable-i2c-on-raspberry-pi-ubuntu)

Dont worry it also works for Ubuntu 16.04

6. Install Servonode

(https://www.youtube.com/watch?v=iLiI_IRedhI&t=146s)

While building the i2cpwmboard package. The error shows some files missing i.e i2c/smbus.h and library i2c.

You can remove the i2c library dependency from the CMakelist file of the package by changing the CMakeList file:

search for line target_link_libraries(i2cpwm_board i2c ${catkin_LIBRARIES})
and remove the i2c.

Also you have to comment out the line where smbus.h was included.

7. Write the Low level controler

(https://www.youtube.com/watch?v=iLiI_IRedhI&t=146s)

After writing it an compiling. You have to enable the computer to execute the file low_level_control.py by,

$ chmod -x low_level_control.py

8. Test if the LLC Node works:

open three terminals on the raspberry pi.

$ roscore

$ rosrun i2cpwm_board i2cpwm_board

$ rosrun donkey_llc low_level_control.py


9. Test it from remote.

connect again with the ROS_MASTER on the Raspbi

$ export ROS_MASTER_URI=http://<host_ip>:11311

and change the NAMESPACE back from rtbmap:

$ export ROS_NAMESPACE=/

install teleop_twist_keyboard:

(http://wiki.ros.org/teleop_twist_keyboard)

$ sudo apt-get install ros-kinetic-teleop-twist-keyboard

disable firewall on local machine:
$ sudo ufw disable
$ sudo reboot
and run:

$ rosrun teleop_twist_keyboard teleop_twist_keyboard.py

10. make it a bit simpler and write an launch file.
(https://www.youtube.com/watch?v=iLiI_IRedhI&t=146s)


#FINALY#
Now, you just have to start the roscore and the launchfile on the raspberry pi:

$ roscore
$ roslaunch donkey_llc keyboard_demo.launch

and on the laptopside you have to set the loaction of the ROS_MASTER and start the teleop_twist:

$ export ROS_MASTER_URI=http://<host_ip>:11311

$ rosrun teleop_twist_keyboard teleop_twist_keyboard.py





#############################################################################################################################################

All together (Installation):

sudo apt-get update ; sudo apt-get upgrade ; sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' ; sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 ; sudo apt-get update ;  sudo dpkg --configure -a ; sudo apt-get update ; sudo apt-get install ros-kinetic-desktop-full

echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc ; source ~/.bashrc ; sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential ; sudo apt install python-rosdep ; sudo rosdep init ; rosdep update

sudo apt install freenect ; sudo apt install ros-kinetic-freenect-launch ; sudo apt-get install ros-kinetic-rtabmap-ros

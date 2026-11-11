# Trash and Recycling Sorter
 
A ROS 2 simulation of a robot that sorts waste items into recycling, organic, and trash bins.
 
**Team:** Zoe Bel, Sophia Leese, Ujjwal Raghuvanshi
 
## Requirements
 
- Ubuntu 24.04
- ROS 2 Jazzy with Gazebo Harmonic
- TurtleBot3 packages
## Environment Setup
 
Add these lines to the end of `~/.bashrc`, skipping any that are already there:
 
```bash
source /opt/ros/jazzy/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
unset ROS_DOMAIN_ID
export TURTLEBOT3_MODEL=waffle
```
Note: Model could be burger also.
 
Then open a new terminal.
 
## Create the Workspace
 
The repo root is the workspace. Clone it into `sorter_ws`:
 
```bash
cd ~
git clone git@github.com:UjjwalUMN/Trash-and-Recycling-Sorter-CSCI-4551.git sorter_ws
```
 
## Build
 
```bash
cd ~/sorter_ws
colcon build
```
 
A `listing git files failed` warning during the build is harmless.
 
## Source
 
Run this in every new terminal you use for the project:
 
```bash
cd ~/sorter_ws
source install/local_setup.bash
```
 
Check that the packages are found:
 
```bash
ros2 pkg list | grep trash_sorter
```
 
You should see `trash_sorter`.
 
## Layout
 
All project code lives in one package, `src/trash_sorter/`:
 
- `trash_sorter/`: Python nodes (perception, manipulation, navigation, coordinator)
- `launch/`: launch files
- `worlds/`, `models/`: Gazebo world, bins, and waste items
- `maps/`: maps built with SLAM
- `config/`: Nav2 and other parameters
- `rviz/`: RViz configuration

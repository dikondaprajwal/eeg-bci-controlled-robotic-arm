#!/bin/bash
# 1. Kill all Gazebo processes (New Gazebo, Classic, and Ruby wrappers)
pkill -9 -f gz; pkill -9 -f gazebo; pkill -9 -f ruby

# 2. Kill leftover ROS 2 communication nodes and daemons
killall -9 ros_gz_bridge rviz2 _ros2_daemon

# 3. Wipe out hidden temporary and transport cache files
rm -rf ~/.gazebo/ ~/.gz/ /tmp/gazebo* /tmp/org.gazebosim*


colcon build --build-base artifacts/build --install-base artifacts/install --symlink-install
source /opt/ros/humble/setup.bash
source ~/eeg_robot_ws/artifacts/install/setup.bash


# =====================================================================
# ADDED LINE: Automatically train the model and generate dataset2a_model.pkl
# =====================================================================
echo "Starting Machine Learning Training with real EEG dataset..."
python3 src/bci/train_dataset2a.py
echo "Training complete! Moving to simulation execution."
# =====================================================================


gnome-terminal -- bash -c \
"ros2 launch ur_simulation_gz ur_sim_moveit.launch.py; exec bash"

sleep 10

gnome-terminal -- bash -c \
"source ~/eeg_robot_ws/artifacts/install/setup.bash;
ros2 run eeg_robot_arm_control robot_controller;
exec bash"

sleep 2

gnome-terminal -- bash -c \
"source ~/eeg_robot_ws/artifacts/install/setup.bash;
ros2 run eeg_robot_arm_control eeg_predictor_node;
exec bash"

sleep 2

gnome-terminal -- bash -c \
"source ~/eeg_robot_ws/artifacts/install/setup.bash;
ros2 run eeg_robot_arm_control eeg_visualizer_node;
exec bash"

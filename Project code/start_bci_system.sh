#!/bin/bash

# ==========================================================
# BCI ROS2 PROJECT RUN SCRIPT
# Ubuntu 24.04 + ROS2 Jazzy
# ==========================================================

set -e

echo ""
echo "=================================================="
echo "         STARTING BCI ROS2 SYSTEM"
echo "=================================================="
echo ""

WORKSPACE=~/ros2_ws
PROJECT=complete_bci_ros2_gazebo_project

# ==========================================================
# SOURCE ROS2
# ==========================================================

echo "[1/6] Sourcing ROS2 Jazzy..."

source /opt/ros/jazzy/setup.bash

echo ""

# ==========================================================
# MOVE TO WORKSPACE
# ==========================================================

echo "[2/6] Moving to workspace..."

cd $WORKSPACE

echo ""

# ==========================================================
# ACTIVATE VENV
# ==========================================================

echo "[3/6] Activating Python virtual environment..."

source venv/bin/activate

echo ""

# ==========================================================
# SOURCE WORKSPACE
# ==========================================================

echo "[4/6] Sourcing workspace..."

source install/setup.bash

echo ""

# ==========================================================
# START GAZEBO
# ==========================================================

echo "[5/6] Starting Gazebo..."

gz sim &

GAZEBO_PID=$!

sleep 8

echo "Gazebo started."

echo ""

# ==========================================================
# START HAND CONTROLLER
# ==========================================================

echo "[6/6] Running BCI pipeline..."

python3 src/$PROJECT/hand_controller_node.py &

HAND_PID=$!

sleep 2

python3 src/$PROJECT/run_bci.py

echo ""

echo "=================================================="
echo "          BCI SYSTEM FINISHED"
echo "=================================================="
echo ""

# ==========================================================
# CLEANUP
# ==========================================================

kill $GAZEBO_PID || true
kill $HAND_PID || true

echo "Processes stopped."
echo ""
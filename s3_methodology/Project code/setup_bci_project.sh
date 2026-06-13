#!/bin/bash

# ==========================================================
# BCI ROS2 PROJECT SETUP SCRIPT
# Ubuntu 24.04 + ROS2 Jazzy
# ==========================================================

set -e

echo ""
echo "=================================================="
echo "      BCI PROJECT INITIALIZATION STARTED"
echo "=================================================="
echo ""

WORKSPACE=~/ros2_ws
PROJECT=complete_bci_ros2_gazebo_project

# ==========================================================
# SOURCE ROS2
# ==========================================================

echo "[1/10] Sourcing ROS2 Jazzy..."

source /opt/ros/jazzy/setup.bash

echo ""

# ==========================================================
# UPDATE SYSTEM
# ==========================================================

echo "[2/10] Updating packages..."

sudo apt update

echo ""

# ==========================================================
# INSTALL ROS2 DEPENDENCIES
# ==========================================================

echo "[3/10] Installing ROS2 dependencies..."

sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-colcon-common-extensions \
    ros-jazzy-ros-gz \
    ros-jazzy-xacro \
    ros-jazzy-rviz2 \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-robot-state-publisher \
    gazebo \
    libgz-sim8-dev

echo ""

# ==========================================================
# MOVE TO WORKSPACE
# ==========================================================

echo "[4/10] Moving to workspace..."

cd $WORKSPACE

echo ""

# ==========================================================
# CREATE VIRTUAL ENVIRONMENT
# ==========================================================

echo "[5/10] Creating Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo "Virtual environment activated."

echo ""

# ==========================================================
# UPGRADE PIP
# ==========================================================

echo "[6/10] Upgrading pip..."

pip install --upgrade pip setuptools wheel

echo ""

# ==========================================================
# INSTALL PYTHON REQUIREMENTS
# ==========================================================

echo "[7/10] Installing Python dependencies..."

pip install -r src/$PROJECT/requirements.txt

echo ""

# ==========================================================
# CLEAN WORKSPACE
# ==========================================================

echo "[8/10] Cleaning old build..."

rm -rf build install log

echo ""

# ==========================================================
# BUILD WORKSPACE
# ==========================================================

echo "[9/10] Building workspace..."

colcon build --symlink-install

echo ""

# ==========================================================
# SOURCE WORKSPACE
# ==========================================================

echo "[10/10] Sourcing workspace..."

source install/setup.bash

echo ""

echo "=================================================="
echo "      BCI PROJECT SETUP COMPLETE"
echo "=================================================="
echo ""

echo "Now run:"
echo "./run_bci_project.sh"
echo ""
# EEG-Based BCI Human-Like Robotic Hand (Gazebo + ROS2)

## Features
- Butterworth Filter (8–30 Hz)
- ICA Artifact Removal
- CSP + Welch PSD
- SVM-RBF
- ROS2 Command Publisher
- Gazebo Hand Controller
- Grasp / Release

## Setup

Install dependencies:

pip install -r requirements.txt

Train model:

python train_model.py

Run BCI:

python run_bci.py

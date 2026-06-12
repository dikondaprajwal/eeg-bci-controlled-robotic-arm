from setuptools import find_packages, setup

package_name = 'eeg_robot_arm_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='prajwal',
    maintainer_email='prajwal@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [

        'eeg_command_node = eeg_robot_arm_control.eeg_command_node.eeg_command_node:main',

        'eeg_predictor_node = eeg_robot_arm_control.eeg_command_node.eeg_predictor_node:main',

        'robot_controller = eeg_robot_arm_control.robot_controller.robot_controller:main',
        
        'eeg_visualizer_node = eeg_robot_arm_control.eeg_visualizer.eeg_visualizer_node:main',

    ],
    },
)

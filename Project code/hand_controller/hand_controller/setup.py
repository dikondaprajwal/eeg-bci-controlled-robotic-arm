
from setuptools import setup
setup(name='hand_controller', version='0.0.1')


from setuptools import setup

package_name = 'hand_controller'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    package_dir={'': 'src'},
)



entry_points={
    'console_scripts': [
        'hand_controller_node = hand_controller.hand_controller_node:main',
    ],
},
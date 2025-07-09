from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'scoutbot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # Register the package with the ROS 2 index
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
            
        # Install the package.xml
        ('share/' + package_name, ['package.xml']),

        # ✅ Install launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),

        # (optional) install URDF or meshes if needed later
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),

        #Add all mesh files 
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*')), 

        #Add any config files 
        (os.path.join('share', package_name, 'config'), glob('config/*')), 
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bbhanda',
    maintainer_email='bbhanda@todo.todo',
    description='URDF + RViz visualization for ScoutBot',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joint_sim = scoutbot_description.joint_sim:main'
        ],
    },
)

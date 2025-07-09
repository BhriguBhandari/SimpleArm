from setuptools import find_packages, setup

package_name = 'arm_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bbhanda',
    maintainer_email='bbhanda@todo.todo',
    description='Basic arm controller',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joint_publisher = arm_controller.joint_publisher:main', 
            'joint_subscriber = arm_controller.joint_subscriber:main', 
        ],
        'launch': [ 
            'display = launch.display.generate_launch_description',
        ],
    },
)

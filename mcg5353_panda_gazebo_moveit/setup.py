from setuptools import find_packages, setup
from glob import glob

package_name = 'mcg5353_panda_gazebo_moveit'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ("share/ament_index/resource_index/packages",
         ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
        ("share/" + package_name + "/config", glob("config/*")),
        ("share/" + package_name + "/worlds", glob("worlds/*")),
        ("share/" + package_name + "/meshes/visual", glob("meshes/visual/*.dae")),
        ("share/" + package_name + "/rviz", glob("rviz/*")),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ali',
    maintainer_email='[alikarimzade999@gmail.com]',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)

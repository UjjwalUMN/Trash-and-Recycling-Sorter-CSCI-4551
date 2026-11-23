import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'trash_sorter'

data_files = [
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
]

for folder in ['models', 'worlds', 'maps', 'config', 'rviz']:
    for root, dirs, files in os.walk(folder):
        files = [f for f in files if f != '.gitkeep']
        if files:
            install_dir = os.path.join('share', package_name, root)
            data_files.append((install_dir, [os.path.join(root, f) for f in files]))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='raghu099',
    maintainer_email='raghu099@umn.edu',
    description='Trash and recycling sorter robot (CSCI 4551)',
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
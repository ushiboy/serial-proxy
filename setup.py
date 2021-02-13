#!/usr/bin/env python3
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='serialproxy',
    version='0.2.0',
    author='ushiboy',
    license='MIT',
    description='A proxy that connects serial ports to each other',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ushiboy/serial-proxy',
    py_modules=['serialproxy'],
    python_requires='>=3.7',
    install_requires=[
        'pyserial==3.5'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux'
    ],
    entry_points = {
        'console_scripts': [
            'serialproxy = serialproxy:main'
        ]
    }
)

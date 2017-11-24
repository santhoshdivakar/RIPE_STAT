from setuptools import setup

setup(
    name='ripeutil',
    version='0.1',
    description='Installer for ripe_util',
    author='Santhosh Divakar',
    author_email="santhosh.kumar.divakar@gmail.com",
    packages=['ripeutil'],
    install_requires=['requests','dicttoxml','pyyaml']
)
from setuptools import find_packages, setup

NAME = 'nyam_restaurants_algorithms'
DESCRIPTION = 'Alghorithms for names and prices of restaurants'
VERSION = '1.0.1'

setup(
    description=DESCRIPTION,
    include_package_data=True,
    name=NAME,
    packages=find_packages(),
    version=VERSION
)

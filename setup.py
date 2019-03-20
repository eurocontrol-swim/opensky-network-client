
from setuptools import setup, find_packages

__author__ = 'EUROCONTROL (SWIM)'

setup(
    name='opensky-network-client',
    version='0.0.1',
    description='Opensky Network Client',
    author='EUROCONTROL (SWIM)',
    author_email='',
    packages=find_packages(exclude=['tests']),
    url='https://bitbucket.org/antavelos-eurocontrol/opensky-network-client',
    install_requires=[
        'requests'
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    platforms=['Any'],
    license='see LICENSE',
    zip_safe=False
)

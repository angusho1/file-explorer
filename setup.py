from setuptools import setup, find_packages

setup(
    name='fe',
    version='0.0.1',
    packages=['src', 'src.displays', 'src.explorer'], 
    entry_points={
        'console_scripts': [
            'fe=src.main:main'
        ]
    }
)
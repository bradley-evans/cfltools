from setuptools import setup

setup(
        name = 'cfltools',
        version = '0.0.1',
        packages = ['cfltools'],
        entry_points = {
            'console_scripts': [
                'cfltools = cfltools.__main__:main'
            ]
        })

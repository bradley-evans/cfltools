from setuptools import setup, find_packages

setup(
        name='cfltools',
        version='0.0.2',
        packages=find_packages(),
        include_package_data = True,
        install_requires=[
            'click',
            'ipwhois',
            'pycountry_convert',
            'netaddr',
            'appdirs',
            'dateparser',
            'requests',
            'sqlalchemy>=1.3.5'
            'pyasn'
            ],
        entry_points={
            'console_scripts': [
                'cfltools = cfltools.cli:cli',
                'cfltools-gui = cfltools.gui:gui',
            ]
        }
     )

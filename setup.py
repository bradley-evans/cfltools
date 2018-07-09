from setuptools import setup, find_packages

setup(
        name = 'cfltools',
        version = '0.0.1',
        packages = find_packages(),
        include_package_data = True,
        install_requires=[
            'click',
            ],
        entry_points = '''
            [console_scripts]
            cfltools = cfltools.cli:cli
            ''',
     )

from setuptools import setup

setup(
    name='farrut-flights-app',
    version='1.0',
    py_modules=['farrut'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        farrut=farrut:cli
    ''',
)

from setuptools import setup

setup(
    name='beerprogress',
    description='Command line progress indicator library for Python3',
    version='0.0.2',
    packages=[
        'beerprogress',
    ],
    author='Filipe Varela',
    author_email='fcvarela@gmail.com',
    url='https://github.com/fcvarela/beerprogress',
    install_requires=[
        "psutil==2.1.1"
    ]
)

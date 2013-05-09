
from setuptools import setup, find_packages

setup(name='data-store',
    version='0.1',
    install_requires=['redis','pymongo'],
    description="Some python tools for doing key-value storing ",
    author='Tristan Hearn',
    author_email='tristanhearn@gmail.com',
    url='https://github.com/thearn/data-store',
    license='Apache 2.0',
    packages=['datastore'],
)

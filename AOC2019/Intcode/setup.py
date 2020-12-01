from setuptools import setup
from setuptools import find_packages

setup(name='Intcode',
      version='0.2',
      description='Intcode machine from AOC2019',
      url='',
      author='rodalgar',
      author_email='rodalgar@gmail.com',
      license='MIT',
      packages=find_packages("."),
      entry_points = {},
      include_package_data=True,
      zip_safe=False)

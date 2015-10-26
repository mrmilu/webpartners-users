import os

from setuptools import setup

def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(name='webpartners-users',
      version='0.1.3',
      description='Web Partners base user package',
      url='https://github.com/webpartners/webpartners-users',
      author='Jaime Herencia',
      author_email='jherencia@webpartners.es',
      license='MIT',
      packages=get_packages('webpartners_users'),
      install_requires=[
          'django',
          'djangorestframework',
          'djangorestframework-jwt',
      ],
      zip_safe=False
)

from distutils.core import setup

from pickle_warehouse import version

setup(name='pickle-warehouse',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Easily dump python objects to files, and then load them back.',
      url='https://github.com/tlevine/pickle-warehouse',
      packages=['pickle_warehouse'],
      install_requires = [],
      tests_require = ['nose'],
      version=version,
      license='BSD',
)

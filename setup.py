from distutils.core import setup

from pickle_warehouse import __version__, __author__

setup(name='pickle-warehouse',
      author=__author__,
      author_email='_@thomaslevine.com',
      description='Easily dump python objects to files, and then load them back.',
      url='https://github.com/tlevine/pickle-warehouse',
      packages=['pickle_warehouse'],
      install_requires = [],
      tests_require = ['nose'],
      version=__version__,
      license='AGPL',
)

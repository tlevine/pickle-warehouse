from distutils.core import setup

from pickle_warehouse import __version__

setup(name='pickle-warehouse',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Easily dump python objects to files, and then load them back.',
      url='https://github.com/tlevine/pickle-warehouse',
      packages=['pickle_warehouse'],
      install_requires = [],
#     extras_require = [
#         'PyYAML',
#         'http://danse.cacr.caltech.edu/packages/dev_danse_us/dill-0.2b1.tgz',
#         'lxml',
#         'numpy',
#     ],
      tests_require = ['nose'],
      version=__version__,
      license='AGPL',
)

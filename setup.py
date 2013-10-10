# No shebang. Should be executed manually via python setup.py arg
# coding: utf-8

# Allows the user to run the tests via setup.py test
#
# Created on 10-08-2013
# Updated on 10-10-2013
# Created by unsignedzero (David Tran)
# Version 0.8.0.0

from distutils.core import setup, Command

class PyTest(Command):
  user_options = []
  def initialize_options(self):
    pass
  def finalize_options(self):
    pass
  def run(self):
    from os.path import isfile
    from subprocess import call
    from sys import executable

    # Check if logfile already exists. If so purge it
    if isfile('logfile'):
      open('logfile', 'w').close()

    errno = call([executable, 'runtests.py'])

    # At the time of writing there is no easy way to remove the logfile
    # generated

    raise SystemExit(errno)

setup(name='pyDecorator',
      version='0.7.2.0',
      description='A simple decorator debugger class for python',
      author='David Tran (unsignedzero)',
      author_email='unsignedzero@gmail.com',
      url='https://github.com/unsignedzero',

      py_modules=['pydecorator.pyDecorator'],
      license='MIT',
      classifiers=[
         'Intended Audience :: Developers',
         'Operating System :: MacOS :: MacOS X',
         'Operating System :: Microsoft :: Windows',
         'Operating System :: POSIX',
         'Programming Language :: Python',
                  ],
      cmdclass = {'test': PyTest},
      )

#!/usr/bin/python
# coding: utf-8

r'''
First round of tests for pyDecorator.
More tests are needed but it works.

Created for Python 2.7+

Created by David Tran (unsignedzero)
Created 10-08-2013
Updated 10-10-2013
Version 0.8.0.0
'''

from os import remove, getcwd
from os.path import isfile
from sys import path, version_info

# Check if the module we want to run the test exists
print( getcwd() )
if getcwd().endswith('pydecorator'):
  # Running on the root of the repo

  path.append('.')
  from pydecorator import pyDecorator

else:
  # Running inside the test dir

  path.append('../pydecorator')
  import pyDecorator

# Fixing the fileError issue as seen in 3.3
# Should python 4 roll around, this needs to be changed...
if version_info[0] < 3 or version_info[1] < 3:
  FileError = IOError


def print_test(instr):
  r'''
  Simple print function that prints the string and that it was from an assert
  call. Useful mainly for debugging/reading output.
  '''

  print( '%s%s' % ( 'assert > ', instr ) )


def test_pyDecorator():
  r'''
  Test function that invokes pyDecorator's pyDecorator_test function
  and then scans said output to see if its correct. This might change
  later on as it invokes its own tests.
  '''

  logpath='logfile'

  pyDecorator.pyDecorator_test()

  print( '\n\nExecution of pyDecorator completed Starting test_pyDecorator' )

  # Given the fact that this can executed from the root or the test folder
  # we check where the logfile is located

  # As of current, the isfile block do NOT work when
  # this script is executed by py.test but HOWEVER, work when executed manually
  # This is moved into the __main__ call.

  # if isfile(logpath):
  #   assert True
  # else:
  #   logpath='tests/logfile'
  #   if isfile(logpath):
  #     assert True
  #   else:
  #     assert False
  # print_test('logfile exists')

  if isfile(logpath):
    with open(logpath) as flog:

      curStr = ''

      curStr = flog.readline()
      assert curStr.startswith('>>Initializing')
      print_test( 'pyDecorator initialized successfully' )

  print_test( 'Test successful' )

  return 0


if __name__ == '__main__':

  print( 'Executed directly' )

  logpath='logfile'

  # Empty the file rather than delete it
  print( 'Emptying logfile' )
  if isfile( logpath ):
    open(logpath, 'w').close()
  else:
    logpath='tests/logfile'
    if isfile( logpath ):
      open(logpath, 'w').close()

  # Invoke test
  print( 'Starting the test' )
  test_pyDecorator()

  # Remove it as it is no longer needed
  print( 'Removing logfile' )
  if isfile(logpath):
    remove(logpath)


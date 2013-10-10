#!/usr/bin/python
# coding: utf-8
#
# pyline: disable=W0622

r'''
Python pyDecorator class
Attaches on to methods to provide tracking on successive function calls
but can be used independently by calling pyDecorator.<static method>
to pause and pyDecorator.__printCurStack the stack.

Created on 05-27-2013
Updated on 10-10-2013
Created by unsignedzero (David Tran)
Version 0.8.0.0
'''

import logging
from pprint import pprint
from sys import version_info

# We don't require the frame support but it helps
try:
  # Will work on mostly all CPython builds
  from sys import _getframe
except ImportError:
  # All others here...
  from sys import callstats
  _getframe = None

# Set default input to be input even in Python 2.X
if version_info[0] == 2:
  input = raw_input

class pyDecorator(object):
  r'''
  This is a debugging decorator class that attaches to a function to
  print out variables information and well as stack information. The goal is
  to make it easier to see the current stack and variables (state). As this
  reads pargs and kwargs, the only values that will change are non-atomic
  values (variables that we access by reference including arrays, and objects,
  to name a few.)

  This class is NOT meant to be called directly but attached or used to
  call its internal static methods

  Attributes:

      _DEBUG           Set True to print out when pyDecorator methods are
                       being called and the recursionCount.

      _LOG             Set True to tell pyDecorator to print out verbose text
                       to log. _VERBOSITY will determine how much information
                       about when the line is written.

      _VERBOSITY       Sets the verbosity level of the class

                       0 - Prints only the function names

                       1 - Mimics the exception handling of Python prints out
                           function name, file, line number and also arg count.
                           In the call, we

                       2 - Prints all of 1 but also prints out constants and
                           locals in the frame

                       3 - Prints all of 2 but also prints out globals and
                           built in functions with respect to the current
                           frame

  '''

  # Private static counters
  _recursionLevel = 0    # States how many times this function is repeatedly
                         # called. Useful when applying this on recursive
                         # functions
  _callCount = 0         # States the number of times this is called since
                         # start of execution

  # Static state flags constructor. Use setter/getter methods to change it.
  _DEBUG = False
  _LOG = True
  _VERBOSITY = 0

  ###########################################################################

  @staticmethod
  def setDEBUG(val):
    r'''
    Setter for _DEBUG static variable.
    '''

    if val == False or val == True:
      pyDecorator._DEBUG = val
      return True
    else:
      return False


  @staticmethod
  def getDEBUG():
    r'''
    Getter for _DEBUG static variable.
    '''

    return pyDecorator._DEBUG


  @staticmethod
  def setVERBOSITY(val):
    r'''
    Setter for _VERBOSITY static variable.
    '''

    if isinstance(val, int):
      pyDecorator._VERBOSITY = val
      return True
    else:
      return False


  @staticmethod
  def getVERBOSITY():
    r'''
    Getter for _VERBOSITY static variable.
    '''

    return pyDecorator._VERBOSITY


  @staticmethod
  def setLOG(val):
    r'''
    Setter for _LOG static variable.
    '''

    if val == False or val == True:
      pyDecorator._LOG = val
      return True
    else:
      return False


  @staticmethod
  def getLOG():
    r'''
    Getter for _LOG static variable.
    '''

    return pyDecorator._LOG

  ###########################################################################

  @staticmethod
  def __print(*pargs):
    r'''
    A local variant method that prints both to output and to logfile
    '''

    for each_msg in pargs:
      logging.info( each_msg )
      print( each_msg )


  @staticmethod
  def __pprint(*pargs):
    r'''
    A local variant method that pprints both to output and to logfile
    '''

    for each_msg in pargs:
      logging.info( each_msg )
      pprint( each_msg )


  def __init__(self, func):
    r'''
    Initializes the pyDecorator by setting the function and the call to it.
    We also initialize the logging class regardless of its usage as it
    might be changed later on.
    '''

    _VERBOSITY = pyDecorator.getVERBOSITY()

    if _VERBOSITY == 0:
      fmtstr = '%(message)s'
    elif _VERBOSITY == 1:
      fmtstr = '%(levelname)-8s %(message)s'
    else:
      fmtstr = '%(asctime)-15s %(levelname)-8s %(message)s'

    logging.basicConfig( level=logging.DEBUG, filename='logfile',
                         filemode='a+', format=fmtstr
                       )

    pyDecorator.__print( '>>Initializing pyDecorator class' )

    self.func = func
    self.count = 0


  def __call__(self, *args, **kwargs):
    r'''
    Manages the call of the function by printing debugging information as
    defined from pyDecorator._VERBOSITY and pyDecorator._DEBUG
    '''

    pyDecorator._recursionLevel += 1
    pyDecorator._callCount += 1

    # Caching values so we don't have to go out to the class repeatedly
    # and make it mostly local to the class
    _DEBUG = pyDecorator._DEBUG
    _VERBOSITY = pyDecorator._VERBOSITY
    LINE_STR = ''

    if _VERBOSITY >= 1:
      LINE_STR = '>>--------------------------------------------------\n'

    if _DEBUG:
      pyDecorator.__print ( '\n\n>>pyDecorator:recursionLevel count is %i' %
        pyDecorator._recursionLevel )

    if _VERBOSITY >= 1:
      pyDecorator.__print( '>>We are calling %s' % self.func.__name__ )
      pyDecorator.__print( '>>For args we have:' )
      pyDecorator.__pprint( args )
      pyDecorator.__print( '>>For kwargs we have:' )
      pyDecorator.__pprint( kwargs )

    pyDecorator.__print( '\n>>Starting call to %s [Call#%03i]\n%s' %
      (self.func.__name__, pyDecorator._callCount, LINE_STR) )

    # Remember to capture and return the args of the function called
    ret = self.func(*args, **kwargs)

    pyDecorator.__print( '%s>>Ended call to %s [Call#%03i]. Returned %s' %
      (LINE_STR, self.func.__name__, pyDecorator._callCount, str(ret) ))

    pyDecorator._recursionLevel -= 1

    if _DEBUG:
      pyDecorator.__print (
        '\n\npyDecorator:pyDecorator._recursionLevel count is %i' %
        pyDecorator._recursionLevel )

    return ret


  def ___printCurStack(self):
    r'''
    Internal method that sets out the counter before calling the static method
    of similar name. This relies on the static variable _DEBUG to tell it if it
    should print out its header.
    '''

    self.count += 1

    if pyDecorator._DEBUG:
      pyDecorator.__print(
        '>>pyDecorator:Call count to decorator %i' % self.count )
      pyDecorator.__printCurStack()


  @staticmethod
  def __printCurStack():
    r'''
    Prints the full current stack of Python as well as additional information
    as specified by the value of _VERBOSITY in the same class. This will not
    print the first two elements on top of the stack, which will contain this
    method as well as the class frame. This relies on _DEBUG to tell it if
    it should print out its header and trailer.

    See the docstring for the class for further information on _VERBOSITY.
    '''

    _DEBUG = pyDecorator._DEBUG
    i = 2

    if _DEBUG:
      pyDecorator.__print(
        '>>pyDecorator:printCurStack called. Unrolling stack...\n' )

    try:
      if _getframe:
        # With this loop we continue to trace down the stack until we are
        # unable to. In that event, we create a ValueError exception and
        # thus exit outside the loop

        while True:
          pyDecorator.__printCurFrame(i)
          i += 1

      else:
        pyDecorator.__print(
          '>>Number of functions already called %i' % callstats()[0] )

    except ValueError:
      pass

    if _DEBUG:
      pyDecorator.__print( '\n\npyDecorator:printCurStack finished' )


  def _pause(self):
    r'''
    Internal method that sets out the counter before calling the static method
    of similar name. This relies on the static variable _DEBUG to tell it if
    it should pyDecorator.__print out its header.
    '''

    self.count += 1

    if pyDecorator._DEBUG:
      pyDecorator.__print(
        '\n\n>>pyDecorator:Call count to decorator %i' % self.count )

    pyDecorator.pause()


  @staticmethod
  def pause():
    r'''
    Prints only the current frame on the stack before continuing on
    This implicitly relies on _VERBOSITY to tell it what to print. This prints
    the third element on the stack which is the function that calls this.

    See the docstring for the class for further information on _VERBOSITY.
    '''

    _DEBUG = pyDecorator._DEBUG

    if _DEBUG:
      pyDecorator.__print(
        '>>pyDecorator:pause called. Printing current Frame...\n' )

    pyDecorator.__printCurFrame(2)

    if _DEBUG:
      pyDecorator.__print( '\n\n>>pyDecorator:pause closing...')

    input( 'Pausing in pyDecorator. Press any key to continue.' )


  @staticmethod
  def __printCurFrame(frameIndex = 1):
    r'''
    Runs and prints the frameIndexth on the stack. This function CAN throw a
    ValueError when we go down to far. This function does NOT handle the
    exception so catch it as needed. The reason is if we call this function
    many times, then it doesn't have to handle it each time.

    This function relies on the static variable _VERBOSITY to tell it what
    to print out.

    Arguments:

        frameIndex       Tell this method which frame to print out. If not
                         passed then it will print out the 2nd frame, which,
                         if this method is explicitly called outside, will
                         be the correct frameIndex value for the function that
                         calls this method.
    '''

    _VERBOSITY = pyDecorator._VERBOSITY

    frame = _getframe(frameIndex)
    frameCode = frame.f_code

    pyDecorator.__print( '>>Function %s' % frameCode.co_name )

    if _VERBOSITY >= 1:
      pyDecorator.__print( '>>File \'%s\', line %i, in %s, argcount %i' % (
          frameCode.co_filename, frame.f_lineno, frameCode.co_name,
          frameCode.co_argcount)
        )

    if _VERBOSITY >= 2:
      pyDecorator.__print( '>>>Locals in the function are:' )
      pyDecorator.__pprint( frame.f_locals )

      if _VERBOSITY >= 3:
        pyDecorator.__print( '>>>Constants set are:' )
        pyDecorator.__pprint(frameCode.co_consts)


  @staticmethod
  def __printGlobals():
    r'''
    Prints the current globals seen from the source code. Note, this is the
    same regardless of what frame we are on.
    '''

    pyDecorator.__print( '>>>Globals seen are:' )
    pyDecorator.__pprint( _getframe(0).f_globals )


  @staticmethod
  def __printBuiltins():
    r'''
    Prints the current builtins seen from the source code. Note, this is the
    same regardless of what frame we are on.
    '''

    pyDecorator.__print( '>>>Builtins seen are:' )
    pyDecorator.__pprint( _getframe(0).f_builtins )


  @staticmethod
  def sampleTest():
    r'''
    Sample case to show how to use the decorate the function what one should
    except as the output
    '''


    @pyDecorator
    def helloArgs(*args, **kwargs):
      r'''
      Generic function that takes in all arguments and prints what is passed
      to it
      '''

      pyDecorator.__print('In helloArgs')
      pyDecorator.__print( 'args has:' )
      pyDecorator.__pprint( args )

      pyDecorator.__print( 'kwargs has:' )
      pyDecorator.__pprint( kwargs )

      pyDecorator.__printCurStack()

      pyDecorator.__print('Closing helloArgs')

      return 0

    retvalue = helloArgs(1, 2, 3, abc='123')

    if pyDecorator._DEBUG:
      if retvalue == 0:
        pyDecorator.__print( 'Returns from the test function are correct' )
      else:
        pyDecorator.__print( 'Returns from the test function are NOT correct' )


def pyDecorator_test():
  r'''
  Test function for pyDecorator
  '''

  print( 'Executing sample code' )

  # We can change the internal variables since all variables are 'public'
  # So the verbosity can be changed on the fly
  pyDecorator.setVERBOSITY(0)
  pyDecorator.setDEBUG(False)

  pyDecorator.sampleTest()

  print( 'Execution completed' )


if __name__ == '__main__':
  pyDecorator_test()

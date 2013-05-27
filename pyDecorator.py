#!/usr/bin/python

# Python pyDecorator class
# Attaches on to methods to provide tracking on successive function calls
# but can be used independently by calling pyDecorator.<static method>
# to pause and print the stack
#
# Created on 05-27-2013
# Updated on 05-27-2013
# Created by unsignedzero (David Tran)
# Version 0.6.0.0

from pprint import pprint
from sys import version_info

# We don't require the frame support but it helps
try:
  # Will work on all CPython builds
  from sys import _getframe
except ImportError:
  # All others here...
  from sys import callstats
  _getframe = None

# Set default to be default input even if in Python 2.X
if version_info[0] == 2:
  input = raw_input

class pyDecorate(object):
  r""" 
  This is a debugging decorator class that attaches to a function to
  print out variables information and well as stack information. The goal is 
  to make it easier to see the current stack and variables (state). As this
  reads pargs and kwargs, the only values that will change are non-atomic
  values (variables that we access by reference including arrays, and objects,
  to name a few.)

  This class is NOT meant to be called directly but attached or used to
  call its internal static methods

  Attributes:

      DEBUG            Set True to print out when pyDecorate methods are being
                       called and the recursionCount. 
      VERBOSE          Sets the verbosity level of the class

                       0 - Prints only the function names

                       1 - Mimics the exception handling of Python prints out
                           function name, file, line number and also arg count

                       2 - Prints all of 1 but also prints out constants and 
                           locals in the frame

                       3 - Prints all of 2 but also prints out globals and
                           built in functions with respect to the current
                           frame
  """
  # Static Counter
  recursionCall = 0

  DEBUG = False
  VERBOSE = 1

  def __init__(self, func):
    print( ">>Initializing pyDecorate class" )
    self.func = func
    self.count = 0

  def __call__(self, *args, **kwargs):
    pyDecorate.recursionCall += 1
    if pyDecorate.DEBUG:
      print ( "\n\n>>debugDecorator:pyDecorate.recursionCall count is %i" %
        pyDecorate.recursionCall )

    print( ">>We are calling %s" % self.func.__name__ )

    print( ">>For args we have:" )
    pprint( args )
    print( ">>For kwargs we have:" )
    pprint( kwargs )

    print( "\n>>Starting call to %s" % self.func.__name__ )
    print( ">>--------------------------------------------------" )
    self.func(*args, **kwargs)
    print( ">>--------------------------------------------------" )
    print( ">>Ended call to %s" % self.func.__name__ )

    pyDecorate.recursionCall -= 1
    if pyDecorate.DEBUG:
      print ( "\n\ndebugDecorator:pyDecorate.recursionCall count is %i" %
        pyDecorate.recursionCall )

  def _printCurStack(self):
    r"""
    Internal method that sets out the counter before calling the static method
    of similar name. This relies on the static variable DEBUG to tell it if it
    should print out its header.
    """
    self.count += 1
    if pyDecorate.DEBUG:
      print( ">>debugDecorator:Call count to decorator %i" % self.count )

      pyDecorate.printCurStack()

  @staticmethod
  def printCurStack():
    r"""
    Prints the full current stack of Python as well as additional information
    as specified by the value of VERBOSE in the same class. This will not
    print the first two elements on top of the stack, which will contain this
    method as well as the class frame. This relies on DEBUG to tell it if
    it should print out its header and trailer.

    See the docstring for the class for further information on VERBOSE.
    """

    i = 2

    if pyDecorate.DEBUG:
      print( ">>debugDecorator:printCurStack called. Unrolling stack...\n" )

    try:
      if _getframe:
        # With this loop we continue to trace down the stack until we are 
        # unable to. In that event, we create a ValueError exception and
        # thus exit outside the loop
        while True:
          pyDecorate.printCurFrame(i)
          i += 1
      else:
        print( ">>Number of functions already called %i" % callstats()[0] )
    except ValueError:
      pass
    
    if pyDecorate.DEBUG:
      print( "\n\ndebugDecorator:printCurStack finished" )

  def _pause(self):
    r"""
    Internal method that sets out the counter before calling the static method
    of similar name. This relies on the static variable DEBUG to tell it if
    it should print out its header.
    """
    self.count += 1

    if pyDecorate.DEBUG:
      print( "\n\n>>debugDecorator:Call count to decorator %i" % self.count )

    pyDecorate.pause()

  @staticmethod
  def pause():
    r"""
    Prints only the current frame on the stack before continuing on
    This implicitly relies on VERBOSE to tell it what to print. This prints
    the third element on the stack which is the function that calls this.

    See the docstring for the class for further information on VERBOSE.
    """

    if pyDecorate.DEBUG:
      print( ">>debugDecorator:pause called. Printing current Frame...\n" )

    pyDecorate.printCurFrame(2)

    if pyDecorate.DEBUG:
      print( "\n\n>>debugDecorator:pause closing...")
    input( "Pausing in pyDecorate. Press any key to continue." )

  @staticmethod
  def printCurFrame(frameIndex = 1):
    r"""
    Runs and prints the frameIndexth on the stack. This function CAN throw a
    ValueError when we go down to far. This function does NOT handle the
    exception so catch it as needed. The reason is if we call this function 
    many times, then it doesn't have to handle it each time.

    This function relies on the static variable VERBOSE to tell it what 
    to print out.

    ArgumentsL
        frameIndex       Tell this method which frame to print out. If not
                         passed then it will print out the 2nd frame, which,
                         if this method is explicitly called outside, will
                         be the correct frameIndex value for the function that
                         calls this method.
    """
    frame = _getframe(frameIndex)
    frameCode = frame.f_code

    print( ">>Function %s" % frameCode.co_name )
    if pyDecorate.VERBOSE >= 1:
      print( ">>File \"%s\", line %i, in %s, argcount %i" % (
          frameCode.co_filename, frame,f_lineno, frameCode.co_name,
          frameCode.co_argcount)
        )

    if pyDecorate.VERBOSE >= 2:
      print( ">>>Constants set are:" )
      pprint(frameCode.co_consts)
      print( ">>>Locals in the function are:" )
      pprint( frame.f_locals )
      if pyDecorate.VERBOSE >= 3:
        print( ">>>Globals seen are:" )
        pprint( frame.f_globals )
        print( ">>>Builtins seen are:" )
        pprint( frame.f_builtins )

def sampleTest():
  r"""
  Sample case to show how to use the decorate the function what one should
  except as the output
  """
  @pyDecorate
  def helloArgs(*args, **kwargs):
    print("In helloArgs")
    print( "args has:" )
    pprint( args )
    print( "kwargs has:" )
    pprint( kwargs )
    pyDecorate.pause()
    print("Closing helloArgs")

  helloArgs(1,2,3, abc="123")

if __name__ == '__main__':
  print( "Executing sample code" )
  sampleTest()

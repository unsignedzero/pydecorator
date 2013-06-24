#!/usr/bin/python

# Python pyDecorator class
# Attaches on to methods to provide tracking on successive function calls
# but can be used independently by calling pyDecorator.<static method>
# to pause and print the stack
#
# Created on 05-27-2013
# Updated on 05-28-2013
# Created by unsignedzero (David Tran)
# Version 0.7.0.0

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
# If default input is used elsewhere, regex the only use of "input"
# in this function to raw_input and comment the below two lines
if version_info[0] == 2:
  input = raw_input


class pyDecorator(object):
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

      DEBUG            Set True to print out when pyDecorator methods are being
                       called and the recursionCount. 
      VERBOSITY        Sets the verbosity level of the class

                       0 - Prints only the function names

                       1 - Mimics the exception handling of Python prints out
                           function name, file, line number and also arg count.
                           In the call, we 

                       2 - Prints all of 1 but also prints out constants and 
                           locals in the frame

                       3 - Prints all of 2 but also prints out globals and
                           built in functions with respect to the current
                           frame
  """

  # Static Counters
  recursionCall = 0
  callID = 0

  # State flags
  DEBUG = False
  VERBOSITY = 0

  def __init__(self, func):
    r"""
    Initializes the pyDecorator by storing the function and the call to it.
    """

    print( ">>Initializing pyDecorator class" )
    
    self.func = func
    self.count = 0


  def __call__(self, *args, **kwargs):
    r"""
    Manages the call of the function by printing debugging information as
    defined from pyDecorator.VERBOSITY and pyDecorator.DEBUG
    """

    pyDecorator.recursionCall += 1
    pyDecorator.callID += 1 

    # Caching values so we don't have to go out to the class repeatedly
    # and make it mostly local to the class
    DEBUG = pyDecorator.DEBUG
    VERBOSITY = pyDecorator.VERBOSITY
    LINE_STR = ""

    if VERBOSITY >= 1:
      LINE_STR = ">>--------------------------------------------------\n" 

    if DEBUG:
      print ( "\n\n>>pyDecorator:pyDecorator.recursionCall count is %i" %
        pyDecorator.recursionCall )

    if VERBOSITY >= 1:
      print( ">>We are calling %s" % self.func.__name__ )
      print( ">>For args we have:" )
      pprint( args )
      print( ">>For kwargs we have:" )
      pprint( kwargs )

    print( "\n>>Starting call to %s [Call#%03i]\n%s" %
      (self.func.__name__, pyDecorator.callID, LINE_STR) )

    # Remember to capture and return the args of the function called
    ret = self.func(*args, **kwargs)

    print( "%s>>Ended call to %s [Call#%03i]. Returned %s" %
      (LINE_STR, self.func.__name__, pyDecorator.callID, str(ret) ))

    pyDecorator.recursionCall -= 1

    if DEBUG:
      print ( "\n\npyDecorator:pyDecorator.recursionCall count is %i" %
        pyDecorator.recursionCall )

    return ret


  def _printCurStack(self):
    r"""
    Internal method that sets out the counter before calling the static method
    of similar name. This relies on the static variable DEBUG to tell it if it
    should print out its header.
    """

    self.count += 1

    if pyDecorator.DEBUG:
      print( ">>pyDecorator:Call count to decorator %i" % self.count )
      pyDecorator.printCurStack()


  @staticmethod
  def printCurStack():
    r"""
    Prints the full current stack of Python as well as additional information
    as specified by the value of VERBOSITY in the same class. This will not
    print the first two elements on top of the stack, which will contain this
    method as well as the class frame. This relies on DEBUG to tell it if
    it should print out its header and trailer.

    See the docstring for the class for further information on VERBOSITY.
    """

    i = 2

    if pyDecorator.DEBUG:
      print( ">>pyDecorator:printCurStack called. Unrolling stack...\n" )

    try:
      if _getframe:
        # With this loop we continue to trace down the stack until we are 
        # unable to. In that event, we create a ValueError exception and
        # thus exit outside the loop

        while True:
          pyDecorator.printCurFrame(i)
          i += 1

      else:
        print( ">>Number of functions already called %i" % callstats()[0] )

    except ValueError:
      pass
    
    if pyDecorator.DEBUG:
      print( "\n\npyDecorator:printCurStack finished" )


  def _pause(self):
    r"""
    Internal method that sets out the counter before calling the static method
    of similar name. This relies on the static variable DEBUG to tell it if
    it should print out its header.
    """

    self.count += 1

    if pyDecorator.DEBUG:
      print( "\n\n>>pyDecorator:Call count to decorator %i" % self.count )

    pyDecorator.pause()


  @staticmethod
  def pause():
    r"""
    Prints only the current frame on the stack before continuing on
    This implicitly relies on VERBOSITY to tell it what to print. This prints
    the third element on the stack which is the function that calls this.

    See the docstring for the class for further information on VERBOSITY.
    """

    if pyDecorator.DEBUG:
      print( ">>pyDecorator:pause called. Printing current Frame...\n" )

    pyDecorator.printCurFrame(2)

    if pyDecorator.DEBUG:
      print( "\n\n>>pyDecorator:pause closing...")

    input( "Pausing in pyDecorator. Press any key to continue." )


  @staticmethod
  def printCurFrame(frameIndex = 1):
    r"""
    Runs and prints the frameIndexth on the stack. This function CAN throw a
    ValueError when we go down to far. This function does NOT handle the
    exception so catch it as needed. The reason is if we call this function 
    many times, then it doesn't have to handle it each time.

    This function relies on the static variable VERBOSITY to tell it what 
    to print out.

    Arguments:
        frameIndex       Tell this method which frame to print out. If not
                         passed then it will print out the 2nd frame, which,
                         if this method is explicitly called outside, will
                         be the correct frameIndex value for the function that
                         calls this method.
    """

    frame = _getframe(frameIndex)
    frameCode = frame.f_code

    print( ">>Function %s" % frameCode.co_name )

    if pyDecorator.VERBOSITY >= 1:
      print( ">>File \"%s\", line %i, in %s, argcount %i" % (
          frameCode.co_filename, frame.f_lineno, frameCode.co_name,
          frameCode.co_argcount)
        )

    if pyDecorator.VERBOSITY >= 2:
      print( ">>>Locals in the function are:" )
      pprint( frame.f_locals )

      if pyDecorator.VERBOSITY >= 3:
        print( ">>>Constants set are:" )
        pprint(frameCode.co_consts)


  @staticmethod
  def printGlobals():
    r"""
    Prints the current globals seen from the source code. Note, this is the
    same regardless of what frame we are on.
    """

    print( ">>>Globals seen are:" )
    pprint( _getframe(0).f_globals )


  @staticmethod
  def printBuiltins():
    r"""
    Prints the current builtins seen from the source code. Note, this is the 
    same regardless of what frame we are on.
    """

    print( ">>>Builtins seen are:" )
    pprint( _getframe(0).f_builtins )


  @staticmethod
  def sampleTest():
    r"""
    Sample case to show how to use the decorate the function what one should
    except as the output
    """

    @pyDecorator
    def helloArgs(*args, **kwargs):
      r"""
      Generic function that takes in all arguments and prints what is passed
      to it
      """

      print("In helloArgs")
      print( "args has:" )
      pprint( args )

      print( "kwargs has:" )
      pprint( kwargs )

      pyDecorator.printCurStack()

      print("Closing helloArgs")

      return 0

    a = helloArgs(1,2,3, abc="123")

    if pyDecorator.DEBUG:
      if a == 0:
        print( "Returns from the test function are correct" )
      else:
        print( "Returns from the test function are NOT correct" )

if __name__ == '__main__':
  print( "Executing sample code" )

  # We can change the internal variables since all variables are "public"
  # So the verbosity can be changed on the fly 
  pyDecorator.VERBOSITY = 0
  pyDecorator.DEBUG = True

  pyDecorator.sampleTest()

  print( "Execution completed" )


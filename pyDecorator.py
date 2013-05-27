#!/usr/bin/python

# Python pyDecorator class
# Attaches on to methods to provide tracking on successive function calls
# but can be used independently by calling pyDecorator.<static method>
# to pause and print the stack
#
# Created on 05-27-2013
# Updated on
# Created by unsignedzero (David Tran)
# Version 0.5.0.0

from pprint import pprint
from sys import version_info

# We don't require the frame support but it helps
try:
  from sys import _getframe
except ImportError:
  from sys import callstats
  _getframe = None

# Set default to be default input
if version_info[0] == 2:
  input = raw_input

# We create a global "self" variable to allow users in their code to
# print the stack

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
  """
  # Static Counter
  recursionCall = 0

  DEBUG = False
  VERBOSE = 0

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
    self.count += 1
    if pyDecorate.DEBUG:
      print( ">>debugDecorator:Call count to decorator %i" % self.count )

      pyDecorate.printCurStack()

  @staticmethod
  def printCurStack():
    i = 2

    if pyDecorate.DEBUG:
      print( ">>debugDecorator:printCurStack called. Unrolling stack...\n" )

    try:
      if _getframe:
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
    self.count += 1

    if pyDecorate.DEBUG:
      print( "\n\n>>debugDecorator:Call count to decorator %i" % self.count )

    pyDecorate.pause()

  @staticmethod
  def pause():

    if pyDecorate.DEBUG:
      print( ">>debugDecorator:pause called. Printing current Frame...\n" )

    pyDecorate.printCurFrame(2)

    if pyDecorate.DEBUG:
      print( "\n\n>>debugDecorator:pause closing...")
    input( "Pausing in pyDecorate. Press any key to continue." )

  @staticmethod
  def printCurFrame(value = 1):
    frame = _getframe(value)
    frameCode = frame.f_code

    print( ">>We are in %s with %i args passed" %
      (frameCode.co_name, frameCode.co_argcount) ) 
    if pyDecorate.VERBOSE >= 1:
      print( ">>Filename: %s" % frameCode.co_filename )
      print( ">>Line Number: %i" % frame.f_lineno )

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

@pyDecorate
def helloArgs(*pargs, **kwargs):
  print("In helloArgs")
  print( "pargs has:" )
  pprint( pargs )
  print( "kwargs has:" )
  pprint( kwargs )
  pyDecorate.pause()
  print("Closing helloArgs")


if __name__ == '__main__':
  helloArgs(1, 2, 3, aba="blue")

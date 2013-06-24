# pyDecorator #

This is a simple python decorator library that attaches onto functions and
adds additional debugging functionality to the function in question. This
decorator can print out the current stack as well as local/global
methods/variables that are local to each function on the stack as well
as names and related.

Created by unsignedzero and started on 05-27-2013 as an idea.

# TO DO #

# Version/Changelog #

# 0.7.1.0 04-24-2013 #
* Added small test for return value of helloArgs
* Added more comments in code
* Set default verbosity to 0

# 0.7.0.0 05-28-2013 #
* Return values of function now return correctly
* SampleTest now an integrated static method
* Cleaned up comments and made VERBOSE 0 less VERBOSE
* Removed printing of globals and builtins in the frame since they are the
  same across all frames. Changed to static functions that people can access.
* Change all names of functions so they are all pyDecorator and not pyDecorate,
  VERBOSE is now VERBOSITY, added more whitespace between methods to make it 

# 0.6.0.0 05-27-2013 #
* Additional comments added to code and this README.md is created

# 0.5.0.0 05-27-2013 #
* Basic idea formed and concept created.

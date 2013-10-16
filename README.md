# pyDecorator [![Build status:Can't load apt.travis-ci.org](https://api.travis-ci.org/unsignedzero/pydecorator.png)](https://travis-ci.org/unsignedzero/pydecorator)

This is a simple python decorator library that attaches onto functions and
adds additional debugging functionality to the function in question. This
decorator can print out the current stack as well as local/global
methods/variables that are local to each function on the stack as well
as names and related.

Created by unsignedzero and started on 05-27-2013 as an idea.

## TO DO #
### Test Suite #
* Create more/new tests

* * * *

# Version/Changelog #

* * * *

# 0.8.2.0 10-15-2013 #
* New warning added to class comments.
* Constants, setters and getters are now in CamelCase for ease of typing.
* Hook points noted for further API expansion
* Bugfix with printCurStack
* Reordered methods so it is easier to read
* Method print function added.
* Print functions can now be set to not print to logs

# 0.8.1.0 10-10-2013 #
* Bugfix with regex used on pyDecorator.
* Removed comment in travis file about running the test using setup.py

# 0.8.0.0 10-10-2013 #
* Converted header docs into docstrings
* Public Release.
* Python test min version 2.7+
* Fixed problem with running tests at root or in test directory or via
  a py.test tests or python setup.py test call. All calls should be consistent.
* Integrated logger class for easy output.
* Integrated setup.py to this module and set up basic py.test tests.

# 0.7.2.0 10-04-2013 #
* Added setter/getter for static variables
* Added .gitignore file
* Removed extra spaces at end of line and updated comments

# 0.7.1.0 06-24-2013 #
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

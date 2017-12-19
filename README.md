# SVN Autocommit

This simple python script is used for auto-commit the local filesystem changes
into global svn repository. The agenda of this script is to utilise svn tool  
but there is no limitation to use it for git and other cvs tools too

prerequisites:
* Python 2.7 
* watchdog framework, If not installed use  "pip install watchdog"
* platform, socket, os and subprocess are common in python world if not instal
-led use "pip install platform socket subprocess os"
* In windows older version of TortoiseSVN "svn" command line is not enabled by
default, Reinstall TortosiseSVN and select command line svn in setup config

script usage:
python autocommit.py <[--path = <user source path>] [--destinatio = <SVN Destination path>] [
--ignore= <File format needs to ignore>] [--no-recursive=no] [--force=no] [
--sleep-time = 60]>
By defualt autommit.py takes default arguments in "command" dictnory parameters
NOTE: For multiple ignore patterns use space

API's of autocommit.py can be invoked by wrapper functions, Refer autocommit_wrapper.py for example
wrapper functions

To use functions in stand alone mode i.e without running on background interrupt functions,
change dictonary value of command["STAND_ALONE"] to "yes" where by default its "no".

 For running in background
 * Windows:
   "pythonw autocommit.py" 

 * Linux:
   "nohup python autocommit.py&" 
   TIP: To check status use "tail -f nohup.out"

TODO:
 1. set the PATH in windows environment for python running 
 2. Test 'taskkill' in Windows 
 3. Passing "command" dictnory from the wrapper functions 
 4. Testing CLI commands in windows --- Low priority
 6. rm -rf /path/ results error impliment SVN cleanup once recived a error  -- Low priority
 7. Add a switch to not produce nohup.out file in linux 
 8. Analise stored TEXT logs in Windows
 9. If passowrd experise throw the Exception message
10. Impliment ignore_patterns macros for wathcdoghandler
11. Add dictionary word for command["STAND_ALONE"] to disable watchdog timer
12. Make uinque way of passing variables to functions

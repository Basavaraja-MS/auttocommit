# SVN Autocommit



This simple python script is used for auto-commit the local filesystem changes

into global svn repository. The agenda of this script is to utilize svn tool  

but there is no limitation to use it for git and other cvs tools too



prerequisites:

* Python 2.7 

* watchdog framework, If not installed use  "pip install watchdog"

* platform, socket, os and subprocess are common in python world if not installed
use "pip install platform socket subprocess os"

* In windows older version of TortoiseSVN "svn" command line is not enabled by

default, Reinstall TortoiseSVN and select command line svn in setup config



script usage:

python autocommit.py <[--path = <user source path>] [--destinatio = <SVN Destination path>] [

--ignore= <File formats needs to ignore>] [--no-recursive=no] [--force=no] [

--sleep-time = 60]>

By defualt autommit.py takes default arguments in "command" dictnory parameters

NOTE: For multiple ignore patterns use space



API's of autocommit.py can be invoked by wrapper functions, Refer autocommit_wrapper.py for example

wrapper functions



 For running in background

 * Windows:

   "pythonw autocommit.py" 



 * Linux:

   "nohup python autocommit.py&" 

   TIP: To check status use "tail -f nohup.out"



TODO:

 1. set the PATH in windows environment for python running 
* Give these instructions to user

 2. Test 'taskkill' in Windows 
* Tested working successfully 

 3. Passing "command" dictnory from the wrapper functions 
* Use command line variables to pass as parameters 

 4. Testing CLI commands in windows --- Low priority
* Done working fine 

 6. rm -rf /path/ results error impliment SVN cleanup once recived a error  -- Low priority
* Working fine 

 7. Add a switch to not produce nohup.out file in linux
* Done 

 8. Analise stored TEXT logs in Windows
* TODO:

 9. If there is password expiry throw the Exception message
* Currently terminal will open for password entry, Need to test robustly   

10. Implement ignore_patterns macros for watchdog handler
* Done 

11. Add dictionary word for command["STAND_ALONE"] to disable watchdog timer
* Done

12. Make unique way of passing variables to functions
* TODO:
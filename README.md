# SVN Autocommit

This simple python script is used for auto commit the local filesystem changes
into global svn repository. The agenda of this script is to utilise svn tool  
but there is no limitation to use it for git and other cvs tools too

prerequisites:
* Python 2.7 
* watchdog frame work "pip install watchdog"
* platform, socket, os and subprocess are common in python world if not instal
-led use "pip install platform socket subprocess os"
* In windows older version of TortoiseSVN "svn" command line is not enabled by
default, Re install TortosiseSVN and select command line svn in setup config
TODO: 1.Create a function which checks all above things if not found do the above
chages with user permission 

script usage:
python autocommit.py <[Folder path] [--destinatio = <SVN Destination path>] [
--ignore= <File format needs to ignore>] [--no-recursive=no] [--force=no] [
--sleep-time = 60]>

By default it takes current directory and commits changes to the GLOBAL_SVN
path

 For running in background
 * Windows:
   pythonw autocommit.py 

 * Linux:
   nohup python autocommit.py& 
   TIP: To check status use "tail -f nohup.out"

TODO:
2. user name passowrd handling guidelines
3. For running background use 'exec' or write background sckip

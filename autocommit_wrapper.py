import autocommit
import platform 
import os

os_name = platform.system()

#chekc of svn installed in winodws and Linux 
#chekc for watchdog and argparse 
#In windows set python path 

#cmd = nohup python -c "import autocommit as a; a.svn_main()" &
cmd = "python autocommit &"
if os_name == 'Linux':
    cmd = "nohup python autocommit.py &"
    os.system(cmd)
elif os_name == 'Windows':
    #os.system("pythonw -c "import autocommit as a; a.svn_main()"")
    cmd = "pythonw autocommit.py"
    os.system(cmd)
else:
    print "Implimented for Linux and Winows only"

import autocommit
import platform 
import os

os_name = platform.system()
nohuplogs = 1     #To not generate nohup output

#cmd = nohup python -c "import autocommit as a; a.svn_main()" &
cmd = "python autocommit &"
if os_name == 'Linux':
    cmd = "nohup python autocommit.py &"
    if nohuplogs == 1:
        cmd = "nohup python autocommit.py >/dev/null 2>&1 &"
    os.system(cmd)
elif os_name == 'Windows':
    #os.system("pythonw -c "import autocommit as a; a.svn_main()"")
    cmd = "pythonw autocommit.py"
    os.system(cmd)
else:
    print "Implimented for Linux and Winows only"


def kill_svn():
    if os_name == 'Linux':
        os.system("kill $(ps aux | grep autocommit.py | awk '{ print $2 }')")
    elif os_name == 'Windows':
        os.system("taskkill /f /im  autocommit.py")

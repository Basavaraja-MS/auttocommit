#!/usr/bin/python
import time
import sys
import platform
import socket
import os
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
        
class Module_ReturnValue(object):
    def __init__(self, Status, Message, Error_Code, Warning_Codes):
        self.Status = Status
        self.Message = Message
        self.Error_Code = Error_Code
        self.Warning_Codes = Warning_Codes

def github_chekin():
    hostname = socket.gethostname()
    osused = platform.system()
    os.chdir(user_path)
#TODO: User name and passowrd needs to add it 
    os.system("git config --global user.name \"Basavaraja-MS\"")
    os.system("git config --global user.name")
    retval = os.system("pwd")
    retval = os.system("git add *")
    retval = os.system("git commit -m \"'hostname' 'osused' \"")
    retval = os.system("git push -f")
    print retval 

def FORCE(command):
    print "Comming"
    if command["FORCE"] == "yes":
        print "Comming here and crash"
        return " --force "
    else:
        return ""

def RECURSIVE(command):
    if command["RECURSIVE"] == "yes":
        return " --recursive "
    else:
        return ""

def svn_checkin(src_path):
    print "Checkin:"
    hostname = socket.gethostname()
    osused = platform.system()
    message = "Host: " + hostname + "OS: " + osused 
    p = subprocess.Popen(['svn', 'ci', '-m', str(message)])
    p.wait()

def svn_add(src_path):
    global gCommands
    hostname = socket.gethostname()
    osused = platform.system()
    print "svn add soruce path "
    print src_path
    #TODO:
    #cmd = "svn add: FORCE(gCommands)+ RECURSIVE(gCommands) + src_path
    cmd = "svn add --force " + src_path
    retval = os.system(cmd)
    return retval

def svn_remove(src_path):
    global gCommands
    hostname = socket.gethostname()
    osused = platform.system()
    #TODO:
    #cmd = "svn del " + FORCE(gCommands) + src_path
    cmd = "svn del --force " + src_path
    retval = os.system(cmd)
    print"svn del:", retval
    return retval

def svn_checkout(src_path):
    retval = os.system("svn checkout " + src_path + " .")
    print "SVN chekout:", retval
    return retval

def svn_up(command):
    os.chdir(command["USER_PATH"])
    cmd = "svn up " +  command["USER_PATH"] + FORCE(command)
    
    try:
        retval = os.system(cmd)      
    except Exception:
        svn_checkout(command["DEST"])
        if retval == "E155037":
            os.system("svn cleanup")
        elif retval == "E155007":
            svn_checkout(command["DEST"])
            
    print "svn up:", retval
    return retval 


def svn_ignore(command):
    print "SVN autocommit: Ignored"
    for ignore_str in command["IGNORE"].split():
        cmd = "svn propset svn:ignore " + ignore_str + " " + command["USER_PATH"] + FORCE(command) + RECURSIVE(command)
        os.system(cmd)


def svn_app_init(command):
    os.chdir(command["USER_PATH"])
    retval = os.system("svn info")
    if retval != 0:                     # if there is unsucessfull in svn info 
        print "SVN autocommit: Creating local repo"
        svn_checkout(command["DEST"])
        
    retval = svn_up(command)
    print "SVN autocommit: Updating local repo"
    if retval != 0:
        print "Failure in svn up"
        return retval
    svn_ignore(command)

class watchdogHandler(PatternMatchingEventHandler):
#TODO: Need to check and change

    def __init__(self):
        self._patterns = None
        self._ignore_patterns = ["*.swp", "*.swx", 'entries', 'format', 'pristine', 
                                          '*.svn-base', 'tmp', '*wc.db*', '*svn*']
        self._case_sensitive = False
        self._ignore_directories=False

    def process(self, event):
        if event.event_type == 'modified':
            print 'Modified', event.src_path
            svn_checkin(event.src_path)
        elif event.event_type == 'created':
            print 'Created', event.src_path
            svn_add(event.src_path)
        elif event.event_type == 'moved': 
            print 'Moved', event.src_path
        elif event.event_type == 'deleted':
            print 'Deleted', event.src_path
            svn_remove(event.src_path)
        else:
            print "Error in", event.event_type

    def on_modified(self, event):
        self.process(event)
    def on_created(self, event):
        self.process(event)
    def on_moved(self, event):
        self.process(event)
    def on_deleted(self, event):
        self.process(event)

import argparse
def default_command_init():
    commands = {
                    "USER_PATH" : "D:/Python/sw",
                    "DEST"      : "http://cosmicsvn/svnserintf/Standard/Validation/IP/sw/",
                    "IGNORE"    : "*.swp " "*.swx " "*.swa ",
                    "RECURSIVE" : "yes",
                    "FORCE"     :"no",
                    "SLEEP"     :60
                }
    
    return commands


def get_user_args():
    phrase = argparse.ArgumentParser(description='SVN autocommit tool')
    phrase.add_argument(
        '-p', '--path', type=str, help='user source path')
    phrase.add_argument(
        '-d', '--destination', type=str, help='Destination svn path')
    phrase.add_argument(
        '-i', '--ignore', type=str, help='Files to be ignored')
    phrase.add_argument(
        '-r', '--recursive', type=str, help='Recursive search enabled')
    phrase.add_argument(
        '-f', '--force', type=str, help='Enable forced operations')
    phrase.add_argument(
        '-s', '--sleep', type=int, help='Sleep time in ms')
    args = phrase.parse_args()
    return args

def set_user_args(usr_cmds, deflt_cmds):
    if usr_cmds.destination != None:
        deflt_cmds["USER_PATH"] = usr_cmds.path
    if usr_cmds.destination != None:
        deflt_cmds["DEST"] = usr_cmds.destination
    if usr_cmds.ignore != None:
        deflt_cmds["IGNORE"] = usr_cmds.ignore.split(",")
    if usr_cmds.recursive != None:
        deflt_cmds["RECURSIVE"] = usr_cmds.recursive
    if usr_cmds.force != None:
        deflt_cmds["FORCE"] = usr_cmds.force
    if usr_cmds.sleep != None:
        deflt_cmds["SLEEP"] = usr_cmds.sleep
    return deflt_cmds

def args_sanity_check(command):
    try:
        os.chdir(command["USER_PATH"])
    except Exception:
        msg = "SVN Autocommit: user path not exists"
        Failure = True
        Error_Code  = 81.0
        Warning_Code_list = None
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)

    try:
        os.system("svn info " + command["DEST"])
    except Exception:
        msg = "SVN Autocommit: SVN path not exist"
        Failure = True
        Error_Code  = 81.1
        Warning_Code_list = None
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)

    if (command["IGNORE"] != "yes" and command["IGNORE"] != "no"):
        msg = "SVN Autocommit: Invalid --ignore value"
        Failure = True
        Error_Code  = 81.2
        Warning_Code_list = None
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)

    if (command["FORCE"] != "yes" and command["FORCE"] != "no"):
        msg = "SVN Autocommit: Invalid --force value"
        Failure = True
        Error_Code  = 81.3
        Warning_Code_list = None
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)

    if (command["RECURSIVE"] != "yes" and command["RECURSIVE"] != "no"):
        msg = "SVN Autocommit: Invalid --recursive value"
        Failure = True
        Error_Code  = 81.3
        Warning_Code_list = None
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)
    return command



def svn_main():
    print "Welcome to autocommit"
    deflt_cmds = default_command_init()
    print deflt_cmds
    try:
         usr_cmds = get_user_args()
    except Exception:
        msg = "SVN Autocommit: Error in command phrasing"
        Failure = True
        Error_Code  = 80.0
        Warning_Code_list = None
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)

    commands = set_user_args(usr_cmds, deflt_cmds)
    global gCommands
    gCommands = args_sanity_check(commands)
    print gCommands

    svn_app_init(commands)
    print "svn app: Init done successfull"

    event_handler = watchdogHandler()
    observer = Observer()
    try:
        observer.schedule(event_handler, 
			path = commands["USER_PATH"],
			recursive=True)
    except Exception:
        msg = "SVN Autocommit: Error in job scheduling"
        Failure = True
        Error_Code  = 82.0
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)

    observer.start()
    while True:
        time.sleep(60)
    observer.join()

#While writing CLI enable below comments
if __name__ == "__main__":
    svn_main() 

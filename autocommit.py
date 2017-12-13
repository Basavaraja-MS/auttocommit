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

def svn_checkin(src_path):
    print "Checkin:"
    hostname = socket.gethostname()
    osused = platform.system()
    message = "Host: " + hostname + "OS: " + osused 
    p = subprocess.Popen(['svn', 'ci', '-m', "Test message on ci"])
    p.wait()

def svn_add(src_path):
    hostname = socket.gethostname()
    osused = platform.system()
    retval = os.system("svn add --force " + src_path)
    return retval

def svn_remove(src_path):
    hostname = socket.gethostname()
    osused = platform.system()
    retval = os.system("svn del --force " + src_path)
    print"svn del:", retval
    return retval

def svn_clone(src_path):
    print "Clone will be taken care later"

def svn_up(src_path, server_path):
    retval = os.system("svn up --force " + src_path)
    print "svn up:", retval
    return retval 

def svn_init(user_path, server_path):
    os.chdir(user_path)
    svn_clone(server_path)
    svn_up(user_path, server_path)
    svn_ignore(user_path)

def svn_ignore(usr_path):
    print "svn ignore will be called"
    os.chdir(usr_path)
    os.system("svn propset svn:ignore *.swx " + usr_path)
    os.system("svn propset svn:ignore *.swp " + usr_path)
    os.system("svn propset svn:ignore dirname .svn "  + usr_path)

class watchdogHandler(PatternMatchingEventHandler):
#TODO: Need to check and change

    def __init__(self):
        self._patterns = None
        self._ignore_patterns = ["*.swp", "*.swx"]
        self._ignore_directories=["xtensa_ivp"]
        self._case_sensitive = False

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

def get_args():
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

def set_args(usr_cmds, deflt_cmds):
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

def svn_sanity_check(user_path, server_path):
    try:
        os.chdir(user_path)
    except Exception:
        msg = "SVN Autocommit: user path not exists"
        Failure = True
        Error_code  = 81.0
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)

    try:
        os.system("svn info " + server_path)
    except Exception:
        msg = "SVN Autocommit: SVN path not exist"
        Failure = True
        Error_code  = 81.1
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)


def app_init():
    commands = {
                    "USER_PATH" : "/media/basavam/autocommit/sw",
                    "DEST"      : "http://10.246.128.9/svnserintf/Standard/Validation/IP/sw/",
                    "IGNORE"    : "*.swp " "*.swx " "*.swa " ".svn",
                    "RECURSIVE" : "yes",
                    "FORCE"     :"no",
                    "SLEEP"     :60
                }
    return commands

def svn_main():
    deflt_cmds = app_init()
    
    try:
         usr_cmds = get_args()
    except Exception:
        msg = "SVN Autocommit: Error in command phrasing"
        Failure = True
        Error_code  = 80.0
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)

    commands = set_args(usr_cmds, deflt_cmds)

    svn_sanity_check(commands["USER_PATH"], commands["DEST"])

    svn_init(commands["USER_PATH"], commands["DEST"])
    event_handler = watchdogHandler()
    observer = Observer()

    try:
        observer.schedule(event_handler, 
			path = commands["USER_PATH"],
			recursive=True)
    except Exception:
        msg = "SVN Autocommit: Error in job scheduling"
        Failure = True
        Error_code  = 82.0
        return Module_ReturnValue(Failure, msg, Error_Code, Warning_Code_list)

    observer.start()
    while True:
        time.sleep(60)
    observer.join()

#While writing CLI enable below comments

"""
if __name__ == "__main__":
    svn_main() 
"""

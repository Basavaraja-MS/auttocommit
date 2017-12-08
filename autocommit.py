#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler

count=0
user_path = "/media/basavam/autocommit/git_gateway/Helloworld/master"
user_path_svn = "/media/basavam/autocommit/sw"
FORCE = "-f" # user is resposible for activating this

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global count
        count += 1
        print (count)

import platform
import socket
import os
import subprocess


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

def svn_chekin():
    print("Chekin:")
    hostname = socket.gethostname()
    osused = platform.system()
    os.chdir(user_path_svn)
    #retval = os.system("svn ci --force-log --username basavam -m " + "Test commits " + user_path_svn)
    cmd = "svn ci --force-log --username basavam -m "     + "Test commits " + user_path_svn
    p = subprocess.Popen(['svn', 'ci', '-m', 'cmd'])
    p.wait()

def svn_add(src_path):
    hostname = socket.gethostname()
    osused = platform.system()
    os.chdir(user_path_svn)
    retval = os.system("svn add --force " + src_path)
    return retval

def svn_remove(src_path):
    hostname = socket.gethostname()
    osused = platform.system()
    os.chdir(user_path_svn)
    retval = os.system("svn del --force " + src_path)
    return retval

def svn_clone():
    print "Clone will be taken care later"

def svn_up():
    print"svn up:"
    retval = os.system("svn up --force " + user_path_svn)
    print retval

def svn_init():
    svn_clone()
    svn_up()

def svn_ignore():
    print "svn ignore will be called"
    os.chdir(user_path_svn)
    os.system("svn propset svn:ignore *.swx " + user_path_svn)
    os.system("svn propset svn:ignore *.swp " + user_path_svn)

class watchdogHandler(PatternMatchingEventHandler):
    def __init__(self):
        self._patterns = None
        self._ignore_patterns = ["*.swp", "*.swx"]
        self._ignore_directories=None
        self._case_sensitive = False
        svn_init()
        svn_ignore() 
    def process(self, event):
        if event.event_type == 'modified':
            print 'Modified', event.src_path
            svn_chekin()
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



if __name__ == "__main__":
    #event_handler = MyHandler()
    event_handler = watchdogHandler()
    observer = Observer()
    observer.schedule(event_handler, 
			path='.' if user_path_svn == "" else user_path_svn,
			recursive=False)
    observer.start()
    while True:
        time.sleep(60)
    observer.join()
"""
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
"""


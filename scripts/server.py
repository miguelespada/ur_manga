#!/usr/bin/env python3
from OSC import OSCServer
import sys
from time import sleep


import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

from controllerLib import *
robot, scene, group, zeroPose  = initRobot()

HOST = (ip, 7000)
server = OSCServer( HOST  )
server.timeout = 0
run = True

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)

def zero_callback(path, tags, args, source):
    if args[0] == 1.0: goToZero()

def uno_callback(path, tags, args, source):
    if args[0] == 1.0:  pushTwo((2, 4), (2, 5))

def all_callback(path, tags, args, source):
    if args[0] == 1.0:  pushAll()

def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

def stop_callback(path, tags, args, source):
    group.stop()

def trajectory_callback(path, tags, args, source):
    if args[0] == 1.0:
        trajectory = "0,0;2,11;2,0;0,11"
        tokens = trajectory.split(";")
        tPoints = []
        for t in tokens:
            tPoints.append(map(lambda x: int(x), t.split(",")))
        createPath(tPoints)

server.addMsgHandler( "/1/push4",  trajectory_callback )
server.addMsgHandler( "/1/push5", stop_callback )
server.addMsgHandler( "/1/push6", quit_callback )
server.addMsgHandler( "/1/push1",  zero_callback )
server.addMsgHandler( "/1/push2",  uno_callback )
server.addMsgHandler( "/1/push3",  all_callback )

# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()


print "Listening ", HOST 
# simulate a "game engine"
try:
    while run:
        sleep(0.1)
        # call user script
        each_frame()
    raise KeyboardInterrupt
except KeyboardInterrupt:
    pass

print "Bye!"
print "Close rospy"
rospy.signal_shutdown("final")
server.close()
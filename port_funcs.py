#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Jonathan Robinson (@robin0025)
###########################################################################
#
# Simple set of functions for different EEG trigger communication systems.
# containing:
# 1 - nidaq_init() = Initates national instrument port with key parameters.
# 2 - serial_init() = Initates national instrument port with key parameters.
# 3 - portreset() = Resets port by sending high/low for 3 common trigger types.
# 4 - initTrig() = Handles initiation of 3 common trigger types and resets ports
# 5 - send = trigselect() = placed under win.flip() to send trigger and reset send variable 		immediately after screen is flipped.
###########################################################################


from psychopy import parallel, core
import sys


#######################################################
# Initiate Nation instruments triggering
#
# Input:
# - path = a path to the required python library (nidaqmx). 
#	Easy to install in anaconda. 
# Output:
# - port = an object for use in subsequent triggering
#######################################################
def nidaq_init(path):
    if path:
        sys.path.insert(1, path)
    #~/anaconda3/lib/python3.7/site-packages/nidaqmx
    import nidaqmx 
    from nidaqmx.constants import LineGrouping
    port = nidaqmx.Task()
    port.do_channels.add_do_chan('Dev1/port0/line0:7',line_grouping=LineGrouping.CHAN_FOR_ALL_LINES) #Address for access to pins[0-7]
    
    return port


#######################################################
# Initiate Serial Trigger
#
# Input:
# - add = address of the serial port to be found in devices manager eg. 'COM#' [default='COM6']
# Output:
# - port = an object for use in subsequent triggering
#######################################################
def serial_init(add='COM6'):
    import serial
    port= serial.Serial()
    port.Port = add
    port.open()
    
    return port


#######################################################
# Port rest trigger function.
#
# Input:
# - mode = allows experimenter to switch between different trigger modes. 
#	0[default] = no port trigger sent for testing.
#	1 = LPT triggers reset.
#	2 = national instruments port reset.
#	3 = serial port reset.
# - port = object created by port initialisation functions [default=empty]
# Output:
# - triggers are sent to max (255) and then to all off (0)
#######################################################
def portreset(mode=0, port = []):
    base = 0
    max = 255
    
    if mode == 1 and port: #parallel port
        port.setData(max)
        print('Sending max trigger value')
        core.wait(1.0)
        print('Sending zero trigger value')
        port.setData(base)
    elif mode == 2 and port: #national instruments port
        port.write(max)
        print('Sending max trigger value')
        core.wait(1.0)
        print('Sending zero trigger value')
        port.write(base)
    elif mode == 3 and port:
        port.write(chr(int(max)))
        print('Sending max trigger value')
        core.wait(1.0)
        print('Sending zero trigger value')
        port.write(chr(int(base)))
    else:
        print('No port was reset')


#######################################################
# Generic trigger initiation
# Raps in the previous two functions to initialise triggers and also reset port by sending it high and then to zero.
# Input:
# - mode = allows experimenter to switch between different trigger modes. 
#	0[default] = no port initated for testing.
#	1 = LPT initialisation.
#	2 = national instruments port initialisation.
#	3 = serial port initialisation.
# - add = address of the serial port to be found in devices manager eg. 'COM#' (not needed for NI port) [default=0]
# - path = path to nidaqmx python library (not required for others) [default='']
# Output:
# - port = an object for use in subsequent triggering
#######################################################
def initTrig(mode=0,add=0,path=''):
    if mode == 1: #mod 1 sends parallel port triggers.
	if add != 0:        
	   port = parallel.ParallelPort(address=add)
           portreset(mode,port)
	else:
	   port = parallel.ParallelPort(address=888) #the standard LTP 1
           portreset(mode,port)
    elif mode == 2:
        port = nidaq_init(path) #national instruments port
        portreset(mode,port)
    elif mode == 3 and add != 0:
	if add != 0:
           port = serial_init(add)  # open first serial port
           portreset(mode,port)
	else: 
           port = serial_init()  # open first serial port
           portreset(mode,port)
    else: 
        print('Warninig: No port initiated.')
        port = []
    
    return port


#######################################################
# Send trigger function.
#
# Function usually ptrigselect(code,send,mode=0,port=[],clock=None)laced with win.flip(), so that triggers are sent immediately when stim is flipped to screen. 
# Useage if sendTrigger is set to zero before exp and set to one on event onset:
# - sendTrigger = trigselect(<someCode>, sendTrigger, <someMode>, <somePortObject>)
#
# Input:
# - code = the trigger you want to send (0-255).
# - send = A value set to one by an event onset, function then sets it back to zero in the following frame
# - mode = allows experimenter to switch between different trigger modes. 
#	0[default] = no port trigger sent for testing.
#	1 = LPT triggers sned.
#	2 = national instruments trigger sent.
#	3 = serial port trigger sent.
# - port = object created by port initialisation functions [default=empty].
# - clock = a clock object to tell the user when the trigger was sent [default=None].
# Output:
# - send = should be named consistent with the send input, it will reset it.
# - A triggers betwee 0 and 255, these are reset to zero on the following frame.
#######################################################
def trigselect(code,send,mode=0,port=[],clock=None):
    if mode == 1 and port: #parallel port
        port.setData(0)
        if send == 1:
            port.setData(code)
            send = 0
            if clock != None:
                print('code %s sent at time= %s'%(code,clock.getTime()))
                
    elif mode == 2 and port: #national instruments port
        port.write(0)
        if send == 1:
            port.write(code)
            send = 0
            if clock != None:
                print('code %s sent at time= %s'%(code,clock.getTime()))
                
    elif mode == 3 and port:
        port.write(chr(int(0)))
        if send == 1:
            port.write(chr(int(code)))
            send = 0
            if clock != None:
                print('code %s sent at time= %s'%(code,clock.getTime()))
    else:
        if send == 1:
            print('code %s sent at time= %s'%(code,clock.getTime()))
            send = 0
    
    
    return send 
   

#####################################################################
# Automatically generated file
# Don't edit this file
# Created on: 9 March 2013
#####################################################################

import threading
import sys, os 

sys.path.insert(0, os.path.join(os.path.abspath('.'), 'dpdebug.zip'))

import pydevd
pydevd.settrace('172.16.3.154', stdoutToServer=False, stderrToServer=False, suspend=False, trace_only_current_thread=False)
threading.settrace(pydevd.GetGlobalDebugger().trace_dispatch)

print "Debugging Dia framework ...\r\n"

if not os.path.isdir('C:/Users/Lewis/Dropbox/Dia releases/Dia versions/Dia_2.1.0/'):
    execfile(os.path.join(os.path.abspath('.'), 'dia.py'))
else:
    execfile('C:/Users/Lewis/Dropbox/Dia releases/Dia versions/Dia_2.1.0/dia.py')


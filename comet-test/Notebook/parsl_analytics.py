import re
import os
import subprocess
import pandas as pd
from datetime import datetime

def stamp_to_num(ss):
    
    DB_DATE_FORMAT = '%H:%M:%S.%f'
    time = datetime.strptime(ss, DB_DATE_FORMAT).timestamp()
    return time

def get_session_tstamps():
       
        s    = list()
        dur  = list()
        line = "/home/aymen/RADICAL/Parsl-RP/comet-test/Parsl/parsl_sessions"
        cmd  =  "find %s -iname 'interchange.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            session_id = (paths[f].decode().split('/')[8])
            with open(paths[f], 'rb') as fh:
                first = next(fh).decode()
                fh.seek(-4096, 2)
                last = fh.readlines()[-1].decode()
                f = first.split()[1]
                l = last.split()[1]
                s.append(session_id)
                dur.append(stamp_to_num(l) - stamp_to_num(f))
        df = pd.DataFrame(list(zip(s, dur)), columns =['Session', 'Duration'])
        dd = df.sort_values('Duration')
        return(dd.reset_index(drop=True))

def get_workers_tstamps():
        
        dur = list()
        line = '/home/aymen/RADICAL/Parsl-RP/comet-test/Parsl/parsl_sessions'
        cmd  =  "find %s -iname 'worker_*.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            with open(paths[f], 'rb') as fh:
                first = next(fh).decode()
                last = fh.readlines()[-1].decode()
                f = first.split()[1]
                l = last.split()[1]
                dur.append(stamp_to_num(l) - stamp_to_num(f))
        print (dur)
        return dd


def get_manager_tstamps():

        dur  = list()
        line ='/home/aymen/RADICAL/Parsl-RP/comet-test/Parsl/parsl_sessions'
        cmd  =  "find %s -iname 'manager.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            with open(paths[f], 'rb') as fh:
                first = next(fh).decode()
                last = fh.readlines()[-1].decode()
                f = first.split()[1]
                l = last.split()[1]
                dur.append(stamp_to_num(l) - stamp_to_num(f))
        print (dur)
        return dur

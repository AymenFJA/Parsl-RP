import re
import os
import subprocess
import pandas as pd
from datetime import datetime

def stamp_to_num(ss):
    
    DB_DATE_FORMAT = '%H:%M:%S.%f'
    time = datetime.strptime(ss, DB_DATE_FORMAT).timestamp()
    return time

def get_queue_tstamps(s_path):
    s    = list()
    t    = list()
    dur  = 0
    file = s_path
    with open(file, 'rb') as fh:
        for line in fh:
            if re.match("(.*)0/0/1(.*)",str(line)):
                time_stmp = line.decode().split()[1]
                try:
                    t.append(stamp_to_num(time_stmp))
                except Exception as e:
                    print(e)
            else:
                pass
        try:
            dur = t[-1]-t[0]
        except IndexError:
            dur = 0
    return dur

                
                


def get_session_tstamps():
       
        s    = list()
        dur  = list()
        line = "/home/aymen/RADICAL/Parsl-RP/comet-test/Parsl/parsl_sessions/SS"
        cmd  =  "find %s -iname 'parsl.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            session_id = (paths[f].decode().split('/')[9])
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

def get_interchange_tstamps():
       
        s    = list()
        dur  = list()
        line = "/home/aymen/RADICAL/Parsl-RP/comet-test/Parsl/parsl_sessions/SS"
        cmd  =  "find %s -iname 'interchange.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            session_id = (paths[f].decode().split('/')[9])
            with open(paths[f], 'rb') as fh:
                first = next(fh).decode()
                fh.seek(-4096, 2)
                last = fh.readlines()[-1].decode()
                f = first.split()[1]
                l = last.split()[1]
                s.append(session_id)
                dur.append(stamp_to_num(l) - stamp_to_num(f))
        df = pd.DataFrame(list(zip(s, dur)), columns =['Session', 'Interchange_Duration'])
        dd = df.sort_values('Interchange_Duration')
        return(dd.reset_index(drop=True))

def get_workers_tstamps():
        
        s   = list()
        dur = list()
        line = '/home/aymen/RADICAL/Parsl-RP/comet-test/Parsl/parsl_sessions/SS'
        cmd  =  "find %s -iname 'worker_*.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            session_id = (paths[f].decode().split('/')[9])
            with open(paths[f], 'rb') as fh:
                first = next(fh).decode()
                last = fh.readlines()[-1].decode()
                f = first.split()[1]
                l = last.split()[1]
                s.append(session_id)
                dur.append(stamp_to_num(l) - stamp_to_num(f))
        df = pd.DataFrame(list(zip(s, dur)), columns =['Session', 'Worker_Duration'])
        dd = df.sort_values('Session')
        return(dd.reset_index(drop=True))


def get_manager_tstamps():
    
        s    = list()
        dur  = list()
        line ='/home/aymen/RADICAL/Parsl-RP/comet-test/Parsl/parsl_sessions/SS'
        cmd  =  "find %s -iname 'manager.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            session_id = (paths[f].decode().split('/')[9])
            with open(paths[f], 'rb') as fh:
                first = next(fh).decode()
                last = fh.readlines()[-1].decode()
                f = first.split()[1]
                l = last.split()[1]
                s.append(session_id)
                dur.append(stamp_to_num(l) - stamp_to_num(f))
        df = pd.DataFrame(list(zip(s, dur)), columns =['Session', 'Manager_Duration'])
        dd = df.sort_values('Session')
        return (dd.reset_index(drop=True))

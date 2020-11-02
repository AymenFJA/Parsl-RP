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
        line = "/home/aymen/RADICAL/radical.pilot/examples/parsl/WS"
        cmd  =  "find %s -iname 'parsl.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            session_id = (paths[f].decode().split('/')[9])
            with open(paths[f], 'rb') as fh:
                print(paths[f])

                first_line = fh.readline()
                print(first_line)
                for last_line in fh:
                    if 'parsl.dataflow.dflow:846' in last_line.split():
                        print(last_line.split())
                        f = first_line.split()[1]
                        l = last_line.split()[1]
                        s.append(session_id)
                        dur.append(stamp_to_num(l) - stamp_to_num(f))
                    else:
                         print ("something is wrong ")
        df = pd.DataFrame(list(zip(s, dur)), columns =['Session', 'Duration'])
        dd = df.sort_values('Duration')
        return(dd.reset_index(drop=True))
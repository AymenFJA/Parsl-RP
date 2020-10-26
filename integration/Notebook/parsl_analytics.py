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
        line = "/home/aymen/RADICAL/radical.pilot/examples/parsl/WS/runinfo/000/parsl.log"
        cmd  =  "find %s -iname 'parsl.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            session_id = (paths[f].decode().split('/')[9])
            with open(paths[f], 'rb') as fh:
                first = next(fh).decode()
                fh.seek(0, os.SEEK_END)
                last = fh.readlines()[-1].decode()
                f = first.split()[1]
                l = last.split()[1]
                s.append(session_id)
                dur.append(stamp_to_num(l) - stamp_to_num(f))
        df = pd.DataFrame(list(zip(s, dur)), columns =['Session', 'Duration'])
        dd = df.sort_values('Duration')
        return(dd.reset_index(drop=True))
import re
import os
import subprocess
from datetime import datetime

def stamp_to_num(ss):
    
    DB_DATE_FORMAT = '%H:%M:%S.%f'
    time = datetime.strptime(ss, DB_DATE_FORMAT).timestamp()
    return time

def get_session_tstamps():
        
        dur = list()
        line = "/home/aymen/SummerRadical/Parsl-RP/comet-test/Parsl/parsl_sessions"
        cmd =  "find %s -iname 'interchange.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            with open(paths[f], 'rb') as fh:
                first = next(fh).decode()
                fh.seek(-4096, 2)
                last = fh.readlines()[-1].decode()
                f = first.split()[1]
                l = last.split()[1]
                dur.append(stamp_to_num(l) - stamp_to_num(f))
        print (dur)
        return dur
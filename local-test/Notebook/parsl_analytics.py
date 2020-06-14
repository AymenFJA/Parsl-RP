import re
import os
import subprocess

def stamp_to_num(ss):
    test_num = re.split(":", ss)[2]
    return float(test_num)

def get_session_tstamps():
        
        dur = list()
        line = "/home/aymen/SummerRadical/Parsl-RP/local-test/Parsl/parsl_sessions"
        cmd =  "find %s -iname 'parsl.log'" %line
        paths = [line for line in subprocess.check_output(cmd , shell=True).splitlines()]
        for f in range(len(paths)):
            with open(paths[f], 'rb') as fh:
                first = next(fh).decode()
                fh.seek(-1024, 2)
                last = fh.readlines()[-1].decode()
                f = first.split()[1]
                l = last.split()[1]
                dur.append(stamp_to_num(l) - stamp_to_num(f))
        print (dur)
        return dur

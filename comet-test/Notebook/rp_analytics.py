import os
import sys
import pprint
import pandas as pd
import radical.pilot as rp
import radical.utils     as ru
import radical.analytics as ra

def get_session_tstamps():
    
    s    = list()
    time_stamps = list()
    loc = [dI for dI in os.listdir('../RP/sessions/') if os.path.isdir(os.path.join('../RP/sessions/',dI))]
    for session in range(len(loc)):
        session_id = (loc[session])
        src = os.path.dirname(loc[session])
        sid = os.path.basename(loc[session])
        session = ra.Session(sid=sid, stype='radical.pilot', src=os.path.join('../RP/sessions/',loc[session]))
        event_entity = 'pilot'
        pilot = session.filter(etype=event_entity, inplace=True)
        s.append(session_id)
        time_stamps.append(pilot.ttc)
        
    df = pd.DataFrame(list(zip(s, time_stamps)), columns =['Session', 'Duration'])
    dd = df.sort_values('Duration')
    return (dd.reset_index(drop=True))

def get_unit_tstamps():
    time_stamps = list()
    loc = [dI for dI in os.listdir('../RP/sessions/') if os.path.isdir(os.path.join('../RP/sessions/',dI))]
    for session in range(len(loc)):
        src = os.path.dirname(loc[session])
        sid = os.path.basename(loc[session])
        session = ra.Session(sid=sid, stype='radical.pilot', src=os.path.join('../RP/sessions/',loc[session]))
        event_entity = 'unit'
        unit = session.filter(etype=event_entity, inplace=True)
        print(unit.uid)
        time_stamps.append(unit.timestamps())
    return (time_stamps)
    
#!/usr/bin/env python

__copyright__ = 'Copyright 2013-2014, http://radical.rutgers.edu'
__license__   = 'MIT'

import os
import sys

import radical.pilot as rp
import radical.utils as ru

# ------------------------------------------------------------------------------
#
# READ the RADICAL-Pilot documentation: https://radicalpilot.readthedocs.io/
#
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    # we use a reporter class for nicer output
    report = ru.Reporter(name='radical.pilot')
    report.title('Getting Started (RP version %s)' % rp.version)


    # Create a new session. No need to try/except this: if session creation
    # fails, there is not much we can do anyways...
    session = rp.Session(uid=ru.generate_id('rp.session.ss.18N.%(item_counter)04d', mode=ru.ID_CUSTOM))

    # all other pilot code is now tried/excepted.  If an exception is caught, we
    # can rely on the session object to exist and be valid, and we can thus tear
    # the whole RP stack down via a 'session.close()' call in the 'finally'
    # clause...
    try:

        # read the config used for resource details
        config = ru.read_json('%s/config.json' % os.path.dirname(os.path.abspath(__file__)))
        pmgr   = rp.PilotManager(session=session)
        umgr   = rp.UnitManager(session=session)

        report.header('submit pilots')

        # Add a Pilot Manager. Pilot managers manage one or more ComputePilots.

        # Define an [n]-core local pilot that runs for [x] minutes
        # Here we use a dict to initialize the description object
        pd_init = {'resource'      : 'xsede.comet_ssh',
                   'runtime'       : 600,  # pilot runtime (min)
                   'exit_on_error' : True,
                   'project'       : 'unc100',
                   'queue'         : 'compute',
                   'access_schema' : 'gsissh',
                   'cores'         :  432,
                   'gpus'          : 0,
                  }
        pdesc = rp.ComputePilotDescription(pd_init)

        # Launch the pilot.
        pilot = pmgr.submit_pilots(pdesc)

        n = 1728  #number of units to run
        report.header('submit %d units' % n)

        # Register the ComputePilot in a UnitManager object.
        umgr.add_pilots(pilot)

        # Create a workload of ComputeUnits.
        # Each compute unit runs '/bin/date'.

        report.progress_tgt(n, label='create')
        cuds = list()
        for i in range(0, n):

            # create a new CU description, and fill it.
            # Here we don't use dict initialization.
            cud = rp.ComputeUnitDescription()
            cud.executable    = '/home/aymen/stress-ng/stress-ng --cpu 1 --timeout 300 --metrics-brief'
            cud.cpu_processes = 1
            cuds.append(cud)
            report.progress()

        report.progress_done()
        #pilot.wait([rp.PMGR_ACTIVE])

        # Submit the previously created ComputeUnit descriptions to the
        # PilotManager. This will trigger the selected scheduler to start
        # assigning ComputeUnits to the ComputePilots.
        umgr.submit_units(cuds)

        # Wait for all compute units to reach a final state (DONE, CANCELED or FAILED).
        umgr.wait_units()


    except Exception as e:
        # Something unexpected happened in the pilot code above
        report.error('caught Exception: %s\n' % e)
        ru.print_exception_trace()
        raise

    except (KeyboardInterrupt, SystemExit):
        # the callback called sys.exit(), and we can here catch the
        # corresponding KeyboardInterrupt exception for shutdown.  We also catch
        # SystemExit (which gets raised if the main threads exits for some other
        # reason).
        ru.print_exception_trace()
        report.warn('exit requested\n')

    finally:
        # always clean up the session, no matter if we caught an exception or
        # not.  This will kill all remaining pilots.
        report.header('finalize')
        session.close(download=True)

    report.header()


# ------------------------------------------------------------------------------


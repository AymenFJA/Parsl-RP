"""RADICAL-Executor builds on the RADICAL-Pilot/ParSL
"""

from concurrent.futures import Future

import radical.pilot as rp
import radical.utils as ru

import typeguard
import logging
import threading
import queue
import pickle
import os
from multiprocessing import Process, Queue
from typing import Any, Dict, List, Optional, Tuple, Union

from ipyparallel.serialize import pack_apply_message  # ,unpack_apply_message
from ipyparallel.serialize import deserialize_object  # ,serialize_object

from parsl.app.errors import RemoteExceptionWrapper
from parsl.executors.errors import *
from parsl.executors.base import ParslExecutor
from parsl.dataflow.error import ConfigurationError
from parsl.providers.provider_base import ExecutionProvider

from parsl.utils import RepresentationMixin
from parsl.providers import LocalProvider

logger = logging.getLogger(__name__)



class RADICALExecutor(StatusHandlingExecutor):
    """Executor designed for cluster-scale

    The RADICALExecutor system has the following components:
      1. "start" resposnible for creating the RADICAL-executor session and pilot.
      2. "submit" resposnible for translating and submiting ParSL tasks the RADICAL-executor.
      3.  "shut_down"  resposnible for shutting down the RADICAL-executor components

    Here is a diagram

    .. code:: python
                                                                                                                     RADICAL Executor
        ----------------------------------------------------------------------------------------------------------------------------------------------------
                        ParSL API                          |         ParSL DFK/dflow               |      Task Translator      |     RP-Client/Unit-Manager
        ---------------------------------------------------|---------------------------------------|---------------------------|----------------------------                                                     
                                                           |                                       |                           |
         parsl_tasks_description ------>  ParSL_tasks{}----+-> Dep. check ------> ParSL_tasks{} ---+--> ParSL Task/Tasks desc. | umgr.submit_units(RP_units)
                                           +api.submit     | Data management          +dfk.submit  |             |             |
                                                           |                                       |             v             |
                                                           |                                       |     RP Unit/Units desc. --+->   
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """        

    @typeguard.typechecked
    def __init__(self,
                 label: str = 'RADICALExecutor',
                 resource: str = Optional[str] = "NULL",
                 tasks = list(),
                 cores_per_task = 1,
                 managed: bool = True,
                 max_tasks: Union[int, float] = float('inf'),
                 worker_logdir_root: Optional[str] = "."):

        logger.debug("Initializing RADICALExecutor")
        self.label = label
        self.session = rp.Session(uid=ru.generate_id('parsl.radical_executor.session.%(item_counter)04d',
                                  mode=ru.ID_CUSTOM))
        self.pilot_manager = rp.PilotManager(session=self.session)
        self.unit_manager  = rp.UnitManager(session=self.session)
        self.resource = resource
        self.tasks = tasks
        self.cores_per_task = cores_per_task
        self.managed = managed
        self.max_tasks = max_tasks
        self._task_counter = 0
        self.run_dir = '.'
        self.worker_logdir_root = worker_logdir_root

        
    def start(self):
        """Create the Pilot process and pass it.
        """
        pmgr = self.pilot_manager

        if self.resource is None : report.exit('specify remoute or local resource')


        else : pd_init = {'resource'      : self.resource,
                          'runtime'       : 30,  # pilot runtime (min)
                          'exit_on_error' : True,
                          'project'       : 'unc100',
                          'queue'         : config[resource].get('queue', None),
                          'access_schema' : config[resource].get('schema', None),
                          'cores'         : config[resource].get('cores', 1),
                          'gpus'          : config[resource].get('gpus', 0),}

        pdesc = rp.ComputePilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)

        return pilot

    def submit(self, func, *args, **kwargs):
        """Submits task/tasks to RADICAL unit_manager.

        Args:
            - func (callable) : Callable function
            - *args (list) : List of arbitrary positional arguments.

        Kwargs:
            - **kwargs (dict) : A dictionary of arbitrary keyword args for func.

        Returns:
              Future
        """
                
        if self._executor_bad_state.is_set():
            raise self._executor_exception

        # here call the start function

        pilot = self.start
        umgr   = self.unit_manager
        report.header('submit pilots')

        self._task_counter += 1
        task_id = self._task_counter

        report.header('submit %d units' % max_tasks)

        # Register the ComputePilot in a UnitManager object.
        umgr.add_pilots(pilot)

        for i in range(0, self.max_tasks):
            
            task = rp.ComputeUnitDescription()
            self.tasks[task_id] = Future()
            task executable = func
            task.arguments = [args, kwargs]
            task.cpu_processes = self.cores_per_task
            self.tasks.append(task)
        
        umgr.submit_units(tasks)
        umgr.wait_units()


    def shutdown(self, hub=True, targets='all', block=False):
        """Shutdown the executor, including all RADICAL-Pilot components."""
        self.unit_manager.close()
        self.pilot_manager.close()
        self.session.close(download=True)
        logger.info("Attempting RADICALExecutor shutdown")

        return True

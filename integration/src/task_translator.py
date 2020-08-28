import radical.pilot as rp
import radical.utils as ru

tasks = {}
parsl_task_description = [executable, self.tasks[task_id]['resource_specification'], *args, **kwargs]

class TaskTranslator(object):
        """
        -------------------------------------------------------------------------------------------------------------------------
         ParSL API                       |                   | ParSL DFK/dflow |                     |      Task Translator      
        ---------------------------------|                   |-----------------|                     |---------------------------
                                         |                   |                 |                     |                           
         parsl_tasks_description ------>  ParSL_tasks{}--->    Dep. check       --> ParSL_tasks{} -->      ParSL Task/Tasks desc.
                                         |                   | Data management |                     |             |             
                                         |                   |                 |                     |             v             
                                         |                   |                 |                     |     RP Unit/Units desc.   
        -------------------------------------------------------------------------------------------------------------------------
        """        

    def __init__(self):

        pass

    def task_translator(self, parsl_task_description):

        cud = rp.ComputeUnitDescription()
        cuds = list()
        cud.executable = parsl_task_description[0]
        cud.cores      = parsl_task_description[1]['cores'] #assuming that the resource specification first item is cores .... TBD
        cuds.append(cud)

        return cuds



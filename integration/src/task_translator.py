import radical.pilot as rp
import radical.utils as ru

#This is a simple python dictionary

tasks = {'task1000':{
                    'status':'TBD',#---------------> Status of the task faile/sucess
                    'app_fu':'TBD',#---------------> Function/executable to be executed
                    'hashsum':'TBD',#--------------> Need to be invistagated
                    'executor':'TBD',#-------------> Type of executor (HTEX, Low_Latency, etc.)
                    'from_memo':'TBD',#------------> Need to be invistagated
                    'fail_count':'TBD',#-----------> Number of times this task failed
                    'parsl_resource_specification': # Resource specification of this task
                                                   {'cores': 1,
                                                    'memory': 1000,
                                                    'disk': 1000}}}


task_id = 'task0001'
parsl_task_description = [executable, self.tasks[task_id]['resource_specification'], *args, **kwargs]

class TaskTranslator(object):
        """
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

    def __init__(self):

        pass

    def task_translator(self, parsl_task_description):

        cud = rp.ComputeUnitDescription()
        cuds = list()
        cud.executable = parsl_task_description[0]
        cud.cores      = parsl_task_description[1]['cores'] #assuming that the resource specification first item is cores .... TBD
        cuds.append(cud)

        return cuds



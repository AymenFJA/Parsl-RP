import parsl
import os 
from parsl.app.app import python_app, bash_app
from parsl import File

parsl.set_stream_logger()

from parsl.config import Config
from parsl.channels import SSHChannel
from parsl.providers import SlurmProvider
from parsl.addresses import address_by_query
from parsl.executors import HighThroughputExecutor
from parsl.executors.high_throughput import interchange	


config = Config(
    executors=[
        HighThroughputExecutor(
            label='comet_htex',
            worker_debug=True,
            address='js-17-185.jetstream-cloud.org',
            max_workers=24,
            #workers_per_node = 24, # Getting error for unexpexted argument
            cores_per_worker=1,
            worker_logdir_root = '/home/aymen/parsl_scripts',
            interchange_address= 'comet-ln2.sdsc.edu', #'js-17-185.jetstream-cloud.org','comet-ln2.sdsc.edu',
            interchange_port_range=(50000, 50400),
            worker_port_range=(50500, 51000),
            provider=SlurmProvider(
                'debug',
                channel=SSHChannel(
                    hostname='comet-ln2.sdsc.edu',
                    username='aymen',     # Please replace USERNAME with your username
                    password='xSeDe2017',
                    script_dir='/home/aymen/parsl_scripts',    # Please replace USERNAME with your username
                ),
                #launcher=SrunLauncher(),
                scheduler_options='',     # Input your scheduler_options if needed
                worker_init='source ve/parsl-env/bin/activate',     # Input your worker_init if needed
                #worker_init='source activate /oasis/projects/nsf/unc100/aymen/anaconda3/envs/conda-parsl',
                #partition = "debug",
                walltime="00:10:00",
                init_blocks=1,
                max_blocks=1,
                #tasks_per_node = 24, # Getting error for unexpexted argument
                nodes_per_block=1,
                #cores_per_node=24, # Getting error for unexpexted argument
                parallelism=24,
            ),
            #working_dir="/home/aymen/parsl_scripts",
        )
    ],
strategy=None,
)
#os.environ['SSH_AUTH_SOCK'] ='/tmp/ssh-sxsiHjHLhr/agent.6773'
parsl.load(config)

@bash_app
def stress_ng(outputs=[], stdout='/home/aymen/stress_output/stress_ng.stdout', stderr='/home/aymen/stress_output/stress_ng.stderr'):
    return '/home/aymen/stress-ng/stress-ng --cpu 1 --timeout 300 > {0}'.format(outputs[0])

# loop to execute the simulation app 3 times
results = []

for i in range(24):
    out_file = "/home/aymen/stress_output/stress_ng_{0}".format(i)
    results.append(stress_ng(outputs=[out_file]))

# print each job status, initially all are running
print ("Job Status: {}".format([r.done() for r in results]))

# wait for all apps to complete
[r.result() for r in results]

# print each job status, they will now be finished
print ("Job Status: {}".format([r.done() for r in results]))

# collect up the output files and print their values
outputs = [r.outputs[0] for r in results]
for o in outputs:
    with open(o.filename, 'r') as f:
        print(f.read().strip())

parsl.dfk().cleanup()

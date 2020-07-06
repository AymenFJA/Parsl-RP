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
#from parsl.data_provider.scheme import GlobusScheme


config = Config(
    executors=[
        HighThroughputExecutor(
            label='comet_htex',
            worker_debug=True,
            address='js-17-185.jetstream-cloud.org',
            max_workers=1,
            cores_per_worker=24,
            worker_logdir_root = '/home/aymen/parsl_scripts',
            #address=address_by_query(),
            interchange_address='comet-ln2.sdsc.edu',
            interchange_port_range=(50100, 50400),
            #client_address = "129.114.17.185",
            worker_port_range=(50500, 51000),
            provider=SlurmProvider(
                'debug',
                channel=SSHChannel(
                    hostname='comet-ln2.sdsc.edu',
                    username='aymen',     # Please replace USERNAME with your username
                    password='xSeDe2017',
                    script_dir='/home/aymen/parsl_scripts',    # Please replace USERNAME with your username
                ),
                # launcher=SrunLauncher(),
                scheduler_options='',     # Input your scheduler_options if needed
                #worker_init='conda activate /oasis/projects/nsf/unc100/aymen/anaconda3/envs/parsl-env',     # Input your worker_init if needed
                worker_init='source /home/aymen/ve/parsl-env/bin/activate',
                walltime="00:10:00",
                init_blocks=1,
                max_blocks=1,
                nodes_per_block=1,
                parallelism=24,
            ),
            working_dir="/home/aymen/parsl_scripts",
            #client_address = "129.114.17.185",
            #worker_port_range=(54000, 55000), 

            #interchange_address = "js-17-185.jetstream-cloud.org" 
            #storage_access=[GlobusScheme(
            #    endpoint_uuid='de463f97-6d04-11e5-ba46-22000b92c6ec',
            #    endpoint_path='/',
            #    local_path='/')],
        )
    ],
strategy=None,
)
#os.environ['SSH_AUTH_SOCK'] ='/tmp/ssh-zJpG5aVnTM/agent.1985'

parsl.load(config)

@python_app
def create_unsorted_file(outputs=[]):
    """Create an unsorted file by generating random numbers"""
    from random import randint
    file = open(outputs[0], 'w')
    for i in range(0,50):
        file.write("{0}\n".format(randint(1,100)))
    file.close()

@bash_app
def sort(unsorted, outputs=[]):
    """Call sort executable on the input file"""
    return "sort -g {0} > {1}".format(unsorted, outputs[0])

# create the unsorted file
unsorted = create_unsorted_file(outputs=[os.path.join('/home/aymen/parsl_scripts', "unsorted-generated.txt")])

# sort the file into a new file called sorted_d.txt
s = sort(unsorted.outputs[0],
         outputs=[os.path.join('/home/aymen/parsl_scripts', "sorted_d.txt")])

# wait for the app to complete
output_file = s.outputs[0].result()

# use Parsl's SSH channel to copy the sorted file
dfk.executor.execution_provider.channel.pull_file(output_file, '.')
with open(os.path.basename(output_file), 'r') as f:
     print(f.read().replace("\n",","))
parsl.dfk().cleanup()

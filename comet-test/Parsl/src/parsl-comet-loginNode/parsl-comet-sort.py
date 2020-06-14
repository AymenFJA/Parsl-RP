import os
import parsl
from parsl.app.app import python_app, bash_app
from parsl.config import Config
from parsl.launchers import SrunLauncher
from parsl.providers import SlurmProvider
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_query
config = Config(
    executors=[
        HighThroughputExecutor(
            label='Comet_HTEX_multinode',
            address=address_by_query(),
            worker_logdir_root='/home/aymen/parsl_scripts',
            max_workers=1,
            provider=SlurmProvider(
                'debug',
                launcher=SrunLauncher(),
                # string to prepend to #SBATCH blocks in the submit
                # script to the scheduler
                scheduler_options='',
                # Command to be run before starting a worker, such as:
                # 'module load Anaconda; source activate parsl_env'.
                worker_init='source /home/aymen/parsl-env/bin/activate',
                walltime='00:10:00',
                init_blocks=1,
                max_blocks=1,
                nodes_per_block=1,
            ),
        )
    ]
)
parsl.load(config)
@bash_app
def sort(unsorted, outputs=[]):
    """Call sort executable on the input file"""
    return "sort -g {} > {}".format(unsorted, outputs[0])
s = sort(os.path.abspath("input/unsorted.txt"),
         outputs=[os.path.abspath("output/sorted_c.txt")])
output_file = s.outputs[0].result()
print("Contents of the unsorted.txt file:")
with open('input/unsorted.txt', 'r') as f:
    print(f.read().replace("\n",","))
print("\nContents of the sorted output file:")
with open(output_file, 'r') as f:
    print(f.read().replace("\n",","))
parsl.clear()

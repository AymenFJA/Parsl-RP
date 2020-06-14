import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config

from parsl.providers import LocalProvider
from parsl.channels import LocalChannel
from parsl.config import Config
from parsl.executors import HighThroughputExecutor

print(parsl.__version__)


local_htex = Config(
    executors=[
        HighThroughputExecutor(
            label="htex_Local",
            worker_debug=True,
            max_workers=3,
            cores_per_worker=1,
            provider=LocalProvider(
                channel=LocalChannel(),
                init_blocks=1,
                max_blocks=3,
                parallelism=3,
            ),
        )
    ],
    strategy=None,
)

parsl.load(local_htex)

@bash_app
def stress_ng(outputs=[], stdout='stress_ng.stdout', stderr='stress_ng.stderr'):
    return 'sudo stress --cpu 1 --timeout 20 > {0}'.format(outputs[0])

# loop to execute the simulation app 3 times
results = []

for i in range(3):
    out_file = "stress_ng_{0}".format(i)
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
        
parsl.clear()




#stress_ng().result()



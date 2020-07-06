import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config
print(parsl.__version__)

'''
load configurations
'''
parsl.load(config)
# App that generates a random number after a delay
@python_app
def generate(limit,delay):
    from random import randint
    import time
    time.sleep(delay)
    return randint(1,limit)

# Generate 5 random numbers between 1 and 10
rand_nums = []
for i in range(5):
    rand_nums.append(generate(10,i))

# Wait for all apps to finish and collect the results
outputs = [i.result() for i in rand_nums]

# Print results
print(outputs)

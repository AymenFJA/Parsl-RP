# Use Case Requirements

Following [This work can be viewed here as part of Aymen-Matteo supervision](https://docs.google.com/document/d/1GNeHzy-5H5JRo2VR5Gdu6m4NxN1OPv0SX8JIcaESbi0/edit?pli=1#heading=h.nrnw03t7conb).


# Experiments Specification

In this reposirory, we are studying the scaling performance of 2 systems [RADICAL-Pilot](https://github.com/radical-cybertools/radical.pilot) and [PaRsL Highthroughput executor (HTEX)](https://github.com/Parsl/parsl/tree/master/parsl/executors). The expirements varies from 1-72 nodes (24 cores per node) on comet. 

## Weak Scaling Non-MPI wokload

| Experiment ID | # Tasks  | # Nodes | # Cores/t  | Runtime/t |
|---------------|----------|---------|------------|-----------|
| 1             | 24       | 1       | 24         |  300s     |
| 2             | 1728     | 72      | 1728       |  300s     |



- n number of tasks depends on the number of cores of (24 cores per node).
- Tasks are homogeneous.
- The executablke is a single `stress-ng` that runs for `300s` or `5m` on a single core.
- The number of cores is just a function of the number of GPUs that each task requires.

## PaRsL:
| Session ID    | # Tasks/# Cores  | # Nodes | Theoritical TTX | Calculated TTX |
|---------------|------------------|---------|-----------------|----------------|
|session0000.1N | 24/24            | 1       |  300s           |  301.166042    |
|session0001.1N | 24/24            | 1       |  300s           |  301.369750    |
|session0002.1N | 24/24            | 1       |  300s           |  301.128917    |
|session0003.1N | 24/24            | 1       |  300s           |  300.904375    |
|session0000.72N| 1728/1728        | 72      |  300s           |  311.790120    |
|session0001.72N| 1728/1728        | 72      |  300s           |  342.917255    |
|session0002.72N| 1728/1728        | 72      |  300s           |  304.714755    |
|session0003.72N| 1728/1728        | 72      |  300s           |  331.325476    |


## RADICAL-Pilot:

| Session ID    | # Tasks/# Cores  | # Nodes | Theoritical TTX | Calculated TTX |
|---------------|------------------|---------|-----------------|----------------|
|session0000.1N | 24/24            | 1       |  300s           |  303.0         |
|session0001.1N | 24/24            | 1       |  300s           |  304.0         |
|session0002.1N | 24/24            | 1       |  300s           |  302.0         |
|session0003.1N | 24/24            | 1       |  300s           |  302.0         |
|session0000.72N| 1728/1728        | 72      |  300s           |  392.0         |
|session0001.72N| 1728/1728        | 72      |  300s           |  363.0         |
|session0002.72N| 1728/1728        | 72      |  300s           |  385.0         |
|session0003.72N| 1728/1728        | 72      |  300s           |  391.0         |

## Strong Scaling

We fix the maximum amount of tasks we are able to run from the weak scaling experiments (1728) and we increase the number of cores by a factor sed for the weak scaling experiments. We then run these tasks on a progressively large amount of resources until we get to full concurrency as run in the weak scaling experiments.


### TBD.....!

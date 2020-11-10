# Use Case Requirements

### TBD....

# Experiments Specification

In this reposirory, we are studying the scaling performance of 2 systems [RADICAL-Pilot](https://github.com/radical-cybertools/radical.pilot) and [PaRsL Highthroughput executor (HTEX)](https://github.com/Parsl/parsl/tree/master/parsl/executors). The expirements varies from 1-72 nodes (24 cores per node) on comet. 

Links for the integration work progress:

- 1 [RP-Parsl integration details](https://docs.google.com/document/d/1Z5hu-M8ynCmIum7KFFAyENn3CUNM9NhG9cjw-gWjriA/edit?usp=sharing)
- 2 [RP-Parsl High level](https://docs.google.com/document/d/1vm3C3ESE6S-C5zFd_mJs9lybQQO521k8RNh16qn2078/edit?usp=sharing)

## Weak Scaling Non-MPI wokload

| Experiment ID | # Tasks  | # Nodes | # Cores/t  | Runtime/t |
|---------------|----------|---------|------------|-----------|
| 1             | 24       | 1       | 24         |  300s     |
| 2             | 48       | 48      | 48         |  300s     |
| 3             | 432      | 36      | 432        |  300s     |
| 4             | 1728     | 72      | 1728       |  300s     |



- n number of tasks depends on the number of cores of (24 cores per node).
- Tasks are homogeneous.
- The executablke is a single `stress-ng` that runs for `300s` or `5m` on a single core.

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

## PaRsL:
| Session ID       | # Tasks/# Cores  | # Nodes | Theoritical TTX | Calculated TTX |
|------------------|------------------|---------|-----------------|----------------|
|parsl.ss.18N.0001 | 1728/24          | 1       |                 |                |
|parsl.ss.18N.0001 | 1728/48          | 2       |                 |                |
|parsl.ss.18N.0001 | 1728/432         | 18      |                 |                |
|parsl.ss.18N.0001 | 1728/864         | 36      |                 |                |

## RADICAL-Pilot:
| Session ID       | # Tasks/# Cores  | # Nodes | Theoritical TTX | Calculated TTX |
|------------------|------------------|---------|-----------------|----------------|
|rp.ss.1N.0001     | 1728/24          | 1       |                 |                |
|rp.ss.2N.0001     | 1728/48          | 2       |                 |                |
|rp.ss.18N.0001    | 1728/432         | 18      |                 |                |
|rp.ss.36N.0001    | 1728/864         | 36      |                 |                |

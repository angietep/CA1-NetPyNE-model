# CA1-NetPyNE-model

## Description
NetPyNE (www.netpyne.org) version of a model of CA1 microcircuits.

Original model and publication: https://modeldb.yale.edu/234233 

## Setup and execution

Requires NEURON with Python . 

1. Type `nrnivmodl mod`. This should create a directory called either i686 or x86_64, depending on your computer's architecture. 
2. To run type: `python init.py`

## Overview of file structure:

* /init.py: Main executable; calls functions from other modules. Sets what parameter file to use.

* /netParams.py: Network parameters

* /cfg.py: Simulation configuration


For further information please contact: salvadordura@gmail.com 


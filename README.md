# HMC FWI Visualization

> Interactive visualization supplemental to "Bayesian elastic Full-Waveform Inversion using Hamiltonian Monte Carlo".

Visualization of sampling results of probabilistic full-waveform inversion using Hamiltonian Monte Carlo. This program will visualize the correlation structure of the chequerboard models interactively within the acquistition geometry.

This program takes the raw / thinned samples of the Markov chain and computes the correlation matrix. Subsequently, it extracts one row of this matrix and maps it back into the model. In this way, it visualizes the correlation to one specific parameter throughout the medium.

In the correlation visualization, **one is able to click** on any parameter. The program then recomputes the correlation to that specific parameter, and plots it in the current view.

## Running the program

If all steps below are followed (i.e. all requirements are installed), the program can be started from the program root directory (the folder where you find this file) by running: 
``` bash
python3 gui.py
```
Or, if you directly want to run the correlation visualization of a specific Markov chain:
``` bash
python3 correlation_chain_[insert appropriate name].py
```

## Requirements / installation

This program requires Python 3, and has only been tested with Python 3.7. For the GUI, TKinter is required. This package is typically installed with every Python distribution. On Ubuntu-like systems, it is manually available as:
``` bash
sudo apt-get install python3-tk
```

### Installation using Pip
Additionally, it relies on the following packages available through pip:

* numpy
* matplotlib
* pytz
* pillow

To install all:

``` bash
pip3 install numpy matplotlib pytz pillow
```

### Installation using Anaconda/Miniconda
If you have a Conda distribution, you might find installing a separate environment more practical. For this, minimal and exact Anaconda environment specifications are provided in this folder.

**Recommended**
To install with minimal dependencies run:
``` bash
conda env create -f environment.minimal.yaml    
```
And activation is done by:
``` bash
conda activate hmcfwi-min
```

**Alternatively**
For the complete environment (as is used in the development):
``` bash
conda env create -f environment.exact.yaml
```
And activation is done by:
``` bash
conda activate hmcfwi-ex
```

### License

BSD 3-Clause License

Copyright (c) 2019, **Lars Gebraad et al.**
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
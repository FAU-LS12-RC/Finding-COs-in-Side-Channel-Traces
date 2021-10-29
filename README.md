# Finding Cryptographic Operations in Side-Channel Traces

This repository contains artifacts for the paper "Semi-Automatic Locating of Cryptographic Operations in Side-Channel Traces" published in TCHES 2022 Volume 1.
In this repository you can find traces, testcases and a GPU accelerated implementation of the algorithm detailed in the paper.

The goal of the provided tool is to segment a long side-channel trace into multiple traces that each cover the execution of a single Cryptographic Operation (CO).
Having obtained these trace segments one can perform classical statistical attacks such as Differential Power Analysis (DPA) or Correlation Power Analysis (CPA).

We provide one example that can be executed in a free, GPU enabled, Google Colab environment. Additionally, we provide several Jupyter Notebook based examples that demonstrate how the tool can be used.

We recommend to start by trying out the Google Colab notebook first, as it should be the most convenient to get working.


## In the cloud: Google Colab GPU instance

We provide a Google Colab notebook that implements a basic step-by-step example. The advantage of this notebook is that it can be executed from the comfort of your browser, without requiring special hardware or software setup. In fact, the provided Colab notebook is the same as [Simple-Notebook.ipynb](Simple-Notebook.ipynb), but requires no setup on your part. 

The Google Colab notebook can be accessed by browsing to the following URL:
https://colab.research.google.com/drive/132c4Jr2tN133tRINeAfmwAmFSMPA0aYV



## Bring your own GPU

Google Colab notebooks are convenient but also have some limitations. We recommend executing the remaining examples locally on your own machine for the best experience.


### Setup and requirements

The provided implementation relies on OpenCL and a GPU for acceleration. This means that your machine will require a reasonably powerful GPU, and you will have to install OpenCL and setup a suitable Python environment. In theory the provided implementations should work on any OpenCL capable GPU, we tested all of the examples on an NVIDIA RTX3070 and on a NVIDIA Titan Xp.

You will need to install an OpenCL device driver (often referred to as Installable Client Driver (ICD)). Instructions on how to install the OpenCL ICD for your specific hardware is beyond the scope of this document. However, the OpenCL ICD for NVIDIA GPUs is included in the device drivers (https://developer.nvidia.com/opencl). 

The provided notebooks require Python 3.7 and the following packages:
* scipy
* jupyter
* holoviews
* bokeh
* ipykernel
* tikzplotlib
* numba
* pyopencl
* ocl-icd-system 
    * Helps pyopencl to find your openCL capable device, more information here: https://documen.tician.de/pyopencl/misc.html
* scared
    * Used in [secure_boot_walk_through.ipynb](secure_boot_walk_through.ipynb) to perform CPA


We recommend installing these packages as part of a new Conda environment or Python virtual environment.
You can use the Python 3.7 build of [miniconda](https://docs.conda.io/en/latest/miniconda.html#linux-installers) or create a normal Python virtual environment. 

To create a suitable Conda environment:
* `conda create -n co-finder`
* `conda activate co-finder`
* `conda install -c conda-forge scipy jupyter holoviews bokeh ipykernel tikzplotlib numba pyopencl ocl-icd-system scared`
* `conda install -c eshard scared`

Or to create a Python 3.7 virtualenv:
* `Python3.7 -m venv ./co-finder`
* `source co-finder/bin/activate`
* `pip3 install scipy jupyter holoviews bokeh ipykernel tikzplotlib numba pyopencl ocl-icd-system scared`

Once this setup is complete you should be able to run the provided notebooks.
To do so you can run the following commands in a terminal:

* `git clone https://github.com/FAU-LS12-RC/Finding-COs-in-Side-Channel-Traces`
* Ensure that your Conda environment (or Python virtual environment) is still active!
    * Conda: `conda activate co-finder`
    * Python virtualenv: `source co-finder/bin/activate`
* `cd Finding-COs-in-Side-Channel-Traces`
* Start the Jupyter server: `jupyter notebook`

We recommend starting with the [setup_test.ipynb](setup_test.ipynb) to ensure that your installation is working correctly.
Afterwards you can try the other notebooks listed below.

### Jupyter Notebooks

The provided Jupyter Notebooks demonstrate how to use the API that we provide for semi-automatically finding COs in a side-channel trace. Notebook specific instructions and additional information are provided within each notebook.

Provided examples:
1. [setup_test.ipynb](setup_test.ipynb) 
    * Can be used to test if your environment is setup properly.
2. [Simple-Notebook.ipynb](Simple-Notebook.ipynb) 
    * This notebook has the same functionality as the one in Google-Colab. It provides a detailed overview of the algorithm.
3. [encapsulated_execution.ipynb](encapsulated_execution.ipynb) 
    * Shows how to use the provided API and allows to reproduce the results presented in the paper.
4. [secure_boot_walk_through.ipynb](secure_boot_walk_through.ipynb) 
    * A complete end-to-end example demonstrating an attack on a secure boot example.
    * In the notebook you first segment the raw trace using our tool and subsequently perform CPA to recover the key.


### Troubleshooting

* Try one or more of the following things if you encounter the error: `RuntimeError: clEnqueueReadBuffer failed: OUT_OF_RESOURCES` 
    * Increase the decimation factor (the samples per clock should still be an integer!)
    * Crop the trace such that your GPU and RAM can handle the computation and copying of the data.
    * Try to get access to a machine with more resources 
* If your having trouble with your pyopencl: https://documen.tician.de/pyopencl/misc.html
    * The error `pyopencl._cl.LogicError: clGetPlatformIDs failed: PLATFORM_NOT_FOUND_KHR` indicates that you may be missing an OpenCL ICD.
* If pyopencl keeps asking for the correct device use this command to set the standard device to 0: `export PYOPENCL_CTX=0` 









# Finding-COs-on-Side-Channel-Traces

This repository was created for the Paper "Semi-Automatic Locating of Cryptographic Operations in Side-Channel Traces" and includes the traces, testcases and code of the algorithm shown there.

## Step-By-Step Google-Colab:

We've provided a step by step walk-through with a simple example <a href="https://colab.research.google.com/drive/132c4Jr2tN133tRINeAfmwAmFSMPA0aYV?usp=sharing" target="_blank">here</a>.
This will only include the easiest example, as the GPU in the Google-Colab is not the strongest one.
Therefore, the other, more advanced traces can be tried out with your own Jupyter Notebook.


## Jupyter Notebooks:
The provided Notebooks show the usage of the API that we provide for semi-automatically finding COs on a side-channel trace.
Instructions on how to use the provided Notebooks are given within the files:
1. [setup_test.ipynb](setup_test.ipynb) can be used to test if your conda / python environment is capable of using pyopencl in the required way.
2. [simple-notebook.ipynb](simple-notebook.ipynb) is the same notebook as the one in Google-Colab and shows the algorithms of the API a bit closer and not capsulated.
3. [encapsulated_execution.ipynb](encapsulated_execution.ipynb) shows how to access the provided API to produce the results from the paper
4. [secure_boot_walk_through.ipynb](secure_boot_walk_through.ipynb) shows the finding of COs in a secure boot trace and the subsequent successful CPA on the segmented traces.

### Requirements:

To use the provided notebooks, you can use anaconda (https://docs.anaconda.com/anaconda/install/) or install the needed packages manually.
The new environment should be with python 3.7 and have the following packages installed:
- scipy
- jupyter
- holoviews
- bokeh
- ipykernel
- tikzplotlib
- numba
- pyopencl
- (ocl-icd-system) (helps pyopencl to find your openCL capable device, more information here: https://documen.tician.de/pyopencl/misc.html)

If you dont want to do this manually, here is the conda create comand:
```properties
conda create -n clean37 python=3.7 scipy jupyter holoviews bokeh ipykernel tikzplotlib numba pyopencl ocl-icd-system"
```  

After executing this and trying the setup_test.ipynb you should be good to go!


For the secure-boot example you might also need the following packages:
 - "scared" (https://pypi.org/project/scared/)


### Troubleshooting

- If you encounter the error: "RuntimeError: clEnqueueReadBuffer failed: OUT_OF_RESOURCES" then you probably need to try the following things
  - increase decimation factor (the samples per clock should still be an integer!)
  - cut the trace down so your GPU and RAM can handle the computation and copying of the data.
  - (get a better PC to test those testcases, they will work on anything greater than an RTX3070 :])
- If your having trouble with your pyopencl: https://documen.tician.de/pyopencl/misc.html
- If pyopencl keeps asking for the correct device use this command to set the standard device to 0: export PYOPENCL_CTX=0 
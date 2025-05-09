# Install with Mamba

It is also possible to install all the dependencies with Mamba in a new environment.

This installation option supports Linux and has been tested most on Ubuntu.

First install Miniconda or Anaconda, or Miniforge

- [Miniforge](https://github.com/conda-forge/miniforge) Recommended as it includes Mamba
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [Anaconda](https://www.anaconda.com)

If you chose Anaconda or Miniconda you will have to also install Mamba.
```bash
conda install-c conda-forge mamba
```

Once you have a version of Conda installed then proceed with cloning or [download](https://github.com/fusion-energy/neutronics-workshop/archive/refs/heads/main.zip) the repository.

```bash
sudo apt-get install git
git clone https://github.com/fusion-energy/neutronics-workshop.git
cd neutronics-workshop
```

Then create the environment with Mamba.

```bash
mamba env create --name neutronicsworkshop --file=environment.yml
```

Then activate the environment with  
```bash
mamba activate neutronicsworkshop
```

The download the nuclear data. This will create a ```nuclear_data``` folder in your home directory and download several Gb of data needed for the simulations.

```bash
bash postBuild
```

Clone or otherwise [download](https://github.com/fusion-energy/neutronics-workshop/archive/refs/heads/main.zip) the repository and cd into the repository directory.

```bash
git clone https://github.com/fusion-energy/neutronics-workshop.git
cd neutronics-workshop
```

Then you should be able to run the ```jupyter lab``` command and within Jupyter Lab you can load up the ipynb tasks found in the ```tasks``` folders.

```bash
jupyter lab
```

Then navigate to the task that you want to run in the tasks folder.

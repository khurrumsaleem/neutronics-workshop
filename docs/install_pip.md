# Install with pip

To install with pip first create a python 3.11 environment, then activate the environment and install all the required packages.

This installation option supports Linux and has been tested most on Ubuntu.

Currently just python 3.11 is supported, in the future other versions will be supported.

You will need Python installed which comes pre installed on most Linux distributions.

In addition to install with pip you will need pip installed.
```
sudo apt-get --yes install python3-pip
```

I would also recommend installing python3-venv so that the dependencies can be installed into a virtual environment.
```
sudo apt-get --yes install python3-venv
```

Once you have a version of Conda installed then proceed with cloning or [download](https://github.com/fusion-energy/neutronics-workshop/archive/refs/heads/main.zip) the repository.

```bash
sudo apt-get install git
git clone https://github.com/fusion-energy/neutronics-workshop.git
cd neutronics-workshop
```

You should then be able to make a virtual environment.
```bash
python3.11 -m venv .neutronicsworkshop
```

Activate the virtual environment
```bash
source .neutronicsworkshop/bin/activate
```

Then install the dependencies.
```bash
python3.11 -m pip install -r https://raw.githubusercontent.com/fusion-energy/neutronics-workshop/refs/heads/main/requirements.txt
```

The download the nuclear data. This will create a ```nuclear_data``` folder in your home directory and download several Gb of data needed for the simulations.

```bash
bash postBuild
```

Then you should be able to run the ```jupyter lab``` command and within Jupyter Lab you can load up the ipynb tasks found in the ```tasks``` folders.

```bash
jupyter lab
```

Then navigate to the task that you want to run in the tasks folder.

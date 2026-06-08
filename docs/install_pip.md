# Install with pip

## Install with pip on Linux

This installation option supports Linux.

You will need Python installed which comes pre installed on most Linux distributions.

````{admonition} WSL2 / minimal Linux users — extra system dependencies
:class: tip, dropdown

Most desktop Linux distributions already include the system libraries needed to run the simulations and graphics. However minimal environments such as WSL2 images may be missing some of them. If you hit missing library errors, install them with:

```bash
sudo apt-get install --yes git wget mpich libmpich12 libhdf5-310 libhdf5-mpich-310 hdf5-tools libnetcdf22 libtbb12 libglfw3 libglx0 libgl1 libglut3.12 libosmesa6 libgles2 libxft2 libxcursor1 libxinerama1 xvfb
```
````

In addition to install with pip you will need pip installed.
```
sudo apt-get --yes install python3-pip
```

I would also recommend installing python3-venv so that the dependencies can be installed into a virtual environment.
```
sudo apt-get --yes install python3-venv
```

Then proceed with cloning or [download](https://github.com/fusion-energy/neutronics-workshop/archive/refs/heads/main.zip) the repository.

```bash
sudo apt-get install git
git clone --depth 1 --branch main https://github.com/fusion-energy/neutronics-workshop.git
cd neutronics-workshop
```

You should then be able to make a virtual environment.
```bash
python3 -m venv .neutronicsworkshop
```

Activate the virtual environment
```bash
source .neutronicsworkshop/bin/activate
```

Then install the Python dependencies.

```bash
python3 -m pip install -r requirements.txt
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


## Install with pip on Mac OS

This installation option supports Mac OS.

You will need Python 3 installed. The easiest way to get an up to date version is with [Homebrew](https://brew.sh).
```
brew install python
```

Alternatively, running ```python3``` in a terminal on a fresh Mac will prompt you to install the Xcode Command Line Tools, which also provide Python 3.

Unlike Linux, pip and venv come bundled with Python 3 on Mac OS, so no additional packages are needed.

Then proceed with cloning or [download](https://github.com/fusion-energy/neutronics-workshop/archive/refs/heads/main.zip) the repository. Git is included with the Xcode Command Line Tools, or can be installed with ```brew install git```.

```bash
git clone --depth 1 --branch main https://github.com/fusion-energy/neutronics-workshop.git
cd neutronics-workshop
```

You should then be able to make a virtual environment.
```bash
python3 -m venv .neutronicsworkshop
```

Activate the virtual environment
```bash
source .neutronicsworkshop/bin/activate
```

Then install the Python dependencies.

```bash
python3 -m pip install -r requirements.txt
```

The download the nuclear data. This will create a ```nuclear_data``` folder in your home directory and download several Gb of data needed for the simulations.

```bash
zsh postBuild
```

Then you should be able to run the ```jupyter lab``` command and within Jupyter Lab you can load up the ipynb tasks found in the ```tasks``` folders.

```bash
jupyter lab
```

Then navigate to the task that you want to run in the tasks folder.

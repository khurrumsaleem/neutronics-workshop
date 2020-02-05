# Fusion Neutronics workshop with OpenMC
A selection of resources for learning OpenMC with particular focus on simulations relevant to fusion energy.

There are a few [slides](https://slides.com/openmc_workshop/neutronics_workshop) that introduce the workshop and show the expected outputs of each task.

The use of OpenMC for neutronics analysis requires several software packages and nuclear data. These have been installed inside a Docker container.
**It is recommended that this workshop be completed using the Docker container.**

The majority of the workshop can also be completed using Google Colab Notebooks which do not require Docker. The links to these notebooks are provided below. (Note - not all tasks can be completed in Colab as it lacks some required dependencies).

## Docker Container Installation

### Linux (Recommended)

1. Install Docker CE for [linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/), including the part where you enable docker use as a non-root user.

2. Pull the docker image from the store by typing the following command in a terminal window.

    ```docker pull openmcworkshop/openmc_nndc_workshop```

3. Now that you have the docker image you can enable graphics linking between your os and docker, and then run the docker container by typing the following commands in a terminal window.

    ```xhost local:root```

    ```docker run --net=host -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix  -v $PWD:/my_openmc_workshop -e DISPLAY=unix$DISPLAY --privileged openmcworkshop/openmc_nndc_workshop```

**Permission Denied Error**
- If a *permission denied* error is returned when running docker commands, add ```sudo``` to the front of the command. This runs the command with administrative priviledges (you may be required to enter your password).

### Mac

1. Install Docker Desktop for [mac](https://store.docker.com/editions/community/docker-ce-desktop-mac).

2. Ensure Docker Desktop is running and pull the docker image from the store by typing the following command in a terminal window.

    ```docker pull openmcworkshop/openmc_nndc_workshop```

2. Install [XQuartz Version: 2.7.8](https://www.xquartz.org/releases/XQuartz-2.7.8.html) which is a visualization system for mac allowing you to run GUI applications. Restart your computer once install has completed - this updates your DISPLAY environment variable to point to XQuartz.app rather than X11.app (the previous visualization system for mac).

3. Open XQuartz using the command ```open -a XQuartz``` in a terminal window. Go to Preferences -> Security and select *Allow connections from network clients*. Close the XQuartz application to implement the selection.

4. Add your local machine network IP address to *IP* variable using the command:

    ```IP=$(ipconfig getifaddr en0)```

5. Add IP address to xhost. XQuartz should launch when this command is run (unless XQuartz is already open).

    ```xhost + $IP```

6. Run the docker container using the command:

    ```docker run --net=host -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix  -v $PWD:/my_openmc_workshop -e DISPLAY=$IP:0 --privileged openmcworkshop/openmc_nndc_workshop```

### Windows

1. Install Docker Desktop for [windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows). During this install make sure to check the box that adds your user account to the docker-users account otherwise you will require admin writes to launch docker-desktop.

2. Next is to install an X server to allow a visual connection to docker. The options here are [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (recommended) or [Xming](https://sourceforge.net/projects/xming/). Install VcXsrv and be sure to check the "Disable access control" check box during installation,  [detailed instructions](https://dev.to/darksmile92/run-gui-app-in-linux-docker-container-on-windows-host-4kde) are avaiable.

3. Run VcXsrv which now should be found in the start menu

4. Open Windows PowerShell, this can be found by searching the start menu.

5. Within Windows PowerShell type ```ipconfig``` and find your IP address

6. Within Windows PowerShell type ```set-variable -name DISPLAY -value yourip:0.0``` and replace ```yourip``` with your IP address found in the previous step. The full command should look something like this ```set-variable -name DISPLAY -value 10.11.128.118:0.0```

7. Within Windows PowerShell type ```docker run --net=host -it --rm -v $PWD:/my_openmc_workshop -e DISPLAY=$DISPLAY --privileged openmcworkshop/openmc_nndc_workshop```


### Checking that everything works

Running the docker image with the ```docker run``` command should load up an Ubuntu 18.04 Docker container with OpenMC, DAGMC, Python3, Paraview, nuclear data and other libraries.

Running the docker image places you in the ```/openmc_workshop``` directory which contains all of the files required to complete the workshop.

You can quickly test the graphics options worked by typing ```paraview``` in the container environment. This should open the paraview program after a short wait.

If the graphics options still don't work there is another way of visulising the outputs of the simulations. All the images, html graphs and paraview vtk files produced during the workshop are copied across to the directory where you performed the docker run command from. This is ensured by the ```-v $PWD:/my_openmc_workshop``` part of the command.

The docker container also contains a folder called ```/my_openmc_workshop``` which is mapped to the local directory from which you ran the image. Placing files into this directory allows you to tranfer files from your docker container to your local machine.


**IMPORTANT:** Any changes you make to scripts in the docker container will be lost when you exit the container. Make sure you copy any files you want to keep into the ```my_openmc_workshop``` folder before exiting the container. **Note:** The output files created by the task scripts are automatically copied to this folder.

## Core workshop tasks

- [Task 1 - Cross section plotting - 25 minutes](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_1)
- [Task 2 - Building and visualizing the model geometry - 25 minutes](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_2)
- [Task 3 - Visualizing neutron tracks - 20 minutes](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_3)
- [Task 4 - Finding neutron interactions with mesh tallies - 15 minutes](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_4)
- [Task 5 - Finding the neutron and photon spectra - 15 minutes](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_5)
- [Task 6 - Finding the tritium production - 15 minutes](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_6)
- [Task 7 - Finding the neutron damage and stochastic volume calculation - 15 minutes](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_7)

## Optional workshop tasks

- [Task 8 - Survey breeder blanket designs for tritium production - 25 minutes](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_8)
- [Task 9 - Optimize a breeder blanket for tritium production - 25 minutes](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_9)
- [Task 10 - Using CAD geometry - 30 minutes](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_10)

&ensp;

## Acknowledgments
Fred Thomas for providing examples from previous years Serpent workshop,
Enrique Miralles Dolz for providing the CSG tokamak model, Andrew Davis for his work on the fusion neutron source, Chris Bowman for his Gaussian process software, John Billingsley for the CoLab tasks and the OpenMC team for their software.

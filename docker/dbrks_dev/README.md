This is for local development only, higher environments will run within the databricks runtime.

##miniconda
Environment name will be taken from the environment.yml file dynamically
Miniforge Python 3.x in /opt/conda with both conda and mamba
No preinstalled scientific computing packages this need to be added to the environment yml.
tini as the container entrypoint alongside the conda env

##Jupyter
Install Jupyter Lab only (within conda environment), accessed via http://127.0.0.1:8888/, password = "Databricks_dev"
All code in the repo will be available to the server

##Scripts
jupyter-lab script to connect via databricks connect.

add setting for detecting databricks notebooks as notebooks in jupyter

##Databricks connect
jdk8 installed
installed globally
Parameters set in .databricks-connect (created via local-setup.sh using template)
Version set in .env in root (Must match https://docs.microsoft.com/en-us/azure/databricks/dev-tools/databricks-connect)

##Repo file sharing
by default the location of the repo will be shared and mounted with the container.

If your local repo is outside of the Users directory (cd ~), then you need to share the drive or location of the Dockerfile and volume you are using. If you get runtime errors indicating an application file is not found, a volume mount is denied, or a service cannot start, try enabling file or drive sharing. Volume mounting requires shared drives for projects that live outside of C:\Users (Windows) or /Users (Mac), and is required for any project on Docker Desktop for Windows that uses Linux containers. For more information, see File sharing on Docker for Mac, and the general examples on how to Manage data in containers.

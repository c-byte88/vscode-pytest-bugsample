#Jupyter/pyspark development via databricks connect
FROM openjdk:8-jdk-slim

LABEL maintainer="Cognizant - Microsoft Business Group"

ARG SOURCEPATH=/home/dev
ARG DBCONNECT_VRS

#Jupyter labs port
EXPOSE 8888

# Configure apt
ENV DEBIAN_FRONTEND=noninteractive

# Mini Conda Start
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

#TODO add user and group

RUN apt-get update --fix-missing \
    #conda dependencies
    && apt-get install -y --no-install-recommends wget bzip2 ca-certificates curl git \
    # VSCode DevContainers
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    # Verify git, needed tools installed
    && apt-get -y install git iproute2 procps curl lsb-release \
    # Local build tool
    && apt-get -y install make

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate dbrks_dev" >> ~/.bashrc 

ENV PATH /opt/conda/bin:$PATH
ENV PATH /opt/conda/envs/dbrks_dev/bin:$PATH

COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

#set jupyter lab to use dbconnect
RUN conda install -c conda-forge jupyterlab \
    && pip install -U databricks-connect=="${DBCONNECT_VRS}" \
    && python -m ipykernel install --user --name dbrks_dev --display-name "Databricks Connect (dbrks_dev)" 

#db connect config from repo
COPY .databricks-connect jupyter-lab.sh /root/
#Jupyter setup and start
COPY jupyter_server_config.py /etc/jupyter/
CMD [ "/root//jupyter-lab.sh" ]

#Tini
ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini

#permissions fix workaround until user added
RUN chmod +x /usr/bin/tini \
    && chmod +x /root/jupyter-lab.sh

# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && conda clean --all -f -y \
    #based on https://github.com/jupyter/docker-stacks/issues/861#issuecomment-489737844
    && find /opt/conda/ -type f,l -name '*.a' -delete \
    && find /opt/conda/ -type f,l -name '*.pyc' -delete \
    #We are not debugging java so this is not needed...
    && find /opt/conda/ -type f,l -name '*.js.map' -delete \
    && rm -rf /opt/conda/pkgs 

ENV DEBIAN_FRONTEND=dialog

# Allow for a consistant java home location for settings
RUN if [ ! -d "/docker-java-home" ]; then ln -s "${JAVA_HOME}" /docker-java-home; fi

#set python source path in container (mount)
ENV PYTHONPATH=$PYTHONPATH:${SOURCEPATH}

#set entry poiint for tini and conda env
ENTRYPOINT ["/usr/bin/tini", "--", "conda", "run", "--no-capture-output", "-n", "dbrks_dev"]
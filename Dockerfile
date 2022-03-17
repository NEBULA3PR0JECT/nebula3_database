FROM ubuntu:latest 
# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8
LABEL com.nvidia.volumes.needed="nvidia_driver"
COPY environment.yaml /environment.yaml
ENV PYTHON_VERSION=3.9
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64
ENV PATH=$PATH:/opt/conda/bin/
ENV USER nebula

RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    ca-certificates \
    build-essential \
    gcc \
    git \
    zip \
    unzip \
    openssh-client && \
    apt-get install -y --no-install-recommends curl wget && \
    apt-get install -y --no-install-recommends python-dev python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    curl -o ~/miniconda.sh -O  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda install conda-build && \
    conda env create -f environment.yaml && \
    conda clean --all -y 
# Create Environment
WORKDIR /notebooks
# Activate Source
#CMD source activate nebula && source ~/.bashrc
ENV PATH /opt/conda/bin:$PATH
ENV PATH /opt/conda/envs/nebula/bin:$PATH
COPY run.sh /run.sh

#CMD ["/run.sh"]

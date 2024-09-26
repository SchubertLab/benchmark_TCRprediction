FROM ubuntu:22.04


ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN apt-get update
RUN apt-get update && apt-get upgrade -y && apt-get install gcc --yes
RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install vim -y
RUN apt-get -y update && apt-get install unzip

RUN apt-get update && \
    apt-get install -y wget bzip2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Anaconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/miniconda && \
    rm /tmp/miniconda.sh
ENV PATH=/opt/miniconda/bin:$PATH
RUN echo "source /opt/miniconda/etc/profile.d/conda.sh && conda activate base" >> /root/.bashrc


# ePytope-TCR
WORKDIR /
RUN git clone https://github.com/SchubertLab/epytope.git
SHELL ["/bin/bash", "-c"]

# Benchmark tool
COPY ./benchmark_TCRprediction /benchmark_TCRprediction


# External tools
WORKDIR /epytope/external
RUN apt-get update && apt-get install -y dos2unix

# Download tools
RUN chmod 777 /benchmark_TCRprediction/docker/scripts/download.sh
RUN dos2unix /benchmark_TCRprediction/docker/scripts/download.sh
RUN /benchmark_TCRprediction/docker/scripts/download.sh

# Create environmens
RUN chmod 777 /benchmark_TCRprediction/docker/scripts/create_envs.sh
RUN dos2unix /benchmark_TCRprediction/docker/scripts/create_envs.sh
RUN /benchmark_TCRprediction/docker/scripts/create_envs.sh

# Install tools
RUN chmod 777 /benchmark_TCRprediction/docker/scripts/install.sh
RUN dos2unix /benchmark_TCRprediction/docker/scripts/install.sh
RUN /benchmark_TCRprediction/docker/scripts/install.sh


EXPOSE 8001
ENTRYPOINT ["tail", "-f", "/dev/null"]

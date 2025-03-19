#!/usr/bin/env bash
# Script to install environments

conda env create -f /benchmark_TCRprediction/docker/envs/epytope_base.yml
conda env create -f /external/ImRex/environment.yml
conda env create -f /benchmark_TCRprediction/docker/envs/epytope_torch21.yml
conda env create -f /benchmark_TCRprediction/docker/envs/epytope_torch11.yml
conda env create -f /benchmark_TCRprediction/docker/envs/epytope_numpy195.yml
conda env create -f /benchmark_TCRprediction/docker/envs/epytope_torch111.yml
conda env create -f /benchmark_TCRprediction/docker/envs/epytope_tcrgp.yml
conda create --name epytope_stapler python=3.9

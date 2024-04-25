FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3

ENV TERM=xterm
ENV DEBIAN_FRONTEND=noninteractive


#
# setup environment
#
ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_HOME="/usr/local/cuda"
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
		gnupg2 \
        apt-utils \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean


#
# configure nvidia apt repo
#
# COPY packages/nvidia-l4t-apt-source.list /tmp/apt/nvidia-l4t-apt-source.list
# COPY packages/nvidia-l4t-apt-source.clean.list /tmp/apt/nvidia-l4t-apt-source.clean.list
    
#
# install CUDA Toolkit
#    
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
		  cuda-toolkit-* \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python 3.9
# RUN apt-get update && \
#     apt-get install -y \
#     apt-utils\
#      \
#     software-properties-common &&\
#     add-apt-repository ppa:deadsnakes/ppa && \
#     apt-get install -y \
#     python3.9-dev \
#     python3.9-distutils

RUN ln -sf /usr/bin/python3.8 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.8 /usr/bin/python

# Install pip (needs to be >=20.3 for open3d)
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py pip==20.3

ENV TZ=US/Pacific
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# # Install essential packages
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg2 \
    git \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    libgtk2.0-dev \
    bzip2 \
    ca-certificates \
    vim \
    tmux \
    g++ \
    gcc \
    cmake \
    checkinstall \
    gfortran \
    libjpeg8-dev \
    libtiff5-dev \
    pkg-config \
    yasm \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libdc1394-22-dev \
    libxine2-dev \
    libv4l-dev \
    qt5-default \
    libtbb-dev \
    libatlas-base-dev \
    libfaac-dev \
    libmp3lame-dev \
    libtheora-dev \
    libvorbis-dev \
    libxvidcore-dev \
    libopencore-amrnb-dev \
    libopencore-amrwb-dev \
    x264 \
    v4l-utils \
    libprotobuf-dev \
    protobuf-compiler \
    libgoogle-glog-dev \
    libgflags-dev \
    libgphoto2-dev \
    libhdf5-dev \
    doxygen \
    libflann-dev \
    libboost-all-dev \
    proj-data \
    libproj-dev \
    libyaml-cpp-dev \
    cmake-curses-gui \
    libzmq3-dev \
    freeglut3-dev \
    cmake \
    && apt-get clean

RUN cd / && git clone https://github.com/pybind/pybind11 &&\
    cd pybind11 && git checkout v2.10.0 &&\
    mkdir build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release -DPYBIND11_INSTALL=ON -DPYBIND11_TEST=OFF &&\
    make -j6 && make install

ENV PYTHONPATH=/usr/local/lib/python3.x/dist-packages:$PYTHONPATH

RUN cd / && wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz &&\
    tar xvzf ./eigen-3.4.0.tar.gz &&\
    cd eigen-3.4.0 &&\
    mkdir build &&\
    cd build &&\
    cmake .. &&\
    make install

# ENV TORCH_INSTALL=https://developer.download.nvidia.cn/compute/redist/jp/v511/pytorch/torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl


# RUN pip install --no-cache $TORCH_INSTALL

RUN curl -LO https://github.com/NVIDIA/cub/archive/1.10.0.tar.gz &&\
    tar xzf 1.10.0.tar.gz &&\
    export CUB_HOME=$PWD/cub-1.10.0

RUN pip install "git+https://github.com/facebookresearch/pytorch3d.git@stable"

# We need to manually remove pyyaml because another package installs it via distutils
RUN apt-get remove -y python3-yaml 

RUN pip install scipy joblib scikit-learn ruamel.yaml trimesh opencv-python imageio open3d transformations warp-lang einops kornia pyrender kaolin

# We're building on CUDA 11.3 as in the orignial FoundationPose work. This is a minor version mismatch with the CUDA used for torch (11.8)
# RUN cd / && git clone --recursive https://github.com/NVIDIAGameWorks/kaolin
# RUN cd /kaolin &&\
#     FORCE_CUDA=1 python setup.py develop

RUN cd / && git clone https://github.com/NVlabs/nvdiffrast &&\
    cd /nvdiffrast && pip install .

ENV OPENCV_IO_ENABLE_OPENEXR=1

RUN apt-get install -y python3-h5py

RUN pip install scikit-image meshcat webdataset omegaconf pypng roma seaborn opencv-contrib-python openpyxl wandb imgaug Ninja xlsxwriter timm albumentations xatlas rtree nodejs jupyterlab objaverse g4f ultralytics==8.0.120 pycocotools videoio numba

ENV SHELL=/bin/bash
RUN ln -sf /bin/bash /bin/sh

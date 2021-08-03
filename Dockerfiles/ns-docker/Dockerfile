FROM ubuntu:latest
LABEL Description="Docker image for NS-3 version 3.33"

### avoid freezing in tzdata setup
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

RUN apt-get update && apt-get install -y \
    neovim \
    git \
### Minimal requirements
    build-essential \
    python3 \
### Minimal requirements for Python API
    pkg-config \
    python3-dev \
    sqlite3 \
### Minimal requirements for Python development
    python3-setuptools \
### Support for generating Python bindings
    automake \
    cmake \
    libc6-dev \
    libc6-dev-i386 \
    libclang-11-dev \
    llvm-11-dev \
    python3-pip \
### Support for ns-3-pyviz visualizer
    ipython3 \
    gir1.2-gtk-3.0 \
    gir1.2-goocanvas-2.0 \
    python3-gi \
    python3-gi-cairo \
    python3-pygraphviz \
### Support for utils/check-style.py
    uncrustify \
### Support for Bake build tool
    autoconf \
    bzr \
    cvs \
    unrar \
### Statistics Framework
    libsqlite3-dev \
    sqlite \
### GNU Scientific Library support (Wi-Fi 802.11b error models)
    gsl-bin \
    libgsl-dev \
    libgslcblas0 \
### Netanim Support
    qt5-default \
### Xml-based configuration (ConfigStore)
    libxml2 \
    libxml2-dev \
### GTK-based configuration system
    libgtk-3-dev \
### Analyze pcaps
    tcpdump \
### Support to virtual machines
   lxc \
   uml-utilities \
   vtun \
### Debugging
    gdb \
    valgrind \
### Support to MPI
    libopenmpi-dev \
    openmpi-bin \
    openmpi-common \
    openmpi-doc \
### Documentation
    doxygen \
    dvipng \
    graphviz \
    imagemagick \
    latexmk \
    texlive  \
    texlive-extra-utils \
    texlive-font-utils \
    texlive-latex-extra \
### ns-3 manual and tutorial
    dia \
    python3-sphinx \
    && rm -rf /var/lib/apt/lists/* \
# Support for generating Python bindings
    && pip install cxxfilt pybindgen pygccxml castxml

WORKDIR /usr

RUN git clone https://gitlab.com/nsnam/ns-3-dev.git ns
WORKDIR /usr/ns

RUN ./waf configure --enable-tests --enable-examples \
    && ./waf build

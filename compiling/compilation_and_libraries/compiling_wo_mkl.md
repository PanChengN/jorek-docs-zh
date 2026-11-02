---
title: "不使用 Intel MKL 编译"
nav_order: 7
parent: "编译与依赖库"
grand_parent: "编译与运行"
layout: default
render_with_liquid: false
---

# 在无法访问 Intel-MKL 依赖库的情况下编译 JOREK 及其依赖

当 ScaLAPACK 之类的依赖库不由支持团队提供时，用 GNU 编译器编译 JOREK 并不完全直接。下面给出一种可行做法。

此处假设：

- 你有较新的 GNU 编译器，例如 7.5
- 你有 CMake
- 你可能需要编译较旧版本的 SCOTCH 与 PASTIX，最新版 OpenMPI（4.0）无法用于这些版本
- 你在下列目录下工作：

```text
/home/user/lib/
```

## HDF5

首先需要编译 HDF5 依赖库。

需从下列地址下载源码：

- <https://www.hdfgroup.org/downloads/hdf5/source-code/>

不要尝试使用 HDF Git 仓库中的代码；它对 Fortran 依赖库不能正常工作。

解包 HDF5 tar 包后，执行以下操作：

```bash
cd ./hdf5/
mkdir install
./configure --prefix=/home/user/lib/hdf5/install/ --enable-fortran
make -j8
make -j8 install
```

## OpenMPI

接下来从下列地址下载 OpenMPI 源码：

- <https://www.open-mpi.org/software/ompi/v3.0/>

解包 tar 包，然后运行：

```bash
cd ./openmpi
mkdir install
./configure --prefix=/home/user/lib/openmpi/install/
make -j8
make -j8 install
export LD_LIBRARY_PATH=/home/user/lib/openmpi/install/lib:$LD_LIBRARY_PATH
export PATH=/home/user/lib/openmpi/install/bin:$PATH
```

## OpenBLAS

接下来构建 OpenBLAS 依赖库：

```bash
git clone https://github.com/xianyi/OpenBLAS.git
export CC=mpicc
export FC=mpifort
export CXX=mpicxx
cd OpenBLAS
mkdir build install
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=/home/user/lib/OpenBLAS/install
make -j8
make -j8 install
```

## LAPACK

接下来构建 LAPACK 依赖库：

```bash
git clone https://github.com/Reference-LAPACK/lapack.git
mkdir build install
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=/home/user/lib/lapack/install
make -j8
make -j8 install
```

## ScaLAPACK {#scalapack}
接下来构建 ScaLAPACK 依赖库：

```bash
git clone https://github.com/Reference-ScaLAPACK/scalapack.git
mkdir build install
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=/home/user/lib/scalapack/install
make -j8
make -j8 install
```

## PASTIX-5

只要把 `PATH` 与 `LD_LIBRARY_PATH` 设置为包含 OpenMPI 的编译器，SCOTCH 的编译就很直接。

对 PASTIX 求解器，需在 `config.in` 中包含以下内容：

```makefile
BLAS_HOME=/home/user/lib/scalapack/install/lib
BLASLIB = -L$(BLAS_HOME) -lscalapack
```

注意：只要在 JOREK 中正确完成链接，这一项可能根本不需要。

## JOREK

对 JOREK，需在 `Makefile.inc` 中用以下行代替通常的 MKL 设置：

```makefile
SCA_HOME  = /home/user/lib/scalapack/install
BLA_HOME  = /home/user/lib/OpenBLAS/install
LAP_HOME  = /home/user/lib/lapack_GNU/install
LIBLAPACK = -L$(SCA_HOME)/lib -lscalapack -L$(LAP_HOME)/lib64 -llapack -L$(BLA_HOME)/lib64 -lopenblas
SCALAP    = -L$(SCA_HOME)/lib -lscalapack -L$(LAP_HOME)/lib64 -llapack -L$(BLA_HOME)/lib64 -lopenblas
```

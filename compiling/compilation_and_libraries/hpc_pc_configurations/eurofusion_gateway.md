---
title: "EUROfusion 网关"
nav_order: 14
parent: "HPC 与 PC 配置"
grand_parent: "编译与依赖库"
layout: default
render_with_liquid: false
---

## 网关独立集群的硬件资源

9 个虚拟节点，包含以下 Gateway 用户服务器：

- ITM MySQL 数据库 `itmcatalog`：`itmmysql1.eufus.eu`
- `gforge.eufus.eu`
- `portal.eufus.eu`
- `www.eufus.eu`
- `ticket.eufus.eu`
- 1 个带 FC HBA 的 `x3550 M5` 节点，作为 `eufus.eu` 单元的 AFS 文件服务器
- 1 个带 FC HBA 的 `x3550 M5` 节点，作为登录节点并兼作 AFS 服务器备用
- 4 个 `thinkSystem SD530` 节点，作为配备 NVIDIA K80 高级图形适配器的登录节点
- 16 个 `thinkSystem SD530` 节点，作为具有 192 GB 内存的计算节点
- 8 个 `thinkSystem SD530` 节点，作为具有 384 GB 内存的计算节点
- 10 TB 的 AFS 文件服务器存储区
- 15 PB 的 AFS/GPFS 备份存储区
- 600 TB 的 MARCONI GSS 高性能存储区

`thinkSystem SD530` 节点基于 2 颗主频 2.10 GHz 的 24 核 Intel Xeon 8160（SkyLake）处理器。

## 访问系统

- 以下链接说明了**如何获取** Gateway 机器的访问权限：<https://wiki.eufus.eu/doku.php>
- 另见一次 mini CodeCamp 的资料：
  - [此处](https://box.pionier.net.pl/d/6a7d79934c2b4a4db7e2/)（密码：`miniC0d3C4mp5`）
  - [此处](https://docs.psnc.pl/pages/viewpage.action?pageId=70884347)

随后即可用 SSH 客户端访问该机器：

```bash
ssh -CXY <username>@login.eufus.eu
```

## 编译 JOREK

需要加载以下模块，例如将它们写入 `~/.bashrc_profile`：

```bash
module purge
module load cineca
module load intel/pe-xe-2017--binary
module load intelmpi/2017--binary
module load mkl/2017--binary
module load fftw/3.3.4--intelmpi--2017--binary
module load szip/2.1--gnu--6.1.0
module load zlib/1.2.8--gnu--6.1.0
module load hdf5/1.8.17--intelmpi--2017--binary
```

用于编译 JOREK 的 `Makefile.inc` 如下：

```bash
# --- Select physics model
MODEL             = model303

# --- Compiler and options
FC                = mpiifort
CC                = mpiicc
CXX               = mpiicpc

FFLAGS += -O3
FFLAGS += -vecabi=compat -mcmodel=medium

# --- Various switches
USE_PASTIX              = 1
USE_PASTIX_MURGE        = 0
USE_COMPLEX_PRECOND     = 0
USE_STRUMPACK           = 0
USE_HDF5                = 1
USE_FFTW                = 1
USE_MUMPS               = 0
USE_DIRECT_CONSTRUCTION = 0
USE_BLOCK               = 1

LIBDIR = /afs/eufus.eu/user/g/g2iholod/public
LIBS += -liomp5 -pthread -ldl -lm

ifeq (1, $(USE_MUMPS))
# --- MUMPS
 MKLLIB= -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 \
         -lmkl_intel_thread -lmkl_core -lmkl_blacs_intelmpi_lp64
 MKLINC = -I${MKL_HOME}/include

 MUMPSDIR = $(LIBDIR)/MUMPS_5.2.1
 LIB_MUMPS = -L$(MUMPSDIR)/lib -ldmumps -ldmumps -lmumps_common -lpord
 INC_MUMPS = $(MUMPSDIR)/include

 LIB_MUMPS += $(MKLLIB)
 INC_MUMPS += $(MKLINC)
endif

##################

ifeq (1, $(USE_PASTIX))
 MKLLIB = -L${MKL_HOME}/lib/intel64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core
 MKLINC = -I${MKL_HOME}/include

 INC_PASTIX += $(MKLINC)
 LIB_PASTIX += $(MKLLIB)

 PASTIX_DIR=$(LIBDIR)/pastix_5.2.3/install
 SCOTCH_DIR=$(LIBDIR)/scotch_5.1.12

 LIB_PASTIX += $(PASTIX_DIR)/libpastix.a $(SCOTCH_DIR)/lib/libscotch.a $(SCOTCH_DIR)/lib/libscotcherr.a
 INC_PASTIX += -I$(PASTIX_DIR)

endif

##################

ifeq (1, $(USE_STRUMPACK))
 MKLLIB= -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 \
         -lmkl_intel_thread -lmkl_core -lmkl_blacs_intelmpi_lp64
 MKLINC = -I${MKL_HOME}/include

 PARMETIS_HOME=$(LIBDIR)/parmetis-4.0.3/build
 STRUMPACK_HOME=$(LIBDIR)/STRUMPACK_MKL/install

 STRUMPACKINC = -I$(STRUMPACK_HOME)/include
 STRUMPACKLIB = $(STRUMPACK_HOME)/lib/libstrumpack.a

 STRUMPACKINC += -I$(PARMETIS_HOME)/include
 STRUMPACKLIB += $(PARMETIS_HOME)/libparmetis/libparmetis.a

 STRUMPACKINC += -I$(PARMETIS_HOME)/metis/include
 STRUMPACKLIB += $(PARMETIS_HOME)/libmetis/libmetis.a

 STRUMPACKINC += $(MKLINC)
 STRUMPACKLIB += $(MKLLIB)

 DEFINES += -DNEWSPK
endif

##################

LIBFFTW           = $(FFTW_LIB)/libfftw3f.a
INC_FFTW          = -I$(FFTW_INC)

HDF5INCLUDE = $(HDF5_HOME)/include
HDF5LIB     =-L$(HDF5_HOME)/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -L$(SZIP_LIB) -lsz -lz
```

## 提交作业

批处理作业提交脚本示例：

```bash
#!/bin/bash

#SBATCH --job-name=jorek
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=24
#SBATCH --time=00:10:00
#SBATCH --partition=gw

export OMP_NUM_THREADS=24

srun ./jorek_model303 < ./inxflow > logfile.out
```

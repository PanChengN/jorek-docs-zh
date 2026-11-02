---
title: "Pitagora（CPU）"
nav_order: 6
parent: "HPC 与 PC 配置"
grand_parent: "编译与依赖库"
layout: default
render_with_liquid: false
---

# 在 CINECA 托管的 Pitagora CPU 分区上运行 JOREK

## 获取访问权限

1.  通过 <https://userdb.hpc.cineca.it/> 创建账号——选择 Create New User
2.  然后填写 HPC 相关信息，并上传身份证件/护照的扫描件
3.  联系相应的 PI 将你加入项目

## README

- （针对 Leonardo）CINECA 于 2025 年 2 月 18 日举办的网络研讨会幻灯片
- CINECA 帮助台电子邮箱：superc@cineca.it
- 与 EUROFUSION TSVV-F 项目相关的本项目名称为：**FUPA1_REDISMHD**
- 文档：
  <https://docs.hpc.cineca.it/hpc/pitagora.html#pitagora-card>
- Cineca 提供的幻灯片（访问方式、模块等）：
  <https://learn.cineca.it/course/view.php?id=2121>

## 登录

    ssh -Y <user>@login.pitagora.cineca.it

该命令与某个可用的登录节点建立连接。也可以显式指定登录节点：

    login01-ext.pitagora.cineca.it
    login02-ext.pitagora.cineca.it
    login03-ext.pitagora.cineca.it
    login04-ext.pitagora.cineca.it
    login05-ext.pitagora.cineca.it
    login06-ext.pitagora.cineca.it

编号为奇数的登录节点（01、03、05）与计算节点的 CPU 分区类似：2 × AMD EPYC 9745
(<https://www.amd.com/en/products/processors/server/epyc/9005-series/amd-epyc-9745.html>)，
共 128 核，768 GiB DDR5 内存。

编号为偶数的登录节点（02、04、06）与配备 GPU 的计算节点一致：2 × Intel Xeon Gold 6548Y+
(<https://www.intel.com/content/www/us/en/products/sku/237564/intel-xeon-gold-6548y-processor-60m-cache-2-50-ghz/specifications.html>)，
共 32 核，512 GiB DDR5 内存，1 × NVIDIA H100 NVL GPU
(<https://www.nvidia.com/en-us/data-center/h100/>)。

若希望代码在特定的计算节点分区上执行，请在相应的登录节点上编译。

## 可用软件

与通常一样，`module avail/load/list/show` 可用于访问可用软件。

部分未预装的软件（gnuplot、paraview、visit）位于 /pitagora_work/FUPA1_MHD/JOREK_LIBRARIES/。

如需使用 gnuplot，请设置：

    export PATH=/pitagora_work/FUPA1_MHD/JOREK_LIBRARIES/gnuplot/bin:$PATH

visit 与 paraview（从 Viper 复制而来）在 Intel CPU 节点（login02/04/06）上可正常工作，但在 AMD CPU 节点（login01/03/05）上无法启动。

可通过以下方式启用 visit：

    export PATH=/pitagora_work/FUPA1_MHD/JOREK_LIBRARIES/mpcdf/soft/RHEL_9/packages/x86_64/visit/3.4.2/bin:$PATH

paraview 可通过两步启用：

    export PATH=/pitagora_work/FUPA1_MHD/JOREK_LIBRARIES/mpcdf/soft/RHEL_9/packages/x86_64/paraview/5.11.2/bin:$PATH
    alias paraview='paraview --mesa' # to disable hardware rendering, as H100 is only for computing

## 使用 INTEL oneAPI 编译 JOREK

下面给出 `.bashrc` 与 Makefile.inc 配置的一些示例。

- 在 `.bashrc` 文件中添加以下行

<!-- -->

    module purge
    module load git
    module load intel-oneapi-mpi/
    module load intel-oneapi-compilers
    module load intel-oneapi-mkl/2024.0.0--intel-oneapi-mpi--2021.12.1
    module load hdf5/1.14.3--intel-oneapi-mpi--2021.12.1--oneapi--2024.1.0

- **Makefile.inc** 示例（注意 PaStiX 与 STRUMPACK 不应同时选用）。
- 注意 AMD 与 Intel 登录节点上各有一套已编译的依赖库。
- PaStiX 使用 intel-oneapi-compilers-classic（icc 与 ifort）重新编译，Strumpack 使用 intel-oneapi-compilers（icx 与 ifx）重新编译，因此推荐使用 STRUMPACK。
- MUMPS（use_MUMPS）与 64 位（USE_INTSIZE64）依赖库尚未重新编译。
- 截至目前（2025-06-02），这些依赖库仅测试了完整 MHD 模型（不含粒子）。

``` Make
MODEL             = model711
FC                = mpiifx
CC                = mpiicx
CXX               = mpiicpx
 
FFLAGS += -mcmodel=medium -O2
FFLAGS += -g -traceback -check bounds  # error tracing

FFLAGS += -march=skylake-avx512 -axCORE-AVX512 # for AMD
# FFLAGS += -xHost                             # for Intel
# FFLAGS += -march=sapphirerapids
# FFLAGS += -double-size 64 -integer-size 32 #-DFUNNELED
# FFLAGS += -fpp -mcmodel=medium -axCORE-AVX512 -align array64byte -qopt-zmm-usage=high

EXTRA_FLAGS += -lstdc++
COMPILER_FAMILY   = intel
# Never use STRUMPACK and PASTIC at the same time 
USE_PASTIX        = 0
USE_PASTIX_MURGE  = 0
USE_PASTIX6       = 0
USE_STRUMPACK     = 1
USE_MUMPS         = 0
USE_BLOCK         = 1
USE_HDF5          = 1
USE_FFTW          = 1
USE_MKL           = 0
USE_DIRECT_CONSTRUCTION=0
USE_BICGSTAB      = 0
USE_INTSIZE64     = 0
DEBUG             = 0
LIBS += -liomp5 -pthread -ldl -lm
 
# TODO: MUMPS for USE_MUMPS needs to be compiled
# TODO: 64bits libraries for USE_INTSIZE64 need to be compiled
# LIB64DIR =

LIBDIR = /pitagora_work/FUPA1_MHD/JOREK_LIBRARIES/libraries_recompile_amd
# LIBDIR = /pitagora_work/FUPA1_MHD/JOREK_LIBRARIES/libraries_recompile_intel
 
ifeq (1, $(USE_PASTIX))
 
 MKLLIB += -L${MKLROOT}/lib/intel64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core
 MKLINC = -I${MKLROOT}/include
 PASTIX_DIR = $(LIBDIR)/pastix_5.2.3/install
 SCOTCH_DIR = $(LIBDIR)/scotch_5.1.12
 ifeq (1, $(USE_INTSIZE64))
   PASTIX_DIR = $(LIBDIR)/pastix_5.2.3_i64/install
   SCOTCH_DIR = $(LIBDIR)/scotch_5.1.12_i64
 endif
 
 LIB_PASTIX = -L$(PASTIX_DIR) -lpastix -L$(SCOTCH_DIR)/lib -lscotch -lscotcherr
 INC_PASTIX = -I$(PASTIX_DIR)/include
 
 INC_PASTIX += $(MKLINC)
 LIB_PASTIX += $(MKLLIB)
 
endif
 
ifeq (1, $(USE_MUMPS))
# --- MUMPS
 MKLLIB += -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 \
         -lmkl_intel_thread -lmkl_core -lmkl_blacs_intelmpi_lp64
 MKLINC = -I${MKLROOT}/include
 MUMPS_DIR = $(LIBDIR)/MUMPS_5.4.1
 LIB_MUMPS = -L$(MUMPS_DIR)/lib -ldmumps -lmumps_common -lpord
 INC_MUMPS = $(MUMPS_DIR)/include
 
 LIB_MUMPS += $(MKLLIB)
 INC_MUMPS_EXTRA += $(MKLINC)
 
endif
 
ifeq (1, $(USE_STRUMPACK))
 MKLLIB= -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 \
         -lmkl_intel_thread -lmkl_core -lmkl_blacs_intelmpi_lp64
 MKLINC = -I${MKLROOT}/include
 GKLIB_HOME = $(LIBDIR)/GKlib/install
 METIS_HOME = $(LIBDIR)/METIS/install
 PARMETIS_HOME = $(LIBDIR)/ParMETIS/install
 STRUMPACK_HOME=$(LIBDIR)/STRUMPACK/install

 ifeq (1, $(USE_INTSIZE64))
   METIS_HOME = $(LIB64DIR)/METIS_64/install
   PARMETIS_HOME = $(LIB64DIR)/ParMETIS_64/install
   STRUMPACK_HOME=$(LIB64DIR)/STRUMPACK_64/install
 endif
 
 STRUMPACKINC = -I$(STRUMPACK_HOME)/include
 STRUMPACKLIB = -L$(STRUMPACK_HOME)/lib64 -lstrumpack
 
 STRUMPACKINC += -I$(METIS_HOME)/include -I$(GKLIB_HOME)/include -I$(PARMETIS_HOME)/include
 STRUMPACKLIB += -L$(METIS_HOME)/lib -lmetis -L$(GKLIB_HOME)/lib -lGKlib -L$(PARMETIS_HOME)/lib -lparmetis
 
 STRUMPACKINC += $(MKLINC)
 STRUMPACKLIB += $(MKLLIB)
 
 DEFINES += -DNEWSPK
endif
 
# --- FFTW Library
INC_FFTW          = -I$(MKLROOT)/include/fftw
 
# --- HDF5 Library
HDF5INCLUDE = $(HDF5_HOME)/include
HDF5LIB     = -L$(HDF5_HOME)/lib -lhdf5_hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -lz

```

## 使用 GNU OpenMP 编译 JOREK

下面给出 `.bashrc` 与 Makefile.inc 配置的一些示例。

\* 在 `.bashrc` 文件中添加以下行

    module purge

    # GCC + OPENMPI
    module load gcc/12.3.0
    module load openmpi/4.1.6--gcc--12.3.0
    module load openblas/0.3.26--gcc--12.3.0
    module load netlib-scalapack/2.2.0--openmpi--4.1.6--gcc--12.3.0
    module load fftw/3.3.10--openmpi--4.1.6--gcc--12.3.0
    module load boost/1.85.0--openmpi--4.1.6--gcc--12.3.0
    module load hdf5/1.14.3--openmpi--4.1.6--gcc--12.3.0
    module load metis/5.1.0--gcc--12.3.0
    module load parmetis/4.0.3--openmpi--4.1.6--gcc--12.3.0

    # Other module loads
    module load python/3.11.7

``` Make

MODEL             = model600
FC                = mpif90
CC                = mpicc
CXX               = mpicxx

FFLAGS_OMP       = -fopenmp
FFLAGS           = -w -fallow-argument-mismatch -fdefault-real-8 -fdefault-double-8 -DFUNNELED
FFLAGS          := $(FFLAGS) -O2 -msse2 -march=native

DEBUGFLAGS  = -g -p

FFLAGS_FIXEDFORM := $(FFLAGS) $(DEBUGFLAGS) $(FFLAGS_OMP)
FFLAGS_NOBOUNDS  := $(FFLAGS)               $(FFLAGS_OMP)
FFLAGS           := $(FFLAGS) $(DEBUGFLAGS) $(FFLAGS_OMP)

USE_STRUMPACK = 1
USE_HIPS   = 0
USE_PASTIX = 0
USE_PASTIX_MURGE = 0
USE_PASTIX6 = 0
USE_MUMPS = 1
USE_WSMP   = 0
USE_FFTW = 1
USE_HDF5 = 1
USE_BOOST = 0
USE_STD_BESSELK = 1
USE_TASKLOOP = 0
USE_MKL           = 0
USE_DIRECT_CONSTRUCTION=0
USE_BICGSTAB      = 0
USE_INTSIZE64     = 0
DEBUG             = 0

LIBDIR_GNU = /pitagora_work/FUPA1_MHD/JOREK_libraries_gnu

ifeq (1, $(USE_MUMPS))

 # METIS
 LIB_METIS = -L$(METIS_LIB) -lmetis
 INC_METIS = -I$(METIS_INCLUDE)

 # PARMETIS
 LIB_PARMETIS = -L$(PARMETIS_LIB) -lparmetis
 INC_PARMETIS = -I$(PARMETIS_INCLUDE)

 MUMPS_DIR = $(LIBDIR_GNU)/MUMPS_v541_recompiled
 LIB_MUMPS  = -L$(MUMPS_DIR)/lib -lzmumps -ldmumps -lmumps_common $(LIB_PARMETIS) $(LIB_METIS) -L${NETLIB_SCALAPACK_LIB} -lscalapack -L${OPENBLAS_LIB} -lopenblas

 INC_MUMPS  = $(MUMPS_DIR)/include $(INC_SCOTCH) $(INC_PARMETIS) $(INC_METIS)
 ORDLIB     = -L$(MUMPS_DIR)/PORD/lib -lpord
endif

ifeq (1, $(USE_STRUMPACK))
 STRUMPACK_HOME= $(LIBDIR_GNU)/STRUMPACK_gnu
 STRUMPACKINC = -I$(STRUMPACK_HOME)/include
 STRUMPACKLIB = -L$(STRUMPACK_HOME)/lib64 -lstrumpack

 STRUMPACKINC += -I${METIS_HOME}/include -I${PARMETIS_HOME}/include
 STRUMPACKLIB += -L${METIS_HOME}/lib -lmetis -L${PARMETIS_HOME}/lib -lparmetis -L${NETLIB_SCALAPACK_LIB} -lscalapack -L${OPENBLAS_LIB} -lopenblas

endif

# --- FFTW Library
INC_FFTW  = -I${FFTW_INCLUDE}
LIBFFTW = -L${FFTW_LIB} -lfftw3_mpi -lfftw3

# --- HDF5 Library
HDF5INCLUDE = ${HDF5_HOME}/include
HDF5LIB     = -L${HDF5_HOME}/lib -lhdf5_hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -lz

```

## 使用 INTEL oneAPI 编译 STARWALL

编译 STARWALL 所需的 `.bashrc` 与 config.in 文件如下（由 D. Bonfiglio 测试）。

- 在 `.bashrc` 文件中添加以下行

<!-- -->

    module purge
    module load git
    module load intel-oneapi-mpi/
    module load intel-oneapi-compilers
    module load intel-oneapi-mkl/2024.0.0--intel-oneapi-mpi--2021.12.1

- 使用下面的 `config.in` 文件编译 STARWALL（make clean; make -j 8）

``` config.in
# config.in file for the LINUX systems
MKL_HOME = $(INTEL_ONEAPI_MKL_HOME)/mkl/latest

include $(FILES_MK)
FC = mpif90 -f90=ifort -fc=ifort
FFLAGS = -autodouble -I$(OBJ_DIR) -module $(OBJ_DIR) -g

ifeq ($(DEBUG),1)
  FFLAGS += -O0 -warn all,nounused -check all,noarg_temp_created -debug all    \
  -debug-parameters -fstack-security-check -ftrapuv -traceback
else
  FFLAGS += -O3 -g
endif

FPPFLAGS =

LD = $(FC)
LDFLAGS = $(FFLAGS)

DPREF = -D
FPPFLAGS += $(DPREF)$(COMPILER) $(DPREF)$(OSTYPE)

########################################################################

MKLLIB = $(MKL_HOME)/lib/intel64
LAPACK_LIB = $(MKLLIB)/libmkl_sequential.a -Wl,--start-group                   \
  $(MKLLIB)/libmkl_intel_lp64.a $(MKLLIB)/libmkl_sequential.a                  \
  $(MKLLIB)/libmkl_core.a $(MKLLIB)/libmkl_scalapack_lp64.a                    \
  $(MKLLIB)/libmkl_blacs_intelmpi_lp64.a    -Wl,--end-group -lpthread

LIB = $(LAPACK_LIB) #-lX11 -lpmapi
########################################################################

all: $(EXECOS_MAIN)

$(EXECOS_MAIN): $(MAIN_OBJ) $(OS_MK) $(FILES_MK)
        $(LD) $(LDFLAGS) -o $@ $(MAIN_OBJ) $(addprefix -L,$(LIB_DIR)) $(LIB)
        mv $@ $(OBJ_DIR)

$(OBJ_DIR)/%.o: %.f90
        $(FC) -fpp $(FPPFLAGS) $(FFLAGS) -c -o $@ $<
```

### 作业脚本示例

- 截至 2025-07-02，配合作业脚本使用 sbatch 似乎仍不能完美工作：若已加载某些模块，会返回如下错误信息：*"sbatch: error: Batch job submission failed: Unexpected message received"*。
- 通过 sbatch 提交作业前请先执行 ***module purge***。
- 在作业脚本内部加载所需的全部模块。
- （kuan-wen）对于以 STRUMPACK 为求解器的动理学 MHD 程序，MPI 进程总数必须为 2 的幂，例如 2\^6=64。否则求解器会在粒子循环与投影步骤之后永久挂起，因为 STRUMPACK 使用分布式符号分解。

``` bash
#!/bin/bash

#SBATCH -J jorek
#SBATCH -p cpu

#SBATCH --nodes=5
#SBATCH --ntasks-per-node=16                   # number of tasks per node
#SBATCH --cpus-per-task=16                     # number of cores per task max 256 cores per node

#SBATCH --mem=760000                           # memory per node

#SBATCH --time=24:00:00
#SBATCH --output=./jorek.%j.out
#SBATCH --error=./jorek.%j.err


### Request e-mail notification
#SBATCH --mail-type=FAIL   # can be BEGIN, END, TIME_LIMIT, FAIL, ALL, NONE
#SBATCH --mail-user=xxxx@ipp.mpg.de

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

## For Intel compiler
module load intel-oneapi-mpi/
module load intel-oneapi-compilers
module load intel-oneapi-mkl/2024.0.0--intel-oneapi-mpi--2021.12.1
module load hdf5/1.14.3--intel-oneapi-mpi--2021.12.1--oneapi--2024.1.0

# This line is critical (at least for PastiX, tbc for Strumpack).
# This infiniband option was changed to default ``export FI_PROVIDER=verbs`` by Cineca team,
# which causes runs to hang forever after a few time-steps (usually during the PastiX solve)
export FI_PROVIDER=MLX

# srun ./jorek_model711 < ./input | tee logfile
mpirun -np $SLURM_NTASKS ./jorek_model711 < ./input | tee logfile
```

- 也可以交互式地通过 salloc 提交测试作业，例如：

``` bash
salloc --nodes=5 --ntasks=80 --cpus-per-task=16 --partition=cpu bash -c 'export OMP_NUM_THREADS=16; mpirun -np 80 ./jorek_model711 < ./input | tee logfile'
```

\<color #ed1c24\> 若使用 Intel 与 STRUMPACK 时模拟在矩阵分解处挂起，请尝试在作业脚本中添加以下行： \</color\>

``` bash
unset UCX_TLS
```

*请谨慎使用——在少数情况下观察到这会改变模拟结果！*

## 机时核算

\<color #ed1c24\> 请注意 CPU 消耗，目前我们消耗得太快了！可用下面的 saldo 命令查看用量。 \</color\>

要查看 Leonardo DCGP 上已使用的资源，请使用

`saldo -b –dcgp`

要查看更详细的信息（包含所有用户的用量），可以使用

`saldo -ra PROJECT_NAME –dcgp`

---
title: "ITER 集群"
nav_order: 13
parent: "HPC 与 PC 配置"
grand_parent: "编译与依赖库"
layout: default
render_with_liquid: false
---

# ITER 集群概述

参见：

- <https://confluence.iter.org/pages/viewpage.action?pageId=267026649> 获取访问权限
- <https://confluence.iter.org/display/IMP/ITER+Computing+Cluster> 获取更详细的信息

# 编译 {#compiling}
需要加载合适的模块并导出若干环境变量，以准备一个专用环境。

可以准备一个专用的 `.sh` 文件，如下所示：

```bash
#!/bin/bash

module purge

module load IMAS/3.41.0-2024.04-intel-2023b
module load VSCode/1.88.1
module load SCOTCH/7.0.4-iimpi-2023b
module load MUMPS/5.7.2-intel-2023b-parmetis
module load HDF5/1.14.3-iimpi-2023b
module load PaStiX/5.2.3-intel-2023b
module load FFTW/3.3.10-GCC-13.2.0
module load STRUMPACK

export PASTIX_HOME=$EBROOTPASTIX
export MUMPS_HOME=$EBROOTMUMPS
export METIS_HOME=$EBROOTPARMETIS
export SCOTCH_HOME=$EBROOTSCOTCH
export MKL_HOME=$EBROOTIMKL
export HDF5_HOME=$EBROOTHDF5
export LANG=C
export JOREK_HOST=iter-hpc
export compilethreads=8
export MAKEFLAGS="-j$compilethreads"
export PRERUN="export OMP_NUM_THREADS=8"
export MPIRUN="mpirun -np "
export BATCHCOMMAND="qsub"
export CXXFLAGS=-O0 # problem with stdio library on ITER http://gcc.1065356.n8.nabble.com/g-4-8-fails-with-Ox-option-td953876.html
```

既可以在编译前载入该文件：

```bash
source env2024.sh
```

也可以在每次启动时通过更新 `.bashrc` 文件直接载入，例如当 `env2024.sh` 位于 `~/public` 时：

```bash
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

if [ -f $HOME/.setup.sh ]; then
        . $HOME/.setup.sh
fi

# User specific aliases and functions

export PATH=.:$PATH
export CC=mpiicx
export FC=mpiifort
export F90=ifort
export plots=~/scripts_hub/scripts_javier/plot_scripts/

alias l.='ls -d .* --color=auto'
alias ll='ls -l --color=auto'
alias ls='ls --color=auto'
alias sqe='squeue -u $USER -o "%.8i %.2t %.10M %.6D %Z %R"'
alias q10='squeue -p gen10'

if [ -z "$PS1" ]; then
    # prompt var is not set, so this is *not* an interactive shell
    return
fi

# Decide OS and load correct environment file
source /etc/os-release
if [[ "$ID" == "rhel" ]]; then
    echo "RedHat"
    source ~/public/env2024.sh
elif [[ "$ID" == "centos" && "$VERSION_ID" == "8" ]]; then
#    echo 2
    echo "CentOS 8"
    source ~/public/env2020.sh
elif [[ "$ID" == "centos" && "$VERSION_ID" == "7" ]]; then
    echo "CentOS 7"
    source ~/public/env.sh
else
    echo "Unknown OS or version"
fi


export MPLBACKEND=TkAgg
export PATH="~/.local/bin:$PATH"

ulimit -s unlimited
```

如果已经启动了会话，最好的做法可能是重新执行这两个文件中的指令。在 `$HOME` 目录下的 shell 中运行：

```bash
source .bashrc
source ./public/env2024.sh
```

然后进入 JOREK 代码目录：

```bash
cd <jorek_directory>
```

并从头开始编译：

```bash
make clean
make cleanall
make
```

# 运行

建议通过 SLURM 调度器运行。

必须选择运行程序所在的分区，生产运行可以使用 `gen10` 或 `gen11`。调试运行可以使用专用分区 `gen10_debug` 或 `gen11_debug`。

典型的批处理脚本如下所示：

```bash
#!/bin/bash -l
#SBATCH --time=01:00:00
#SBATCH --job-name=JOREK_TM
#SBATCH --exclusive
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=14
#SBATCH --nodes=2
#SBATCH --partition=gen11_debug
#SBATCH --error myjob.err

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SLURM_CPU_BIND="rank"  
#export I_MPI_PMI_VALUE_LENGTH_MAX=512
export I_MPI_THREAD_LEVEL_DEFAULT=multiple
srun ./jorek_model600 < input > output
```

其中，`input` 是配置文件，`output` 是用于保存运行时日志信息的文本文件。

关于资源的合理分配，请参阅 ITER-SDCC 指南。

请记得将所需的额外文件放入工作目录，例如平衡剖面或壁响应文件，后者通常命名为 `starwall-response.dat`。

# 编译 CARIDDI

如果 CARIDDI 在上述环境下无法编译，请执行以下操作：

```bash
module purge
module load intel/2023b
module load ScaLAPACK/2.2.0-gompi-2023b-fb
make clean
make
```

---
title: "Leonardo（CPU）"
nav_order: 1
parent: "HPC 与 PC 配置"
grand_parent: "编译与依赖库"
layout: default
render_with_liquid: false
---

# 在 Leonardo CPU 分区（DCGP）上运行 JOREK

## 获取访问权限

- 通过 https://userdb.hpc.cineca.it/ 创建账户——选择 Create New User
- 然后填写与 HPC 相关的信息，并上传身份证／护照扫描件
- 联系相应的 PI，将你加入项目

## README

- [LEONARDO 用户指南](https://wiki.u-gov.it/confluence/display/SCAIUS/LEONARDO+User+Guide)
- [Eurofusion 用户的配置](https://wiki.u-gov.it/confluence/display/SCAIUS/EUROfusion+users%3A+Marconi+and+Leonardo+environments)
- CINECA 于 2025 年 2 月 18 日举办的网络研讨会的幻灯片 [slides_qa.pdf](slides_qa.pdf)
- CINECA 帮助台的电子邮件地址：superc@cineca.it

## 登录

所有登录节点（4 个 icelake 节点，不含 GPU）环境完全相同，均可通过 SSH（Secure Shell）协议使用"集合"主机名访问：

```bash
ssh -Y <user>@login.leonardo.cineca.it
```
该命令会建立到某个可用登录节点的连接。也可以显式指定登录节点：

```bash
login01-ext.leonardo.cineca.it
login02-ext.leonardo.cineca.it 
login05-ext.leonardo.cineca.it
login07-ext.leonardo.cineca.it
```
**如果收到错误信息“WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!”，请按[此链接](https://wiki.u-gov.it/confluence/display/SCAIUS/FAQ#FAQ-Ikeepreceivingtheerrormessage%22WARNING:REMOTEHOSTIDENTIFICATIONHASCHANGED!%22evenifImodifyknown_hostfile)中的说明处理。**

## 可用的软件
一如往常，通过 module avail/load/list/show 即可访问可用的软件

要使用文件管理器 midnight commander，请将下列两行写入 .bashrc：

```bash
export PATH=/leonardo/pub/userexternal/dbonfigl/mc/bin:$PATH
export LD_LIBRARY_PATH=/leonardo/pub/userexternal/dbonfigl/mc/shares/
mc:$LD_LIBRARY_PATH
```

## 编译 JOREK（截至 2025.02：测试中）
下面给出若干 .bashrc 与 Makefile.inc 配置示例。

[使用 GNU + OPENMPI](leonardo_cpu_with_gnu_openmpi.md)（目前最稳定的配置，且依赖库可公开访问）

[使用 Intel + OneAPI](leonardo_cpu_with_intel_oneapi.md)（测试中，且需要 FUAL8_MHD 项目的访问权限）

[使用 Intel + OneAPI + Raven 库](leonardo_cpu_with_raven_libraries.md)（测试中，使用从 Raven 复制的库）

## 文件系统
最重要的是 $HOME（用户专属）与 $WORK（项目专属），详情参见 LEONARDO 用户指南。请注意，$HOME 是唯一会做备份的文件系统！（目前暂停）

可用如下命令检查配额：

bash
cindata

## 批处理系统
- 基本命令：
```bash
sbatch <jobscript>                          # Submit a job script
sbatch -d afterok:<jobid> <jobscript>       # Submit a job script to start after <jobid> is finished

squeue -t running                           # List all currently running jobs
squeue -u <username>                        # List all own jobs

scancel <jobid>                             # Delete a queued or running batch job
```

- 作业脚本示例
作业脚本示例：2*8 个 MPI 任务分布在 2 个不同节点上，每个任务使用 14 个 OpenMP 线程。注意：需要在项目名后加上 _0，例如 FUA38_MHD_0

```bash
#!/bin/bash
  
#SBATCH -J test_jobscript
#SBATCH -A your_project
#SBATCH -p dcgp_fua_prod
#SBATCH --qos=<qos_name>

#SBATCH --nodes=2
#SBATCH --cores-per-socket=56                  # 56*2 sockets
#SBATCH --ntasks-per-node=8                    # number of tasks per node
#SBATCH --cpus-per-task=14                     # number of cores per task max 32 cores per node

#SBATCH --mem=494000                           # memory per node
#SBATCH --gres=tmpfs:10g

#SBATCH --time=24:00:00
#SBATCH --output=job.out
#SBATCH --error=job.err


### Request e-mail notification
#SBATCH --mail-type=FAIL   # can be BEGIN, END, TIME_LIMIT, FAIL, ALL, NONE
#SBATCH --mail-user=your_email_address

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_STACKSIZE='50M'  ## Optional, depending on the size of the job
export I_MPI_THREAD_LEVEL_DEFAULT=funneled #multiple

srun --cpu-bind=cores --cpus-per-task=$SLURM_CPUS_PER_TASK ./jorek_model600 < jorek_namelist > logfile
```
## 资源核算
要查看 Leonardo DCGP 上已使用的资源，请使用：

```bash
saldo -b --dcgp
```
要查看更详细的信息（包含所有用户的使用情况），可使用：

```bash
saldo -ra PROJECT_NAME --dcgp
```
可用的分区（另见[此处](https://wiki.u-gov.it/confluence/display/SCAIUS/EUROfusion+users%3A+Marconi+and+Leonardo+environments)）：

- 串行分区 lrd_all_serial。2 个专用的登录型节点。每个作业最多 4 个物理核，最大墙钟时间 4 小时。作业免费（不核算计算资源）。例如适合运行 jorek2_postproc。

- 生产分区 dcgp_fua_prod。258 个动态分配的计算节点。每个作业最多 16 个节点，最大墙钟时间 24 小时。对于大型生产运行（最少 17 个整节点，最多 64 个节点），可以指定 QOS dcgp_qos_fuabprod。

- 调试分区 dcgp_fua_dbg。2 个动态分配的计算节点。最多 2 个节点，最大墙钟时间 10 分钟。

- 生产分区上的低优先级队列。最多 16 个节点，最大墙钟时间 8 小时。作业免费（不核算计算资源）。可通过指定 FUA38_LOWPRIO_0 账户（需向 CINECA 申请加入该"项目"）与 QOS qos_fualowprio 来使用。适合节省项目资源。这类作业通常会在提交后的周末开始运行。

---
title: "压缩响应矩阵"
nav_order: 7
parent: "自由边界扩展（STARWALL、CARIDDI）"
grand_parent: "模型扩展"
layout: default
render_with_liquid: false
---

# 压缩响应矩阵

> **警告——此功能尚未合并。**
>
> 响应矩阵压缩在标准 `develop` 分支上不可用。本页的说明适用于未合并的 `feature/IMAS-4734-response-matrix-compression` 分支，可能与最终实现存在差异。不要指望这些命令、文件或响应矩阵格式能在常规 JOREK 检出中正常工作。

## 快速概览

该实现于 `feature/IMAS-4734-response-matrix-compression` 分支上开发，由两部分组成：

- `compress_response` 程序，位于 `jorek/vacuum/compression/`。其编译与用法见下文。
- `vacuum` 模块的改写版本，位于 `jorek/vacuum/`，可自动处理压缩格式。

关于该方法、目标与测试的详细描述见[响应矩阵压缩文稿](https://arxiv.org/abs/2404.16546)。

## 编译与运行 `compress_response`

该程序目前没有专用的输入文件 namelist。其参数必须在 `jorek/vacuum/compression/mod_compression.f90` 中直接修改，具体见下一节。

`compress_response` 使用 ScaLAPACK，因此编译前必须在 `Makefile.inc` 中设置 `SCALAPACKLIB` 与 `SCALAPACKINCLUDE` 变量。例如，在 MarconiFusion 上使用了如下配置：

```makefile
##################
ifeq (1, ${COMPRESSION_TOOL})
  SCALAPACKLIB     = -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_blacs_intelmpi_lp64
  SCALAPACKINCLUDE = -I${MKL_HOME}/include
endif
##################
```

在 `jorek` 目录内运行以下命令：

```bash
make -j8 compress_response
```

若编译成功，会生成名为 `compress_response` 的可执行文件。

在提交脚本中用以下命令运行它：

```bash
mpirun -np ${NTASKS} ./compress_response
```

算例目录中必须存在 `starwall-response.dat` 文件。使用 SLURM 调度器时，`NTASKS` 可替换为 `SLURM_NTASKS`。若任一矩阵的 $n=0$ 部分必须保持不压缩，则还须提供 `boundary.txt` 文件。

程序写出 `starwall-response-compr.dat`，其 `file_version` 设置为：

- 若任一矩阵被因子化，则为 `7`。
- 若所有矩阵均采用聚合格式（包括压缩后重新聚合的矩阵），则为 `6`。

要在 JOREK 中使用结果，将 `starwall-response-compr.dat` 重命名为 `starwall-response.dat`。

## `mod_compression.f90` 中的参数

在 `jorek/vacuum/compression/mod_compression.f90` 中修改这些参数。默认值以粗体显示。

| 参数 | 类型 | 可选值 | 说明 |
|:---|:---|:---|:---|
| `compr_a_ye` | `logical` | `.true.` 或 **`.false.`** | 压缩 `a_ye` 响应矩阵。 |
| `compr_a_ye_n0` | `logical` | `.true.` 或 **`.false.`** | 压缩 `a_ye` 的 $n=0$ 部分。 |
| `compr_a_ye_n0_sep` | `logical` | `.true.` 或 **`.false.`** | 分别压缩 `a_ye` 的各个 $n=0$ 部分。 |
| `compr_a_ey` | `logical` | `.true.` 或 **`.false.`** | 压缩 `a_ey` 响应矩阵。 |
| `compr_a_ey_n0` | `logical` | `.true.` 或 **`.false.`** | 压缩 `a_ey` 的 $n=0$ 部分。 |
| `compr_a_ey_n0_sep` | `logical` | `.true.` 或 **`.false.`** | 分别压缩 `a_ey` 的各个 $n=0$ 部分。 |
| `compr_a_ee` | `logical` | `.true.` 或 **`.false.`** | 压缩 `a_ee` 响应矩阵。 |
| `compr_s_ww` | `logical` | `.true.` 或 **`.false.`** | 压缩 `s_ww` 响应矩阵。 |
| `compr_s_ww_inv` | `logical` | `.true.` 或 **`.false.`** | 压缩 `s_ww_inv` 响应矩阵。 |
| `retained` | `real*8` | 在 `[0.d0, 1.d0]` 内取值；默认 **`-1.d0`** | 压缩后保留的奇异值比例。 |
| `retained_a_ye` | `real*8` | 在 `[0.d0, 1.d0]` 内取值；默认 **`-1.d0`** | `a_ye` 保留的奇异值比例。 |
| `retained_a_ey` | `real*8` | 在 `[0.d0, 1.d0]` 内取值；默认 **`-1.d0`** | `a_ey` 保留的奇异值比例。 |
| `retained_a_ee` | `real*8` | 在 `[0.d0, 1.d0]` 内取值；默认 **`-1.d0`** | `a_ee` 保留的奇异值比例。 |
| `retained_s_ww` | `real*8` | 在 `[0.d0, 1.d0]` 内取值；默认 **`-1.d0`** | `s_ww` 保留的奇异值比例。 |
| `retained_s_ww_inv` | `real*8` | 在 `[0.d0, 1.d0]` 内取值；默认 **`-1.d0`** | `s_ww_inv` 保留的奇异值比例。 |
| `debug` | `logical` | **`.true.`** 或 `.false.` | 压缩过程中输出调试信息。 |
| `printsv` | `logical` | `.true.` 或 **`.false.`** | 将奇异值写入文件。 |
| `writeout` | `logical` | **`.true.`** 或 `.false.` | 写出输出文件。 |
| `filevers` | `integer` | **`6`** 或 `7` | 选择输出文件版本。 |
| `CARIDDI` | `logical` | `.true.` 或 **`.false.`** | 以 `CARIDDI_mode` 读取输入。 |
| `reaggregate` | `logical` | **`.true.`** 或 `.false.` | 重新聚合经因子化的奇异值分解。 |
| `verify_split` | `logical` | `.true.` 或 **`.false.`** | 检查 $n=0$ 矩阵拆分是否正确执行。 |

## 真空模块说明与限制

### 说明

- 改写后的真空模块应能自动处理 `file_version` 为 `6` 或 `7` 的 `starwall-response.dat` 文件。
- 要用压缩后的响应矩阵运行 JOREK，将 `starwall-response-compr.dat` 重命名为 `starwall-response.dat`，然后照常运行 JOREK。
- `jorek/vacuum/vacuum.f90` 中定义的 `t_response_mat` 数据类型初始化了几个新变量。详情见该文件中的注释。

### 限制

- 当前实现只能处理 `a_ye` 与 `a_ey` 的压缩版本。
- `a_ye` 与 `a_ey` 的格式必须一致：不能其中一个因子化而另一个聚合。

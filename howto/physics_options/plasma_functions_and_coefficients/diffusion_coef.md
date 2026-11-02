---
title: "为稳态剖面求 D_perp 与 ZK_perp"
nav_order: 1
parent: "等离子体函数与系数"
grand_parent: "物理选项"
layout: default
render_with_liquid: false
---

# 扩散系数与传导系数计算器

许多 JOREK 用户在长时间仿真（n=0）中难以维持稳态的 H 模 ne 与 T 剖面。要做到这一点，需要选择与下列内容一致的输运系数：

- 所施加的粒子源与加热源，以及
- 期望的目标剖面或平衡剖面（假定为磁面函数）。

下面说明如何使用相关工具来完成这件事。

## 步骤 1：从平衡中获取度规、源与目标剖面

为此，直接使用 [`jorek2_postproc`](../../introduction_to_jorek_diagnostics.md#jorek2_postproc)，命令为 `pol_contour_integrals`。在 postproc 中需要执行的操作如下：

```text
namelist input
set surfaces 300
for step 0 do
  pol_contour_integrals
done
```

这会导出一个包含全部所需剖面（度规、目标、源）的文件，用于求解扩散系数：

```text
postproc/pol_contour_integrals_s000000.dat
```

## 步骤 2：用 Python 求系数

运行 `jorek_repo/util/obtain_diff_coefficients.py` 中的 Python 脚本：

```bash
python jorek_repo/util/obtain_diff_coefficients.py postproc/pol_contour_integrals_s000000.dat --skiprows 2
```

这会在以下文件中生成可直接使用的系数：

```text
D_profile.dat
kappa_i.dat
kappa_e.dat
kappa_t.dat   # Total temperature
```

在输入文件的 `d_perp_file`、`zk_i_perp_file`、`zk_e_perp_file` 和 `zk_perp_file` 中引用这些文件。之后即可开始计算。

## 所求解的方程

所采用的方法可在此处找到。它本质上是平衡态下的一维扩散＋源方程，具有解析解。

**J. Artola**  
*2021 年 10 月 29 日*

取平衡连续性方程

$$
\nabla \cdot \left(D\nabla \rho\right) = -S,
\tag{1}
$$

其中 $S$ 包含所有汇／源，也包括流动项。

将方程变换到磁面对齐坐标并作一些代数运算后，可得到 $D$ 的解析解：

$$
D(\psi_N)
=
-
\frac{(\psi_{\mathrm{bnd}}-\psi_{\mathrm{axis}})^2}
{\alpha(\psi_N)\,
\displaystyle\frac{\partial \rho}{\partial \psi_N}}
\int_0^{\psi_N}
\gamma(\psi_N')
\left\langle S \right\rangle_{\psi_N'}
\,d\psi_N'.
\tag{2}
$$

这里 $\left\langle S \right\rangle_{\psi_N'}$ 是磁面平均的净源。该方程也可由散度定理导出。

我们定义了如下几何系数：

$$
\alpha(\psi_N)
=
\oint_{\psi_N}
R |\nabla\psi|\,dl_{\mathrm{pol}},
\tag{3}
$$

以及

$$
\gamma(\psi_N)
=
\oint_{\psi_N}
\frac{R}{|\nabla\psi|}
\,dl_{\mathrm{pol}},
\tag{4}
$$

其中 $dl_{\mathrm{pol}}$ 是磁面极向轮廓的微分线元。

## 说明

- 式 (2) 在 SOL 中不适用。在该区域内必须手动设定扩散，才能在分界面处得到合理的 $\rho$。

- 当包含 SOL 时，式 (2) 并不能完全确定 $\rho$，因为式 (1) 在 $\rho$ 上可相差一个整体常数。为此需要调节 SOL 中的源与汇，或调节边界条件。

- 式 (2) 在 $\psi_N = 0$ 处或当

  $$
  \rho' = 0.
  $$

  时发散。在这些情况下必须对剖面作平滑处理。此外必须给定源，否则不存在唯一解。

- 流动项可以用 `jorek2_postproc` 作平均后计入 $\left\langle S \right\rangle$。

- 同一公式也可用于温度方程。

## Python 脚本中的注意事项与硬编码参数

该 Python 脚本有意通过文件顶部附近的硬编码常数来配置（而不是提供大量命令行开关）。在新算例上使用该工具之前，应先检查这些参数。

最重要的设置是用于数值稳定性的 MIN/MAX 边界。

**若源处于激活状态而梯度为零，则方程不存在解**。例如，平坦剖面只能在无源的情况下存在。**在仅含扩散＋源的问题中，非单调的目标剖面没有解。**

### 1. 数值容差（`EPS_*`）

这些参数控制脚本如何识别解析公式病态的区域。

- `EPS_INT`：判定源项累积积分"近似为零"的阈值。
- `EPS_DER_RHO`、`EPS_DER_Ti`、`EPS_DER_Te`、`EPS_DER_T`：判定导数"近似为零"的阈值。

若 `EPS_DER_*` 阈值过小，数值噪声可能产生极大的系数。
若阈值过大，则可能把大片区域误判为"平坦／无约束"。

### 2. MIN/MAX 边界（对数值稳定性至关重要）

在计算并清理剖面之后，脚本会把系数截断到硬编码范围内：

- 密度扩散系数边界：`D_MIN_RHO`、`D_MAX_RHO`。
- 热传导系数边界：`KAPPA_I_MIN`、`KAPPA_I_MAX`、`KAPPA_E_MIN`、`KAPPA_E_MAX`、`KAPPA_T_MIN`、`KAPPA_T_MAX`。

用这些限值避免数值问题（扩散过小或过大）。

### 3. 芯部处理（`EXTR_CORE_PSIN`）

在磁轴附近，剖面／度规可能定义不佳或含有噪声。脚本对最终计算得到的系数剖面强制施加规整的芯部行为：

- 使用满足 `psi_N >= EXTR_CORE_PSIN` 的前两个点拟合一条直线。
- 用该直线覆盖 `psi_N < EXTR_CORE_PSIN` 处的所有系数值。

必要时调整 `EXTR_CORE_PSIN`：

- 若轴附近区域不可靠／含噪声，则增大该值。
- 若信任芯部的数值，则减小该值。

### 4. SOL 延展（`EXTEND_TO_PSIN` 与斜坡参数）

脚本按以下方式把每个系数剖面延展到 `EXTEND_TO_PSIN`：

- 在最后一个输入点之外增加 `N_SOL_POINTS` 个点。
- 采用等于最后计算值的常数尾部（默认）。
- 可选地在 SOL 中施加平滑的 arctan 斜坡。

控制参数：

- `EXTEND_TO_PSIN`、`N_SOL_POINTS`。
- `RAMP_AMP`（0 表示不加斜坡）、`RAMP_CENTER`、`RAMP_WIDTH`。

若希望在 SOL 中增强输运，同时保持芯部／边界（psi_N <= 1）不变，这一功能很有用。

## 实用故障排查

若系数出现尖峰：

- 收紧相应的 MAX 值。
- 考虑增大 `EPS_DER_*`（避免除以极小的导数）。

若剖面仍随时间演化：

- 检查源与目标梯度在物理上是否相容。
- 考虑使用 `--hard-fail-impossible` 以尽早识别不相容的区域。

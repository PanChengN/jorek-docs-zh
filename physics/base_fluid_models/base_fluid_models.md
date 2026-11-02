---
title: "基础流体模型"
nav_order: 5
parent: "物理模型"
has_children: true
nav_fold: true
layout: default
render_with_liquid: false
---

Andres 正在编写本页。

# JOREK 物理模型

请注意，除下文描述的模型之外，**还有多个开关可用来激活／停用方程中的不同项与边界条件**。相关说明见 [howto/physics_options](../../howto/physics_options.md)。

## [约化 MHD](reduced_mhd.md)：

__model 600__ 是约化 MHD 的主力模型，它允许用户在[硬编码参数](../../compiling/compilation_and_libraries/hard-coded_parameters.md)阶段自行组合希望保留在模拟中的不同物理内容（$v_\parallel$、$T_e$ 与 $T_i$ 分离、流体中性粒子、流体杂质……）。__model 600__ 中始终存在的变量为：

| 变量 | 符号 | 变量编号 | 
| --- | --- | --- |
| 极向磁通： | $\psi$ | 1 |
| 速度流函数： | $u$ | 2 |
| 环向电流密度： | $zj$ | 3 |
| 涡量： | $\omega$ | 4 |
| 质量密度： | $\rho$ | 5 |
| 温度： | $T$ 或 $T_i$ | 6 |

当使用 $v_\parallel$ 时，其编号始终为 `var_vpar=7`。

对 __model 600__ 而言，变量编号在编译时分配。

除 __model 600__ 之外，下面还列出了较旧的遗留约化 MHD 模型。__但是__，新的开发成果未必会包含在这些模型中，因此建议用户使用 __model 600__。

| 模型 | 说明 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| model199 | 无平行流 | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T$ | | | | |
| model303/333 | 含平行流 | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T$ | $v_{\vert\vert}$ | | | |
| model305 | ECCD 1 电流模型 | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T$ | $v_{\vert\vert}$ | $J_{ECCD}$ | | |
| model306 | ECCD 2 电流模型 | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T$ | $v_{\vert\vert}$ | $J_{EC1}$ | $J_{EC2}$ | |
| model400 | 含平行流；$T_e$ 与 $T_i$ 分离 | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T_i$ | $v_{\vert\vert}$ | $T_e$ | | |
| model500/501/555 | 含平行流以及中性粒子／杂质密度 | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T$ | $v_{\vert\vert}$ | $\rho_{n/imp}$ | | |


## [全 MHD](full_mhd.md)

| 模型 | 变量：1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| model710 | $A_3$ | $A_R$ | $A_Z$ | $u_R$ | $u_Z$ | $u_\phi$ | $\rho$ | $T$ | | |
| model711 | $A_3$ | $A_R$ | $A_Z$ | $u_R$ | $u_Z$ | $u_\phi$ | $\rho$ | $Ti$ | $Te$ | |
| model712 | $A_3$ | $A_R$ | $A_Z$ | $u_R$ | $u_Z$ | $u_\phi$ | $\rho$ | $Ti$ | $Te$ | $\rho_n$ |


另请参阅 [符号约定](../notation.md) 页面。

## Emmanuel Franck 等人的推导

  * [第一部分：关于双流体与单流体 MHD 的文档](assets/hierarchymhd.pdf)
  * [第二部分：关于约化 MHD 的文档](assets/reduced_mhd.pdf)

---
title: "ADAS 原子数据"
nav_order: 4
parent: "杂质"
grand_parent: "模型扩展"
layout: default
render_with_liquid: false
---

## 简要概述

在涉及电离、复合、线辐射、轫致辐射、复合辐射等过程的 JOREK 模型（如 500、501、502、565、600 等）中，相应的速率系数常取自原子数据与分析结构（Atomic Data and Analysis Structure，ADAS）数据库。这些系数按元素以 ASCII 文本文件给出，原则上可从 OPEN-ADAS 网页 [https://open.adas.ac.uk/](https://open.adas.ac.uk/) 下载。
为方便起见，氢、氖、氩等常用元素对应的文件已预先下载，可在[此处](https://www.jorek.eu/wiki/lib/exe/fetch.php?media=adas_data.tar.gz)获取。运行 JOREK 时，若要使用 ADAS 系数，须在输入／namelist 文件中通过输入参数 `adas_dir` 提供存放这些文件的文件夹路径。

## 命名约定

我们使用 [ADF11 等核主文件](http://open.adas.ac.uk/adf11)。该数据集包含以下系数：（W 不具备的系数以 `()` 标出）

| 符号 | 电子—离子碰撞的电离态 |
|--------|-----------------------------------------------|
| ACD    | 有效复合系数          |
| SCD    | 有效电离系数             |
| (QCD)  | (交叉耦合系数)                 |
| (XCD)  | (母体交叉耦合系数)                  |

| 符号 | 氢离子碰撞的电离态    |
|--------|---------------------------------------------------|
| (CCD)  | (电荷交换有效复合系数) |

| 符号 | 电子—离子碰撞的辐射发射 |
|--------|-------------------------------------------------|
| PLT    | 由离子激发驱动的线功率         |
| PRB    | 由主离子的复合与轫致辐射驱动的连续谱与线功率 |
| (PLS)  | (主离子选定跃迁的线功率) |

| 符号 | 氢离子碰撞的辐射发射 |
|--------|-------------------------------------------------|
| (PRC)  | (由热中性氢向主离子的电荷转移引起的线功率) |

在聚变等离子体中模拟 W 杂质需要 ACD、SCD、CCD。为估计辐射损失，还需要 PLT、PRB。

W 的数据集中没有 CCD，因此目前暂不使用。

文件名遵循简单的格式：

| 类型 | 文件名       | 单位  |
|------|----------------|--------|
| ACD  | acd50_w.dat    | cm3s-1 |
| SCD  | scd50_w.dat    | cm3s-1 |
| PLT  | plt50_w.dat    | Wcm3   |
| PRB  | prb50_w.dat    | Wcm3   |

全部亚稳态未分辨。

## 用系数进行参数化

所有系数都只是自由电子密度与电子温度的函数。目前这些系数的适用电子密度上限为
  * 氢：$2\times 10^{21} m^{-3}$
  * 氖、氩：$3\times 10^{21} m^{-3}$？
数据在扩展密度范围内也可获得（对氘可达 1e24 m^-3），但这些数据尚未在 JOREK 中使用。

速率对系数的参数化（函数依赖关系）如下，

---待补充---

## ADAS 文件的数据格式

注意原始 ADAS 数据的组织方式是：所有复合数据（ACD 与 PRB）表示从 Z = 1 到 N 的复合，而所有电离数据（SCD 与 PLT）表示电离到 Z = 1 到 N。为避免差一错误，我们在读取原始 ADAS 数据时于 mod_openadas.f90 中将原始数据平移了一个索引。

文件格式的更多细节也可参见 [Open-ADAS 站点](http://open.adas.ac.uk/man/appxa-11.pdf)。

  * 按电离能级
    * 按温度（log10，eV）
      * 按密度（log10，cm^-3）
        * 广义碰撞辐射系数（ACD、SCD、PLT、PRB）的 log10

## 从上述数据获取电离率

  * 电离系数按电离到能级 z 给出，取 z = 1..n_Z。
  * 复合系数按从能级 z 复合给出，取 z = 1..n_Z

  * 体积内电离到 z 的速率 = SCD(z, Te) * n_e * n_z
  * 单个原子电离到 z 的速率（1/s）= SCD(z, Te) * n_e
  * 原子在给定时间内发生电离的概率 = SCD(z, Te) * n_e * dt，该式仅在小概率时有效

复合率以及每个原子的 LT/RB 功率可作与上述相同的计算

## 系数的插值

系数在 Te 与 ne 的 log10 上作线性插值。例如可以改用高阶样条。

## 检查辐射功率函数及其各分量 {#checking-the-radiation-power-function-and-its-components}
检查辐射功率函数及其各分量的快捷方式是使用 radiation_function_diagno 程序，它针对一组硬编码参数与杂质种类输出上述数据。 

另一种方式是检查自动生成的 charge_distribution.dat 文件，其中包含一系列电子温度下的日冕平衡电荷态分布，以及总辐射功率函数。

## 数据

也可以从下面下载数据
  * **[JOREK 当前使用的数据](https://www.jorek.eu/wiki/lib/exe/fetch.php?media=adas_data.tar.gz)**
  * **[扩展密度的数据（仅氢可用）](https://www.jorek.eu/wiki/lib/exe/fetch.php?media=files.tar.gz)**

## 联系人

如有问题，可尝试联系下列人员之一。他们各自接触 ADAS/JOREK 的程度不同，因此并非每个人都能回答你的所有问题。
  * Martin O'Mullane（ADAS 主要开发者之一，非 JOREK 用户），邮箱：martin.omullane@strath.ac.uk
  * Di Hu，邮箱：hudi2@buaa.edu.cn
  * Sven Korving，邮箱：Sven.Korving@iter.org
  * Fabian Wieschollek，邮箱：fawie@ipp.mpg.de
  * Vinodh Bandaru，邮箱：vkb@ipp.mpg.de
  * Máté Szűcs，邮箱：mate.szuecs@ipp.mpg.de

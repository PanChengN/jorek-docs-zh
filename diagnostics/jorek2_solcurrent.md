---
title: "jorek2_SOLcurrent"
nav_order: 31
render_with_liquid: false
parent: "General"
---

## jorek2_SOLcurrent

该诊断对 jorek_restart.h5 做后处理，通过求解 Stangeby 式 17.29 来确定刮削层（SOL）电流（靶板之间的热电电流）。运行方式为

```
jorek2_SOLcurrent < input
```

其中 "input" 是运行 jorek 所用的输入 namelist 文件（jorek_model600 < input）。生成的输出会放入 "SOLcurrent" 文件夹（若该文件夹尚不存在则会自动创建），文件名为 "stepXXXXXX.dat"（例如当 jorek_restart.h5 是 jorek00200.h5 时，文件名为 step000200.dat）。输出文件的内容是沿边界对每条磁力线求解该方程的结果，并附带若干中间输出。输出示例如下（此处截断为两行，实际输出行数为 n_bnd_elements）：

```
 #            R_b               Z_b             Phi_b               R_e               Z_e             Phi_e              ne_b              ne_e              Te_b              Te_e                 L      av_sigma_par         P_h - P_c           pe_term         j_hat_par             j_par             bdotn            j_wall                dl             I_loc
    5.56420000E+00   -4.55671484E+00    0.00000000E+00    5.56420000E+00   -4.55671484E+00    0.00000000E+00    5.82638640E+16    5.82638640E+16    4.51428697E-01    4.51428697E-01    0.00000000E+00    0.00000000E+00    0.00000000E+00    0.00000000E+00    0.00000000E+00    0.00000000E+00   -5.36382742E-02    0.00000000E+00    1.48283537E-02    0.00000000E+00
    5.56420000E+00   -4.54188649E+00    0.00000000E+00    4.16796881E+00   -3.90608038E+00   -6.46920674E+00    4.45768773E+17    4.09077666E+17    4.51369085E-01    5.35422967E-01    3.17676936E+01    3.72828298E+03   -8.04289104E-02    3.90718320E-01    8.92291495E-02    4.20341276E+01   -5.26322395E-02   -1.93477645E+00    1.51329629E-02   -1.02361670E+00
```

_b 表示所求解方程对应磁力线的起点，_e 表示该磁力线的终点，R、Z、Phi 为坐标，ne、Te 为电子密度与温度，L 为连接长度，av_sigma_par 为平均平行电导率，P_h-P_c 为沿磁通管从热端到冷端的压降（可用作合理性检查，把 (R_b,Z_b,Phi_b) 处的压力与 (R_e,Z_e,Phi_e) 处的压力相比较），pe_term 为方程中的压力积分项（即最后一项），j_hat_par 为方程的解，j_par 为 (R_b,Z_b,Phi_b) 处的物理热电平行电流密度，bdotn 为 (R_b,Z_b,Phi_b) 处的螺距角点积，j_wall 为壁上的热电电流密度（已计入螺距角），dl 为该磁通管的极向长度，I_loc 为该磁通管打到壁上的电流。

对于 n_bnd_elements ~ 500 的生产级有限元网格，若 jorek2_SOLcurrent 编译时未开启 DEBUG 选项，在单个 omp 核上运行该诊断约需 3 分钟；若使用 omp 并行（在调用诊断前设置 "export OMP_NUM_THREADS=..."）则更快。诊断运行过程中，输出会告知你当前进行到哪一步，通常 "Initialising element neighbours" 约占一半时间，另一半用于实际的磁力线追踪与方程求解（其间会给出形如 "starting point =         49 of        482" 的中间进度更新）

诊断结束时，它会给出所有 I_loc 值之和作为合理性检查：

```
Sanity check: total current over the whole wall (i.e. discretisation error, usually of order 10 A, should be negligible compared to target current, usually of order 10 kA) =    -0.11341611E+02 A
```

原则上这个和应趋于 0，因为每条磁通管在内靶与外靶上的电流大小应相同、符号相反。


要计算实际的靶板电流，可用你熟悉的任意编程语言对 stepXXXXXX.dat 做后处理，具体取决于你希望计入多大范围内的电流。下面给出 Python 示例代码：

```python
#importing modules
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

#load .dat file
filepath = '/path/to/sim/folder/.../SOLcurrent/stepXXXXXX.dat'
j_SOL_dat = np.genfromtxt(filepath,dtype=None).T

#definitions of all variables
yl_SOLcurrentdat = ["$R_b$ (m)","$Z_b$ (m)","$\phi_b$","$R_e$ (m)","$Z_e$ (m)","$\phi_e$","$n_{e,b}$ (m⁻³)",
              "$n_{e,e}$ (m⁻³)","$T_{e,b}$ (eV)","$T_{e,e}$ (eV)","$L$ (m)",
              "$\sigma_{\parallel,av}$ ($\Omega$⁻¹m⁻¹)","$P_{e,h} - P_{e,c}$ (Pa)","$p_e$ term",
              "$\hat{j}_{\parallel}$ (-)","$j_{\parallel}$ (A/m²)", "$\hat{b} \cdot \hat{n}$", 
              "$j_{wall}$ (A/m²)","dl (m)", "$I_{loc}$ (A)"]

#target mask (ITER)
[R,Z] = j_SOL_dat[0:2]
[R2,Z2] = j_SOL_dat[3:5]
mask_IT = (R < 5) & (Z < -2.5) & (-0.625*R + Z > -6.5)
mask_OT = (R > 5.55) & (Z < -3.3) & (Z > -4.5)

#SOL current at both targets
I_SOL_IT = sum(j_SOL_dat[-1][mask_IT])
I_SOL_OT = sum(j_SOL_dat[-1][mask_OT])

print(f'sum I_loc = {(sum(j_SOL_dat[-1])/1e3):.2f} kA')
print(f'I_SOL into   IT = {(-I_SOL_IT)/1e3:.1f} kA')
print(f'I_SOL out of OT = {(I_SOL_OT) /1e3:.1f} kA')

#plot quantities
plot_from = 10
for j in range(len(j_SOL_dat[plot_from:])):
    i = j + plot_from
    qty = j_SOL_dat[i]
    plt.figure()
    plt.plot(Z[mask_IT],qty[mask_IT],'.',label='started at IT')
    plt.plot(Z2[mask_OT],qty[mask_OT],'x',label='ended at IT')
    plt.xlabel('Z (IT end of fieldline)')
    plt.ylabel(yl_SOLcurrentdat[i])
    plt.xlim([-4,-3])
    plt.grid("show")
    plt.legend()
    plt.show()
```
该脚本会打印两个靶板上的电流以及所有电流之和（即前面提到的合理性检查）：
```
sum I_loc = -0.01 kA
I_SOL into   IT = 15.5 kA
I_SOL out of OT = 15.5 kA
```
并生成一系列图（示例图在上游已缺失）：

<!-- 原站引用的图/附件已缺失：上游仓库与旧 wiki 均无此文件，故移除引用 -->

从这张图可以看出，从内靶出发的示踪粒子与从外靶出发的示踪粒子所得到的计算结果相同，这本应如此。

关于该程序中标量 j 的符号约定：若电流在起点位置 (R_b,Z_b,Phi_b) 从壁流出，则定义为正。通常外靶温度更高，电流一般从 OT 流向 IT，因此 OT 处为正号、IT 处为负号。

可以写一个简单的 bash 脚本对许多重启文件循环处理，从而免去逐个重启文件手动运行的麻烦。

关于实现细节、ITER 算例的计算结果以及与 SOLPS 的 SOL 电流结果对比，见 [Daniël 的硕士论文报告](https://research.tue.nl/files/340298012/1367803_-Maris_D.-MSc_thesis_Thesis-_NF.pdf) 第 4.1 节

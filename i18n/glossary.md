# JOREK 中文文档术语表（i18n/glossary.md）

本表用于约束全站译名一致。**翻译时严格遵守，不要自创译法。**

## 一、保持英文原文（不翻译）

| 类别 | 术语 |
|---|---|
| 代码与项目名 | JOREK、JOREK-STARWALL、JOREK-CARIDDI、STARWALL、CARIDDI |
| 物理模型缩写 | MHD、RMHD、full MHD、VMS、TG（Taylor-Galerkin） |
| 计算与软件 | MPI、OpenMP、SLURM、HDF5、VTK、FFT、FFTW、MKL、SCOTCH、PaStiX、MUMPS、METIS、BLAS、LAPACK |
| 工具与格式 | ParaView、VisIt、gnuplot、EFIT、eqdsk、IMAS、ADAS、namelist、Makefile、Makefile.inc |
| 装置名 | ITER、JET、ASDEX Upgrade、Leonardo、LUMI、Pitagora、TGCC-CEA、EUROfusion Gateway |
| 参数名 | 所有 namelist 变量（`tstep`、`nstep`、`nout`、`eta`、`visco`、`F0`、`n_tor`、`D_perp`、`ZK_par` 等）、所有 shell 变量、函数名、文件名、路径 |
| 物理量符号 | $\psi$、$\Phi$、$j_\phi$、$\omega$、$\rho$、$T$、$q$、$B$ 等 LaTeX 符号一律原样 |

## 二、固定译名

| 英文 | 中文 |
|---|---|
| tokamak | 托卡马克 |
| stellarator | 仿星器 |
| X-point | X 点 |
| limiter | 限制器 |
| divertor | 偏滤器 |
| separatrix | 分界面 |
| scrape-off layer (SOL) | 刮削层（SOL） |
| flux surface | 磁面 |
| flux-surface aligned | 磁面对齐（的） |
| poloidal | 极向 |
| toroidal | 环向 |
| toroidal harmonic | 环向谐波 |
| toroidal mode number (n) | 环向模数（n） |
| poloidal mode number (m) | 极向模数（m） |
| safety factor | 安全因子 |
| aspect ratio | 长径比 |
| equilibrium | 平衡 |
| Grad-Shafranov equation | Grad-Shafranov 方程 |
| edge localized mode (ELM) | 边界局域模（ELM） |
| disruption | 破裂 |
| tearing mode | 撕裂模 |
| peeling-ballooning mode | 剥离—气球模 |
| resistive wall | 电阻壁 |
| vertical displacement event | 垂直位移事件 |
| free boundary | 自由边界 |
| finite element | 有限元 |
| Bezier surface | 贝塞尔曲面 |
| isoparametric | 等参 |
| grid / mesh | 网格 |
| time step | 时间步 |
| time integration | 时间积分 |
| implicit | 隐式 |
| fully implicit | 全隐式 |
| Newton iteration | Newton 迭代 |
| solver | 求解器 |
| preconditioner | 预条件器 |
| sparse matrix | 稀疏矩阵 |
| convergence | 收敛 |
| residual | 残差 |
| resistivity | 电阻率 |
| viscosity | 黏性 |
| hyperresistivity | 超电阻率 |
| hyperviscosity | 超黏性 |
| diffusivity | 扩散系数 |
| heat conduction | 热传导 |
| parallel / perpendicular | 平行／垂直（磁力线方向／垂直于磁力线） |
| diamagnetic drift | 抗磁漂移 |
| neoclassical | 新经典 |
| bootstrap current | 自举电流 |
| sheath boundary condition | 鞘层边界条件 |
| heat flux | 热流 |
| Ohmic heating | 欧姆加热 |
| runaway electron | 逃逸电子 |
| energetic ion | 高能离子 |
| impurity | 杂质 |
| neutral | 中性粒子 |
| particle tracer | 粒子追踪器 |
| marker | 标记粒子 |
| pusher | 推进器 |
| MGI (massive gas injection) | 大规模气体注入（MGI） |
| SPI (shattered pellet injection) | 碎裂弹丸注入（SPI） |
| RMP (resonant magnetic perturbation) | 共振磁扰动（RMP） |
| controller / actuator | 控制器／执行器 |
| diagnostics | 诊断（工具） |
| post-processing | 后处理 |
| restart file | 重启文件 |
| growth rate | 增长率 |
| normalization | 归一化 |
| normalized units | 归一化单位 |
| hard-coded parameters | 硬编码参数 |
| compile / build | 编译／构建 |
| library | 依赖库 |
| module (环境模块) | 模块 |
| batch system / job script | 批处理系统／作业脚本 |
| run directory | 算例目录 |
| benchmark | 基准算例 |
| verification / validation | 校核／确认 |

## 三、文风约定

1. **命令、代码、路径、参数一律保留原文**，包括注释里的变量名。
2. 段落按原文一段对一段，不合并、不增删；原文的列表结构、表格列数保持一致。
3. 保留 kramdown 特殊语法：`{: .note }`、`{: .warning }`、属性列表 `{:.align-center}`、引用式图片 `![alt][ref]` 及其定义。
4. 数学公式原样保留（`$$ ... $$`、`\( ... \)`），只翻译公式外的说明文字。
5. 链接目标路径不改（相对 `.md` 路径保持原样），只翻译链接文字。
6. 首次出现的缩写写法：中文（英文缩写），如"边界局域模（ELM）"；其后直接用缩写。
7. 语气：技术说明用陈述句，避免"我们可以"这类口语；操作步骤用动词开头的祈使句。

## 四、页首翻译提示块（翻译完成后删除）

翻译完成的页面必须**删掉**下列标记，否则会被同步脚本判定为未翻译：

```
<!-- untranslated-notice -->
<div class="warning" markdown="1">
**本页尚未翻译**……
</div>
```

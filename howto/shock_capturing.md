---
title: "使用激波捕捉功能"
nav_order: 5
parent: "数值方法与稳定化"
grand_parent: "使用指南"
layout: default
render_with_liquid: false
---

如何使用激波捕捉稳定化
----------------------------------------

如果在激波／间断面存在时出现数值振荡、进而导致数值稳定性问题，就应使用激波捕捉稳定化项。目前激波捕捉并未包含在 JOREK 的所有分支中，只有 model600 与 model750 包含。

该技术包括间断的检测，以及在间断附近、沿平行方向局部添加数值稳定化。激波检测基于压力梯度。

实际使用时，若激波捕捉格式开关 **use_sc** 设为 .true.，则在每个时间步通过用稳定化系数更新 visco_T、visco_par、D_perp、ZK_perp、Dn0 与 D_perp_imp 来加入稳定化。激波捕捉稳定化的强度可通过输入文件中的下列参数控制：

  * 黏性
    * visco_sc_num  
    * visco_par_sc_num
  * 扩散系数
    * D_par_sc_num     
    * D_perp_sc_num 
    * D_par_imp_sc_num
    * D_perp_imp_sc_num
  * 单温度
    * ZK_par_sc_num 
    * ZK_perp_sc_num
  * 双温度  
    * ZK_i_par_sc_num
    * ZK_i_perp_sc_num 
    * ZK_e_par_sc_num
    * ZK_e_perp_sc_num
  * 中性粒子
    * Dn_p_sc_num      
    * Dn_pol_sc_num
  * 杂质
    * D_par_imp_sc_num
    * D_perp_imp_sc_num 

默认情况下，上述参数均设为零。稳定化只能用于那些确实出现了激波／间断的选定 MHD 变量。通常对任一 MHD 变量，可在输入文件中将平行与垂直参数取相同值，例如 D_par_sc_num = 10、D_perp_sc_num = 10；这样的取值会各向同性地添加稳定化。若 10 仍不足，可尝试增大到 20，依此类推。对中性粒子密度方程，'Dn_p_sc_num' 与 'Dn_pol_sc_num' 分别控制 phi（平行）方向与极向平面内的稳定化。

可以将激波捕捉扩展到 visco_par_par 并一并引入 visco_par_par_sc_num。这一做法曾尝试过，但对所考虑的弹丸膨胀算例未见显著改善。

  * **add_sources_in_sc：**
在输入文件中将逻辑变量 'add_sources_in_sc' = .t. 可“升级”稳定化格式。该变量默认为 .false.。设 'add_sources_in_sc' = .t. 会增强源所在位置附近的稳定化强度。当源较强时可能需要这一处理。

  * **一个示例：**
以下是用于单温度、含杂质模拟的各向同性激波捕捉稳定化参数示例：

```
use_sc = .t. 
add_sources_in_sc = .t. 
visco_par_sc_num = 10 
visco_sc_num = 10 
D_par_sc_num = 10
D_perp_imp_sc_num = 10 
ZK_par_sc_num = 10 
ZK_perp_sc_num = 10 
D_par_imp_sc_num = 10 
D_perp_imp_sc_num = 10 
```


 ### 几点说明： 

1. 要在某个变量上添加“各向同性”稳定化，对应的平行与垂直参数应取相等值。建议从此简单而有效的“各向同性”格式开始。

2. 平行方向指磁场方向。若要使用“各向异性”稳定化（平行方向更强），令 par_sc_num 的取值高于 perp_sc_num，例如：ZK_par_sc_num = 100、ZK_perp_sc_num = 1。

3. 遗憾的是，设定激波捕捉参数的最优值需要一定的经验。就我在 full MHD 的 SPI 模拟中的经验，par_sc_num = perp_sc_num = 10 似乎是较好的参数选择。不过，对不同网格与问题，它们可以不同。

4. 请注意，激波捕捉稳定化格式不影响感应方程、电流方程与涡量方程，因此没有相应的数值参数。

细节请见 [shock_capturing.pdf](assets/shock_capturing/bv_stabilization.pdf)

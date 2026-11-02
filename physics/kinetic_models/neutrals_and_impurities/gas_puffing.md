---
title: "气体注入"
nav_order: 8
parent: "中性粒子与杂质"
layout: default
render_with_liquid: false
---

## 气体注入

气体注入系统分为两部分编写：先用 valve 对象在仿真域中指定位置，随后即可通过 puff\_ctrl 对象为各个 part\_group\_configs 从这些阀门注入气体。

### 设置阀门
阀门通过 namelist 中的 valves 对象定义。最多可指定 n\_valves\_max = 20 个阀门。每个阀门的选项为：

| valves(i)%           | 选项含义 |
|----------------------|----------------|
| type                 | 阀门类型的四字符代码。目前实现了极向圆形（'circ'）和极向 4 点多边形（'poly'）两种选项 |
| phi                  | 阀门的环向角（粒子将在此环向角处生成） |
| r\_valve              | 极向圆形阀门的半径（类型必须为 'circ'）|
| R\_valve\_loc          | 圆形阀门的 R 位置（类型必须为 'circ'） |
| Z\_valve\_loc          | 圆形阀门的 Z 位置（类型必须为 'circ'） |
| poly\_R               | 四边形阀门的 4 个 R 顶点（类型必须为 'poly'） |
| poly\_Z               | 四边形阀门的 4 个 Z 顶点（类型必须为 'poly'） |

若 valves%(i)%type='circ'，需要在极向平面上用 r\_valve、R\_valve\_loc、Z\_valve\_loc 定义一个圆形阀门。可以选择性地指定阀门所在的特定环向位置 phi（若不指定，则从此阀门注入的粒子将被置于随机的环向位置）。
若 valves%(i)%type='poly'，需要通过设置 poly\_R 和 poly\_Z（均恰好为 4 个点）来定义四边形阀门，其四个角点依次为：左上：(poly\_R(1),poly\_Z(1))，右上：(poly\_R(2),poly\_Z(2))，左下：(poly\_R(3),poly\_Z(3))，右下：(poly\_R(4),poly\_Z(4))。

### 设置阀门处的注入速率

在定义好阀门之后，每个中性粒子或杂质粒子组都可以通过设置相应的 part\_group\_configs(j)%puff\_ctrl(i) 对象，从每个阀门注入。这里 part\_group\_configs(j)%puff\_ctrl(i) 表示组分 j 对应于 valves(i) 的注入控制对象（因此，在 part\_group\_configs(j)%puff\_ctrl(1) 处设置注入速率，意味着从 valves(1) 指定的阀门注入粒子组 j）。每个 puff\_ctrl 对象的选项为：

| part\_group\_configs(j)%puff\_ctrl(i)% | 选项含义 |
|-------------------------------------|----------------|
| supers\_num\_puff                     | 每次注入动作初始化的新超粒子数 |
| supers\_weight\_puff                  | 每次注入动作初始化的新超粒子的目标权重（每个超粒子代表的真实粒子数） |
| supers\_ratio\_puff                   | 每次注入动作所使用的、分配给该组的超粒子总数（即 part\_group\_configs(i)%n\_particles）的比例 |
| times | 指定注入速率的时间检查点数组（SI 单位，秒）（要求已定义长度相同的 puff\_ctrl(i)%rates） |
| rates | 在给定时间检查点处指定的注入速率数组（原子/秒）（要求已定义长度相同的 puff\_ctrl(i)%times） |
| from\_file | ASCII 分段线性注入速率文件名，包含两列：时间（s），速率（原子/s） |

supers\_...\_puff 变量设定此阀门处每次注入动作将创建多少个超粒子，与其他粒子创建动作类似，例如 [等离子体–壁相互作用](../neutrals_and_impurities/particle_wall_interactions.md) 中所述的那些。三个 supers\_...\_puff 变量只能设置其中一个。若三者都不设置，则使用 supers\_ratio\_puff 方式，其默认值由 mod\_particle\_puffing.f90 中的 supers\_ratio\_puff\_default=$10^{-4}$ 设定

随时间变化的实际注入速率由分段线性函数设定。既可从 ASCII 文件指定（包含两列，第一列给出时间，最后一列给出对应时刻的速率）。这种情况下时间点数目不受限制，因此注入速率可具有任意时间分辨率。另一种方式，如果不需要超过 n\_puff\_segments\_max=20 个时间点，可直接从输入 namelist 指定注入速率。此时，在 "times" 中设置时间点，并在 "rates" 中设置对应的注入速率。无论哪种方式（namelist 或从文件读取），对于小于第一个定义时间的 t，都将使用第一个速率；而在最后一个指定时间点之后，将使用最后指定的速率。因此，若希望注入速率随时间恒定，只需设置 rates(1)=...、times(1)=0。

注意，单个粒子组可以从任意多或任意少的已指定阀门注入，并且可以分别控制每个阀门处的速率和创建方案。

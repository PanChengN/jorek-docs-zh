---
title: "particle wall_actions 介绍"
nav_order: 8
parent: "中性粒子与杂质"
layout: default
render_with_liquid: false
---

## particle wall\_actions 介绍

在壁面处，可能发生多种影响仿真中动理学粒子的事情。例如等离子体可能复合为中性粒子并同时溅射钨，动理学杂质种类可能中性化并以不同的速度重新进入计算域，钨也可能发生自溅射。在后端（位于 particles/mod\_particle\_wall\_interaction.f90）中，所有这些壁面处的相互作用都通过 wall\_action 对象处理，这些对象包含相互作用类型、源种类（进入壁面的是什么）以及目标种类（从壁面出来的是什么）的信息。每个 wall\_action 对象只处理一种相互作用，以保持代码的模块化。目前实现的 wall\_action %type 有："reflection"，处理中性粒子/杂质在壁面中性化并以不同能量（但权重相同）重新进入等离子体；"self sputter"，处理动理学壁面杂质的自溅射；"fluid sputter"，处理由等离子体造成的溅射；"wall recomb"，处理等离子体在壁面复合为动理学中性粒子；以及 "pump"，处理抽气面。目前所实现的类型聚焦于动理学中性粒子与杂质，但若其他类型的粒子需要边界条件，此框架可以扩展以包含它们（例如诊断来自 RE 的壁面负荷，或处理聚变 He 粒子的排出）。

为了给用户完全的自由度来选择仿真中使用哪些相互作用，wall\_actions 可以通过壁面作用配置对象（wall\_act\_configs）从 namelist 设置。一个种类在壁面处可以做多件事，因此可能需要对每个源种类通过其配置指定多个 wall\_actions。

对每个 wall\_act\_config 对象可指定以下选项：
| wall\_act\_configs(i)% | 选项含义 |
|----------------------|----------------|
| type                 | 上述类型之一（例如 "wall recomb"） |
| target\_group\_id      | 目标组的 %id（对 "self sputter" 这类自相互作用类型留空） |
| weight\_factor        | 可选因子，用于缩放结果权重，在较复杂的场景中有用 |
| only\_in\_polygon      | 若只想在由 poly\_R、poly\_Z 定义的多边形内执行此动作，设为 .true.（默认 .false.）|
| poly\_R               | 多边形的 R 坐标（仅当 only\_in\_polygon=.true. 时相关）。在 R,Z 平面内按顺序定义多边形（点 1 连到 2，再连到 3，依此类推） |
| poly\_Z               | 多边形的 Z 坐标（仅当 only\_in\_polygon=.true. 时相关） |
| nametag              | 可选，用于在输出文件中区分此 wall\_action 与类似的 wall\_action |
| supers\_num\_wall      | 设置所创建的超粒子数 |
| supers\_weight\_wall   | 设置每个所创建超粒子的权重 |
| supers\_ratio\_wall    | 设置此动作所创建的超粒子占该种类总数（%n\_particles）的比例 |

目前，only\_in\_polygon 仅对粒子相互作用（"reflection"、"self sputter" 和 "pump"）有效，并且很可能主要用于 "pump" 类型的 wall\_action。其工作方式是只选取那些在丢失时最后已知位置位于给定多边形内的粒子（在其离开计算域之前）。最后已知位置必须位于边界单元内（否则粒子被彻底丢失并会抛出错误），因此要捕捉所有到达你想选取的边界的粒子，务必把边界单元的厚度包含在多边形内。

将 nametag 选项设为一个可理解的多边形名称（例如 "outer\_target"），特别是当你在不同多边形中使用同一动作类型和同一目标的多个实例时（例如你有多个抽气面）。

supers\_...\_wall 选项至多只能设置一个，而且对于不产生超粒子的 %type（例如 "reflection" 或 "self sputter"），它们必须全部留空。若 %type 会创建粒子而未设置任何 super\_...\_wall，则默认为比率为 5.d-4 的 supers\_ratio\_wall 方案

要设置 MHD 流体与壁面的相互作用（它会创建动理学粒子），需要设置 fluid\_configs 对象。如果你运行的是简单等离子体，通常只需要 1 个 fluid\_config，但你可能希望在壁面处把单一 MHD 流体视为不同种类的组合（例如含痕量 N 的 D+T 等离子体）。对每个 fluid\_configs(i)（i=1,2,...）可指定以下选项：

| fluid\_configs(i)%   | 选项含义 |
|---------------------|----------------|
| Z                   | 该种类的原子序数（或 D 取 -2，T 取 -3）（此选项始终必需） |
| density\_fraction    | 该种类所代表的 MHD 流体密度的份额（fluid\_configs(:)%density\_fraction 之和必须为 1） |
| wall\_act\_configs(:) | 该种类对应的 wall\_action 配置 |

注意，若只指定一个种类，可以将 %density\_fraction 留空，因为它将被默认为 1。

在后端，所有 wall\_action 都将由这些 wall\_act\_configs 生成，并按类型和目标分组。自相互作用类型（如 "self sputter" 和 "reflection"）的 wall\_action 将在粒子推进器之后运行，而其他类型则在推进器之前运行，因为它们会生成新粒子。

如果你为同一种类在同一区域指定了多个 wall\_action（例如在全局 "self sputter" 动作之上叠加一个局部 "pump" 动作），则任何给定粒子撞到壁面时只会执行一种相互作用。"pump" 动作被硬编码为优先于 "self sputter" 和 "reflection"。例如，若你在同一区域同时设置了 "pump" 动作和 "self sputter" 动作（例如因为 "pump" 是带 only\_in\_polygon=.t. 的局部动作，而 "self sputter" 是默认的全局动作），则在该区域内只会发生 "pump" 动作。

更复杂的场景：避免指定其他重叠的动作（例如 2 个重叠的局部 "pump"，或重叠的 "reflection" 与 "self sputter"。它将会执行第一个适用的 "pump" 动作，否则执行你所指定的第一个适用的 "reflection" 或 "self sputter" 动作，但这一切远比直接确保多边形不重叠更令人困惑。对此没有检查。）。如果你出于某种原因想在所有地方抽气，唯独某个局部区域要 "reflection" 或 "self sputter"，那就为 "pump" 动作定义一个排除了你不想抽气那部分的多边形。

"fluid sputter" 类型按目标种类分组，并且该组使用第一个 "fluid sputter" 类型的创建方案，而不是用那个单独的溅射动作的方案，因为这意味着生成的 W 权重更均匀。（例如在含痕量 N 的 D 等离子体中；$D^+ \rightarrow W$ 流体溅射生成的 W 超粒子权重与 $N^+ \rightarrow W$ 流体溅射相同。）

你可以通过 `part_group_configs(i)wall_act_each_nstep_part` 指定粒子 wall\_action 的发生频率高于每个_流体_时间步一次（即每第 n 个_粒子_步一次）。当大部分粒子在单个流体时间步内撞到壁面时，这很有用。另见 [动理学时间推进](../timestepping.md)

### 展示该功能的实用示例

假设你想做带中性粒子的动理学粒子仿真，并希望中性粒子撞到壁面时从壁面反射。照常先指定你的中性粒子种类：

```fortran
part_group_configs(1)%id              = "D01"
part_group_configs(1)%Z               = -2
part_group_configs(1)%mass            = 2.01410178
part_group_configs(1)%coupling_scheme = 'ncs'
part_group_configs(1)%n_particles     = 1e4
part_group_configs(1)%type            = 'particle_kinetic_leapfrog'
```

源种类设置好后，即可为该种类设置壁面动作：

```fortran
part_group_configs(1)%wall_act_configs(1)%type = "reflection"
```

在后端，新速度由 Eckstein 公式确定，其系数必须在仿真文件夹中的文件里指定（对于 "reflection" 和 "wall recomb"，将依据这些系数判定是热脱附还是快反射。对于氘-氘反应，它会查找文件 y\_DD.dat 和 ye\_DD.dat，其示例可在 reg\_tests/testcases/particle\_imp\_xpoint\_600 中找到）。由于反射类型必然意味着目标种类就是源种类，因此无需显式指定目标种类；又因为此相互作用不产生新的超粒子，所以无需设置 supers\_...\_wall 选项。
 
如果你现在想要一个非完全饱和的壁面（或等效地在壁面处进行全局抽气），可以把 %weight\_factor 设为小于 1 的值，以模拟中性粒子被壁面部分吸收：

```fortran
part_group_configs(1)%wall_act_configs(1)%weight_factor=0.98d0
```

现在你可能还想模拟一个抽气管道。可以针对特定多边形（例如私有通量区中）设置一个 "pump" 动作，设置 weight\_factor < 1（这样抽气面的吸收系数为 1-weight\_factor；要获得真实的吸收系数，请参考 [Kukushkin et al. 2017](https://doi.org/10.1016/j.jnucmat.2007.01.094) 的式 2），并定义边界为抽气面的多边形（此例中即对角为 (R,Z)=(2.75,-1.4) 与 (3.2,-1.7) 的正方形内的所有部分）：

```fortran
  part_group_configs(1)%wall_act_configs(2)%type="pump"
  part_group_configs(1)%wall_act_configs(2)%weight_factor=0.7d0
  part_group_configs(1)%wall_act_configs(2)%only_in_polygon=.t.
  part_group_configs(1)%wall_act_configs(2)%poly_R= 2.75,3.2,3.2,2.75
  part_group_configs(1)%wall_act_configs(2)%poly_Z= -1.4,-1.4,-1.7,-1.7  
  part_group_configs(1)%wall_act_configs(2)%nametag="PFR"
```

好，在这样的设置下，所定义多边形内的抽气将以 (100%-70%=)30% 的吸收因子进行（因为 "pump" 动作优先于其他粒子粒子动作，且每个粒子只执行一个粒子粒子动作）。在多边形之外（其他所有地方），粒子将从壁面反射（热脱附或快反射），吸收为 (100%-98%=)2%，以模拟非完全饱和的壁面。

假设你的中性粒子在偏滤器区域占主导，因而也大量撞到壁面，那么你希望该粒子组的 wall_actions 发生频率高于每个_流体_时间步一次。如果是这样，可以设置壁面动作每 n 个整数_粒子_时间步执行一次（此例中为每 2 个粒子时间步）

```fortran
part_group_configs(1)wall_act_each_nstep_part  = 2
```

好，中性粒子部分就定了。现在假设你想研究硼化之后的第一炮等离子体，场景是钨偏滤器仍部分被硼覆盖，而你对这种情况下的钨输运感兴趣（我不知道为什么，但，随你）。于是你加入第二种动理学杂质种类——钨：

```fortran
part_group_configs(2)%id              = 'W01'
part_group_configs(2)%Z               = 74
part_group_configs(2)%mass            = 183.84
part_group_configs(2)%coupling_scheme = 'ics'
part_group_configs(2)%n_particles     = 1e4
part_group_configs(2)%type            = 'particle_kinetic_leapfrog'
```

假设壁面上有 20% B 和 80% W，并且你忽略进入等离子体的硼，那么你希望对硼使用 "reflection" 类型，而对钨使用 "self sputter" 类型。于是设置

```fortran
part_group_configs(2)%wall_act_configs(1)%type          = "reflection"
part_group_configs(2)%wall_act_configs(1)%weight_factor = 0.2d0
part_group_configs(2)%wall_act_configs(2)%type          = "self sputter"
part_group_configs(2)%wall_act_configs(2)%weight_factor = 0.8d0
```

好，粒子这一侧都已设置完毕，但现在你还需要指定 MHD 流体在壁面处应如何表现。假设你有一个含痕量氮（用于溅射）的氘等离子体。你希望氘在壁面复合为动理学中性氘，希望氘溅射钨，还希望氮溅射钨。于是设置流体配置及其壁面动作：

```fortran
fluid_configs(1)%Z                = -2
fluid_configs(1)%density_fraction = 0.99d0
fluid_configs(1)%wall_act_configs(1)%type               = "wall recomb"
fluid_configs(1)%wall_act_configs(1)%target_group_id    = "D01"
fluid_configs(1)%wall_act_configs(1)%supers_weight_wall = 1.d16

fluid_configs(1)%wall_act_configs(2)%type               = "fluid sputter"
fluid_configs(1)%wall_act_configs(2)%target_group_id    = "W01"
fluid_configs(1)%wall_act_configs(2)%weight_factor      = 0.8d0
fluid_configs(1)%wall_act_configs(2)%supers_num_wall    = 10

fluid_configs(2)%Z                = 7
fluid_configs(2)%density_fraction = 0.01d0
fluid_configs(2)%wall_act_configs(1)%type               = "fluid sputter"
fluid_configs(2)%wall_act_configs(1)%target_group_id    = "W01"
fluid_configs(2)%wall_act_configs(1)%weight_factor      = 0.8d0
```

注意 %supers\_num\_wall 只对第一个 "fluid sputter" 设置，因为它为那个向 "W01" 做 "fluid sputter" 的 wall\_action 组设定该参数。由于我们还有 20% 的硼，我们仍使用 80% 的 "fluid sputter"。在此示例中，壁面处和等离子体其余部分存在轻微的不一致，因为上述 fluid\_configs 只在壁面处被考虑。对于电离进入 MHD 等离子体的动理学中性氘，只有该电离权重的 99% 会在壁面处复合回氘（因为等离子体中氘的 density\_fraction 被设为 0.99d0）。你可以通过把 "wall recomb" 动作的 %weight\_factor 设为 1/0.99 = 1.010101010101d0 来补偿这种人为的粒子损失。本质上，这类不一致源于我们只有一个 MHD 流体，却又想在壁面处把这一单一种类分离为不同组分，因为痕量杂质对溅射非常重要。

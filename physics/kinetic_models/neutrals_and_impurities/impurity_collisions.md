---
title: "杂质碰撞"
nav_order: 8
parent: "中性粒子与杂质"
layout: default
render_with_liquid: false
---

# 杂质碰撞
目前，带电杂质可使用两类所谓的 Homma 碰撞算子与背景等离子体离子碰撞。
要使用这类杂质碰撞，需设置 `use_kin_bg_collisions=.t.` 并选择 `kin_bg_coll_type`，默认为 Homma 2020。

## Homma 2012
发表于 [*Y. Homma, 2012 JCP*]，以蒙特卡罗二元碰撞模型（BCM）[*T. Takizuka, H. Abe, 1977 JCP*] 为基础，并通过在温度梯度下从畸变 Maxwell 分布中选取背景等离子体离子速度，加入了热力的贡献。
要使用该算子，需设置 `kin_bg_coll_type=Homma2013`。

## Homma 2020
通过加入热流限制因子改进了先前的模型，因为用于采样热流的 Spitzer-Haerm 公式在低碰撞率区间已知会被高估 [*Y. Homma, 2020 Nucl. Fusion*]。

要使用该算子，需设置 `kin_bg_coll_type=Homma2020`。

热流限制因子可通过 `homma2020_alpha` 参数调节，默认并推荐取值为 1.5 [Fundamenski 2005]。

---
title: "已知问题"
nav_order: 7
parent: "动理学粒子模块"
layout: default
render_with_liquid: false
---

# 使用动理学粒子模拟时的已知问题
  * 段错误/内存错误：OpenMP 并行区中的私有数组存放在栈上，如果粒子数很多、网格很细和/或 ntor 很大，就很容易遇到内存问题。尝试通过在作业脚本中加入以下内容来增大栈大小：
    ```
    ulimit -s unlimited
    export OMP_STACKSIZE="500M"
    ```
    确切的栈大小因算例而异，这里设为 500 Mb，可以多试几个值。

    如果这没有帮助且仍然出现段错误，尝试把 feedback_rhs 从粒子演化 OMP do 循环的 reduction 子句中移除，将其声明为 shared，并在每次更新 feedback_rhs 时执行原子更新，例如：
    ```
    !$omp atomic update
    feedback_rhs() = ...
    ```
  * `particles` 出现在 `!$omp shared()` 列表中时，可能在某些编译器上引发问题。修复方法：`sim` 应放在 shared 列表中，而 particles 不应放进去。 
  * 内存泄漏。如果你的模拟在运行数小时后无缘无故停止，且错误文件中没有有用的错误信息，这可能是由内存泄漏引起的。（在 ITER SDCC 上使用 intel 编译器时，该信息例如只显示 `srun: error: 98dci4-clu-3098: task 6: Killed`。这通常发生在对 FE 矩阵做投影或分解之类操作的时候，因为那正是使用大量数据的时刻）。请就此展开讨论，以便我们尝试找到根源并为所有人解决。 
  * 计算速度：当 n_particles << 实际使用的粒子数时，未使用的粒子似乎仍会占用可观的机时（尤其当最大公约数很小（例如 gcd=1）时，见[动理学时间推进](./timestepping.md)），因此尽量避免把 part_group_configs(i)%n_particles 设得没必要地大

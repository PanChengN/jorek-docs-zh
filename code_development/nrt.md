---
title: "回归测试"
nav_order: 2
parent: "代码开发"
layout: default
render_with_liquid: false
---

# 回归测试
TODO：需依据 github 工作流更新。

***回归测试旨在发现意外引入代码的问题。** 回归测试确保：向仓库推送某次提交之后，所选的一组代码结果不发生变化。*

- **每次提交后，测试会在 ITER git 系统上自动运行** —— 见 [ITER Stash 系统](https://git.iter.org/projects/STAB/repos/jorek/branches)中的 "Builds" 列。这确保我们在某次提交"弄坏了代码"时能立即知晓。
- 如下文所述，在本地自行运行这些测试也很容易。

## 测试如何工作？

为缩短执行时间，代码通常**从模拟的非线性阶段重启，且只执行一个时间步**。这次短运行之后，将所得 `nodes%values` 与参考结果作绝对差比较。比较通过 HDF5 工具完成。此外还存在其他类型的测试用例（例如自由边界平衡）。

- `run_test.sh` 脚本可用于运行测试用例。
- 若测试成功，脚本返回错误码 0，否则返回非零值（通常退出状态为 1）。该返回码告知 ITER 平台上的 "Bamboo" 软件某个测试未成功。
- 另外，在输出末尾可看到类似 `Test 'tearing_circ_303' passed.` 的一行。该信息便于用户判断测试是否成功。

## 用户如何运行测试？

### 准备步骤

使用 JOREK 需要常规的准备工作：

- 从 github/ITER git 仓库获取代码（见[此处](../howto/first_steps)）
- 为所用机器创建 Makefile.inc 文件。示例见 Make.inc/ 目录（另见[编译](../compiling/cat_compiling)）
- 加载所需模块，例如 `module load intel impi fftw hdf5`。某些机器已备好相应脚本，例如 Helios：`source reg_tests/job_scripts/helios/env.sh`
- **把 HDF5 依赖库所在目录加入你的 Makefile.inc（见 [HDF5-Tools](../numerics/hdf5tools.md)）**

最后需要获取运行回归测试所需的数据：

- 获取测试所需的重启文件：`reg_tests/get_all_data.sh`。若所用机器无法访问 ITER git 仓库和/或无法直连 jorek.eu，请[按这些说明操作](nrt-preparation-with-rsync)。

### 交互式运行单个测试用例

- 注意 **`reg_tests/run_test.sh -h`** 会打印可用命令行选项列表。
- 列出全部可用测试用例（名称加简短说明）：

    ```
    reg_tests/run_test.sh -l
    ```

- 若你有可交互运行 mpi 作业的机器，用以下命令运行一个测试用例即可（会进行编译＋执行）：

    ```
    reg_tests/run_test.sh -j 8 tear_circ_303
    ```

- 也可以把编译与执行拆成两条命令：

    ```
    reg_tests/run_test.sh -p -j 8 tear_circ_303  # compile the binaries required
    reg_tests/run_test.sh -n tear_circ_303       # run without compiling
    ```

### 通过作业脚本运行单个测试用例

- 为该测试用例编译 jorek 可执行文件（-p 标志表示不运行模拟，只执行编译）：

    ```
    reg_tests/run_test.sh -p -j 8 tear_circ_303
    ```

- 把以下命令写入作业脚本并提交

    ```
    reg_tests/run_test.sh -k -n tear_circ_303
    ```

- 对某些机器，`reg_tests/job_scripts` 中已备好批处理脚本

### 一次执行多个测试用例

- 可用以下命令一次执行全部测试用例

    ```
    cd reg_tests
    compile_all.sh
    run_all.sh
    ```

- 可通过以下命令把全部测试用例作为批处理作业提交

    ```
    cd reg_tests
    compile_all.sh
    launch_all.sh
    ```

- 注意，`launch_all.sh` 脚本需要设置环境变量，例如 `export JOREK_HOST=helios` 与 `export BATCHCOMMAND=sbatch`。也可等价地 source 下列文件：reg_tests/job_scripts/helios/env.sh

## 如何创建新的测试用例？

- 在 `reg_tests/testcases` 中创建目录，例如 `verynew_333`
- 把名为 `input` 的输入文件放入 `reg_tests/testcases/verynew_333`
- （从另一个已有测试用例）复制 `settings.sh` 到 `verynew_333`，并按需要修改
- 启动首次运行，生成 `begin.h5` 与 `end.h5` 文件

    ```
    reg_tests/run test.sh -i verynew_333
    ```

- 把重启文件（`begin.h5` 与 `end.h5`）发送到 jorek.eu 上的 web store。确实，参考重启文件存放在网站 `http://jorek.eu/dav_nrt` 上，以免 git 仓库变得过大。

    ```
    cd reg_tests/testcases/
    ./send_testcase_data.sh verynew_333
    cd -
    ```

- 注意，某些算例不仅需把 `begin.h5` 与 `end.h5` 发送到 jorek.eu 存储，还需附加文件（例如自由边界算例的 STARWALL 响应，或 RMP 场文件）
- 至此完成。你也可以把 verynew_333 加入 git 仓库以分享该测试：

    ```
    cd reg_tests/testcases/
    rm verynew_333/*.h5 verynew_333/*.tar* verynew_333/jorek_model*
    git add verynew_333
    # note, you may need to add more files depending on the case!
    git commit -m "Adding the verynew_333 test case"
    git push
    ```

## 非回归脚本如何工作？

执行 `jorek/reg_tests/run_test.sh -k tear_circ_199` 时，脚本做了什么？

- 编译。生成三个可执行文件并存入 `reg_tests/testcases/tear_circ_199`：

    ```
    jorek_model199_3, rst_bin2hdf5, rst_hdf52bin
    ```

- 创建用于运行测试的目录，然后把所需文件复制到该目录。临时目录名示例：`reg_tests/tmp13027`
- 进入该临时目录运行测试
- 把参考 HDF5 文件 `begin.h5` 转换为 `jorek_restart.rst`
- 启动存放在 `reg_tests/testcases/tear_circ_199/settings.sh` 中的场景
- 把末态 `jorek_restart.rst` 转换为 `jorek_restart.h5`
- 把末态 `jorek restart.h5` 与参考文件 `end.h5` 比较，若一切正常则打印 `Test passed`

## 如何更新测试用例？

例如在 bug 修复之后，代码结果发生变化，测试用例可能需要更新：

- 用 `-i` 选项从头启动该测试用例（即不从 `begin.h5` 重启）

    ```
    reg_tests/run_test.sh -i tear_circ_199
    ```

- 若成功，`begin.h5` 与 `end.h5` 会存入 `reg_tests/testcases/tear_circ_199`，覆盖旧文件
- 随后需用以下命令更新网站 `http://jorek.eu/dav_nrt` 上的重启文件

    ```
    cd reg_tests/testcases/
    ./send_testcase_data.sh tear_circ_199
    cd -
    ```

- 然后，执行完之后，测试目录中的 `.version` 文件将包含该测试最新的版本名。需把它提交并推送到 git 服务器，否则 ITER 上的测试不会知道你最新的版本，例如：

    ```
    git add reg_tests/testcases/tear_circ_303/.version
    git commit -m "Updating regression test tear_circ_303 due to changes XYZ."
    git push
    ```

- `reg_tests/job_scripts/` 中存放了一组可在超级计算机上使用的作业脚本。这有助于你运行完整算例以更新重启文件。

## 如何刷新本地存放的重启文件？

取回新文件之前，需先删除旧文件。命令为：

```
reg_tests/cleanup.sh
reg_tests/get_all_data.sh
```

## 自动化非回归测试

- 测试在 ITER 平台上的 "Bamboo" 中运行，见[此处](https://ci.iter.org/browse/STAB-JOREK)

---
title: "用 rsync 准备 NRT"
parent: "回归测试"
layout: default
render_with_liquid: false
---

# 当所用机器无法访问 ITER git 仓库与 jorek.eu 时如何准备 nrt 测试

- 在一台可对外建立 ssh 连接的机器上，用 git 从仓库获取代码

    ```
    $ git clone ssh://git.iter.org/stab/jorek.git jorek_git
    $ git checkout nrt
    ```

- 从 jorek.eu 网站下载参考测试用例（重启文件）

    ```
    $ jorek_git/non_regression_tests/get_all_data.sh
    ```

- 把该目录传输到用于测试的机器上（示例：Helios）

    ```
    $ rsync -av --progress jorek_git USER@helios.iferc-csc.org:
    $ ssh USER@helios.iferc-csc.org
    $ cd jorek_git
    ```

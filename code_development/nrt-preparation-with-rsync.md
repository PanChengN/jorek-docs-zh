---
title: "用 rsync 准备 NRT"
parent: "回归测试"
layout: default
render_with_liquid: false
---

<!-- untranslated-notice -->
<div class="warning" markdown="1">
**本页尚未翻译**，以下为 JOREK 官方英文原文。

原文页面：[NRT preparation with rsync](https://iterorganization.github.io/JOREK/code_development/nrt-preparation-with-rsync.html)　·　源文件：`code_development/nrt-preparation-with-rsync.md`
</div>

# Preparation of the nrt tests in case the machine you are using does not have access to the ITER git repository and to jorek.eu

- Get the code from the repository with git on a machine where outward ssh connection is available

    ```
    $ git clone ssh://git.iter.org/stab/jorek.git jorek_git
    $ git checkout nrt
    ```

- Download the reference test cases (restart files) from the jorek.eu web site 

    ```
    $ jorek_git/non_regression_tests/get_all_data.sh
    ```

- Transfer the directory to the machine you are using for the tests (example: Helios)

    ```
    $ rsync -av --progress jorek_git USER@helios.iferc-csc.org:
    $ ssh USER@helios.iferc-csc.org
    $ cd jorek_git
    ```

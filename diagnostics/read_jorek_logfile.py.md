---
title: "扫描 JOREK 日志中的特定变量值"
nav_order: 17
render_with_liquid: false
parent: "Running JOREK"
---

<!-- untranslated-notice -->
<div class="warning" markdown="1">
**本页尚未翻译**，以下为 JOREK 官方英文原文。

原文页面：[Scan JOREK logfile for a specific variable value](https://iterorganization.github.io/JOREK/diagnostics/read_jorek_logfile.py.html)　·　源文件：`diagnostics/read_jorek_logfile.py.md`
</div>

#### Scan JOREK logfile for a specific variable value
Usage:
```
read_jorek_logfile.py -fname <logfile_name> -text <variable_name>
```
Optional arguments:
```
  -h, --help    show this help message and exit
  -fname FNAME  input file name
  -text TEXT    string to find
  -sum          Sum of entries
  -n N          max number of entries
```

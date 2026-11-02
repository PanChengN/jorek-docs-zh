---
title: "扫描 JOREK 日志中的特定变量值"
nav_order: 17
render_with_liquid: false
parent: "Running JOREK"
---

#### 在 JOREK 日志文件中扫描特定变量的值
用法：
```
read_jorek_logfile.py -fname <logfile_name> -text <variable_name>
```
可选参数：
```
  -h, --help    show this help message and exit
  -fname FNAME  input file name
  -text TEXT    string to find
  -sum          Sum of entries
  -n N          max number of entries
```

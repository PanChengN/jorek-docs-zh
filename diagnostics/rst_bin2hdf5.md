---
title: "rst_bin2hdf5"
nav_order: 19
render_with_liquid: false
parent: "Running JOREK"
---

## rst_bin2hdf5
- 另见 [hdf5-tools](hdf5-tools.md)

该工具用于把 jorek00XXX.rst 文件转换为 hdf5 格式。
第一个参数是要转换的文件。若未给出参数，则使用 jorek_restart.rst。
用法示例：

  rst_bin2hdf5 jorek00001.rst

其他选项：

  ```
  rst_bin2hdf5 -v --verbose
  rst_bin2hdf5 -h --help
  ```

##### 编译 {#compiling}
编译此工具时，在 `Makefile.inc` 中加入 `USE_HDF5 = 1`，并加入下列各行，告知链接器依赖库所在位置。（`$H5DIR` 是已有的环境变量）

  ```
  #HDF5
  HDF5LIB = -L$(H5DIR)/lib/ -lhdf5_fortran -lhdf5hl_fortran -lhdf5 -lhdf5_hl
  HDF5INCLUDE = $(H5DIR)/include
  ```

## rst_hdf52bin {#rst_hdf52bin}
该工具执行与上述过程相反的操作。

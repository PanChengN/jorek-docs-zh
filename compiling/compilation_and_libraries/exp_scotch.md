---
title: "SCOTCH 配置示例"
nav_order: 8
parent: "编译与依赖库"
grand_parent: "编译与运行"
layout: default
render_with_liquid: false
---

<!-- untranslated-notice -->
<div class="warning" markdown="1">
**本页尚未翻译**，以下为 JOREK 官方英文原文。

原文页面：[Example SCOTCH Configuration](https://iterorganization.github.io/JOREK/compiling/compilation_and_libraries/exp_scotch.html)　·　源文件：`compiling/compilation_and_libraries/exp_scotch.md`
</div>

# Example configuration file for Scotch 5.1.12b

```make
EXE		=
LIB		= .a
OBJ		= .o

MAKE		= make
AR		= ar
ARFLAGS		= -ruv
CAT		= cat
CCS		= icc
CCP		= mpicc -cc=icc
CCD		= icc
CFLAGS		= -O3 -DCOMMON_FILE_COMPRESS_GZ -DCOMMON_PTHREAD -DCOMMON_RANDOM_FIXED_SEED -DSCOTCH_RENAME -DSCOTCH_RENAME_PARSER -DSCOTCH_PTHREAD -restrict -DIDXSIZE64 -DINTSIZE32
CLIBFLAGS	=
LDFLAGS		= -g -lz -lm -lrt -I${I_MPI_ROOT}/intel64/include
CP		= cp
LEX		= flex -Pscotchyy -olex.yy.c
LN		= ln
MKDIR		= mkdir
MV		= mv
RANLIB		= ranlib
YACC		= bison -pscotchyy -y -b y
```

Note: it may be necessary to alter `LDFLAGS` to include `-lpthread`, see Scotch bugtracker [#15048](https://gforge.inria.fr/tracker/?func=detail&atid=1079&aid=15048&group_id=248).

Set `prefix` to install in a non-standard path here.

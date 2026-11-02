---
title: "SCOTCH 配置示例"
nav_order: 8
parent: "编译与依赖库"
grand_parent: "编译与运行"
layout: default
render_with_liquid: false
---

# Scotch 5.1.12b 的配置示例文件

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

注意：可能需修改 `LDFLAGS` 以包含 `-lpthread`，见 Scotch 问题跟踪系统 [#15048](https://gforge.inria.fr/tracker/?func=detail&atid=1079&aid=15048&group_id=248)。

若要安装到非标准路径，在此设置 `prefix`。

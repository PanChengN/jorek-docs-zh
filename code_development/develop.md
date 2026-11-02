---
title: "编码规范"
nav_order: 1
parent: "代码开发"
layout: default
render_with_liquid: false
---

# 编码规范 {#coding-guidelines}
- 另见下文[**提交规范**](#committing-guidelines)
- 另见 [**Matthias 的概览幻灯片**](assets/develop/2021-10-mhoelzl-development-workflow.pdf)

## 源代码应遵循的形式

- **implicit none 语句：**
  - 每个子程序或模块都必须有 "implicit none" 语句。

- **外部函数**
  - 推荐使用模块。若确实要使用外部函数，务必设置 `real*8, external :: funcname`，使依赖关系生成能正常工作。这种情况下建议显式声明接口

- **命名**：
  - 子程序、函数或变量请尽量使用自明其义的名称。
  - 文件名与文件中要在文件外部使用的程序单元名请保持一致（区分大小写，由此可知每个文件应只含一个这样的程序单元）。
    - 构建系统要求程序单元（模块、子程序、函数、程序）名与文件名相同。
    - 只有当文件名与程序单元名相同时，依赖关系才能被正确解析。

- **缩进**：
  - 在每个程序、例程、函数、if 子句、for 循环等内部，使用**两个空格的缩进**
  - 请使用空格，**不要使用制表符**（Makefile 当然除外）

- **对齐**：
  - 结构相似的若干命令请按更易读的方式对齐，例如对齐 "=" 号。

- **注释**：
  - 注释应放在代码不能自明之处
  - 尤其应在每个子程序开头写一条注释说明其用途
  - 对不自明的输入／输出参数，请逐一说明
  - 对相互关联的命令块以及较长的循环，简短说明往往非常有用。这类块之间可用空行分隔，以提高代码可读性
  - 若某种实现在某些情况下不工作，请以注释形式给出警告。
  - 请遵循下面给出的注释形式

- **长行**：
  - 超过 132 字符的行应拆成多行：在第一行末尾加 "&" 号，在下一行以额外两个空格缩进续写该语句。若有助于提高可读性，提前断行也有用。

- **intent 声明**：
  - 请将子程序或函数的每个参数各占一行，指明该参数是输入参数（`"intent(in)"`）、输出参数（`"intent(out)"`）还是两者兼有（`"intent(inout)"`），并以注释补充说明
  - 若输入参数确实自明，可把其中若干项放在同一行且不加注释

- **明确的 end 语句**：
  - 每个 `end` 语句应尽可能精确："end do"、"end if"、"end subroutine test"、……
  - 较长的循环或 if 子句应给出明确、唯一且可读的名称：

```fortran
loop_over_nodes:do i = 1, n_nodes
  ... ! Lots of code inside this loop
end do loop_over_nodes
```

- **打开文件**：
  - 每个 `open` 语句都应包含 `action` 与 `status` 参数。通常 `status` 取值为 "old"（已存在文件）、"new"（新建文件）或 "replace"（覆盖文件）。`action` 可取 "read"、"write" 与 "readwrite"。单位号选择建议使用 "newunit="。

### 示例：

```fortran
  !> Put a short description for the routine in a single line.
  !! 
  !! If necessary, you can add a detailed explanation running over several lines
  !! like this.
  !! *** WARNING*** Please put a warning in case the routine does not work under certain conditions.
  subroutine print_grid_info(element_list, node_list, verbose)
    
    implicit none
    
    ! --- Routine parameters
    type(type_element_list), intent(in) :: element_list
    type(type_node_list),    intent(in) :: node_list
    logical,                 intent(in) :: verbose       !< Describe routine parameters if necessary
    
    ! --- Local variables
    type(type_node) :: node_i
    integer         :: i, j
    
    ! --- Print information about the grid nodes.
    do i = 1, node_list%n_nodes
      node_i = node_list%node(i)
      write(*,*) '...'
      if ( verbose ) then
        write(*,*) '...'
      end if
    end do ! (i = 1, node_list%n_nodes)
    ! in case of long loops, a comment might be useful to indicate which loop ends here
    
    ! --- Print information about the grid elements.
    write(*,*) '...'
    do j = 1, element_list%n_elements
      write(*,*) '...'
    end do
    
    write(*,*) element_list%n_elements, element_list%n_elements, element_list%n_elements,              &
      element_list%n_elements ! Line split after 100 characters and continued with extra indentation
    
  end subroutine print_grid_info
```


# 提交规范 {#committing-guidelines}
TODO：需依据 github 工作流更新。
- 另见上文[**编码规范**](#coding-guidelines)

- 全面介绍见 Simon Pinches 编写的 [ITER 开发指南](https://portal.iter.org/departments/POP/CM/IMAS/IM%20Development%20Guide.docx)
- [Guido 的幻灯片（2016-04）](assets/develop//huijsmans_jorek_general_meeting_2016.pdf)
- [Matthias 的幻灯片（2020-04）](assets/develop/2020-04-mhoelzl-development-coordination.pdf)，其中列出一些反复出现的问题与建议的解决办法

## 正确设置 git

***这是重要的一步！*** 开始使用 GIT 时务必不要跳过。[ITER 开发指南](https://portal.iter.org/departments/POP/CM/IMAS/IM%20Development%20Guide.docx)第 5.1 节对此有清楚的说明。

## 不同类型的分支

- `feature/<name>` —— 用于新功能开发
- `bugfix/<name>` —— 用于修复代码中的问题

## 如何提交一个小 bugfix

- **在 [Stash 中](https://git.iter.org/projects/STAB/repos/jorek/branches)创建 bugfix 分支**
  - 在下拉菜单中选择基线分支（通常为 `develop`）
  - 点击该下拉菜单旁的 '...'，选择 "Create branch from here"
- **在本地检出该分支**
  - `git checkout bugfix/<name>`
- **实施修改、测试并提交**
  - `git add <list of modified files>`
  - `git commit`
- **将提交推送到中心仓库**
  - `git push origin`
- **从 `bugfix/<name>` 分支向 `develop` 发起合并请求（pull request）**
  - 在 [Stash 中](https://git.iter.org/projects/STAB/repos/jorek/branches)的下拉菜单里选择分支 `develop`
  - 点击你的 `bugfix/<name>` 分支
  - 点击 "Create Pull Request"
  - 为你的修改选择合适的评审人
  - 注意：只有当你的分支通过自动回归测试后，发起合并请求才有意义。
- **若该 bugfix 影响人数较多，请通过我们的[邮件列表](mailto:everyone@jorek.eu)通报**

## 如何开展较大的代码修改

- 做法与 bugfix 基本相同。
- 但此类开发通常耗时更长，因此不时把 `develop` 中的修改合并到你的 `feature/<name>` 分支会很有用，以便跟踪变更。
- 务必为你的开发新增[回归测试](nrt)。
- 在向 develop 发起合并请求之前，务必先把 develop 的全部变更合并到你的 feature 分支。
- 务必为你的合并请求选择两位评审人。

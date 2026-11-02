---
title: "开发流程"
nav_order: 1
parent: "代码开发"
layout: default
render_with_liquid: false
---

# 主开发流程

## 提交规范 {#committing-guidelines}
- 另见[**编码规范**](develop#coding-guidelines)

<!--- - [Slides by Guido (2016-04)](assets/develop//huijsmans_jorek_general_meeting_2016.pdf)
- [Slides by Matthias (2020-04)](assets/develop/2020-04-mhoelzl-development-coordination.pdf) with some issues coming up regularly and suggested solutions --->


## 仓库结构
- [主仓库](https://github.com/iterorganization/JOREK)是公开的，作为 JOREK 的中心代码源。
- 开发者各自创建主仓库的 fork，用于个人的开发工作。
- 可把协作者加入 fork，以便针对特定功能或 bug 修复开展团队协作。
- **fork 中的开发成果需尽快合并回主仓库**。

---

## 配置工作流 {#setting-up-the-workflow}
1. **创建 github 账号**
    - 若尚无账号，请创建 github 账号，并确保用户名包含你的姓与名首字母。

2. **fork 主仓库**：
   - 若还没有 fork，请在你的用户账号下新建一个。
   - 打开 [GitHub 上的主仓库](https://github.com/iterorganization/JOREK.git)。
   - 点击 "Fork" 按钮，在你的 GitHub 账号下创建该仓库的个人副本。
   - 若与他人紧密协作，可把协作者加入你的 fork。

3. **克隆你的 fork**：
   - 把 fork 克隆到本地机器：

```bash
     git clone https://github.com/<your-username>/<repository-name>.git
     cd <repository-name>
```

4. **配置文档**：
   - 开发过程中你会为文档做贡献。可在*你的 fork 中*把 'Settings'->'Pages'->'Source' 设为 'GitHub Actions'，
   以预览文档在主仓库中的呈现效果。
   不过为加快迭代，建议在本地构建文档。
   相关说明见[文档配置指南](/docs/contributing.md)。

5. **把主仓库设为上游远端**：
   - 将主仓库添加为 upstream 远端，以保持 fork 同步：

```bash
     git remote add upstream https://github.com/iterorganization/JOREK.git
```

6. **把 fork 与主仓库同步**：
   - 定期抓取并合并主仓库的变更：

```bash
     git fetch upstream
     git merge upstream/develop
```


## 开发与 bug 修复

1. **开发功能或修复 bug**：
   - 为每个功能或 bug 修复新建分支：

```bash
     git checkout -b <feature|bugfix>/branch-name
```

   - 把修改提交到该分支：

```bash
     git add .
     git commit -m "Description of changes"
```

2. **把变更推送到你的 fork**：
   - 将分支推送到你的 fork：

```bash
     git push origin <feature-or-bugfix-branch>
```

3. **创建合并请求**：
   - 从你的 fork 分支向主仓库的 `develop` 分支发起合并请求（PR）。
       - 在你的 fork 仓库主页上会出现一个 "Contribute" 按钮
       - 点击该按钮，然后选择 "Open Pull Request"
       - 填写合并请求表单，以整个社区都能理解的方式描述该合并请求
   - 解决可能存在的合并冲突，并确认自动回归测试通过。
   - 确保合并前该 PR 已至少由两人评审并批准。


## 最佳实践
- 经常把主仓库的变更合并到你的 fork，以避免大型合并冲突。这对长期开发尤为重要
- 功能分支与 bug 修复分支应保持小而聚焦。
- 确保所有变更在合并进主仓库前都已评审（至少 2 人）。
- 务必为你的开发新增[回归测试](nrt)。
- bug 修复应与功能开发独立进行。
- 主仓库中的 bug 修复一旦可用，就尽快合并到你的 fork：

```bash
    git fetch upstream
    git merge upstream/develop
```

## 使用 GitHub 问题跟踪器
使用 [GitHub 问题跟踪器](https://github.com/iterorganization/JOREK/issues)提出重要的 bug 修复、新开发讨论或功能请求。

1. **创建问题（Issue）**：
  - 提供清晰简洁的标题与描述。
  - 包含相关细节，例如复现 bug 的步骤、预期行为，或新功能的动机。
  - 用 `@username` 提及特定用户，使其了解该问题。
  - 使用合适的标签（如 `bug`、`enhancement`、`discussion`）对问题分类。

2. **关联合并请求**：
  - 在合并请求中用 `Fixes #<issue-number>` 这类关键词引用问题，以便 PR 合并时自动关闭该问题。
  - 关闭前确保问题已解决、所有讨论已回应。
  - 关于[把问题关联到 PR](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)的更多信息见此




## 迁移到 GitHub
迁移到 GitHub 的过程中，提交哈希的历史会改变。请按以下步骤确保平稳过渡：

1. **迁移前推送你的分支（7 月底）**：
   - 迁移之前，把所有本地分支推送到当前仓库：

```bash
     git push origin <branch-name>
```

2. **迁移后取回你的分支**：
   - 迁移之后，请联系 **jorek-devel@jorek.eu**，从迁移期间保存旧分支的私有 GitHub 仓库中取回你的新分支，**请在邮件中附上你的 GitHub 用户名**。

3. **用旧分支配置你的 fork**：
   - 确保已按[配置工作流](#setting-up-the-workflow)中的步骤操作

   - 克隆新主仓库的你的 fork：

```bash
     git clone git@github.com:<your-username>/<fork-repo>.git
     cd <fork-repo>
```

   - 把（包含旧分支的）私有仓库添加为远端：

```bash
     git remote add old-repo git@github.com:N-Schwarz/jorek-backup.git
```

   - 抓取你的旧分支：

```bash
     git fetch old-repo <branch-name>
```

   - 基于旧分支在你的 fork 中创建分支：

```bash
     git checkout -b <branch-name> old-repo/<branch-name>
```

   - 把该分支推送到你的 fork：

```bash
     git push -u origin <branch-name>
```

  - 可能需要用以下命令让该分支跟踪你的 fork

```bash             
     git branch feature/m600refluid  -u origin/feature/m600refluid
```

   旧分支与公开仓库共享同一历史，因此提交仍附着在原来的位置：没有内容被重写，
   也不需要解决冲突。

---


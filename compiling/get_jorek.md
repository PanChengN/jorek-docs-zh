---
title: "获取源代码"
nav_order: 1
parent: "编译与运行"
layout: default
render_with_liquid: false
---

# 获取 JOREK 源代码

JOREK 是开源软件，其公开仓库托管在 GitHub 上：

<https://github.com/iterorganization/JOREK>

## 使用 SSH 克隆

如果你已为 GitHub 账号添加 SSH 密钥，并计划向 fork 推送改动，请使用 SSH。有关配置 SSH 密钥的方法，参见 GitHub 的[使用 SSH 连接 GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)指南：

```bash
git clone git@github.com:iterorganization/JOREK.git
cd JOREK
```

主开发分支为 `develop`。注意所有开发工作都必须在 fork 中进行，更多信息见下方链接。

## 贡献代码与问题反馈

- 通过 [GitHub Issues](https://github.com/iterorganization/JOREK/issues) 报告问题或提出改进建议。
- 贡献代码前请先阅读[开发工作流程](../code_development/development_workflow.md)。
- JOREK 依据 [GNU Lesser General Public License Version 3](../code_license.md) 分发。

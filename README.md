# JOREK 中文文档

[JOREK](https://www.jorek.eu/) 非线性扩展 MHD 代码文档的中文译本，**仅供学习与技术交流**。

**[📖 在线阅读](https://panchengn.github.io/jorek-docs-zh/)**

- 英文原站：<https://iterorganization.github.io/JOREK/>
- 上游仓库：<https://github.com/iterorganization/JOREK>

> **非官方社区译本。** 本站与 JOREK 团队无关，不用于任何商业目的。技术内容以[英文原站](https://iterorganization.github.io/JOREK/)为准；发现译文错误请在本仓库提 Issue，不要以此向 JOREK 团队提问。原文版权归 JOREK 团队所有，遵循 LGPL-3.0。

## 特点

- **213 页全站中文**，覆盖编译运行、使用指南、物理模型、数值方法、诊断后处理、装置配置
- **版式与英文原站完全一致**：主题、配色（含深浅色切换）、页头页脚、图标全部直接沿用官方原始文件，未作重写；目录结构与页面 URL 与英文站逐页对应
- **技术内容不做改写**：命令、namelist 参数、数学公式、文件路径一律保留原文，只翻译说明文字

## 本地预览

```bash
bundle install
bundle exec jekyll serve     # http://127.0.0.1:4000/jorek-docs-zh/
```

需要 Ruby ≥ 3.1。

## 版权与许可

本站是上游文档的**中文译本（衍生作品）**。原作品以 LGPL-3.0 发布，因此依其条款，**本站整体同样以 GNU Lesser General Public License v3.0 发布**——不得改用与之不兼容的许可。

| 文件 | 作用 |
|---|---|
| [`COPYING.LESSER`](COPYING.LESSER) | LGPL-3.0 全文 |
| [`COPYING`](COPYING) | LGPL-3.0 引用的 GPL-3.0 全文 |
| [`NOTICE.md`](NOTICE.md) | 原文版权归属、修改声明（LGPL-3.0 §5）、非官方声明、商标与引用要求 |
| [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) | 第三方组件许可声明 |
| [`CITATION.cff`](CITATION.cff) | 原作者与推荐引用信息 |

**原文版权归 JOREK 开发团队所有。** 本站未经 JOREK 团队审阅或认可。

若在论文等成果中使用 JOREK，请遵循官方[发表规则](https://iterorganization.github.io/JOREK/publication_rules.html)并引用 `CITATION.cff` 所列文献；引用本站译文不能替代引用原作品。

## 说明

- 本仓库只包含站点本身（页面、图片、样式、配置与许可证）。上游同步、翻译校验等维护脚本不随仓库发布。
- 译文与上游英文站逐页对应；因上游文档自身缺陷导致的占位页、失效链接、缺失图片均按原样保留，未擅自改写。
- 若发现译文错误，欢迎提 Issue。

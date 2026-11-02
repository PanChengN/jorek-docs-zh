# JOREK 中文文档

[JOREK](https://www.jorek.eu/) 非线性扩展 MHD 代码官方 Wiki 的中文版。

- 英文原站：<https://iterorganization.github.io/JOREK/>
- 源码仓库：<https://github.com/iterorganization/JOREK>

> **非官方翻译。** 本站由社区翻译维护，与 JOREK 团队无关。技术内容以[英文原站](https://iterorganization.github.io/JOREK/)为准；发现译文错误请提 Issue，不要以此向 JOREK 团队提问。原文版权归 JOREK 团队所有，遵循 LGPL-3.0。

## 设计原则

**版式与英文原站完全一致，只有语言不同。**

- 主题、配色（`jorek_light` / `gruvbox_dark` 双配色与运行时切换）、页头页脚、图标、logo、CSS/JS **全部直接沿用官方仓库的原始文件**，未做任何重写；
- 目录结构、导航层级、页面 URL 与英文站逐页对应（`compiling/get_jorek.html` ↔ 中文站同名路径）；
- 每个页面保留官方 front matter 全字段（`nav_order`、`parent`、`has_children` 等），只把 `title` / `parent` / `grand_parent` 换成中文。

## 目录

```
.
├── _config.yml          # 由官方 _config.yml 派生，仅改站点标识与主题加载方式
├── _includes/           # 官方原文件（页头、深浅色切换）
├── _sass/               # 官方原文件（自定义配色）
├── assets/              # 官方原文件（logo、CSS 入口）
├── index.md             # 以下为 213 个文档页，路径与官方 Wiki 一一对应
├── compiling/  howto/  physics/  numerics/  diagnostics/  machines/ …
├── i18n/
│   ├── titles.yml       # 英文标题 → 中文标题映射（导航层级依赖它）
│   └── glossary.md      # 术语表（翻译必须遵守）
└── tools/
    └── sync_upstream.py # 从上游 Wiki 同步结构、素材与新增页面
```

## 本地构建

需要 Ruby ≥ 3.1。

```bash
bundle install
bundle exec jekyll serve          # http://127.0.0.1:4000/jorek-docs-zh/
```

仅生成静态文件：

```bash
bundle exec jekyll build          # 输出到 _site/
```

## 与上游同步

上游新增或修改页面时：

```bash
python3 tools/sync_upstream.py --init   # 补齐缺失页面、刷新素材
python3 tools/sync_upstream.py --report # 查看翻译进度与缺中文标题的页面
```

同步脚本**不会覆盖已有译文**：已存在的页面一律跳过。新增页面会带着官方英文正文落盘，并在页首标注"本页尚未翻译"。

## 翻译状态

页面正文以 `<!-- untranslated-notice -->` 标记区分：

- 有该标记 → 仍是英文原文（页首有黄色提示条）
- 无该标记 → 已翻译

查看当前进度：

```bash
python3 tools/sync_upstream.py --report
```

## 参与翻译

见 [TRANSLATING.md](TRANSLATING.md)。核心要求：先读 `i18n/glossary.md`，命令与参数不得翻译，公式逐字符保留，删掉页首提示块。

## 许可证

- 本站译文与构建脚本：CC BY-SA 4.0
- 原文与所有官方素材（`_includes/`、`_sass/`、`assets/`、页面正文）：LGPL-3.0，版权归 JOREK 团队

# 维护说明

本文件面向想接手或参与维护这个中文镜像站的人，不是在 GitHub 首页展示的项目介绍。

## 目录结构

```
.
├── _config.yml          # 由上游 _config.yml 派生，仅改站点标识与主题加载方式
├── _includes/           # 上游原文件（页头、深浅色切换），勿改
├── _sass/               # 上游原文件（自定义配色），勿改
├── assets/              # 上游原文件（logo、CSS 入口），勿改
├── index.md             # 以下为文档页，路径与上游 Wiki 一一对应
├── compiling/  howto/  physics/  numerics/  diagnostics/  machines/ …
├── i18n/
│   ├── titles.yml       # 英文标题 → 中文标题映射（导航层级依赖它）
│   ├── glossary.md      # 术语表（翻译必须遵守）
│   └── TRANSLATE_BRIEF.md # 翻译作业书
├── tools/
│   ├── sync_upstream.py # 从上游 Wiki 同步结构、素材与新增页面
│   ├── check_upstream.py# 检测上游文档变更
│   ├── verify_site.py   # 站点验收
│   └── _paths.py        # 上游路径解析
├── COPYING / COPYING.LESSER / NOTICE.md / CITATION.cff
└── TRANSLATING.md       # 翻译规范
```

## 本地构建

需要 Ruby ≥ 3.1（版本锁在 `Gemfile.lock`：Jekyll 4.4.1 + just-the-docs 0.10.0）。

```bash
bundle install
bundle exec jekyll serve     # http://127.0.0.1:4000/jorek-docs-zh/
bundle exec jekyll build     # 仅生成静态文件到 _site/
```

## 上游路径配置

维护脚本需要知道上游 JOREK 仓库及其 `docs/` 副本的位置。优先级从高到低：

1. 环境变量：`export JOREK_DOCS_DIR=/path/to/JOREK/docs`、`export JOREK_REPO=/path/to/JOREK`
2. 仓库根目录的 `upstream.local.yml`（已在 `.gitignore` 中，不入库）：

   ```yaml
   docs_dir: ../upstream/docs
   repo:     ../upstream/repo
   ```

3. 默认值：`../upstream/docs` 与 `../upstream/repo`

推荐：

```bash
git clone https://github.com/iterorganization/JOREK.git ../upstream/repo
ln -s ../upstream/repo/docs ../upstream/docs
```

## 同步循环

```bash
python3 tools/check_upstream.py --detail   # 1. 看上游改了什么
git -C ../upstream/repo pull               # 2. 更新上游副本
rsync -a --delete ../upstream/repo/docs/ ../upstream/docs/   # 3. 刷新 Wiki 副本
python3 tools/sync_upstream.py --new       # 4. 补新增页面（不覆盖已有译文）
# 5. 重译被修改的页面
python3 tools/verify_site.py               # 6. 验收
python3 tools/check_upstream.py --accept   # 7. 记录新基线
```

`sync_upstream.py` **不会覆盖已有译文**：已存在的页面一律跳过。新增页面会带着英文原文落盘，页首标注"本页尚未翻译"。

## 翻译状态判定

页面正文以 `<!-- untranslated-notice -->` 标记区分：有标记 = 仍是英文原文，无标记 = 已翻译。

```bash
python3 tools/sync_upstream.py --report
```

## 已知的上游缺陷（本仓库保持一致，未修正）

| 类型 | 数量 | 说明 |
|---|---|---|
| 占位页 | 45 | 上游本身只写了 `This page is a stub` 或留空（含 6 个栏目索引页） |
| 失效链接 | 74 | 上游引用了不存在的页面、`.md` 源码路径、`/docs/` 仓库路径、未入库附件 |
| 坏图 | 25 | 旧 wiki 迁移时丢失的图片 |
| 失效锚点 | 6 | 上游把图片定义名当锚点、链接与锚点拼写不一致 |

原则：**照原样保留，不擅自修正**，保证与英文站逐页可对照。

## 仓库约定

- 页面正文、`_includes/`、`_sass/`、`assets/` 必须与上游逐字节一致，只有语言不同
- 命令、namelist 参数、公式、文件路径一律保留原文
- 标题锚点用 `{#id}`；ID 以数字开头时改用 `<a id="...">`（`{: #id }` 在 kramdown 下无效，会显示成文字）
- 仓库内不得出现维护者的本地路径；本地配置走 `upstream.local.yml`
- 推送 `main` 会自动触发 GitHub Actions 构建并部署到 Pages

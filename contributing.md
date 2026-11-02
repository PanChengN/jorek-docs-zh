---
title: "参与文档建设"
nav_order: 89
layout: default
render_with_liquid: false
---

# 参与文档建设

本站使用 [Jekyll](https://jekyllrb.com) 与 [Just the Docs](https://just-the-docs.com) 主题构建。每个页面都是 `docs/` 下的一个 Markdown 文件。向 `master` 推送会触发 GitHub Actions 的自动构建与部署。

## 访问权限

仓库对具有写权限的协作者开放。若你尚无权限，请写信给 **Luca Greco** 请求加入。

---

## 安装前置依赖

需要 **Ruby ≥ 3.1** 与 **Bundler**。假定 Git 已安装。

**macOS**

系统自带的 Ruby 版本过旧。请通过 [Homebrew](https://brew.sh) 安装当前版本：

```bash
brew install ruby
```

然后按 Homebrew 的指示把 Ruby 加入 PATH（大致为 `export PATH="/opt/homebrew/opt/ruby/bin:$PATH"`），并安装 Bundler：

```bash
gem install bundler
```

**Linux (Debian/Ubuntu)**

```bash
sudo apt install ruby-full build-essential zlib1g-dev
gem install bundler
```

**Windows**

使用 [RubyInstaller](https://rubyinstaller.org/)（选择带 Devkit 的版本）。其中已包含 Bundler。

---

## 本地预览

```bash
git clone git@github.com:<username>/<fork-name>.git
cd fork-name
bundle install        # only needed once, or after Gemfile changes
bundle exec jekyll serve --baseurl /fork-name
```

打开 `http://localhost:4000/fork-name/`。对 `.md` 文件的修改在页面重载时即被纳入，无需重启服务器。

---

## 发起合并请求

1. 克隆 fork（只需一次）并保持更新（见[开发流程](/code_development/development_workflow.md) ）：
   ```bash
   git clone git@github.com:<username>/<fork-name>.git
   git pull origin develop
   ```
2. 从 `develop` 创建分支：
   ```bash
   git checkout -b my-topic
   ```
3. 添加或编辑文件，提交并推送该分支：
   ```bash
   git add docs/my_page.md
   git commit -m "Add documentation for X"
   git push origin my-topic
   ```
4. 在 GitHub 上向主仓库的 `develop` 发起合并请求。合并后站点会自动重新部署——无需进一步操作。

---

## front matter 参考

每个页面都以由 `---` 包围的 YAML 块开头。YAML 对空白敏感，使用 `key: value` 键值对。有几点值得了解：

- **字符串**通常无需引号。若值中含有冒号、`#` 或首尾空格，请使用双引号：`title: "Solver: Details"`。
- **布尔值**写作裸的 `true` / `false` —— 不加引号。
- **整数**写作裸数字 —— 不加引号。
- 缩进必须使用空格，不能用制表符。

本站使用的键列于下表。完整参考见 [Just the Docs 导航文档](https://just-the-docs.com/docs/navigation/)。

| 键 | 类型 | 是否必需 | 说明 |
|---|---|---|---|
| `title` | string | yes | 显示在浏览器标签页与侧栏中的页面标题。 |
| `layout` | string | yes | 内容页面一律为 `default`。 |
| `render_with_liquid` | bool | yes | 设为 `false` 可防止 Jekyll 把 `{{` 与 `{%` 解释为模板语法 —— 对含代码示例的页面很重要。 |
| `nav_order` | integer | no | 侧栏中在父分组内的位置。数值越小越靠上。省略时按页面标题的字母顺序排列。 |
| `parent` | string | no | 父页面标题，须与该页 `title` 字段的写法完全一致。在侧栏中把本页嵌套于其下。 |
| `grand_parent` | string | no | 祖父页面标题。当 `parent` 本身也是子页面（三级页面）时必需。 |
| `has_children` | bool | no | 把页面标记为可包含子页面的章节。 |
| `nav_fold` | bool | no | 默认在侧栏中折叠该章节。仅在 `has_children: true` 时有意义。 |
| `nav_exclude` | bool | no | 在侧栏中隐藏该页面。页面仍会被构建，并可通过其 URL 访问。 |

---

## 创建页面

`docs/` 下的每个 `.md` 文件都是一个页面。它需要 YAML front matter 块：

```yaml
---
title: "My Page"
layout: default
render_with_liquid: false
---

Content goes here.
```

这是最低要求。页面会被构建并可通过其 URL 访问，但除非添加导航字段（见下文），否则不会出现在侧栏中。

若要**把页面从侧栏排除**但仍使其可被链接：

```yaml
nav_exclude: true
```

---

## 添加侧栏章节

侧栏章节就是一个带 `has_children: true` 与 `nav_fold: true` 的页面。按约定，章节落地页命名为 `cat_<name>.md`，并放在各自的子目录中：

```
docs/
  mysection/
    cat_mysection.md   ← section landing page
    page_a.md
    page_b.md
```

`cat_mysection.md` 的 front matter：

```yaml
---
title: "My Section"
nav_order: 8
has_children: true
nav_fold: true
layout: default
render_with_liquid: false
---
```

子页面通过该章节的 `title` 引用它：

```yaml
---
title: "Page A"
nav_order: 1
parent: "My Section"
layout: default
render_with_liquid: false
---
```

---

## 管理侧栏元素

| Front matter 键 | 作用 |
|---|---|
| `nav_order` | 在父分组内的位置（越小越靠上）。适用于每一层级。 |
| `parent` | 把页面嵌套到某章节下。值必须与该章节的 `title` 完全一致。 |
| `grand_parent` | 三级页面必需。值必须与章节标题（祖父页面）一致。 |
| `has_children: true` | 把页面标记为可含子页面的章节。 |
| `nav_fold: true` | 使章节在侧栏中初始为折叠状态。 |
| `nav_exclude: true` | 完全从侧栏隐藏该页面。 |

导航支持多级嵌套。`grand_parent` 键始终指直接的祖父页面（比 `parent` 高一级），不一定是顶层章节。

若要**重命名章节**，修改其 `cat_*.md` 文件中的 `title`，并同步更新每个子页面的 `parent` 字段使其一致。

---

## 页面之间的链接

链接使用带 `.md` 扩展名的标准 Markdown 语法 —— 构建时会自动转换为 `.html`：

```markdown
See [Normalization](normalization.md) for details.
```

对位于不同目录的页面，使用相对于当前文件的路径：

```markdown
[Compiling](compiling/compilation_and_libraries/compiling.md)
```

从仓库根目录起的绝对路径也可用：

```markdown
[Compiling](compiling/compilation_and_libraries/compiling.md)
```

不要硬编码 `.html` 扩展名 —— 若站点 baseurl 变化，这些链接就会失效。

---

## 图片

图片应放在使用它的页面旁边。在 `.md` 文件所在目录创建 `assets/` 文件夹，并在其中创建以该文件名命名的子文件夹：

```
docs/howto/physics_options/physical_terms/
  diamag.md
  assets/
    diamag/
      my_figure.png
```

以相对于该 `.md` 文件的路径引用它们：

```markdown
![Alt text](assets/diamag/my_figure.png)
```

要控制尺寸，使用 HTML 的 `<img>` 标签：

```html
<img src="assets/diamag/my_figure.png" alt="Alt text" width="600">
```

示意图与截图优先使用 PNG 或 SVG；文件大小应保持合理 —— 大的二进制文件会拖慢所有人的仓库。

---

## 数学公式

行内 LaTeX：`$...$`。独立公式：`$$...$$`。MathJax 负责渲染两者。标准宏可用；避免在行内公式中使用裸 `||` —— 请改用 `\\Vert`。

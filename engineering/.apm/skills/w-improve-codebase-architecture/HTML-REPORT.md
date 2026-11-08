# HTML 报告格式

架构评审渲染为操作系统临时目录里的单个自包含 HTML 文件。Tailwind 与 Mermaid 均取自 CDN。Mermaid 可靠地画图状结构；手写 div 与内联 SVG 承担更像编辑设计的视觉（体量图、剖面图）。两者混用——不要把所有图都交给 Mermaid，那样会显得千篇一律。

## 骨架

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <title>架构评审 — {{仓库名}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* Tailwind 覆盖不干净的少量自定义：接缝虚线、手绘感箭头等 */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## 页头

仓库名、日期，加一份紧凑图例：实线框＝模块，虚线＝接缝，红色箭头＝渗漏，粗深色框＝深模块。不写导语，直接进候选。

## 候选卡片

图承担主要信息量。文字稀疏、朴素，直接使用 `/w-codebase-design` 的术语，不加修饰。

每个候选一个 `<article>`：

- **标题**：简短，点明这次合并（例如「合并 Order 接入管线」）
- **徽标行**：建议强度（`Strong` 绿、`Worth exploring` 琥珀、`Speculative` 灰），再加依赖类别标签（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）
- **涉及文件**：等宽列表，`font-mono text-sm`
- **前后对比图**：核心部分。两列并排，范式见下
- **问题**：一句话，痛在哪里
- **方案**：一句话，改什么
- **收益**：要点列表，每条不超过六个字，例如「测试只打一个接口」「定价逻辑不再渗漏」「删掉四个浅包装」
- **ADR 提示**（适用时）：琥珀色框内一行

不写整段解释。图若需要一段话才看得懂，重画图。

## 图范式

按候选选择范式，混着用。不要让每张图长得一样——多样性本身就是目的的一部分。

### Mermaid 图（依赖与调用流的主力）

要点是「X 调 Y、Y 调 Z，看这一团乱」时，用 Mermaid 的 `flowchart` 或 `graph`。外面套一个 Tailwind 卡片，免得像空降来的。用 classDef 把渗漏的边染红、深模块染深。序列图适合表达「之前六次往返，之后一次」。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### 手写方框与箭头（Mermaid 的排布不听使唤时）

模块做成带边框与标签的 `<div>`，箭头用内联 SVG 的 `<line>` 或 `<path>`，绝对定位在相对定位的容器上。需要让「之后」的图呈现为一个粗边框深模块、内部灰化时，用这个范式——Mermaid 画不出那个分量。

### 剖面图（适合层层叠加的浅）

堆叠横向色带（`h-12 border-l-4`）表示调用穿过各层。之前：六条薄层，层层无所作为。之后：一条厚带，标注合并后的职责。

### 体量图（适合「接口与实现一般宽」）

每个模块两个矩形，一个表示接口面积，一个表示实现。之前：接口矩形几乎与实现等高（浅）。之后：接口矩形矮、实现矩形高（深）。

### 调用图折叠

之前：函数调用树渲染为嵌套方框。之后：同一棵树折叠成一个方框，如今变成内部的调用在其中淡显。

## 样式指引

- 偏编辑设计，不要企业仪表盘。留白要足。标题可用衬线（`font-serif` 配 stone／slate 效果好）
- 用色克制：一个强调色（绿或靛），红色只给渗漏，琥珀只给警示
- 图高控制在 320px 上下，前后对比并排时无需滚动
- 图内模块标签用 `text-xs uppercase tracking-wider`，读起来要像示意图，不像界面
- 唯一的脚本是 Tailwind CDN 与 Mermaid 的 ESM 引入。除此之外报告是静态的：没有应用逻辑，除 Mermaid 自身渲染外没有交互

## 首要建议节

一张更大的卡片：候选名称、一句理由、指向该卡片的锚点链接。就这些。

## 语气

平实、简洁，但架构名词与动词直接取自 `/w-codebase-design`。简洁不是跑偏的借口。

**只用这些词：** module、interface、implementation、depth、deep、shallow、seam、adapter、leverage、locality。

**绝不替换为：** component、service、unit（指模块时）· API、signature（指接口时）· boundary（指接缝时）· layer、wrapper（指模块时）。

**符合这套风格的句式：**

- 「Order 接入模块是浅的——接口几乎与实现等宽。」
- 「定价逻辑越过接缝渗漏。」
- 「合并之后：一个接口，一处可测。」
- 「两个适配器才配得上这道接缝：生产走 HTTP，测试走内存。」

**收益要按术语表来写**：*「局部性：缺陷集中在一个模块」*、*「杠杆：一个接口，N 个调用点」*、*「接口收缩，实现吸收包装」*。不要写「更易维护」「代码更干净」——这些词不在术语表里，也不配占位置。

不设防，不铺垫，不写「值得一提的是……」。能写成要点的就写成要点；能删的要点就删。词不在 `/w-codebase-design` 术语表里时，先找表内更合适的词，而不是另造一个。

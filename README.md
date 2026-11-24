# photo-redesign-poster — 照片再设计海报

把**已经有的照片**做成「上半原图 + 下半介质重构」的 **3:4** 海报：同一张照片，上半是现实，下半是它的另一次生命。

作者：**AI绘梦师葉子**

---

## 它解决什么问题

| 常见翻车 | 本 skill 的对策 |
|---|---|
| 让模型一次出整张，上半区被"顺手重画" | **只生成下半区（3:2）**，再用 `compose.py` 拼原图——上半区一个像素都不动 |
| 让模型自己排 1:1，实际中线偏 4~7 个点 | 实测三张：**50.0% / 43.0% / 46.1%**。要求严格等分时一律走程序拼接，**像素级 50:50** |
| 下半区做出来像"原图加了个滤镜" | 介质库每条都带**唯一约束**与**判据**；③ 段强制三句排除（尤其「不能做成滤镜效果」） |
| 问用户"想要什么风格"，得到的答案是"高级一点" | 按 `06-select.md` 直接给 **3 个跨类候选**，每个一句话说清出来长什么样 |
| 装配时把片段概括成效果词（"针脚可见"） | ⛔ **合体片段只能改槽位，不能改写句子**——概括过的三条实测全翻车 |
| 文字放右下角，被出图工具的水印压成两半 | **右下角默认留空**；`--dewm` 可裁掉水印角（等比，仍是 3:4） |

## 核心设计（六条硬纪律）

- **必须有照片** —— 纯文字想象不属于这里（转 `yezi-ai-image-prompt`）
- **一律 3:4** —— 换比例这套版式就散了，不做 16:9 / 9:16 / 1:1
- **给 2~3 个跨类候选让用户选** —— 不替他拍板；同类三个不叫选择，叫换皮
- **上半区一个字不许改** —— 只许轻度调色，且必须写「清除水印、Logo 及非场景文字」
- **下半必须是重构不是滤镜** —— 判据：把下半区单独截出来看，还认得出原物吗
- **严格等分一律走模式 B** —— 只生成下半区 + 程序拼接；模型的「1:1」只当构图意图

## 26 种介质（五类）

| 类 | 介质 |
|---|---|
| **A 图形与符号** | `visual-dna` 视觉DNA · `deconstruct-swiss` 解构瑞士 · `swiss-grid` 瑞士网格 · `magazine-cover` 杂志封面 · `cultural-silhouette` 文化剪影 · `monoline` 一笔线画 · `negative-space` 正负形 |
| **B 纸品印刷** | `vintage-stamp` 旅行邮票 · `riso-poster` Riso 双色 · `archive-sheet` 档案图鉴页 · `map` 手绘地图 |
| **C 材质手工** | `clay-diorama` 黏土微缩 · `paper-cut` 纸雕 · `paper-miniature` 纸艺微缩 · `embroidery` 刺绣 · `mosaic` 马赛克 |
| **D 绘画插画** | `ink-wash` 水墨 · `ukiyoe` 浮世绘 · `picturebook-crayon` 绘本蜡笔 · `pencil-sketch` 素描炭笔 · `comic-panel` 漫画分镜 |
| **E 数字影像** | `bitmap-halftone` 字符网点 · `frosted-glass` 毛玻璃 · `pixel-art` 像素艺术 · `blueprint` 工程蓝图 · `double-exposure` 双重曝光 |

其中 **11 种有公开原文依据**，其余 15 种按同一套五段骨架新写（每条都有唯一约束与判据，不是凑数）。

## 安装

把整个 `photo-redesign-poster` 文件夹放进你所用的 AI 助手加载 skill 的目录即可：

| 范围 | 放哪 |
|---|---|
| 个人级（所有项目可用） | 你的用户级 skills 目录（具体位置以助手说明为准） |
| 项目级（仅当前项目） | `<你的项目>/skills/photo-redesign-poster/` |

放好后跟助手说「这张照片做成上下两半的海报」「照片变黏土 / 变纸雕 / 变邮票」就会触发。

## 目录结构

```
photo-redesign-poster/
├── SKILL.md                    主流程：五步工作流 + 装配规则 + 出图两条路径
├── references/
│   ├── 00-skeleton.md          五段骨架、三句排除、禁写清单
│   ├── 01-graphic.md           A 图形与符号 7 种
│   ├── 02-print.md             B 纸品印刷 4 种
│   ├── 03-material.md          C 材质手工 5 种
│   ├── 04-painting.md          D 绘画插画 5 种
│   ├── 05-digital.md           E 数字影像 5 种
│   ├── 06-select.md            照片 → 推哪 3 个候选（硬门槛表）
│   ├── 07-series.md            一次做一批 / 系列一致性
│   ├── 08-qa.md                症状 → 改哪一处
│   ├── 09-sources.md           原文出处与缺口记录
│   └── 10-lower-only.md        模式 B：只生成下半区的取法与改写
└── scripts/
    ├── compose.py              上下拼接（严格 50:50 由构造保证）
    └── check.py                成品自检：比例 / 尺寸 / 接缝
```

## 脚本

依赖 Pillow：`pip install pillow`

```bash
# 严格 50:50，上半区铺满（源图约 3:2 时用）
python scripts/compose.py --photo src.jpg --lower lower.png --out poster.jpg
# 横图想保留完整构图 → 模糊延展，中线依旧是 50:50
python scripts/compose.py --photo src.jpg --lower lower.png --mode blur --out poster.jpg
# 下半区顶端有暗角/投影，接缝显脏 → 切掉 2% 再接
python scripts/compose.py --photo src.jpg --lower lower.png --trim-top 2 --out poster.jpg
# 右下角有出图工具水印 → 等比裁掉右下角 9%
python scripts/compose.py --photo src.jpg --lower lower.png --dewm --out poster.jpg
# 黏土类走 46:54
python scripts/compose.py --photo a.jpg --lower b.png --ratio 46 --out c.jpg

python scripts/check.py poster_001.jpg --composed   # 拼接产物：位置按构造值判定 + 查接缝
python scripts/check.py poster_001.jpg              # 模型直出：自动找接缝
```

⚠️ 生成下半区时尺寸传 **1536×1024**（严格 3:2）。⛔ 1024×1536 是 2:3，会整体带偏比例。

## 为什么中线不交给模型

实测三张「整张直出、提示词写死 1:1」的结果：**50.0% / 43.0% / 46.1%**，上半区 MAE 14~19，照片也被重画过。
所以「严格上下二等分」只有一条可靠路径：**只生成下半区 → 程序拼接**。`compose.py` 里画布高取偶数、上下各取 `H//2`，等分由构造保证，与模型无关。

## 来源与致谢

26 种介质里，11 种的提示词骨架来自公开发表的 AI 提示词分享文章（见 `references/09-sources.md` 的标题与对应关系），版权归原作者；本项目对其做了结构化整理，并为「上半区被重绘」「中线偏移」两个缺口补了程序化方案。

## 许可

代码与文档：**MIT**，见 [LICENSE](LICENSE)。

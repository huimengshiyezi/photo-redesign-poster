# 介质选择

> 用户不会说"解构瑞士""孔版印刷"。他们只会说"这是我家猫""这是上周去大理拍的"。
> 这份文件把「照片长什么样」翻译成「用哪一种」。

---

## 第一步：先判断主体

| 照片里主要是 | 首选 | 次选 | 第三 |
|---|---|---|---|
| **一个清晰的人（正面/半身）** | `magazine-cover` | `visual-dna` | `pixel-art` · `pencil-sketch` |
| **侧脸 / 剪影 / 背影** | `negative-space` | `double-exposure` | `monoline` |
| **多个人、有互动** | `comic-panel` | `magazine-cover` | `picturebook-crayon` |
| **有人在做某件事（叙事感）** | `comic-panel` | `picturebook-crayon` | `double-exposure` |
| **小孩 / 家庭** | `picturebook-crayon` | `embroidery` | `clay-diorama` |
| **建筑（单栋/立面）** | `swiss-grid` | `blueprint` | `paper-cut` · `mosaic` |
| **城市 / 街景** | `riso-poster` | `map` | `swiss-grid` · `frosted-glass` |
| **自然风景（有纵深、有路有水）** | `map` | `ink-wash` | `paper-miniature` · `ukiyoe` |
| **自然风景（特写/一片）** | `ink-wash` | `embroidery` | `riso-poster` · `bitmap-halftone` |
| **动物** | `cultural-silhouette` | `picturebook-crayon` | `mosaic` · `negative-space` |
| **植物 / 花** | `archive-sheet` | `embroidery` | `ink-wash` · `cultural-silhouette` |
| **小物 / 静物 / 产品** | `archive-sheet` | `clay-diorama` | `frosted-glass` · `riso-poster` |
| **美食** | `clay-diorama` | `picturebook-crayon` | `vintage-stamp` |
| **旅行 / 街拍** | `vintage-stamp` | `map` | `riso-poster` · `archive-sheet` |
| **老照片 / 黑白** | `vintage-stamp` | `pencil-sketch` | `archive-sheet` · `riso-poster` |
| **抽象 / 纹理 / 无明确主体** | `bitmap-halftone` | `archive-sheet` | `pixel-art` |

---

## 第二步：再按照片质量校准 ⭐ 这一步经常比第一步重要

| 照片状态 | 改走 | 为什么 |
|---|---|---|
| 构图好、主体清晰 | 维持首选 | 特征抽得出来 |
| **构图差 / 主体小 / 背景乱** | `bitmap-halftone` | 它明确授权模型"重新导演"，允许小主体 + 大量留白 |
| **光线差 / 色偏 / 有噪点** | `vintage-stamp` · `riso-poster` | 材质和印刷把瑕疵变成风格 |
| **整体糊 / 手机随手拍** | `paper-cut` · `pixel-art` | 只要轮廓，不需要细节 |
| **有故事但没拍好** | `comic-panel` | 靠分镜补足叙事，不靠这张图本身 |
| **白天过曝 / 一片白** | `blueprint` · `monoline` | 反正要重画，白底反而是好事 |

⭐ **一句话记住**：**好照片做减法，烂照片做换算法。**

---

## 第三步：按用途收口

| 用途 | 优先 | 理由 |
|---|---|---|
| 公众号 / 小红书封面 | `visual-dna` · `negative-space` · `riso-poster` | 缩略图下辨识度最高（形状大、对比强） |
| 系列更新（每周一批） | `clay-diorama` · `vintage-stamp` · `archive-sheet` · `visual-dna` | 版式固定，换图不换结构 |
| 单张要惊艳 | `double-exposure` · `mosaic` · `blueprint` | 视觉冲击或工艺门槛高，一眼不俗 |
| 商单 / 品牌调性 | `swiss-grid` · `frosted-glass` | 最"专业"，不花哨 |
| 文艺 / 情绪 | `ink-wash` · `vintage-stamp` · `pencil-sketch` | 有手温和旧感 |
| 童趣 / 温柔 | `picturebook-crayon` · `embroidery` · `clay-diorama` | 材质本身带温度 |
| 硬核 / 技术感 | `blueprint` · `pixel-art` · `comic-panel` | 有"行内人"的语汇 |
| 手机壁纸 | `visual-dna` · `negative-space` | 3:4 裁成 9:19.5 时中间的形状还立得住 |

---

## 反查：用户说的是风格词

| 用户说 | 对应介质 |
|---|---|
| 高级感 / 极简 / 性冷淡 / 干净 | `swiss-grid` · `frosted-glass` · `monoline` |
| 艺术感 / 抽象 / 设计感 | `deconstruct-swiss` · `visual-dna` · `negative-space` |
| 手工 / 温暖 / 治愈 | `clay-diorama` · `paper-miniature` · `embroidery` |
| 复古 / 怀旧 / 文艺 / 老照片 | `vintage-stamp` · `riso-poster` · `archive-sheet` |
| 有文化味 / 国风 / 东方 | `cultural-silhouette` · `ink-wash` · `ukiyoe` |
| 像海报 / 像杂志 / 像展览 | `magazine-cover` · `archive-sheet` |
| 有故事 / 像漫画 / 分镜 | `comic-panel` |
| 童书 / 可爱 / 手绘感 | `picturebook-crayon` |
| 技术 / 工程 / 硬核 / 蓝图 | `blueprint` |
| 像素 / 游戏 / 复古电脑 | `pixel-art` |
| 印刷感 / 版画 / 双色 | `riso-poster` · `ukiyoe` |
| 立体 / 有厚度 / 模型 | `paper-cut` · `clay-diorama` · `paper-miniature` |
| 手绘 / 素描 / 铅笔 | `pencil-sketch` |
| 剪影 / 轮廓 / 像 logo | `cultural-silhouette` · `negative-space` |
| 梦幻 / 叠影 / 双重 | `double-exposure` |
| 科技感 / 未来 / 赛博 | ⚠️ **本项目没有对应介质。** 直接告诉用户：这套语汇里没有赛博的位置，硬做会变成廉价霓虹 |

---

## 给候选：三个，跨类，每个说清"出来长什么样"

⛔ 不要报介质名就完事。用户不知道 `bitmap-halftone` 是什么。

✅ 模板：

> 这张我想到三种做法：
> **① 瑞士网格**——下半是几个纯色圆和一道斜线，像设计师的工作稿，极干净
> **② 纸雕**——下半像用卡纸一层层剪出来叠的立体模型，有厚度和影子，暖一些
> **③ 字符网点**——下半整块是小字和点阵组成的，远看是图形近看是字母，最"设计感"
>
> 或者你说个别的方向，我按你的来。

⭐ **三个候选必须跨类别**（图形 / 纸品 / 材质 / 绘画 / 数字，各取一类）。
同类别给三个（解构瑞士 + 杂志封面 + 瑞士网格）**不叫选择，叫换皮**。

⭐ **第三句要带上理由**，让用户知道你为什么这么推：

> 这张是个建筑立面，线条干净，所以推瑞士网格；如果嫌太冷，纸雕能把它做暖。

---

## 几种介质对源图有硬门槛（不满足就换，别跟词较劲）

> 详细说明写在各介质条目的「硬门槛」里，这里只做候选阶段的快速筛。两边说的是同一件事，改一处记得改另一处。

| 介质 | 源图必须有 | 不满足会怎样 | 换成 |
|---|---|---|---|
| `double-exposure` 双重曝光 | **明确剪影 / 强轮廓**：逆光、深色主体压亮底、侧脸对天空 | 两层同源同调，叠出来就是"带暗角的虚化照"，没有"轮廓里装景象" | `frosted-glass` · `pencil-sketch` |
| `frosted-glass` 毛玻璃 | **主体边界清楚**，且背景有可被遮的层次 | 源图本身就虚（虚焦、晕染），再做磨砂等于什么都没做 | `swiss-grid` · `monoline` |
| `mosaic` 马赛克 | **色块界限清楚**（强光、简洁构图） | 软过渡的图会退化成"照片叠网格" | `riso-poster` · `bitmap-halftone` |
| `embroidery` 刺绣 | 轮廓柔和、颜色不多 | 细节过密的图绣不出针脚，变成印花 | `picturebook-crayon` · `paper-cut` |
| `blueprint` 工程蓝图 | **有明确结构关系**（建筑、机械、道路） | 柔散的主体没有可标注的尺寸，标注会变成装饰 | `archive-sheet` · `swiss-grid` |

⭐ 一条总规律：**工艺类要"色块清楚"，影像类要"轮廓清楚"。** 源图两头都不占（又软又碎），先劝换图。

---

## 不适用的照片（要诚实说，不要硬做）

| 照片类型 | 为什么不行 | 怎么说 |
|---|---|---|
| 纯文字截图 / 文档 / PPT | 没有可重构的形象 | "这类图文没法和原图形成对照，做出来会很难看。换一张实拍图？" |
| 表情包 / 梗图 | 本身就是符号，重构等于重画 | 同上 |
| 糊到看不清主体的 | 抽不出特征 | "这张太糊了，下半区会变成一团。有同场景清楚的图吗？" |
| 大面积纯色 / 纯天空 | 没有信息量 | "这张基本是纯色，下半区无从下手。" |
| 已经加了强滤镜的图 | 上半区不"真"，对照关系就没了 | "这张已经重调过色，上半区不够真。有原图吗？" |

⛔ **不要为了完成任务硬套一个介质。** 做出来难看，用户不会觉得是照片的问题，会觉得是 skill 不行。

---

## 兜底

用户说"你定 / 随便 / 都行"：

**按主体表选第一顺位，直接走，并在交付时说明理由 + 一句"想换风格随时说"。**

⛔ 不要因为用户说"随便"就跳过选择直接套最熟的介质。
"随便"通常是"我不懂，你看着办"，不是"我不在乎"。选错的代价比多问一句大。

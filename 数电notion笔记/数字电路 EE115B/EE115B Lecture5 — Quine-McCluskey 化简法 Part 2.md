# EE115B Lecture5 — Quine-McCluskey 化简法 Part 2

<aside>
🧮

**本节主题：** Quine-McCluskey（Q-M）化简法 —— 一种可程序化的逻辑最小化算法（本讲 Part 2，接 K-map 之后）。

**参考教材：** *Digital Fundamentals*, Table 4-11, p.237；参考实现 [github.com/int-main/Quine-McCluskey。](http://github.com/int-main/Quine-McCluskey。)

**核心脉络：** K-map 的局限 → 术语（Implicant / PI / EPI / Cover）→ Q-M 五步法（写 SOP → 按"1 的个数"分组 → 相邻合并求所有 PI → 写 PI 表 → 选 EPI 得最简 SOP）→ 完整练习 → 与一致性定理（consensus）互证 → 仿真工具。

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md)；与 [EE115B Lecture6 — Combinational Logic Analysis Part 1](EE115B%20Lecture6%20%E2%80%94%20Combinational%20Logic%20Analysis%20Par.md) 的 K-map / 标准式同属"逻辑化简"主线。

</aside>

## 🔁 开篇回顾（slides 2–4）

上一节的化简工具与本节的衔接：

- **SOP / Standard SOP、POS / Standard POS**：与门-或门、或门-与门两种标准式。
- **Minterm / Maxterm**：最小项（行=1）与最大项（行=0）。
- **SOP ↔ POS 互转**：德摩根定理、真值表、K-map 三条路。
- **K-map 化简**：SOP simplification 与 POS simplification。

<aside>
⚠️

**K-map 的局限（slide 4）：** 变量超过 **5** 个时图难画、难判相邻；而且不易写成计算机程序。

**→ 需要 Quine-McCluskey：** 非图形（用列表）、易程序化、能处理更多变量。

</aside>

# 🧮 一、术语 Terminology（slide 5）

| 术语 | 定义 |
| --- | --- |
| **Variable** | 输入变量，如 $A,B,C,D$ |
| **Literal** | 变量的原变量或反变量，如 $A$、$\bar B$ |
| **Implicant** | 由 K-map 得到的乘积项，使该项 = 1 时 $F=1$（如 $\bar A BC,\ AB\bar CD$） |
| **Prime Implicant (PI)** | 不能再化简的 implicant —— 任何一个 literal 都不能再去掉 |
| **Essential PI (EPI)** | 含有"只能被这一种方式圈住"的 1 的 prime implicant —— 必须保留 |
| **Cover** | 能覆盖所有 1 的一组 prime implicants |

![Slide 5 — 术语与 K-map 示例](EE115B%20Lecture5%20%E2%80%94%20Quine-McCluskey%20%E5%8C%96%E7%AE%80%E6%B3%95%20Part%202/slide_5.png)

Slide 5 — 术语与 K-map 示例

<aside>
💡

**slide 5 的例子（变量 A,B,C,D）：** PI 有 $\bar A\bar C,\ ACD,\ ABD,\ BC'D,\ \bar A\bar D$ 等；EPI 是 $ACD$（不是 ABD、不是 BC'D）；一个合法 cover = $ACD,\ \bar A\bar D,\ \bar A\bar C$ 再加 $(BC'D\ 或\ ABD)$。

</aside>

# 🛠 二、Q-M 五步法（例：$X=\sum m(1,3,4,5,10,12,13,15)$）

## 1️⃣ Step 1 — 写成 SOP（slide 6）

先把函数写成最小项之和（standard SOP）：

$$
X=\sum m(1,3,4,5,10,12,13,15)
$$

## 2️⃣ Step 2 — 按"1 的个数"分组（slide 7）

把每个最小项写成二进制（ABCD），按其中 **1 的个数** 分组。合并的理论依据是吸收律：

$$
XY+X\bar Y=X
$$

相邻组（1 的个数差 1）之间才可能合并。

![Slide 7 — 真值表 → 按 1 的个数分组](EE115B%20Lecture5%20%E2%80%94%20Quine-McCluskey%20%E5%8C%96%E7%AE%80%E6%B3%95%20Part%202/slide_7.png)

Slide 7 — 真值表 → 按 1 的个数分组

## 3️⃣ Step 3 — 相邻组比较、合并（slide 8）

相邻两组里只差 **1 个 bit** 的项可以合并，差异位记成 `x`（don't care 化）；被合并的项打勾 ✓ 表示"已被更大的项覆盖"。

![Slide 8 — 第一级合并 First Level](EE115B%20Lecture5%20%E2%80%94%20Quine-McCluskey%20%E5%8C%96%E7%AE%80%E6%B3%95%20Part%202/slide_8.png)

Slide 8 — 第一级合并 First Level

## 4️⃣ Step 3（续）+ Step 4 — 二次合并、写出所有 PI（slides 9–10）

对 First Level 再做一次相邻合并得到 Second Level：$(m_4,m_5,m_{12},m_{13})$ → `x10x`。无法再合并、且未被打勾的立方就是 **Prime Implicant**：

| 立方 (cube) | 覆盖 minterms | 乘积项 |
| --- | --- | --- |
| `x10x` | 4, 5, 12, 13 | $B\bar C$ |
| `00x1` | 1, 3 | $\bar A\bar B D$ |
| `0x01` | 1, 5 | $\bar A\bar C D$ |
| `11x1` | 13, 15 | $ABD$ |
| `1010` | 10 | $A\bar B C\bar D$ |

## 5️⃣ Step 5 — PI 表 + 选 EPI（slides 11–12）

光找出所有 PI 不一定最简，需再列 **Prime Implicant 表**：行 = PI，列 = 各 minterm，打勾表示覆盖。

![Slide 11 — Prime Implicant 表 (TABLE 4-13)](EE115B%20Lecture5%20%E2%80%94%20Quine-McCluskey%20%E5%8C%96%E7%AE%80%E6%B3%95%20Part%202/slide_11.png)

Slide 11 — Prime Implicant 表 (TABLE 4-13)

判定规则：**某个 minterm 若只被一个 PI 覆盖（该列只有一个勾），这个 PI 就是 EPI，必须保留。**

![Slide 12 — 从 EPI 出发选最简覆盖](EE115B%20Lecture5%20%E2%80%94%20Quine-McCluskey%20%E5%8C%96%E7%AE%80%E6%B3%95%20Part%202/slide_12.png)

Slide 12 — 从 EPI 出发选最简覆盖

- $m_{15}$ 只被 $ABD$ 覆盖 → $ABD$ 是 EPI。
- $m_{10}$ 只被 $A\bar B C\bar D$ 覆盖 → 也是 EPI。
- $m_3$ 只被 $\bar A\bar B D$、$m_4/m_{12}$ 只被 $B\bar C$ 覆盖 → 均为 EPI。
- $\bar A\bar C D$（1,5）的两个 minterm 已被前面的 PI 覆盖 → **多余，可删**。

$$
X=B\bar C+\bar A\bar B D+ABD+A\bar B C\bar D
$$

<aside>
🔑

**五步口诀：** 写 SOP → 按 1 的个数分组 → 相邻只差 1 bit 合并（差异位记 `x`，打勾）→ 取未打勾项为 PI → 列 PI 表，先锁 EPI、再补最少 PI 覆盖剩余 minterm。

</aside>

# 📝 三、完整练习：$f(a,b,c,d)=\sum m(0,1,2,5,6,7,8,9,10,14)$（slides 13–20）

## 6️⃣ 分组 → 逐级合并 → 得到全部 PI（slides 13–16）

同样按 1 的个数分组（Group 0–3），逐级两两合并、差异位记 `-`，最后得到 6 个 Prime Implicant：

![Slide 16 — 逐级合并直到得到全部 PI](EE115B%20Lecture5%20%E2%80%94%20Quine-McCluskey%20%E5%8C%96%E7%AE%80%E6%B3%95%20Part%202/slide_16.png)

Slide 16 — 逐级合并直到得到全部 PI

| 立方 (cube) | 覆盖 minterms | 乘积项 |
| --- | --- | --- |
| `0-01` | 1, 5 | $\bar a\bar c d$ |
| `01-1` | 5, 7 | $\bar a b d$ |
| `011-` | 6, 7 | $\bar a b c$ |
| `-00-` | 0, 1, 8, 9 | $\bar b\bar c$ |
| `-0-0` | 0, 2, 8, 10 | $\bar b\bar d$ |
| `--10` | 2, 6, 10, 14 | $c\bar d$ |

## 7️⃣ Prime Implicant Chart 选择（slides 17–18）

![Slide 17 — Prime Implicant Chart](EE115B%20Lecture5%20%E2%80%94%20Quine-McCluskey%20%E5%8C%96%E7%AE%80%E6%B3%95%20Part%202/slide_17.png)

Slide 17 — Prime Implicant Chart

- **Iteration 1（先锁 EPI）：** $m_9$ 只被 $\bar b\bar c$ 覆盖、$m_{14}$ 只被 $c\bar d$ 覆盖 → 这两个是 **EPI**。
- **Iteration 2（补剩余）：** 锁定后 $m_5,m_7$ 仍未覆盖；可选 Option 1 = $(1,5)+(6,7)$ 或 Option 2 = $(5,7)$ —— 选一个 PI 的 Option 2 更省，即补 $\bar a b d$。

![Slide 18 — 从 EPI（实线）到补齐剩余（虚线）](EE115B%20Lecture5%20%E2%80%94%20Quine-McCluskey%20%E5%8C%96%E7%AE%80%E6%B3%95%20Part%202/slide_18.png)

Slide 18 — 从 EPI（实线）到补齐剩余（虚线）

## 8️⃣ 最简覆盖 + 一致性定理互证（slides 19–20）

共需 3 个 prime implicant 覆盖 $f$：

$$
f=\bar a b d+\bar b\bar c+c\bar d
$$

注意 $\bar a b d$ **不是** EPI（$m_5,m_7$ 也能被别的 PI 覆盖，$\bar a\bar c d$ 与 $\bar a b c$ 也可替代）—— 但换了就得不到最小 SOP。

同一结果也能用 **一致性定理（consensus）** $AB+\bar A C+BC=AB+\bar A C$ 反复吸收冗余项得到：

$$
f=\bar a\bar c d+\bar a b d+\bar a b c+\bar b\bar c+\bar b\bar d+c\bar d\ \longrightarrow\ f=\bar a b d+\bar b\bar c+c\bar d
$$

<aside>
⚖️

**重点：** Q-M 的 PI 表法与布尔代数的 consensus 化简殊途同归；Q-M 的优势是"流程固定、可编程、对多变量友好"，代价是项数多时表会变大。

</aside>

# 🧰 四、仿真工具 & 阅读材料（slides 21–24）

- **阅读：** ① [github.com/int-main/Quine-McCluskey（Q-M](http://github.com/int-main/Quine-McCluskey（Q-M) 的代码实现）；② *Digital Fundamentals*, Book 4-11, p.237。
- **Logisim**（免费开源逻辑仿真）：[cburch.com/logisim](http://cburch.com/logisim) ；evolution 版 [github.com/logisim-evolution/logisim-evolution](http://github.com/logisim-evolution/logisim-evolution) 。
- **TINA-TI**（TI 出品、基于 SPICE 的模拟仿真，免费）：[ti.com.cn/tool/cn/TINA-TI](http://ti.com.cn/tool/cn/TINA-TI) 。
- **MultiSim**（商业软件）：[multisim.com](http://multisim.com) 。

# 🔁 五、考前回忆卡：用期中 Problem 10 默写五步法

<aside>
🐈

用期中最后一题 $F(A,B,C,D)=\sum m(0,2,5,6,7,8,10,13,15)$ 把五步法默写一遍：先盖住答案自己做，再回来对。

</aside>

## 1️⃣ Step 1 — 转二进制，按「1 的个数」分组

把每个 minterm 写成 4 位二进制（ABCD），按里面 1 的个数分层（只有相邻组才可能合并）。

| 组（1 的个数） | minterms（二进制 ABCD） |
| --- | --- |
| 0 个 | 0 = 0000 |
| 1 个 | 2 = 0010；8 = 1000 |
| 2 个 | 5 = 0101；6 = 0110；10 = 1010 |
| 3 个 | 7 = 0111；13 = 1101 |
| 4 个 | 15 = 1111 |

## 2️⃣ Step 2 — 相邻组两两合并（第一级）

相邻组里只差 1 个 bit 的两项合并，差异位记 `-`，两个原项都打勾 ✓（依据吸收律 $XY+X\bar Y=X$）。

例如：(0,2)→`00-0`、(0,8)→`-000`、(2,10)→`-010`、(8,10)→`10-0`、(2,6)→`0-10`、(5,7)→`01-1`、(5,13)→`-101`、(6,7)→`011-`、(7,15)→`-111`、(13,15)→`11-1`。

## 3️⃣ Step 3 — 再合并到合不动 → 没打勾的就是全部 PI

第二级：`00-0`+`10-0`→ `-0-0`；`01-1`+`11-1`→ `-1-1`。合不动且没被打勾的项即 Prime Implicant：

| PI (cube) | 盖哪些 minterm | 乘积项 |
| --- | --- | --- |
| `-0-0` | 0, 2, 8, 10 | $\bar B\bar D$ |
| `-1-1` | 5, 7, 13, 15 | $BD$ |
| `0-10` | 2, 6 | $\bar A C\bar D$ |
| `011-` | 6, 7 | $\bar A BC$ |

## 4️⃣ Step 4 — 列 PI 表，先锁 EPI（列里只有一个勾）

- m0 / m8 / m10 只被 $\bar B\bar D$ 盖 → $\bar B\bar D$ 是 EPI。
- m5 / m13 / m15 只被 $BD$ 盖 → $BD$ 是 EPI。

## 5️⃣ Step 5 — 数「还剩谁没盖」，补最少 PI

锁完两个 EPI 后，只剩 **m6** 没盖；m6 能被 $\bar A C\bar D$ 或 $\bar A BC$ 覆盖 → 二选一补一个即可：

$$
F=\bar B\bar D+BD+\bar A C\bar D
$$

<aside>
🔑

**默写口诀：** 写 SOP → 按 1 的个数分组 → 相邻差 1 bit 合并（记 `-`、打勾）→ 没打勾的就是全部 PI → 列 PI 表，先锁 EPI、再数剩谁、补最少 PI。

</aside>

<aside>
⚠️

**期中失分点（务必记住）：** Step 5 数完只剩 m6，却把 $\bar A C\bar D$ 和 $\bar A BC$ 两个等价 PI 都写上 → 多了一个冗余项，没达到 minimal SOP 被扣分。**只差一个 minterm 就只补一个 PI；交卷前逐项试删，删掉后仍能盖全的就是冗余项。**

</aside>

## 🎯 本节总结

<aside>
🎯

1. **为什么用 Q-M：** K-map 超过 5 变量难画、不可编程；Q-M 用列表把化简变成固定流程。
2. **五步法：** SOP → 按 1 的个数分组 → 相邻只差 1 bit 合并（记 `x`/`-`、打勾）→ 未打勾项 = 全部 PI → PI 表先锁 EPI 再补最少覆盖。
3. **EPI 判据 + 最小性：** 列里只有一个勾 ⇒ 该 PI 是 EPI 必留；找全 PI 不等于最简，PI 表那一步才保证最小 SOP（与 consensus 化简一致）。
</aside>

## ✅ 作业 / 待办

- 本节 slides **未单独布置 Homework / 考试**，没有新的 DDL。
- [ ]  用 Q-M 复算一遍练习 $f=\sum m(0,1,2,5,6,7,8,9,10,14)$，并与 K-map 结果对照，确认 $f=\bar a b d+\bar b\bar c+c\bar d$。
- [ ]  选做：clone [github.com/int-main/Quine-McCluskey，跑一个](http://github.com/int-main/Quine-McCluskey，跑一个) 4 变量例子验证手算。

## 📎 原始 Slides

[lecture_5_part2.pdf](EE115B%20Lecture5%20%E2%80%94%20Quine-McCluskey%20%E5%8C%96%E7%AE%80%E6%B3%95%20Part%202/lecture_5_part2.pdf)
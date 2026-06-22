# EE115B Lecture5 — Boolean Algebra & Logic Simplification Part 1

<aside>
🗺️

**本节主题：** Boolean Algebra & Logic Simplification Part 1 —— SOP / POS 标准型 + **卡诺图 Karnaugh Map** 化简。

**参考教材：** *Digital Fundamentals* Ch.4（Boolean Algebra & Logic Simplification）；K-map 部分对应 Figure 4-46 / 4-47。

**核心脉络：** 复习器件 → SOP / POS 标准型（minterm / maxterm）→ 真值表 ↔ SOP / POS → 卡诺图（gray code 排列）→ 圈组化简（groups of 2/4/8）→ don't care → SOP / POS 化简练习 → POS↔SOP 转换。

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md) ｜ 本节为 **Lecture5 Part 1**；Part 2 = Quine-McCluskey 化简法见 [EE115B Lecture5 — Quine-McCluskey 化简法 Part 2](EE115B%20Lecture5%20%E2%80%94%20Quine-McCluskey%20%E5%8C%96%E7%AE%80%E6%B3%95%20Part%202.md)（K-map 不够用时的可编程升级版）。

</aside>

## 🔁 开篇回顾（slides 2–8）

本节正文前先快速复习了前几讲的器件与门电路（不展开，详见对应 Lecture）：

- **PN 结二极管**：正向导通、反向截止、击穿区。
- **BJT 开关**：$V_{BE}>0.7\text{V}$ 导通(ON)，$<0.7\text{V}$ 截止(OFF)；TTL 反相器。
- **MOSFET / CMOS**：n / p 沟道作开关；CMOS 反相器（上拉 PMOS + 下拉 NMOS）；NAND / NOR 的晶体管级实现。
- **其他**：Open Collector / Open Drain、Tristate（三态）门、Fan-out、Source / Sink Current。

<aside>
🧭

这些是**器件层**的铺垫；从 slide 9 起进入本节真正主题 —— **逻辑层的代数化简**。

</aside>

# 1️⃣ SOP 与 POS 标准型（slides 9–16）

任何布尔表达式都能写成两种规范形式之一：

| 维度 | SOP（Sum of Products） | POS（Product of Sums） |
| --- | --- | --- |
| 结构 | **乘积项**之**和**（积之或） | **求和项**之**积**（和之与） |
| 标准型 | 每个乘积项含**全部变量** = **minterm** $m_i$ | 每个求和项含**全部变量** = **maxterm** $M_i$ |
| 真值表来源 | 枚举输出 **=1** 的行 | 枚举输出 **=0** 的行 |
| K-map 圈法 | 圈 **1**，写 SOP | 圈 **0**，写 POS |

**约束：** SOP 中单个上划线不能跨越多个变量（$\overline{AB}\neq\bar A\bar B$）。

## 🔹 化为标准型（补全缺失变量）

- **SOP**：对缺变量 $X$ 的乘积项乘以 $(X+\bar X)=1$，逐步展开。

$$
A\bar B C = A\bar B C\,(D+\bar D) = A\bar B C D + A\bar B C\bar D
$$

- **POS**：对缺变量 $X$ 的求和项加上 $X\bar X=0$，再用分配律 $(A+BC)=(A+B)(A+C)$ 展开。

$$
A+\bar B+C = A+\bar B+C+D\bar D = (A+\bar B+C+D)(A+\bar B+C+\bar D)
$$

## 🔹 minterm / maxterm 的二进制编码

- **minterm** $m_i$：变量取值 **1→原变量、0→反变量**。例 $A\bar B C\bar D = 1010 = m_{10}$。
- **maxterm** $M_i$：规则相反，**0→原变量、1→反变量**（求和项中"补"记为 1）。例 $A+\bar B+C+\bar D = 0101 = M_5$。

<aside>
🔁

**SOP ↔ POS 互换（取补思想）：** $\overline{m_i}=M_i$。某函数取它**没出现的 minterm**，再 DeMorgan 即得对偶形式。
例：$f=\sum m(0,2,3,5,7)$ → 缺 $m_1,m_4,m_6$ → $f=\overline{m_1+m_4+m_6}=M_1M_4M_6$。

</aside>

# 2️⃣ 真值表 ↔ SOP / POS（slides 17–18）

**SOP：枚举所有输出为 1 的行**，每行写一个 minterm 再求和。

![Slide 17 — 真值表枚举 1 → SOP 实现](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_17.png)

Slide 17 — 真值表枚举 1 → SOP 实现

上图 $F=\bar A\bar B C+\bar A B C+A\bar B C$（即 $m_1+m_3+m_5$）。

**POS：枚举所有输出为 0 的行**，每行写一个 maxterm 再求积。

![Slide 18 — 真值表枚举 0 → POS 实现](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_18.png)

Slide 18 — 真值表枚举 0 → POS 实现

同一张真值表，输出为 0 的行给出 $F=(\bar A+\bar B+\bar C)(\bar A+\bar B+C)(\bar A+B+C)(A+\bar B+C)(A+B+C)$。两种写法**等价**，只是分别盯着 1 或 0。

# 3️⃣ 卡诺图 Karnaugh Map 基础（slides 19–23）

<aside>
📖

**K-map = 化简的 "cookbook"：** 用**相邻性 (adjacency)** 自动完成 $X+\bar X=1$ 的合并。**仅适用于 ≤ 4 个变量**（5 变量及以上太难画 → 用 Part 2 的 Quine-McCluskey）。

</aside>

![Slide 19 — 3 变量与 4 变量 K-map 结构](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_19.png)

Slide 19 — 3 变量与 4 变量 K-map 结构

**关键：行 / 列用格雷码 (Gray code) 排列**，保证相邻格只差 1 个变量 → 物理相邻 = 逻辑可合并。

![Slide 20 — 格雷码标号与读法](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_20.png)

Slide 20 — 格雷码标号与读法

- 格 = 1 → 读**原变量**；格 = 0 → 读**反变量**。
- 标准 SOP：每个 minterm 在对应格填 1；非标准 SOP：先展开成 minterm 再填；也可**直接从真值表**填图。

# 4️⃣ 化简 = 圈组 Grouping（slides 24–27）

![Slide 24 — Groups of 2 / 4 的圈法](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_24.png)

Slide 24 — Groups of 2 / 4 的圈法

**圈组规则：**

1. 圈的大小必须是 **2 的幂**（1, 2, 4, 8 …）。
2. 圈**越大越好**（消去的变量越多），且数量越少越好。
3. 每个圈读法：**消去"跨边界发生变化"的变量**，保留不变的变量。
4. 允许重叠、允许**环绕边界**（上下 / 左右相接）。

![Slide 25 — 4 变量 map 的四周环绕相邻](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_25.png)

Slide 25 — 4 变量 map 的四周环绕相邻

4 变量图四条边都各有"环绕邻居"，最外圈与最内圈在拓扑上相邻。

**例：圈 1 读最简逻辑**

![Slide 27 — 圈组实例 X = ĀD̄ + AD](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_27.png)

Slide 27 — 圈组实例 X = ĀD̄ + AD

上方黄组 $B,C$ 变化被消去 → $\bar A\bar D$；下方绿组 → $AD$，故

$$
X=\bar A\,\bar D+AD
$$

# 5️⃣ Don't care 无关项（slide 28）

<aside>
❓

**Don't care（记 "X"）：** 永远不会出现、或不关心输出的输入组合。圈组时可**自由当作 1 或 0**，哪种让圈更大就取哪种 —— 是化简的免费弹药。

</aside>

![Slide 28 — BCD 码的 don't care 化简](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_28.png)

Slide 28 — BCD 码的 don't care 化简

例：BCD 输入，$Y=\sum m(7,8,9)+d(10,11,12,13,14,15)$。

$$
Y_{\text{不用 don't care}}=A\bar B\bar C+\bar A BCD
\qquad\Longrightarrow\qquad
Y_{\text{用 don't care}}=A+BCD
$$

# 6️⃣ SOP 化简练习（slides 29–32）

## 练习一：最简结果不唯一

$$
Y(A,B,C)=A\bar C+\bar A C+\bar B C+B\bar C
$$

![Slide 30 — 两种等价最简 SOP](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_30.png)

Slide 30 — 两种等价最简 SOP

同一张图、不同圈法得到两个**都最简**的解：

$$
A\bar B+\bar A C+B\bar C \qquad\text{或}\qquad A\bar C+\bar A B+\bar B C
$$

<aside>
⚖️

**结论不唯一，但项数与每项变量数相同。** 最简解可能有多个，复杂度等价。

</aside>

## 练习二：圈 0 法（work on 0's）

$$
Y=ABC+ABD+A\bar C D+\bar C\bar D+A\bar B C+\bar A C\bar D
$$

![Slide 32 — 通过补函数 Y' 求 Y](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_32.png)

Slide 32 — 通过补函数 Y' 求 Y

直接圈 1 很碎时，改**圈 0 求补函数** $Y'$ 再取反：

$$
Y'=\bar A D \;\Longrightarrow\; Y=\overline{Y'}=A+\bar D
$$

（此法成立的前提：$Y'$ 恰好是**单个乘积项**，取反后才仍是 SOP。）

# 7️⃣ POS 化简 & POS ↔ SOP 转换（slides 33–37）

**POS 化简：圈 0**，每个 0 圈写成求和项之积。

![Slide 33 — 圈 0 得最简 POS](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_33.png)

Slide 33 — 圈 0 得最简 POS

$$
\text{最简 POS: } A(\bar B+C)\qquad\text{最简 SOP（圈 1）: } AC+A\bar B
$$

**一张图同时拿到四种型：** 标准/最简 POS、标准/最简 SOP。

![Slide 36 — POS ↔ SOP 完整转换](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/slide_36.png)

Slide 36 — POS ↔ SOP 完整转换

- (a) 圈 0 → 最简 POS：$(A+B+\bar C)(\bar B+C+D)(B+C+\bar D)$
- (b) 给非 0 格补 1 → 标准 SOP（一堆 minterm 之和）
- (c) 圈 1 → 最简 SOP：$AC+BC+BD+\bar B\bar C\bar D$

# 🎯 本节总结（记三点就够）

<aside>
🎯

1. **盯 1 写 SOP（圈 1）、盯 0 写 POS（圈 0）；** minterm 与 maxterm 编码规则互为反相（$\overline{m_i}=M_i$）。
2. **K-map 用格雷码排列**让相邻 = 可合并；圈大小取 2 的幂、越大越好、消去跨边界变量；善用 don't care 与环绕相邻。
3. **最简解不唯一但复杂度等价；** 1 太碎就圈 0 求补函数；K-map 仅限 ≤4 变量，更多变量交给 Part 2 的 Quine-McCluskey。
</aside>

## ✅ 作业 / 待办

- 本节 slides 未出现带日期的作业 / 考试 DDL（仅课堂练习），故未新建日历事件。
- [ ]  自测：把 slide 31 / 34 的练习独立做一遍（圈 1 求最简 SOP、圈 0 求最简 POS），再与 Part 2 的 Q-M 解法对照。

## 📎 原始 Slides

[lecture_5 part1-S13.pdf](EE115B%20Lecture5%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Simplifi/lecture_5_part1-S13.pdf)
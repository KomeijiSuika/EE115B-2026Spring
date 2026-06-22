# EE115B Lecture7 — Comparator · MUX / DEMUX · Hazard Part 3

<aside>
🔀

**本节主题：** Combinational Logic Part 3 —— 比较器 Comparator、多路复用 / 解复用 MUX & DEMUX、竞争冒险 Hazard。

**讲义来源：** EE115B（Chenxi Xiao），共 27 页；本节为该讲 **Part 3**。

**核心脉络：** 用 XNOR 判相等 → 数值比较器（>、=、<）→ 多位 / 级联比较器 → MUX 数据选择器 → DEMUX 数据分配器 → 74LS138 当 DEMUX → Hazard（静态 / 动态毛刺）→ 静态冒险的判定与消除。

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md)（组合逻辑部分，位于 HDL / FSM 的 Lecture8 与时序逻辑 Lecture9 之前）。

</aside>

# ⚖️ 一、Comparators 比较器

## 1️⃣ 相等比较：用 XNOR 判同（slides 3, 5）

比较器（comparator）用来比较两个二进制数的大小关系。最简单的形式是用 **XNOR 门测相等**：两位相同输出 1，不同输出 0。

$$
x = \overline{A \oplus B} = A \odot B \qquad\Rightarrow\qquad x = 1 \iff A = B
$$

![Slide 3 — 1-bit 相等比较器（XNOR + 真值表）](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard%20/slide_3.png)

Slide 3 — 1-bit 相等比较器（XNOR + 真值表）

多位相等：把每一位的 XNOR 结果再 **AND** 起来——全部位都相等，整体才相等。两位的情形：

$$
(A = B) = (A_1 \odot B_1)\,(A_0 \odot B_0)
$$

<aside>
💡

**口诀：** 「逐位 XNOR、再总 AND」。XNOR=同或，两位相同得 1；只要有一位不同，AND 就被拉成 0。

</aside>

四位相等的练习：四个 XNOR 的输出送进一个 4 输入 AND 门即可。

$$
\text{Output} = (A_1 \odot B_1)(A_2 \odot B_2)(A_3 \odot B_3)(A_4 \odot B_4)
$$

![Slide 5 — 4-bit 相等比较器（4×XNOR + AND）](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard%20/slide_5.png)

Slide 5 — 4-bit 相等比较器（4×XNOR + AND）

## 2️⃣ 1-bit 数值比较器：>、=、<（slide 6）

相等还不够，数值比较器要同时给出三种关系。对 1 位 $A$、$B$：

$$
Y_{A>B} = A\,\bar{B}, \qquad Y_{A=B} = A \odot B = \overline{A \oplus B}, \qquad Y_{A<B} = \bar{A}\,B
$$

![Slide 6 — 1-bit 数值比较器电路](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard%20/slide_6.png)

Slide 6 — 1-bit 数值比较器电路

<aside>
🧭

**理解：** 「$A$ 为 1 而 $B$ 为 0」⇒ $A>B$；反过来 $\bar A B$ ⇒ $A<B$；两者都不成立（即同或为 1）⇒ $A=B$。三个输出互斥且必有其一为 1。

</aside>

## 3️⃣ 多位比较：从 MSB 往下看（slide 7–9）

多位数值比较的关键思想：**从最高位 (MSB) 开始逐位比较**，高位一旦分出胜负，低位就不用看了。以 $A>B$ 为例（$A \to A_1 A_0$、$B \to B_1 B_0$）：

$$
Y(A>B) = A_1\bar{B}_1 \;+\; (A_1 \odot B_1)\,A_0\bar{B}_0
$$

含义：要么高位就 $A_1>B_1$；要么高位相等（$A_1 \odot B_1$）再看低位 $A_0>B_0$。$A<B$ 同理对称，$A=B$ 则是各位 XNOR 全 AND。

## 4️⃣ 级联比较器 Cascaded（slide 10）

现成 IC 比较器（如 74LS85）带有 **cascading inputs**（$A>B$、$A=B$、$A<B$ 三根级联输入），可把多片串起来扩展位宽。

![Slide 10 — 两片 4-bit 比较器级联成 8-bit](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard%20/slide_10.png)

Slide 10 — 两片 4-bit 比较器级联成 8-bit

- **接法：** 低位片（LSBs）处理 $A_0\text{–}A_3$，高位片（MSBs）处理 $A_4\text{–}A_7$；低位片的三个输出接到高位片的级联输入。
- **初始化：** 最低位片的级联输入要给 $A=B$ 端置 **HIGH**（接 +5.0 V），表示「在更低位之前默认相等」。
- **优先级：** 高位片优先——高位分出大小就直接决定整体，低位结果只在高位相等时才起作用。

<aside>
🔗

**口诀：** 级联比较「高位优先、相等下传」——最低片的 $A=B$ 拉高作种子，逐级把「目前为止是否相等」往高位传递。

</aside>

---

# 🔀 二、Multiplexers（MUX，数据选择器）

## 5️⃣ MUX 概念与表达式（slides 11–12）

**多路复用器 (MUX / data selector)：** 从多条数据输入里，按 **select lines** 选出一条接到输出。$n$ 根选择线 → 可选 $2^n$ 路输入。

4-to-1 MUX 的选择表（2 根选择线 $S_1 S_0$）：

| 选择 $S_1$ | 选择 $S_0$ | 输出 $Y$ |
| --- | --- | --- |
| 0 | 0 | $D_0$ |
| 0 | 1 | $D_1$ |
| 1 | 0 | $D_2$ |
| 1 | 1 | $D_3$ |

对应的布尔表达式（每个 minterm 选一路数据）：

$$
Y = D_0\,\bar{S}_1\bar{S}_0 + D_1\,\bar{S}_1 S_0 + D_2\,S_1\bar{S}_0 + D_3\,S_1 S_0
$$

## 6️⃣ 4-to-1 MUX 电路（slide 13）

![Slide 13 — 4-to-1 MUX 门级电路](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard%20/slide_13.png)

Slide 13 — 4-to-1 MUX 门级电路

电路结构：选择线 $S_1, S_0$ 经反相器产生 $\bar S_1, \bar S_0$；四个 AND 门各自把一路 $D_i$ 与对应的选择组合相与，最后一个 OR 门汇总。任一时刻只有被选中那路的 AND 为 1，其余被选择信号封掉。

<aside>
💡

**口诀：** MUX = 「译码选通 + 或汇总」。选择线译出 $2^n$ 个 AND，只开一扇门，OR 把它接到 $Y$。

</aside>

---

# 🔁 三、Demultiplexers（DEMUX，数据分配器）

## 7️⃣ DEMUX 概念与电路（slides 14–17）

**解复用器 (DEMUX / data distributor)：** 功能与 MUX 相反——把**一条**数据输入，按选择线送到 $2^n$ 条输出线中的某一条，其余输出保持无效。

$$
D_i = \text{Data} \cdot m_i(S) \qquad (m_i \text{ 为第 } i \text{ 个选择 minterm})
$$

![Slide 16 — 4-bit DEMUX 门级电路（AND 选通）](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard%20/slide_16.png)

Slide 16 — 4-bit DEMUX 门级电路（AND 选通）

实现思路（slide 15 的 hint）：用 AND 门「放行」——每个输出 AND 门的输入 = 数据线 + 该输出对应的选择译码（$S_1, S_0$ 经反相器组合），只有选中那一路的 AND 才让 Data 通过。

## 8️⃣ 74LS138 当 DEMUX 用（slides 18–21）

74LS138 本是 3-to-8 **译码器**，但把它的 **enable 输入当作数据输入**，就能当 1-to-8 DEMUX：数据从某个使能端进，按 $A_0 A_1 A_2$ 选址路由到对应输出。

![Slide 18 — 74LS138 作为 DEMUX 的引脚框图](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard%20/slide_18.png)

Slide 18 — 74LS138 作为 DEMUX 的引脚框图

<aside>
⚠️

**关键陷阱 — 输出 active-LOW：** 74LS138 的输出 $Y_0\text{–}Y_7$ 是**低有效**：被选中的那一路输出为 **0（L）**，其余维持 1（H）。看波形 / 算输出时别把高低搞反。使能 $G_1=H,\ \overline{G_{2A}}=\overline{G_{2B}}=L$ 时芯片才工作。

</aside>

---

# ⚡ 四、Hazard 竞争冒险

## 9️⃣ 什么是 Hazard（slides 22–23）

<aside>
⚡

**Hazard（冒险 / 毛刺）：** 由于不同信号路径的**传播延迟不相等**，输出端出现的**非预期瞬态 glitch**。它是组合逻辑的「时间病」——逻辑值算对了，但过渡瞬间会抖。

</aside>

两大类：

| 类型 | 本应 | 实际现象 |
| --- | --- | --- |
| **Static-1 hazard** | 输出保持 1 | 短暂掉一下：1 → 0 → 1 |
| **Static-0 hazard** | 输出保持 0 | 短暂跳一下：0 → 1 → 0 |
| **Dynamic hazard** | 输出做一次跳变 | 稳定前反复多跳几次 |

## 🔟 静态冒险的成因：race condition（slide 24）

![Slide 24 — 静态冒险：A 与 A′ 反相不同步导致毛刺](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard%20/slide_24.png)

Slide 24 — 静态冒险：A 与 A′ 反相不同步导致毛刺

经典例子 $A \wedge \bar{A}$：理论恒为 0，但因为反相器有延迟 $\Delta t_1$，$\bar A$ 的下降比 $A$ 的上升晚一拍，于是在 $\Delta t_1$ 这段时间里 $A$ 和 $\bar A$ **同时为 1**，AND 输出冒出一个宽约 $\Delta t_1 + \Delta t_2$ 的尖峰。这就是「竞争 (race)」：互补信号没能同时翻转。

## 1️⃣1️⃣ 判定与消除：F = A + A′B（slides 25–27）

以 $F = A + \bar{A}B$ 为例，看是否存在静态冒险、怎么修。

**Step 1 — 化成 SOP，找互补变量。** 表达式里同时含 $A$ 与 $\bar A$ ⇒ 可能有冒险，重点查 $B=1$ 的情形。

**Step 2 — 测试冒险。** 令 $B=1$，则 $F = A + \bar A$。当 $A$ 由 0→1：第一项 $A$ 走 0→1，第二项 $\bar A B$ 走 1→0；若两项不同时切换，$F$ 就会在 1→1 的过程中瞬间掉到 0 —— **static-1 hazard**。

**Step 3 — 修复（加冗余项）。** 利用一致性定理：

$$
AB + \bar{A}C = AB + \bar{A}C + BC
$$

那个多出来的 $BC$ **不受** $A$ **影响**，能在 $A$ 翻转时「兜住」输出。本例补上后：

$$
F = A + \bar{A}B = A + \bar{A}B + B = A + B \quad(\text{无冒险})
$$

<aside>
🛡️

**消冒险口诀：** 在卡诺图上，凡是**相邻但没被同一个圈覆盖**的两个 1，就补一个把它们盖在一起的冗余项（consensus term）。这个不随输入翻转的「安全项」就能填掉毛刺。

</aside>

---

## 📝 本节总结（记三点就够）

<aside>
🎯

1. **比较器：** 相等用「逐位 XNOR、再总 AND」；数值比较 $Y_{A>B}=A\bar B$、$Y_{A<B}=\bar A B$、$Y_{A=B}=A\odot B$；多位 / 级联「高位优先、相等下传」，最低片 $A=B$ 端置高作种子。
2. **MUX / DEMUX 互逆：** MUX = 多入一出「译码选通 + OR 汇总」$Y=\sum D_i m_i(S)$；DEMUX = 一入多出，$D_i=\text{Data}\cdot m_i(S)$；74LS138 当 DEMUX 时**输出低有效**。
3. **Hazard：** 路径延迟不等 → 毛刺；static-1 是 1→0→1、static-0 是 0→1→0；判定看互补变量，消除靠补**冗余一致项**（卡诺图上把相邻孤立的 1 圈进来）。
</aside>

## ✅ 作业 / 待办

- 本节 slides 未给出明确的 Homework / 考试 deadline；拿到 syllabus 后再补 Lab / HW 截止时间。
- [ ]  练习：用卡诺图给 $F = \bar A C + A\bar C$（或课上指定式）判定并消除静态冒险。

## 📎 原始 Slides

[lecture_7_part3.pdf](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard%20/lecture_7_part3.pdf)
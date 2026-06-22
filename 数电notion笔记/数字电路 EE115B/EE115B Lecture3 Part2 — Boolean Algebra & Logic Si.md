# EE115B Lecture3 Part2 — Boolean Algebra & Logic Simplification 布尔代数与化简

<aside>
📐

**本节主题：** Boolean Algebra(布尔代数) —— 逻辑函数的三种表示、三大基本定律、12 条化简规则、DeMorgan(德摩根) 定理与布尔表达式化简。

**参考教材：** Floyd《Digital Fundamentals》Ch.4，TABLE 4–1（规则总表）、TABLE 4–2（Rule 10 验证）。

**核心脉络：** 逻辑门 ↔ 布尔表达式 ↔ 真值表 ↔ 电路 → 交换 / 结合 / 分配律 → 12 条规则 → DeMorgan → 综合化简（用更少的门实现同一逻辑）。

</aside>

## 1⃣ Review：逻辑门 ↔ 布尔表达式

每种逻辑门都能用一个布尔表达式(Boolean statement)描述：

| 门 Gate | 布尔表达式 |
| --- | --- |
| AND | $X = A\cdot B$ |
| OR | $X = A + B$ |
| NAND | $X = \overline{A\cdot B}$ |
| NOR | $X = \overline{A + B}$ |
| XOR | $X = A \oplus B$ |
| XNOR | $X = \overline{A \oplus B}$ |
| NOT | $X = \overline{A}$ |

![Slide 3 — ANSI / IEC 门符号与布尔表达式对照](EE115B%20Lecture3%20Part2%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Si/slide_3.png)

Slide 3 — ANSI / IEC 门符号与布尔表达式对照

### 位操作 Bit Manipulation

用逻辑门对某一位(bit)做精确操作，是嵌入式 / Verilog 里的常用技巧：

- **Set bit(置 1)：** 与掩码 **OR 1** —— $x \,|\, 1 = 1$。
- **Clear bit(清 0)：** 与掩码 **AND 0** —— $x \,\&\, 0 = 0$。
- **Invert bit(取反)：** **NOT** 或 **XOR 1** —— $x \oplus 1 = \overline{x}$。

<aside>
🧠

**口诀：** 想动哪一位，就把掩码对应位设好——**OR 置位、AND 清位、XOR 翻位**；其余位的掩码取“不变元”（OR / XOR 用 0、AND 用 1）保持不动。

</aside>

- 📚 拓展 — XOR 1 为什么能翻位？
    - $x \oplus 0 = x$（与 0 异或保持不变），$x \oplus 1 = \overline{x}$（与 1 异或翻转）。
    - 用一个掩码就能“选择性翻转”：掩码为 1 的位翻转、为 0 的位不变——图形 / 加密里的 XOR 技巧就源于此。

## 2⃣ 一个逻辑函数的三种表示

同一个逻辑函数可用**布尔表达式 ↔ 真值表 ↔ 逻辑电路**三种等价方式表示、互相转换。以 $A(B + CD)$ 为例：

<aside>
🧩

**关键思想：** 三者完全等价。**表达式**便于代数化简，**真值表**便于穷举验证，**电路**便于硬件实现——化简的目标就是在保持真值表不变的前提下，让表达式 / 电路更简单。

</aside>

## 3⃣ XOR / XNOR 的门级构造

用与 / 或 / 非门可以搭出 XOR、XNOR：

$$
X_{\text{XOR}} = \overline{A}B + A\overline{B} = A \oplus B
$$

$$
X_{\text{XNOR}} = \overline{A}\,\overline{B} + AB = \overline{A \oplus B}
$$

| A | B | XOR | XNOR |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

<aside>
🧠

**记忆：** XOR =「**不同**为 1」，XNOR =「**相同**为 1」（即同或 / 比较器）。

</aside>

## 4⃣ 三大基本定律

| 定律 | 加法 (OR) | 乘法 (AND) |
| --- | --- | --- |
| 交换律 Commutative | $A + B = B + A$ | $AB = BA$ |
| 结合律 Associative | $A + (B + C) = (A + B) + C$ | $A(BC) = (AB)C$ |

分配律 Distributive 是“**因式分解 factoring**”的依据：

$$
AB + AC = A(B + C)
$$

![Slide 10 — 分配律的等价电路](EE115B%20Lecture3%20Part2%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Si/slide_10.png)

Slide 10 — 分配律的等价电路

<aside>
💡

**工程意义：** 分配律 = “提取公共因子”——把 $AB+AC$（2 个 AND + 1 个 OR）变成 $A(B+C)$（1 个 OR + 1 个 AND），**省一个门**。这是逻辑化简省面积 / 功耗最朴素的来源。

</aside>

## 5⃣ 布尔代数 12 条规则

| # | 规则 | # | 规则 |
| --- | --- | --- | --- |
| 1 | $A + 0 = A$ | 7 | $A\cdot A = A$ |
| 2 | $A + 1 = 1$ | 8 | $A\cdot \overline{A} = 0$ |
| 3 | $A\cdot 0 = 0$ | 9 | $\overline{\overline{A}} = A$ |
| 4 | $A\cdot 1 = A$ | 10 | $A + AB = A$ |
| 5 | $A + A = A$ | 11 | $A + \overline{A}B = A + B$ |
| 6 | $A + \overline{A} = 1$ | 12 | $(A+B)(A+C) = A + BC$ |

<aside>
🔑

**三条带 * 的考点：** Rule 10 吸收律 $A+AB=A$、Rule 11 $A+\overline{A}B=A+B$、Rule 12 $(A+B)(A+C)=A+BC$。化简时优先扫描这三种模式。

</aside>

### Rule 10 证明与验证：$A + AB = A$

$$
A + AB = A\cdot 1 + AB = A(1 + B) = A\cdot 1 = A
$$

依次用 Rule 4 提取 $A$、Rule 2 $(1+B)=1$、Rule 4 $A\cdot 1=A$。真值表(TABLE 4–2)里 $A$ 与 $A+AB$ 两列完全相同：

| A | B | AB | A + AB |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 |

## 6⃣ Rule 11 & 12 的代数证明

**Rule 11：** $A + \overline{A}B = A + B$

$$
\begin{aligned}
A + \overline{A}B &= (A + AB) + \overline{A}B \\
&= (AA + AB) + \overline{A}B \\
&= AA + AB + A\overline{A} + \overline{A}B \\
&= (A + \overline{A})(A + B) \\
&= 1\cdot(A + B) = A + B
\end{aligned}
$$

**Rule 12：** $(A + B)(A + C) = A + BC$

$$
\begin{aligned}
(A + B)(A + C) &= AA + AC + AB + BC \\
&= A + AC + AB + BC \\
&= A(1 + C) + AB + BC \\
&= A\cdot 1 + AB + BC \\
&= A(1 + B) + BC \\
&= A\cdot 1 + BC = A + BC
\end{aligned}
$$

## 7⃣ DeMorgan 定理

![Slide 18 — DeMorgan：NAND ≡ Negative-OR，NOR ≡ Negative-AND](EE115B%20Lecture3%20Part2%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Si/slide_18.png)

Slide 18 — DeMorgan：NAND ≡ Negative-OR，NOR ≡ Negative-AND

$$
\overline{XY} = \overline{X} + \overline{Y} \quad(\text{第一定理})\qquad \overline{X + Y} = \overline{X}\,\overline{Y}\quad(\text{第二定理})
$$

口诀：「**断线、变号**」——把长非线断开，每个变量取反，同时 **AND ↔ OR 互换**。由此得到门的等价：**NAND ≡ Negative-OR**、**NOR ≡ Negative-AND**。

- 📚 拓展 — 3 变量及多变量 DeMorgan
    - 推广：$\overline{XYZ} = \overline{X} + \overline{Y} + \overline{Z}$，$\overline{X+Y+Z} = \overline{X}\,\overline{Y}\,\overline{Z}$。
    - 一般形式：对整个表达式取反 = 把所有 $\cdot$ 与 $+$ 互换、每个变量取反。这是把任意逻辑转成 **NAND-only / NOR-only** 实现的基础。

## 8⃣ 综合练习：布尔化简

### 练习 1（易错陷阱）：$\overline{A}\,\overline{B} \stackrel{?}{=} \overline{AB}$

**不相等！** 由 DeMorgan：

$$
\overline{A}\,\overline{B} = \overline{A + B} \ne \overline{AB} = \overline{A} + \overline{B}
$$

<aside>
⚠️

**最常见错误：** 把长非线“逐项分配”。**非号不能直接分配到每个变量**——必须用 DeMorgan 同时改运算符。$\overline{A}\,\overline{B}$ 等于 $\overline{A+B}$，**不是** $\overline{AB}$。

</aside>

### 练习 2：化简 $\overline{AB + AC} + \overline{A}\,\overline{B}C$

$$
\begin{aligned}
\overline{AB + AC} + \overline{A}\,\overline{B}C &= (\overline{AB})(\overline{AC}) + \overline{A}\,\overline{B}C &&\text{DeMorgan}\\
&= (\overline{A}+\overline{B})(\overline{A}+\overline{C}) + \overline{A}\,\overline{B}C &&\text{DeMorgan}\\
&= \overline{A}\,\overline{A} + \overline{A}\,\overline{C} + \overline{A}\,\overline{B} + \overline{B}\,\overline{C} + \overline{A}\,\overline{B}C &&\text{分配律}\\
&= \overline{A} + \overline{A}\,\overline{C} + \overline{A}\,\overline{B} + \overline{B}\,\overline{C} &&\text{Rule 7, 10}\\
&= \overline{A} + \overline{B}\,\overline{C} &&\text{Rule 10}
\end{aligned}
$$

最终结果：$\overline{A} + \overline{B}\,\overline{C}$。

<aside>
🧠

**化简套路：** ① 先用 DeMorgan 把长非线拆开；② 用分配律展开；③ 用吸收律 Rule 10 / Rule 7 反复吃掉冗余项。Floyd 原话：化简靠 **熟练 + 大量练习 + 一点巧思**，没有唯一路径。

</aside>

## 🎯 本节总结

<aside>
📐

1. **三种表示等价：** 表达式 ↔ 真值表 ↔ 电路；化简 = 真值表不变、表达式 / 电路更省门。
2. **三大律 + 12 规则：** 重点 Rule 10 吸收 $A+AB=A$、Rule 11 $A+\overline{A}B=A+B$、Rule 12 $(A+B)(A+C)=A+BC$。
3. **DeMorgan「断线变号」：** $\overline{XY}=\overline{X}+\overline{Y}$、$\overline{X+Y}=\overline{X}\,\overline{Y}$；非号绝不能逐项分配。
</aside>

<aside>
🐈

**下次打开第一步：** 盖住右列默写 12 条规则；再把 $\overline{AB+AC}+\overline{A}\,\overline{B}C$ 从头化简到 $\overline{A}+\overline{B}\,\overline{C}$，卡壳就回看第 8 节套路。

</aside>

## 📎 原始 Slides

[lecture_3_part2.pdf](EE115B%20Lecture3%20Part2%20%E2%80%94%20Boolean%20Algebra%20&%20Logic%20Si/lecture_3_part2.pdf)
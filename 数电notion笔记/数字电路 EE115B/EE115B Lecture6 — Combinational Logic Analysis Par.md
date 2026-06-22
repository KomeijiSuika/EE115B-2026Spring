# EE115B Lecture6 — Combinational Logic Analysis Part 1

<aside>
⚙️

**本节主题：** 组合逻辑分析 Combinational Logic Analysis（Digital Fundamentals Ch.5）—— 从布尔表达式到门级电路，并用通用门 NAND / NOR 实现任意组合逻辑。

**核心脉络：** 组合逻辑定义 → SOP→AND-OR / POS→AOI → XOR·XNOR → 真值表→电路 → 通用门 NAND/NOR → 德摩根可视化转换 → 把任意 AND-OR-NOT 电路转成纯 NAND / 纯 NOR → 仿真工具（Logisim / TINA）

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md) ｜ 本节为 **Lecture6 Part 1**；组合逻辑的延伸见 [EE115B Lecture7 — Adders & ALU Part 1](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201.md)。

</aside>

## 🔁 开篇回顾（slides 3–4）

- **K-map 术语链：** Implicant（蕴涵项，使 $F=1$ 的乘积项）→ Prime Implicant（不可再化简）→ Essential PI（覆盖只能以一种方式分组的 1）→ Cover（覆盖所有 1 的 PI 集合）。
- **Quine–McCluskey 表格法：** ① 写成 SOP / 最小项 → ② 按「1 的个数」分组、比较相邻组合并相邻项、迭代 → ③ 用质蕴涵表去掉非必要 PI。是 K-map 的程序化替代（变量多时更好用）。在线工具：[https://atozmath.com/KMap.aspx](https://atozmath.com/KMap.aspx)

# ⚙️ 一、组合逻辑与两种标准实现

## 1️⃣ 什么是组合逻辑（slides 2, 5）

> 组合逻辑 (Combinational Logic)：输出**只由当前输入决定**，不含任何对过去输入的记忆（无存储元件）。与时序电路（FSM / 触发器）正相反。
> 

任何逻辑函数都能写成两种标准式，并各自对应一种标准电路：

| 标准式 | 电路结构 | 表达式形态 |
| --- | --- | --- |
| SOP（积之和） | **AND-OR** | 式 $X=AB+CD$ |
| POS（和之积） | **AND-OR-Invert (AOI)** | 式 $X=(\bar A+\bar B)(\bar C+\bar D)$ |

## 2️⃣ SOP → AND-OR（slide 6）

![Slide 6 — AND-OR 实现 SOP](EE115B%20Lecture6%20%E2%80%94%20Combinational%20Logic%20Analysis%20Par/slide_06.png)

Slide 6 — AND-OR 实现 SOP

- 每个乘积项用一个 **AND 门**，再用一个 **OR 门**求和：$X = AB + CD$。
- 右下角是 ANSI 矩形轮廓符号（`&` = AND，`≥1` = OR），与左侧特异形状符号等价。

## 3️⃣ 异或 / 同或（slide 7）

![Slide 7 — XOR 与 XNOR 逻辑](EE115B%20Lecture6%20%E2%80%94%20Combinational%20Logic%20Analysis%20Par/slide_07.png)

Slide 7 — XOR 与 XNOR 逻辑

$$
X_{\text{XOR}} = A\bar B + \bar A B = A \oplus B \qquad X_{\text{XNOR}} = \bar A\,\bar B + AB = \overline{A \oplus B}
$$

- XOR：两输入**不同**时为 1；XNOR（同或）：两输入**相同**时为 1，二者互为反。
- 都可由 AND-OR + 反相器搭出；XOR 有专用符号（带双弧的 `=1` 框）。

## 4️⃣ POS → AND-OR-Invert（slide 8）

![Slide 8 — AOI 实现 POS](EE115B%20Lecture6%20%E2%80%94%20Combinational%20Logic%20Analysis%20Par/slide_08.png)

Slide 8 — AOI 实现 POS

$$
X=(\bar A+\bar B)(\bar C+\bar D)=\overline{AB+CD}
$$

- POS 可改写成「AND-OR 之后再加一级反相」——即 **AOI** 结构。
- 推导用德摩根：$(\bar A+\bar B)(\bar C+\bar D)=\overline{AB}\cdot\overline{CD}=\overline{AB+CD}$。

## 5️⃣ 从真值表到电路（slides 9–10）

- 取输出为 1 的行，写出对应最小项相加 = SOP。本例 Table 5-3 有两行为 1：

$$
X = \bar A B C + A \bar B\,\bar C
$$

- 每个最小项 → 一个 AND 门（输入端按 0/1 加反相器）→ 汇入 OR 门，即得电路。

# 🔌 二、通用门：用 NAND / NOR 搭一切

## 6️⃣ 为什么用 NAND / NOR（slides 11–12）

<aside>
🔑

**通用门 (Universal Gate)：** 单用 NAND 或单用 NOR 一种门就能实现 NOT / AND / OR，从而实现任意逻辑。原因：AND/OR 自身无法取反、XOR/XNOR 无法搭出 AND/OR，而 NAND/NOR 兼具「运算 + 取反」。

**代价：** 门数增加、功耗更高、速度略降；但**简化设计与制造**（尤其 FPGA / PLD 内部全用同种门）。CMOS 里 NAND/NOR 也比 AND/OR 更省晶体管。

</aside>

## 7️⃣ NAND 作为通用门（slides 13–14）

![Slide 13 — NAND 搭 NOT / AND / OR](EE115B%20Lecture6%20%E2%80%94%20Combinational%20Logic%20Analysis%20Par/slide_13.png)

Slide 13 — NAND 搭 NOT / AND / OR

| 目标门 | NAND 数 | 原理 |
| --- | --- | --- |
| NOT 反相器 | 1 | 两输入并联：$\overline{A\cdot A}=\bar A$ |
| AND | 2 | NAND 后再接一个当反相器：$\overline{\overline{AB}}=AB$ |
| OR | 3 | 先把两路各自取反再 NAND：$\overline{\bar A\cdot\bar B}=A+B$ |
| NOR | 4 | 在 OR（3 个）之后再加 1 个反相器 |

## 8️⃣ NOR 作为通用门（slides 15–16）

![Slide 15 — NOR 搭 NOT / OR / AND](EE115B%20Lecture6%20%E2%80%94%20Combinational%20Logic%20Analysis%20Par/slide_15.png)

Slide 15 — NOR 搭 NOT / OR / AND

- 与 NAND 对偶：NOR×1 = NOT，NOR×2 = OR，NOR×3 = AND，NOR×4 = NAND。
- 口诀：**NAND 天生擅长 AND 系，NOR 天生擅长 OR 系**；要得到「另一族」就再多串一级反相。

# 🔄 三、任意电路 → 纯 NAND / 纯 NOR

## 9️⃣ 德摩根可视化转换（slide 17）

![Slide 17 — 气泡推移（德摩根）](EE115B%20Lecture6%20%E2%80%94%20Combinational%20Logic%20Analysis%20Par/slide_17.png)

Slide 17 — 气泡推移（德摩根）

$$
\overline{x_1 x_2}=\bar x_1+\bar x_2 \qquad \overline{x_1+x_2}=\bar x_1\,\bar x_2
$$

- 核心技巧 = **「气泡 (bubble) 推移」**：一个带输出气泡的 AND ＝ 输入端带气泡的 OR，反之亦然。
- 由此把任何门图「换皮」成统一门型，只要让相邻的气泡成对抵消即可。

## 🔟 实战：转成纯 NAND（slides 18–20）

![Slide 20 — NAND-only 电路](EE115B%20Lecture6%20%E2%80%94%20Combinational%20Logic%20Analysis%20Par/slide_20.png)

Slide 20 — NAND-only 电路

**三步法：** ① 把 SOP 电路画成 AND-OR 两级 → ② 在每条连线上**成对加气泡**（两个气泡＝逻辑不变）→ ③ 把气泡吸收进门，AND / OR 全部变成 NAND；输入端多出的单个气泡正好用作变量取反。

## 1️⃣1️⃣ 实战：转成纯 NOR（slides 21–23）

![Slide 23 — NOR-only 电路](EE115B%20Lecture6%20%E2%80%94%20Combinational%20Logic%20Analysis%20Par/slide_23.png)

Slide 23 — NOR-only 电路

- 同样的「成对加气泡」法，但从 **POS（OR-AND 两级）** 出发 → 全部变成 NOR。
- 记忆配对：**SOP ↔ NAND、POS ↔ NOR** 最自然（补的反相器最少）。

## 🛠 仿真工具（slides 24–25）

- **Logisim / Logisim-Evolution：** 免费开源的逻辑电路图形仿真器，适合画门级电路、跑逻辑仿真。
- **TI TINA-TI：** 基于 SPICE 的模拟仿真，适合看真实器件的电压 / 波形。

## 📝 本节总结（记三点就够）

<aside>
🎯

1. **两条标准路：** SOP → AND-OR，POS → AOI；任何真值表都能照此搭出电路。
2. **通用门：** 单用 NAND（或 NOR）即可搭 NOT / AND / OR / 一切；代价是门数↑、速度↓，但利于统一制造（FPGA / PLD）。
3. **转换靠气泡：** 用德摩根「成对加气泡 + 气泡吸收」把 AND-OR 电路换成纯 NAND（配 SOP）或纯 NOR（配 POS）。
</aside>

## ✅ 作业 / 待办

- 课件思考题（无截止日期）：slide 13「用 NAND 实现 NOR」、slide 15「用 NOR 实现 NAND」、Exercise 1（整图转纯 NAND）、Exercise 2（整图转纯 NOR）。
- 本节未单独布置 Homework，也没有出现考试 / 提交 DDL；拿到 syllabus 后再补。

## 📎 原始 Slides

[lecture_6_part1.pdf](EE115B%20Lecture6%20%E2%80%94%20Combinational%20Logic%20Analysis%20Par/lecture_6_part1.pdf)
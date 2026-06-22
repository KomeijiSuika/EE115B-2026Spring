# EE115B Lecture4 — Boolean 定理 & 低层门电路硬件实现 Part 1

<aside>
🔌

**本节主题：** 低层门电路的硬件实现 —— 从器件（二极管 / BJT / MOSFET）到门（TTL / CMOS），再到输出结构（图腾柱 / 开集 / 开漏 / 三态）与时序参数；开头先回顾 Boolean 定理。

**参考教材：** Floyd《Digital Fundamentals》Chapter 15；Boolean 定理参考 ScienceDirect / SlidePlayer。

**核心脉络：** Boolean 定理（含 Consensus）→ PN 结 / 二极管逻辑 → BJT 开关 → TTL（反相器 / NAND / 开集）→ Source/Sink 电流 → MOSFET → CMOS（反相器 / VTC / NAND / NOR）→ 开漏 / 三态 → 扇出与传播延迟。

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md) ｜ 本节为 **Lecture4 Part 1**。

</aside>

# Part 0 — Boolean 定理回顾

## 1️⃣ 基本布尔定理（slide 3）

这 12 条是化简的地基，左列围绕「OR / +」、右列围绕「AND / ·」与互补：

| # | 定理 | # | 定理 |
| --- | --- | --- | --- |
| 1 | $A+0=A$ | 7 | $A\cdot A=A$ |
| 2 | $A+1=1$ | 8 | $A\cdot \bar A=0$ |
| 3 | $A\cdot 0=0$ | 9 | $\bar{\bar A}=A$ |
| 4 | $A\cdot 1=A$ | 10 | $A+AB=A$ |
| 5 | $A+A=A$ | 11 | $A+\bar A B=A+B$ |
| 6 | $A+\bar A=1$ | 12 | $(A+B)(A+C)=A+BC$ |

<aside>
💡

**两条最常被忘记（slide 标了 *）：** 定理 11 $A+\bar A B=A+B$（吸收掉多余的 $\bar A$）、定理 12 $(A+B)(A+C)=A+BC$（分配律的对偶形式）。

</aside>

## 2️⃣ 进阶定理与 De Morgan（slide 4）

每条定理都有 **Function** 与其 **Dual**（把 + 与 · 互换、0 与 1 互换）：

| 定理 | Function | Dual |
| --- | --- | --- |
| Commutation 交换律 | $A+B=B+A$ | $AB=BA$ |
| Association 结合律 | $A+(B+C)=(A+B)+C$ | $A(BC)=(AB)C$ |
| Distribution 分配律 | $A+BC=(A+B)(A+C)$ | $A(B+C)=AB+AC$ |
| Absorption 吸收律 | $A+AB=A$ | $A(A+B)=A$ |
| De Morgan 反演律 | $\overline{A+B}=\bar A\cdot \bar B$ | $\overline{AB}=\bar A+\bar B$ |
| Consensus 一致律 | $AC+B\bar C+AB=AC+B\bar C$ | $(A+C)(B+\bar C)(A+B)=(A+C)(B+\bar C)$ |

<aside>
🧠

**De Morgan 记忆口诀：** 「断线、变号、换运算」——长非号断成两段、每个变量取反、AND↔OR 互换。

</aside>

## 3️⃣ Consensus 一致性定理（slide 5）

命题：第三项 $YZ$（由前两项「一致」推出）是冗余的，可直接删去：

$$
XY+\bar X Z+YZ=XY+\bar X Z
$$

证明（核心是把 $YZ$ 乘上 $(X+\bar X)=1$）：

$$
\begin{aligned}
XY+\bar X Z+YZ &= XY+\bar X Z+(X+\bar X)YZ\\
&= XY+\bar X Z+XYZ+\bar X YZ\\
&= (XY+XYZ)+(\bar X Z+\bar X YZ)\\
&= XY(1+Z)+\bar X Z(1+Y)\\
&= XY+\bar X Z
\end{aligned}
$$

<aside>
🎯

**识别套路：** 当两项里出现「一个变量 $X$ 与它的反 $\bar X$」，且各自还带一个因子（$Y$ 与 $Z$），那么由这两个因子组成的项 $YZ$ 就是 consensus 项，**直接删**。

</aside>

# Part 1 — 低层门电路硬件实现（Floyd Ch.15）

## 4️⃣ PN 结与二极管（slide 7）

二极管 = 一个 PN 结，单向导通：

- **正偏（Forward）：** $V_F$ 越过导通压降（Si ≈ 0.7 V）后电流指数上升，进入正常工作区。
- **反偏（Reverse）：** 仅极小漏电流，直到达到击穿电压 $V_{BR}$ 才进入 Breakdown 区。

![Slide 7 — PN 结结构 / 电路符号 / 伏安特性曲线](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_7.png)

Slide 7 — PN 结结构 / 电路符号 / 伏安特性曲线

## 5️⃣ 二极管逻辑：AND / OR（slide 8）

用二极管 + 电阻就能搭出最原始的逻辑门（约定 $-10\text{V}=0$、$0\text{V}=1$）：

- **AND（左）：** 任一输入为低，对应二极管导通把 $u_Y$ 拉低 → 只有全高才输出高。
- **OR（右）：** 任一输入为高，对应二极管导通把 $u_Y$ 拉高。

![Slide 8 — 二极管 AND / OR 逻辑电路](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_8.png)

Slide 8 — 二极管 AND / OR 逻辑电路

<aside>
⚠️

**二极管逻辑的缺陷：** 每级都掉一个二极管压降，多级级联后电平会逐级劣化、且无法放大 → 所以真正的门要用 BJT / MOSFET 这种有源器件。

</aside>

## 6️⃣ BJT 作为开关（slides 9–11）

BJT 在数字电路里只工作在两个极端：**饱和（ON）↔ 截止（OFF）**，等效成一个受控开关：

$$
V_{BE}>0.7\text{V}\Rightarrow \text{ON（饱和，}C\text{-}E\text{ 导通）},\qquad V_{BE}<0.7\text{V}\Rightarrow \text{OFF（截止，}C\text{-}E\text{ 断开）}
$$

![Slide 10 — BJT(NPN) 饱和/截止开关等效 + 符号](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_10.png)

Slide 10 — BJT(NPN) 饱和/截止开关等效 + 符号

NPN 与 PNP 结构互补（N-P-N vs P-N-P），符号箭头方向与偏置极性相反：

![Slide 11 — NPN vs PNP 结构与符号](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_11.png)

Slide 11 — NPN vs PNP 结构与符号

## 7️⃣ TTL 反相器（slides 12–13）

标准 TTL 反相器：输入级 $Q_1$ + 分相 $Q_2$ + **图腾柱输出（**$Q_3/Q_4$**）**。

- **输入 HIGH：** $Q_2,Q_3$ ON、$Q_4$ OFF → 输出被 $Q_3$ 拉到 LOW。
- **输入 LOW：** $Q_2,Q_3$ OFF、$Q_4$ ON → 输出经 $Q_4$ 拉到 HIGH。

![Slide 13 — TTL 反相器工作过程（输入高 / 输入低）](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_13.png)

Slide 13 — TTL 反相器工作过程（输入高 / 输入低）

<aside>
🏛

**图腾柱（totem-pole）：** 上拉管 $Q_4$ 与下拉管 $Q_3$ 永远一个 ON 一个 OFF，输出阻抗低、驱动能力强；代价是**不能把两个输出直接并联**（会冲突短路）。

</aside>

## 8️⃣ TTL NAND 门（slide 14）

把反相器的输入级换成**多发射极晶体管** $Q_1$（每个输入一个发射极）即得 NAND：只要任一输入为 LOW，$Q_1$ 把 $Q_2$ 关断 → 输出 HIGH；仅当 $A,B$ 全 HIGH 才输出 LOW。

![Slide 14 — TTL NAND 门电路](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_14.png)

Slide 14 — TTL NAND 门电路

## 9️⃣ 集电极开路 Open-Collector & 线与（slide 15）

去掉图腾柱上拉管，输出只剩一个对地的 $Q_3$，需外接 **上拉电阻** $R_p$。好处：多个开集输出可直接并联实现 **Wired-AND（线与）**：

$$
X=\overline{A}\,\overline{B}\,\overline{C}\,\overline{D}\quad(\text{任一管 ON 即把公共线拉低})
$$

![Slide 15 — 开集反相器 + 外部上拉 + 四输入线与](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_15.png)

Slide 15 — 开集反相器 + 外部上拉 + 四输入线与

## 🔟 电流源出 Source / 灌入 Sink（slides 16–18）

驱动门与负载门之间的电流方向分两种：

- **Source（拉电流）：** 输出 HIGH 时，上拉管 $Q_4$ ON，电流从驱动门**流出**进负载（$I_{IH}\approx 40\,\mu\text{A}$）。
- **Sink（灌电流）：** 输出 LOW 时，下拉管 $Q_3$ ON，电流从负载**灌入**驱动门到地（$I_{IL}\approx 1.6\,\text{mA}$）。

![Slide 16 — Source vs Sink 电流路径](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_16.png)

Slide 16 — Source vs Sink 电流路径

**例题（slide 18）：** 开集 NAND 驱动 LED，$I=20\text{mA}$、$V_{LED}=1.5\text{V}$、$V_{OL}=0.1\text{V}$，电源 5 V，求限流电阻 $R_L$：

$$
R_L=\frac{V_{CC}-V_{LED}-V_{OL}}{I}=\frac{5-1.5-0.1}{20\,\text{mA}}=\frac{3.4}{0.02}=170\ \Omega
$$

## 1️⃣1️⃣ MOSFET（slides 19–20）

场效应管靠**栅压**控制沟道导通，是 CMOS 的基本砖块：

- **NMOS：** $V_{GS}$ 高 → ON；衬底 Body 接 GND。
- **PMOS：** $V_{GS}$ 低（栅低于源）→ ON；衬底 Body 接 $V_{DD}$（符号栅极带圈）。

![Slide 19 — MOSFET 符号与 n/p 沟道开关等效](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_19.png)

Slide 19 — MOSFET 符号与 n/p 沟道开关等效

![Slide 20 — NMOS / PMOS 物理结构](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_20.png)

Slide 20 — NMOS / PMOS 物理结构

## 1️⃣2️⃣ CMOS 反相器（slide 21）

上 PMOS + 下 NMOS，栅极接同一 $V_{in}$：

- $V_{in}=V_{DD}$：NMOS ON / PMOS OFF → 输出经 $R_n$ 放电到 **LOW**。
- $V_{in}=0$：PMOS ON / NMOS OFF → 输出经 $R_p$ 充电到 **HIGH**。

![Slide 21 — CMOS 反相器符号 / 原理图 / 充放电等效](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_21.png)

Slide 21 — CMOS 反相器符号 / 原理图 / 充放电等效

<aside>
🔋

**CMOS 最大优点 = 静态零功耗：** 稳态时上下管必有一个 OFF，没有直流通路；功耗主要发生在**翻转瞬间**（给负载电容 $C_L$ 充放电）。

</aside>

## 1️⃣3️⃣ 电压传输特性 VTC（slide 22）

$V_{out}$ vs $V_{in}$ 曲线：理想是垂直跳变；真实曲线在 $V_{IL}$ 与 $V_{IH}$ 之间有过渡区。

$$
V_{OH},V_{OL}\ (\text{输出高/低电平}),\qquad V_{IL},V_{IH}\ (\text{输入判低/判高门限})
$$

![Slide 22 — 反相器 VTC（Ideal vs Realistic）](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_22.png)

Slide 22 — 反相器 VTC（Ideal vs Realistic）

<aside>
🛡

**噪声容限（noise margin）：** $NM_H=V_{OH}-V_{IH}$、$NM_L=V_{IL}-V_{OL}$。过渡区越陡、平台越平，抗噪能力越强。

</aside>

## 1️⃣4️⃣ CMOS NAND / NOR（slides 23–24）

CMOS 组合门的通用法则：**PUN（PMOS 上拉网络）与 PDN（NMOS 下拉网络）互为对偶**——下拉串联则上拉并联，反之亦然。

**NAND：** NMOS 串联（全高才拉低）、PMOS 并联。

![Slide 23 — CMOS NAND 电路与真值表](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_23.png)

Slide 23 — CMOS NAND 电路与真值表

| A | B | X (NAND) |
| --- | --- | --- |
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

**NOR：** NMOS 并联（任一高即拉低）、PMOS 串联。

![Slide 24 — CMOS NOR 电路与真值表](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_24.png)

Slide 24 — CMOS NOR 电路与真值表

| A | B | X (NOR) |
| --- | --- | --- |
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 0 |

## 1️⃣5️⃣ 开漏 Open-Drain & 三态 Tristate（slides 25–26）

- **Open-Drain（开漏）：** 开集的 CMOS 版本——输出只有一个对地 NMOS，漏极悬空，必须外接上拉电阻 $R_p$ 才能输出 HIGH；同样支持 Wired-AND。

![Slide 25 — 开漏门（悬空 / 加上拉电阻）](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_25.png)

Slide 25 — 开漏门（悬空 / 加上拉电阻）

- **Tristate（三态）：** 输出有 HIGH / LOW / **高阻 high-Z** 三态，由 enable 控制。使能时正常工作；禁用时输出从电路断开（倒三角 $\nabla$ 是三态标志），可挂总线。

![Slide 26 — 三态门（正常逻辑 / 高阻态）](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_26.png)

Slide 26 — 三态门（正常逻辑 / 高阻态）

<aside>
🚌

**三态 = 图腾柱 + 开集优点合体：** 既有图腾柱的强驱动，又能像开集那样「让出」总线 —— 多个三态输出共享一条总线时，保证同一时刻只有一个 enable。

</aside>

## 1️⃣6️⃣ 扇出 Fan-Out 与时序参数（slides 27–29）

- **Fan-Out（扇出）：** 一个驱动门能带动的负载门输入数上限。带太多负载会拉垮电平、变慢。TTL 输入阻抗常只有几千欧。

![Slide 27 — 门的负载（Loading）](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_27.png)

Slide 27 — 门的负载（Loading）

- **Propagation delay（传播延迟）：** 输入变化到输出响应的时间，分 $t_{PLH}$（输出低→高）与 $t_{PHL}$（输出高→低）。

![Slide 29 — 传播延迟 $t_{PLH}$ / $t_{PHL}$ 波形](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/slide_29.png)

Slide 29 — 传播延迟 $t_{PLH}$ / $t_{PHL}$ 波形

## 📝 本节总结

<aside>
🎯

1. **器件即开关：** 二极管单向导通、BJT 用 $V_{BE}>0.7$ 切饱和/截止、MOSFET 用栅压控沟道；门电路就是把这些开关按逻辑接出来。
2. **输出结构四件套：** 图腾柱（强驱动但不可并联）→ 开集/开漏（外接 $R_p$、可线与）→ 三态（多一个高阻态、可挂总线）。CMOS NAND/NOR 记「PUN 与 PDN 对偶，串↔并」。
3. **CMOS 静态零功耗**，功耗在翻转瞬间充放电；评估一个门看三件事：**噪声容限（**$V_{OH/OL},V_{IH/IL}$**）、扇出、传播延迟（**$t_{PLH}/t_{PHL}$**）**。
</aside>

## ✅ 作业 / 待办

- 本节 slides 未给出带日期的作业 / 考试 DDL；拿到 syllabus 或作业系统通知后再补 Homework / Lab deadline（届时我会同步到日历）。
- [ ]  自测：手推 slide 18 的 $R_L=170\ \Omega$，并解释为什么开集驱动 LED 要用灌电流（sink）而不是源电流。

## 📎 原始 Slides

[lecture_4 part1 (1).pdf](EE115B%20Lecture4%20%E2%80%94%20Boolean%20%E5%AE%9A%E7%90%86%20&%20%E4%BD%8E%E5%B1%82%E9%97%A8%E7%94%B5%E8%B7%AF%E7%A1%AC%E4%BB%B6%E5%AE%9E%E7%8E%B0%20Part%201/lecture_4_part1_(1).pdf)
# EE115B Lecture7 — Encoders & Decoders Part 2

<aside>
🎛️

**本节主题：** Combinational Logic Part 2 —— 编码器 Encoder 与译码器 Decoder，一对功能互逆的组合逻辑器件。

**讲义来源：** EE115B（Chenxi Xiao），共 24 页；本节为该讲 **Part 2**。

**核心脉络：** 编码器概念 → 8-3 编码器 → 4-to-2 编码器 → Decimal-to-BCD 编码器（74LS147 优先编码）→ 译码器概念 → 基本二进制译码器（active high / low）→ 带使能 2-to-4 → 3-8（74HC138）→ 4-10（74HC42）→ 4-to-16（74HC154）。

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md)（组合逻辑部分）；同为 Lecture7 的 **Part 3** = 比较器 / MUX / Hazard 见 [EE115B Lecture7 — Comparator · MUX / DEMUX · Hazard Part 3](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard.md)。

</aside>

# 🔢 一、Encoders 编码器

## 1️⃣ 编码器概念（slides 2–4）

**编码器 (Encoder)：** 一个组合逻辑电路，接受某一输入线上的有效电平，把「哪一根输入被激活」转换成一组编码输出。二进制编码器把 $2^n$ 路输入压缩成 $n$ 位输出。

<aside>
💡

**用途：** 码制转换（binary → BCD / Gray …）、数据压缩与存储。可以把它看作「哪根线亮了就输出该线的序号」。

</aside>

## 2️⃣ 8-3 编码器（slides 5–6）

8-to-3 编码器把 8 根输入中被激活那一根的**位置**直接转成 3 位二进制码。由真值表化简得：每个输出位 = 所有「该位为 1」的输入号的或。

$$
Y_2 = I_4 + I_5 + I_6 + I_7, \qquad Y_1 = I_2 + I_3 + I_6 + I_7, \qquad Y_0 = I_1 + I_3 + I_5 + I_7
$$

![Slide 6 — 8-3 编码器：真值表 + OR 门电路](EE115B%20Lecture7%20%E2%80%94%20Encoders%20&%20Decoders%20Part%202/slide_6.png)

Slide 6 — 8-3 编码器：真值表 + OR 门电路

<aside>
🧭

**记忆法：** 某输出位的表达式 = 「二进制下该位为 1 的那几个序号」相或。如 $Y_0$（最低位）对应所有奇数序号 1/3/5/7。

</aside>

## 3️⃣ 4-to-2 二进制编码器（slide 7）

![Slide 7 — 4-to-2 编码器：真值表 + 两个 OR 门](EE115B%20Lecture7%20%E2%80%94%20Encoders%20&%20Decoders%20Part%202/slide_7.png)

Slide 7 — 4-to-2 编码器：真值表 + 两个 OR 门

按真值表化简（输入独热）：

$$
y_1 = w_2 + w_3, \qquad y_0 = w_1 + w_3
$$

注意 $w_0$ 不进任何 OR 门——它对应输出 00，“默认态”不需要门。

## 4️⃣ Decimal-to-BCD 编码器（10-line-to-4-line，slides 8–11）

输入是 10 个十进制数字（1–9，加隶含的 0），输出是该数字的 4 位 BCD 码。

$$
A_3 = 8+9, \quad A_2 = 4+5+6+7, \quad A_1 = 2+3+6+7, \quad A_0 = 1+3+5+7+9
$$

![Slide 10 — Decimal-to-BCD 编码器（4 个 OR 门）](EE115B%20Lecture7%20%E2%80%94%20Encoders%20&%20Decoders%20Part%202/slide_10.png)

Slide 10 — Decimal-to-BCD 编码器（4 个 OR 门）

<aside>
ℹ️

**为什么 0 不用：** 数字 0 对应 BCD 码 0000——所有输出都是 0，是「无键按下」的默认状态，所以不需要为它单独接门。

</aside>

## 5️⃣ 74LS147 优先编码器（slide 12）

![Slide 12 — 74LS147 功能表 + 键盘 / 7447 / 数码管应用](EE115B%20Lecture7%20%E2%80%94%20Encoders%20&%20Decoders%20Part%202/slide_12.png)

Slide 12 — 74LS147 功能表 + 键盘 / 7447 / 数码管应用

74LS147 是现成的 Decimal-to-BCD **优先编码器**，现实中可能多个键同时按下，优先编码器只编码**优先级最高**那一个。

<aside>
⚠️

**关键陷阱 — 低有效（Low = 1）：** 74LS147 的输入与输出都是**低电平有效**。表里 $H$=高电平、$L$=低电平、$X$=不关心；被按下的键为 $L$，输出 BCD 也是反码。接 7447 驱动共阳极数码管时这个极性刚好合拍。

</aside>

---

# 🔓 二、Decoders 译码器

## 6️⃣ 译码器概念（slide 13）

**译码器 (Decoder)：** 检测输入上是否出现某个指定的位组合（码），并用对应输出电平指示它的出现。一般形式：$n$ 根输入 → 最多 $2^n$ 根输出。

<aside>
🔄

**与编码器互逆：** 编码器是「$2^n$ 入 → $n$ 出」（压缩）；译码器是「$n$ 入 → $2^n$ 出」（展开）。译码器每个输出对应一个 minterm。

</aside>

## 7️⃣ 基本二进制译码器：active high vs low（slide 14）

![Slide 14 — 基本译码器：高有效（AND）与低有效（NAND）](EE115B%20Lecture7%20%E2%80%94%20Encoders%20&%20Decoders%20Part%202/slide_14.png)

Slide 14 — 基本译码器：高有效（AND）与低有效（NAND）

每个输出对应一个 minterm：把输入变量（原变量 / 反变量）送进一个门。

- **Active High（AND 门）：** 选中时输出 **1**。
- **Active Low（NAND 门）：** 选中时输出 **0**，其余为 1。很多现成 IC（138/42/154）都是低有效输出。

## 8️⃣ 带使能的 2-to-4 译码器（slides 15–16）

![Slide 16 — 2-to-4 译码器（带 ENABLE）真值表 + 电路](EE115B%20Lecture7%20%E2%80%94%20Encoders%20&%20Decoders%20Part%202/slide_16.png)

Slide 16 — 2-to-4 译码器（带 ENABLE）真值表 + 电路

加入使能端 $En$：

$$
y_i = En \cdot m_i(w_1, w_0), \qquad i = 0,1,2,3
$$

- $En=0$：所有输出都不有效（$y_3=y_2=y_1=y_0=0$）。
- $En=1$：由二进制输入 $w_1 w_0$ 决定哪一路输出被拉高。

<aside>
🔑

**使能端的价值：** $En$ 不仅用来「关灯」，还是级联扩展（用低位译码器的输出去使能高位译码器）和把译码器当 DEMUX 用的入口。

</aside>

## 9️⃣ 3-8 译码器 74HC138（slides 17–19）

每个输出就是一个 minterm：

$$
Y_0 = \bar{A}_2\bar{A}_1\bar{A}_0 = m_0, \quad Y_1 = \bar{A}_2\bar{A}_1 A_0 = m_1, \quad \dots, \quad Y_7 = A_2 A_1 A_0 = m_7
$$

![Slide 18 — 74HC138 功能框图（带三个 strobe 使能）](EE115B%20Lecture7%20%E2%80%94%20Encoders%20&%20Decoders%20Part%202/slide_18.png)

Slide 18 — 74HC138 功能框图（带三个 strobe 使能）

<aside>
⚠️

**使能 & 极性：** 138 有三个使能（一个高有效 $G_2$、两个低有效 $\overline{G_1},\overline{G_0}$）。任一 strobe 未满足时输出全被压低；使能满足时只有选中输出有效。上一节把它的使能端当数据输入，138 就变成了 1-to-8 DEMUX。

</aside>

## 🔟 4-10 译码器 74HC42（slides 20–22）

4-line-to-10-line：4 位 BCD 输入译成 10 根十进制输出线（$Y_i = \overline{m_i},\ i=0\sim9$，低有效）。

![Slide 22 — 74HC42 输出波形（BCD 计数输入 → 逐个拉低输出）](EE115B%20Lecture7%20%E2%80%94%20Encoders%20&%20Decoders%20Part%202/slide_22.png)

Slide 22 — 74HC42 输出波形（BCD 计数输入 → 逐个拉低输出）

波形里：BCD 输入从 0 递增到 9，输出线就依次被拉低（每拍只有一根为 0）——直观看出「一热低」的译码行为。

## 1️⃣1️⃣ 4-to-16 译码器 74HC154（slides 23–24）

4 位输入译成 16 根输出线，同样 **输出低有效**：选中那一根为 0，其余 15 根为 1。位宽更宽的译码器可用小译码器 + 使能级联搭出。

## ⚖️ Encoder vs Decoder 一表看清

| 维度 | Encoder 编码器 | Decoder 译码器 |
| --- | --- | --- |
| 方向 | $2^n$ 入 → $n$ 出（压缩） | $n$ 入 → $2^n$ 出（展开） |
| 输出含义 | 被激活输入的编号 | 检测到的 minterm |
| 典型门 | OR 门阵 | AND / NAND 门阵 |
| 典型 IC | 74LS147 | 74HC138 / 42 / 154 |

---

## 📝 本节总结（记三点就够）

<aside>
🎯

1. **编码器 = 哪根输入亮 → 输出其序号**：每个输出位 = 「该位为 1 的输入号」相或（$Y_2=I_4+I_5+I_6+I_7$ …），用 OR 门阵实现。
2. **译码器 = 与编码器互逆**：$n$ 入 $2^n$ 出，每个输出是一个 minterm（$Y_i=m_i$），用 AND/NAND 门阵实现。
3. **低有效与使能是考点**：74LS147、74HC138/42/154 多为 active-LOW；使能端 $En$ / strobe 既能关闭输出，又能用于级联扩展和把译码器当 DEMUX。
</aside>

## ✅ 作业 / 待办

- 本节 slides 未给出明确的 Homework / 考试 deadline；拿到 syllabus 后再补 Lab / HW 截止时间。
- [ ]  练习（slide 20）：用电路图实现 74HC42 的 $Y_0\text{–}Y_2$（$Y_i=\overline{m_i}$）。

## 📎 原始 Slides

[lecture_7_part2.pdf](EE115B%20Lecture7%20%E2%80%94%20Encoders%20&%20Decoders%20Part%202/lecture_7_part2.pdf)
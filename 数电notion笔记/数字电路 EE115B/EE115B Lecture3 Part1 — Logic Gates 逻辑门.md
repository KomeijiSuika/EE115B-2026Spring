# EE115B Lecture3 Part1 — Logic Gates 逻辑门

<aside>
🔣

**本节主题：** 七种基本逻辑门（Logic Gates）—— 符号体系、真值表、布尔表达式、波形（waveform 波形），以及它们在 C 语言里的 bitwise（按位）运算应用。

**教材：** Floyd《Digital Fundamentals》Ch.2；门符号图取自 [learnabout-electronics.org](http://learnabout-electronics.org)。讲义来源 EE115B（Chenxi Xiao），本节为 **Lecture 3 Part 1**，共 26 页。

**核心脉络：** ① 7 种门 + 两套符号（ANSI vs IEC）→ ② 逐门吃透「真值表 + 布尔表达式 + 波形」→ ③ 通用门（universal gate 通用门）NAND / NOR → ④ 用 sum term（和项）/ product term（乘积项）反推输入 → ⑤ 落到 C 语言 bitwise 运算与 bit masking（位掩码）。

</aside>

## 1️⃣ 七种逻辑门总览（Overview）

<aside>
💡

数字电子学只依赖 **7 种**逻辑门工作；最基础的三种是 **AND / OR / NOT**，其余 **NAND / NOR / XOR / XNOR** 都能由这三种组合得到。每个门本质上是一个小的晶体管电路（transistor circuit 晶体管电路）。

</aside>

**① 门符号：ANSI（特征形状 distinctive shape）vs IEC（矩形 + 限定符）**

![Slide 3 — ANSI & IEC 七种门符号对照](EE115B%20Lecture3%20Part1%20%E2%80%94%20Logic%20Gates%20%E9%80%BB%E8%BE%91%E9%97%A8/slide_3.png)

Slide 3 — ANSI & IEC 七种门符号对照

**② 七种门的布尔表达式（Boolean statements）**

| 门 Gate | 布尔表达式 | 一句话定义 |
| --- | --- | --- |
| AND 与 | $X = A \cdot B$ | 全 1 才出 1 |
| OR 或 | $X = A + B$ | 有 1 即出 1 |
| NOT 非（Inverter） | $X = \overline{A}$ | 取反 / complement（补） |
| NAND 与非 | $X = \overline{A \cdot B}$ | AND 再取反 |
| NOR 或非 | $X = \overline{A + B}$ | OR 再取反 |
| XOR 异或 | $X = A \oplus B = \overline{A}B + A\overline{B}$ | 不同才出 1 |
| XNOR 同或 | $X = \overline{A \oplus B} = \overline{A}\,\overline{B} + AB$ | 相同才出 1 |

**③ 二输入真值表总表（A, B 共用）**

| A | B | AND | OR | NAND | NOR | XOR | XNOR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 |

<aside>
🧠

**记忆口诀：** NAND = AND 取反、NOR = OR 取反、XNOR = XOR 取反 —— 带 “N” 的门把对应基础门的输出列整列翻过来即可，不用死背。

</aside>

- 📚 拓展 — 逻辑门能超过 2 个输入吗？
    
    可以。门的输入数叫 **fan-in（扇入）**：n 输入 AND 当且仅当所有输入全 1 才输出 1；n 输入 OR 只要有一个 1 就输出 1。但 fan-in 越大，门延迟越大、驱动越弱，所以实际电路常用 2~4 输入的门级联来实现多输入功能。
    

## 2️⃣ 反相器 Inverter（NOT 门）

- **功能：** 输入 LOW → 输出 HIGH；输入 HIGH → 输出 LOW。即 NOT 操作 / complement（补，取反），布尔式 $X = \overline{A}$，符号上用上划线（overbar 上划线）表示。

**输入 / 输出时序图（timing diagram 时序图）：** 输出始终是输入的镜像翻转。

*（Inverter 输入/输出时序图：见文末「原始 Slides」PDF 第 8 页）*

**两套标准符号（ANSI/IEEE Std. 91）：**(a) 特征形状 + 取反小圆圈（negation indicator 取反标记）；(b) 矩形 + 极性三角（polarity indicator 极性标记）。

*（Inverter 两套标准符号：见文末「原始 Slides」PDF 第 7 页）*

## 3️⃣ 与门 AND（$X = A\cdot B$）

- **功能：** 所有输入都 HIGH 才输出 HIGH，否则 LOW。AND 常省略点写成 $X = AB$。

*（AND 门示例波形：见文末「原始 Slides」PDF 第 10 页）*

<aside>
🎯

**应用 — selective mask（选择性掩码）：** 想“保留”某些位、把其它位清 0，就和一个在保留位置为 1 的掩码做 AND。例：`10100011 AND 00001111 = 00000011`（高 4 位被清零，低 4 位保留）。

</aside>

## 4️⃣ 或门 OR（$X = A + B$）

- **功能：** 任意一个输入 HIGH 即输出 HIGH；全 LOW 才输出 LOW。

*（OR 门示例波形：见文末「原始 Slides」PDF 第 12 页）*

<aside>
🎯

**应用 — 置位（set bits）：** OR 可把指定位“置 1”。例：ASCII 中 bit 5 为 1 表示小写、为 0 表示大写；把字母 OR 上掩码 `00100000` 就强制变成小写。

</aside>

## 5️⃣ 与非门 NAND（$X = \overline{A\cdot B}$）

- **功能：** 所有输入全 HIGH 时输出 LOW，否则 HIGH（即 AND 的输出取反）。

![Slide 14 — NAND 门示例波形](EE115B%20Lecture3%20Part1%20%E2%80%94%20Logic%20Gates%20%E9%80%BB%E8%BE%91%E9%97%A8/slide_14.png)

Slide 14 — NAND 门示例波形

<aside>
⭐

**universal gate（通用门）：** NAND 是“万能门”——任何其它门都能只用 NAND 搭出来。例如把两个输入接在一起的 NAND 就是一个反相器：$\overline{A\cdot A} = \overline{A}$。

</aside>

- 📚 拓展 — 为什么 NAND / NOR 是 universal gate？
    
    因为 NAND 和 NOR 各自都满足 **functional completeness（功能完备性）**：只要能表达 NOT、AND、OR 三种基本操作，就能表达任何布尔函数。
    **用 NAND 搭：** NOT = 输入并接的 NAND；AND = NAND 后再接一个当反相器用的 NAND；OR = 两输入先各自 NOT，再 NAND（德摩根：$\overline{\overline A \cdot \overline B} = A + B$）。
    **工程意义：** 只用一种单元就能造出整个逻辑系统，利于工艺统一、版图复用；CMOS 里 NAND/NOR 的实现也比 AND/OR 更省晶体管。
    

## 6️⃣ 或非门 NOR（$X = \overline{A + B}$）

- **功能：** 任意输入为 HIGH 时输出 LOW；全 LOW 才输出 HIGH（即 OR 的输出取反）。NOR 同样是 universal gate。

![Slide 16 — NOR 门示例波形与 LED 应用](EE115B%20Lecture3%20Part1%20%E2%80%94%20Logic%20Gates%20%E9%80%BB%E8%BE%91%E9%97%A8/slide_16.png)

Slide 16 — NOR 门示例波形与 LED 应用

- **例（slide 中）：** 用一个 4 输入 NOR 驱动 LED——只要 A/B/C/D 任一为 HIGH，NOR 输出 LOW，LED 的亮灭按该电路接法判断。

## 7️⃣ 异或门 XOR（$X = A \oplus B$）

- **功能：** 两输入“电平不同”时才输出 HIGH（exactly one input HIGH 恰好一个为高）。$X = \overline{A}B + A\overline{B} = A \oplus B$。

![Slide 18 — XOR 门示例波形](EE115B%20Lecture3%20Part1%20%E2%80%94%20Logic%20Gates%20%E9%80%BB%E8%BE%91%E9%97%A8/slide_18.png)

Slide 18 — XOR 门示例波形

<aside>
🧠

**性质：** 把 A、B **同时取反**，XOR 输出不变（$\overline A \oplus \overline B = A \oplus B$）；只翻其中一个，输出翻转。XOR 还可当“可控反相器”和奇偶校验（parity 奇偶校验）。

</aside>

## 8️⃣ 同或门 XNOR（$X = \overline{A \oplus B}$）

- **功能：** 两输入“电平相同”时才输出 HIGH，常用于比较（comparison 比较）。$X = \overline{A}\,\overline{B} + AB = A \odot B$。

![Slide 20 — XNOR 门示例波形](EE115B%20Lecture3%20Part1%20%E2%80%94%20Logic%20Gates%20%E9%80%BB%E8%BE%91%E9%97%A8/slide_20.png)

Slide 20 — XNOR 门示例波形

- **性质：** 只翻一个输入，输出翻转；XNOR 本质是“相等检测器”，是构建 comparator（比较器）的核心单元。

## 9️⃣ 课堂练习 Exercise

<aside>
📝

这两题是讲义里的 **例题（已给解）**，用来练 sum term / product term 的判 0 / 判 1。

</aside>

**Exercise 1：** 求 A, B, C 使 sum term（和项）$\overline{A} + B + \overline{C} = 0$。

- 和项 = OR，**只有每个 literal（文字 / 字面量）都为 0** 时整体才为 0。
- $\overline A = 0 \Rightarrow A = 1$；$B = 0$；$\overline C = 0 \Rightarrow C = 1$。
- **答案：** $A=1,\; B=0,\; C=1$。

**Exercise 2：** 求 A, B, C 使 product term（乘积项）$A \cdot \overline{B} \cdot \overline{C} = 1$。

- 乘积项 = AND，**只有每个 literal 都为 1** 时整体才为 1。
- $A = 1$；$\overline B = 1 \Rightarrow B = 0$；$\overline C = 1 \Rightarrow C = 0$。
- **答案：** $A=1,\; B=0,\; C=0$。

<aside>
🧠

**口诀：** 和项（OR）判 0 → 每个字面量都为 0；乘积项（AND）判 1 → 每个字面量都为 1。带反号的变量记得反着取值。

</aside>

## 🔟 C 语言中的位运算（Bitwise Operators）

逻辑门直接对应 C 语言的 **bitwise（按位）运算符**，对整数的每一位并行做逻辑运算：

```
运算符   含义                   示例     结果
|       Bitwise OR  按位或       4|2      6
&       Bitwise AND 按位与       1&3      1
^       Bitwise XOR 按位异或     4^3      7
<<      Left Shift  左移         2<<1     4
>>      Right Shift 右移         4>>1     2
~       Bitwise NOT 按位取反     ~6       -7
```

**Bit masking（位掩码）—— 用** `>>` **+** `& 0xff` **从 32 位数里逐字节抽取：**

```c
int value = 0x04030201;          // 32-bit Number
// Extracting each Byte from value from MSB to LSB
int a = (value >> 24) & 0xff;    // 04 (bits 24-31)  MSB
int b = (value >> 16) & 0xff;    // 03 (bits 16-23)
int c = (value >>  8) & 0xff;    // 02 (bits 8-15)
int d =  value        & 0xff;    // 01 (bits 0-7)    LSB
```

- 📚 拓展 — set / clear / toggle 位操作三连 & 为什么 ~6 = -7
    
    **三个标准位操作（n 为位号）：**
    · **置位 set：** `x |= (1 << n)` —— 用 OR 把第 n 位变 1。
    · **清位 clear：** `x &= ~(1 << n)` —— 用 AND + 取反把第 n 位变 0。
    · **翻位 toggle：** `x ^= (1 << n)` —— 用 XOR 把第 n 位反转。
    **为什么** `~6 = -7`**？** C 用二进制补码（two's complement 补码）表示负数，按位取反满足 $\sim x = -x - 1$，所以 $\sim 6 = -7$——这就是为什么 `~` 的结果会是负数。
    

## ✅ 本节总结（口诀）

<aside>
📌

1. **7 门两符号：** AND / OR / NOT 为本，N 系列（NAND / NOR / XNOR）= 对应门输出整列取反。
2. **通用门：** NAND、NOR 各自就能搭出任何逻辑（functional completeness）。
3. **判值法：** 和项（OR）判 0 看“全 0”，乘积项（AND）判 1 看“全 1”。
4. **门 = C 位运算：** `&` `|` `^` `~` `<<` `>>`；AND 清位、OR 置位、XOR 翻位是 bit masking 三板斧。
</aside>

## 🚀 下次打开第一步

> 先盖住「二输入真值表总表」，凭记忆默写 AND / OR / NAND / NOR / XOR / XNOR 六列输出，再翻看核对；接着把 Exercise 1、2 重做一遍，巩固 sum / product term 判值。
> 

## 📎 原始 Slides

[lecture_3_part1.pdf](EE115B%20Lecture3%20Part1%20%E2%80%94%20Logic%20Gates%20%E9%80%BB%E8%BE%91%E9%97%A8/lecture_3_part1.pdf)
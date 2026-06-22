# EE115B Lecture1 Part3-4 — Number Systems & Conversions 数制与进制转换

<aside>
🔢

**本节主题：** Number Systems（数制）与 Number Conversions（进制转换）——十进制 / 二进制 / 十六进制 / 八进制的表示、位权分析，以及整数 / 小数在不同进制之间的转换。

**讲义范围：** 本 PDF 对应 **Lecture 1 Part 3 + Part 4**，共 19 页。

**核心脉络：** ① 什么是 quantized(量化的) digital signal → ② weighted number system(加权数制) 怎么读数 → ③ binary / hex / oct 各自的规则 → ④ 2 进制和 8/16 进制为何能快速互转 → ⑤ 十进制整数 / 小数如何系统地转成其他进制。

</aside>

## 1️⃣ Number Systems：为什么要学不同进制？

<aside>
💡

数字电路里信息最终都落在 **binary(二进制)** 上，但人类书写、阅读、调试时常常会借助 **decimal(十进制)**、**hexadecimal(十六进制)**、**octal(八进制)** 来表达同一组 bit。

</aside>

**slides 的出发点：** digital signals are **quantized(量化的)** —— 信号不是连续地取任意值，而是被离散地划分成有限状态，因此非常适合用数字系统表示。

*📄 见文末「原始 Slides」第 3 页：decimal / binary / octal / hex 的总对照表。*

### 本节最重要的一个词：weighted number system

所谓 **weighted number system(加权数制)**，就是每一位都有自己的 **column weight(位权)**；一个数的值 = 各位数字 × 对应位权，再全部相加。

<aside>
📌

**一句话记忆：** 读一个数，不是“看长得像什么”，而是“每一位乘自己的位权再求和”。

</aside>

## 2️⃣ Decimal 与 Binary：怎么按位权读数？

### ① Decimal numbers（十进制）

十进制每一位的位权是 10 的幂：

$$
N = \sum_{i=-m}^{n} d_i 10^i
$$

例如：

$$
9240 = 9\times10^3 + 2\times10^2 + 4\times10^1 + 0\times10^0
$$

而带小数时：

$$
480.52 = 4\times10^2 + 8\times10^1 + 0\times10^0 + 5\times10^{-1} + 2\times10^{-2}
$$

*📄 见文末「原始 Slides」第 4 页：480.52 的十进制展开示例。*

### ② Binary numbers to decimal（二进制转十进制）

二进制每一位的位权是 2 的幂：

$$
N = \sum_{i=-m}^{n} b_i 2^i,\quad b_i\in\{0,1\}
$$

其结构是：

$$
\cdots 2^3,\ 2^2,\ 2^1,\ 2^0,\ 2^{-1},\ 2^{-2},\cdots
$$

例如：

$$
(1011001)_2 = 1\times2^6 + 0\times2^5 + 1\times2^4 + 1\times2^3 + 0\times2^2 + 0\times2^1 + 1\times2^0 = 89
$$

再如：

$$
(101.110)_2 = 1\times2^2 + 0\times2^1 + 1\times2^0 + 1\times2^{-1} + 1\times2^{-2} + 0\times2^{-3} = 5.75
$$

*📄 见文末「原始 Slides」第 5 页：binary weighting structure 与两个练习。*

<aside>
🧠

**byte(字节)** = 8 bits。
用 n bits 表示无符号整数时，最大值是 $2^n-1$。

</aside>

- 📚 拓展 — 为什么数字电路天然偏爱 binary？
    
    硬件里真正稳定、便宜、抗噪声强的不是“很多级精确电平”，而是高低两级：0 / 1。也就是说 binary 并不是“最优雅的数学选择”，而是**最适合物理实现**的工程选择。hex 和 oct 本质上只是为了让人更容易读二进制。
    

## 3️⃣ Hexadecimal 与 Octal：为什么它们和二进制关系这么好？

### ① Hexadecimal（十六进制）

十六进制使用 16 个符号：

`0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F`

其中：

- `A=10`
- `B=11`
- `C=12`
- `D=13`
- `E=14`
- `F=15`

它也是 **weighted number system(加权数制)**，位权是 16 的幂：

$$
N = \sum h_i 16^i
$$

例如：

$$
(1A2F)_{16} = 1\times16^3 + 10\times16^2 + 2\times16^1 + 15\times16^0 = 6703
$$

*📄 见文末「原始 Slides」第 6–7 页：hex 的字符表、4-bit 分组思路，以及 1A2F_{16} 转十进制例题。*

### ② Octal（八进制）

八进制使用 8 个符号：

`0,1,2,3,4,5,6,7`

位权是 8 的幂：

$$
N = \sum o_i 8^i
$$

例如：

$$
(3702)_8 = 3\times8^3 + 7\times8^2 + 0\times8^1 + 2\times8^0 = 1986
$$

*📄 见文末「原始 Slides」第 8–9 页：oct 的字符表、3-bit 分组思路，以及 3702_{8} 转十进制例题。*

### ③ 为什么 hex / oct 特别适合表示 binary？

因为：

$$
16 = 2^4,\qquad 8 = 2^3
$$

所以：

- **1 个 hex digit ↔ 4 bits**
- **1 个 oct digit ↔ 3 bits**

这使得它们与二进制之间可以**按组直接互转**，几乎不用真正做“运算”。

### 快速对照表

|  | 位权基数 | 合法数字 | 与 binary 的关系 |
| --- | --- | --- | --- |
| Decimal | 10 | 0–9 | 无直接固定位数组 |
| Binary | 2 | 0, 1 | 底层表示 |
| Octal | 8 | 0–7 | 1 oct digit = 3 bits |
| Hexadecimal | 16 | 0–9, A–F | 1 hex digit = 4 bits |

<aside>
📌

**口诀：** 看见 16 想 4 bits，看见 8 想 3 bits。

</aside>

## 4️⃣ Binary ↔ Hex / Oct：最值得会的“分组法”

### ① Binary → Hex

从 **right to left(从右向左)** 每 4 位一组，不足 4 位时左侧补 0，然后把每组换成一个 hex digit。

例如：

$$
1100101001010111_2 = (1100)(1010)(0101)(0111)_2 = (CA57)_{16}
$$

### ② Hex → Binary

把每个 hex digit 直接替换成 4-bit binary：

- `1 → 0001`
- `0 → 0000`
- `A → 1010`
- `4 → 0100`

所以：

$$
(10A4)_{16} = 0001\ 0000\ 1010\ 0100_2
$$

*📄 见文末「原始 Slides」第 10 页：Hex2Bin & Bin2Hex worked example。*

### ③ Binary → Oct

从右向左每 3 位一组，不足 3 位时左侧补 0。

例如：

$$
011010000100_2 = (011)(010)(000)(100)_2 = (3204)_8
$$

### ④ Oct → Binary

把每个 oct digit 直接替换成 3-bit binary：

$$
(7526)_8 = 111\ 101\ 010\ 110_2
$$

*📄 见文末「原始 Slides」第 11 页：Oct2Bin & Bin2Oct worked example。*

### 常用映射表

| Decimal | Binary(4-bit) | Hex | Binary(3-bit) | Oct |
| --- | --- | --- | --- | --- |
| 0 | 0000 | 0 | 000 | 0 |
| 1 | 0001 | 1 | 001 | 1 |
| 2 | 0010 | 2 | 010 | 2 |
| 3 | 0011 | 3 | 011 | 3 |
| 4 | 0100 | 4 | 100 | 4 |
| 5 | 0101 | 5 | 101 | 5 |
| 6 | 0110 | 6 | 110 | 6 |
| 7 | 0111 | 7 | 111 | 7 |
| 8 | 1000 | 8 | — | — |
| 9 | 1001 | 9 | — | — |
| 10 | 1010 | A | — | — |
| 11 | 1011 | B | — | — |
| 12 | 1100 | C | — | — |
| 13 | 1101 | D | — | — |
| 14 | 1110 | E | — | — |
| 15 | 1111 | F | — | — |
- 📚 拓展 — Oct2Hex / Hex2Oct 为什么通常先借 binary？
    
    8 和 16 之间并不是整次幂关系，不能像 2↔8、2↔16 那样“一位对若干位”直接映射。最稳妥的方法是：
    
    **Oct → Binary → Hex**，或 **Hex → Binary → Oct**。
    
    因为 binary 是两者共同的“中介语言”。
    

## 5️⃣ Decimal → Binary / Other Base：整数怎么转？

## 5.1 试权法 Try and Error（from high bits）

思路：先写出各个二进制位的位权，从高位往低位看，哪些位权能凑出目标十进制数，就放 1；不能就放 0。

例如把 49 转成 binary：

$$
49 = 32 + 16 + 1 = 2^5 + 2^4 + 2^0
$$

所以：

$$
49_{10} = 110001_2
$$

*📄 见文末「原始 Slides」第 13 页：Method 1 — from high bits。*

### 这个方法的本质

不是“猜”，而是在做：

$$
N = \sum b_i 2^i
$$

你在逐位决定每个 $b_i$ 是 0 还是 1。

## 5.2 Division-by-2（除 2 取余法）

对十进制整数不断除以 2，记录每次的 **remainder(余数)**；当 **quotient(商)** 变成 0 时停止。最后把余数**倒着读**，得到 binary。

例如 12：

1. $12\div2=6$，余 0
2. $6\div2=3$，余 0
3. $3\div2=1$，余 1
4. $1\div2=0$，余 1

倒着读：

$$
12_{10} = 1100_2
$$

*📄 见文末「原始 Slides」第 14 页：Division-by-2 图解（强调 first remainder = LSB，last remainder = MSB）。*

<aside>
🧠

**LSB(least significant bit, 最低有效位)** 是第一次产生的余数；
**MSB(most significant bit, 最高有效位)** 是最后一次产生的余数。
所以答案一定要**反向读取**。

</aside>

## 5.3 Decimal → Other Base（任意进制整数）

对于 base = $r$ 的系统，方法完全平行：

- 不断除以 $r$
- 记录余数
- 倒着读余数

于是：

$$
N_{10} \to N_r
$$

的统一算法就是 repeated division by base。

*📄 见文末「原始 Slides」第 15 页：Decimal to Other Base 的 general method。*

- 📚 拓展 — 为什么“倒着读余数”？
    
    因为第一次除法得到的是最低位（个位）信息，第二次得到的是更高一位，依次上升。也就是说算法天然按“从低位到高位”产出，所以最后必须反向读，才能恢复成正常书写顺序。
    

## 6️⃣ Decimal Fraction → Binary：小数怎么转？

### 核心方法：Multiplication-by-2（乘 2 取整法）

对十进制小数不断乘以 2，每次取结果的整数部分（0 或 1）作为下一位 binary digit，继续对新的小数部分重复。

如果：

$$
x_0 = x,\qquad x_{k+1} = \operatorname{frac}(2x_k)
$$

那么第 $k$ 步产生的 binary 位就是：

$$
b_k = \lfloor 2x_{k-1}\rfloor
$$

### 例子：0.188 转 binary

1. $0.188\times2 = 0.376$ → 取 0
2. $0.376\times2 = 0.752$ → 取 0
3. $0.752\times2 = 1.504$ → 取 1
4. $0.504\times2 = 1.008$ → 取 1
5. $0.008\times2 = 0.016$ → 取 0

因此，取 5 位有效二进制小数：

$$
0.188_{10} \approx 0.00110_2
$$

*📄 见文末「原始 Slides」第 16 页：0.188 的 conversion example。*

### 再看一个：0.3125

不断乘 2：

- $0.3125\times2=0.625$ → 0
- $0.625\times2=1.25$ → 1
- $0.25\times2=0.50$ → 0
- $0.50\times2=1.00$ → 1

所以：

$$
0.3125_{10} = 0.0101_2
$$

进一步：

$$
21.375_{10} = 10101.011_2
$$

*📄 见文末「原始 Slides」第 17 页：fraction conversion 的第二个例子。*

<aside>
⚠️

**注意：** 并不是所有十进制小数都能在二进制里有限终止。很多数会出现无限循环，只能截断或近似。

</aside>

- 📚 拓展 — 哪些十进制小数能有限地写成 binary？
    
    一个十进制分数若化到最简后，分母只含 2 的幂，才可能在 binary 中有限终止。
    
    例如：$0.3125 = 5/16$，分母是 $2^4$，所以能有限终止；
    
    而 $0.1 = 1/10 = 1/(2\times5)$ 含因子 5，因此在 binary 中会无限循环。这也是为什么很多编程语言里浮点数会有表示误差。
    

## 7️⃣ Thought Exercises：这节真正要会什么？

slides 最后的题目本质上是在检查 6 类能力：

1. **binary → decimal**
2. **binary → hexadecimal**
3. **binary → octal**
4. **decimal → binary / hexadecimal / octal**
5. **hexadecimal → binary / octal**
6. **octal → binary / decimal**
7. **decimal fraction → binary**

### 做题时的首选路线

| 题型 | 推荐路线 |
| --- | --- |
| Binary → Decimal | 按位权展开：$\sum b_i2^i$ |
| Hex / Oct → Decimal | 按位权展开：$\sum h_i16^i$ 或 $\sum o_i8^i$ |
| Binary ↔ Hex | 按 4 位分组 / 反分组 |
| Binary ↔ Oct | 按 3 位分组 / 反分组 |
| Decimal Integer → Base r | Repeated division by r |
| Decimal Fraction → Binary | Repeated multiplication by 2 |

*📄 见文末「原始 Slides」第 18–19 页：thought exercises 与 calculator / Python conversion 提示。*

## ✅ 本节总结（考前速记版）

<aside>
📌

1. **所有数制都靠位权读数**：值 = 各位数字 × 对应幂次再求和。

2. **Hex / Oct 是 binary 的压缩写法**：1 hex = 4 bits，1 oct = 3 bits。

3. **整数换进制靠“除基取余倒着读”**；小数换进制靠“乘基取整顺着写”。

4. **有限小数不一定在 binary 里有限终止**，这点和浮点误差直接相关。
</aside>

## 🚀 下次打开第一步

> 先自己手算三件事：① `101101_2` 转十进制；② `52_{10}` 转二进制；③ `A2F_{16}` 先转 binary 再转 octal。做完再回来看自己到底卡在“位权展开”还是“分组法 / 除基取余法”。
> 

## 📎 原始 Slides

[lecture_1_p3.pdf](EE115B%20Lecture1%20Part3-4%20%E2%80%94%20Number%20Systems%20&%20Convers/lecture_1_p3.pdf)
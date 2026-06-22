# EE115B Lecture2 Part1 — Binary Arithmetic 二进制加减乘除

<aside>
➕

**本节主题：** 二进制运算：有符号数三种表示（sign-magnitude 原码 / 1's complement 反码 / 2's complement 补码）→ 补码加减法 + overflow 判定 → 二进制乘法（direct addition 直接加法法 / partial products 部分积法）→ 二进制除法（brute force 暴力法 / partial quotient 部分商法）。

**教材：** Floyd《Digital Fundamentals》Ch.2。讲义来源 EE115B（Chenxi Xiao），本节为 **Lecture 2 Part 1**，共 21 页。

**核心脉络：** ① 为什么要补码？→ 把减法变加法，硬件最简 → ② 三种有符号表示的定义 / 范围 / 零的个数对比 → ③ 补码加减 + overflow 判断 → ④ 乘法两种方法 → ⑤ 除法两种方法。

</aside>

## 1️⃣ 为什么把减法变加法？（Motivation）

<aside>
💡

引入 **complement form（补码形式）** 的两大 motivation（动机）：

- **Simplifying（简化）both hardware and arithmetic operations**——only addition hardware is needed（只需加法器），无需单独的减法电路。
- **No need to determine which number is larger**——不需要判断哪个数更大再做运算。
</aside>

**为什么原码直接加法会出错？** 以 $1 + (-1) = 0$ 为例：用原码 `0001 + 1001 = 1010 ≠ 0`，结果完全错误。这正是引入补码的直接动机，即 "This is solved by introducing: complement form"。

## 2️⃣ 有符号数三种表示 Signed Number Representations

### ① 原码 Sign-Magnitude

**定义：** MSB（最高位）= sign bit（符号位），$0$ 表示正，$1$ 表示负；其余位 = magnitude（量值，即绝对值）。

**8-bit 范围：** $-127 \sim +127$，共 255 个有效值。

**致命缺陷：** 存在两个零——`00000000 = +0` 和 `10000000 = -0`；直接相加也会出错。

*📄 见文末「原始 Slides」第 5 页：Eight-bit sign-magnitude 对照表（含 10000000 = -0 的红框标注）。*

### ② 反码 1's Complement

**定义：** 负数 = 对应正数的 bitwise NOT（按位取反）。公式：

$$
[N] = \begin{cases} N, & N \ge 0 \\ 2^n - 1 - |N|, & N < 0 \end{cases}
$$

**8-bit 范围：** $-127 \sim +127$，仍然有两个零——`00000000 = +0`，`11111111 = -0`。

**遗留问题：** 加减法运算后若有 end-around carry（端进位），需要把进位加回最低位，仍比补码麻烦。

*📄 见文末「原始 Slides」第 7 页：Eight-bit ones' complement 对照表（含 11111111 = -0 红框标注 + 公式）。*

### ③ 补码 2's Complement ★ 最常用

**定义：** 负数 = ones' complement + 1（反码加一）。等价公式：

$$
N^* = 2^n - N
$$

**8-bit 范围：** $-128 \sim +127$，共 **256 个数**（比原码 / 反码多一个 $-128$）。

**核心优势：唯一零！** 只有 `00000000 = 0`，不存在 $-0$。

*📄 见文末「原始 Slides」第 8 页：Eight-bit two's complement 对照表（含公式 $`N^*=2^n-N`$，10000000 = −128 是最小值）。*

### 📊 三种表示对比

|  | Sign-Magnitude（原码） | 1's Complement（反码） | 2's Complement（补码）★ |
| --- | --- | --- | --- |
| 定义 | MSB=符号位，其余=绝对值 | 负数 = 正数按位取反 | 负数 = 反码 + 1 |
| 公式 | — | $[N]=2^n-1-|N|$ | $N^*=2^n-N$ |
| 8-bit 范围 | $-127\sim+127$ | $-127\sim+127$ | $-128\sim+127$ ✅ 多一个 |
| 零的个数 | **2 个**（+0 和 -0） | **2 个**（+0 和 -0） | **1 个**（唯一）✅ |
| 加减硬件 | 需判符号后分情况处理 | 需额外处理端进位（EAC） | 直接加法，最简 ✅ |

### 📝 练习 Exercises（slides 9–11）

**8-bit 三种表示对照（+6 / -6 / 0）：**

| 数值 | Sign-Magnitude | 1's Complement | 2's Complement |
| --- | --- | --- | --- |
| +6 | 00000110 | 00000110 | 00000110 |
| -6 | 10000110 | 11111001 | 11111010 |
| 0 | 00000000 / 10000000 | 00000000 / 11111111 | 00000000（唯一）✅ |

**16-bit 2's complement of** $-6$**：** `1111 1111 1111 1010`。

规律：**sign extension（符号扩展）**——把短补码扩展到更宽时，用符号位（1）填充所有高位，数值不变。

- 📚 拓展 — 取 2's complement 的两种等价方法
    
    **方法 A（两步）：** 按位取反，再末位加 1。
    **方法 B（一步快速法）：** 从最低位往高位扫描，遇到第一个 1 之前的所有 0 保留，第一个 1 也保留，之后所有位取反。这两种方法等价，方法 B 在手算时更快（不需要进位传播）。
    例：-6 = 取反 11111001 + 1 = 11111010；或直接从 LSB 扫：**0**（保留）→ 遇第一个 1：**1**（保留）→ 之后 00000 全取反 → 11111，组合 = **11111010** ✅。
    

## 3️⃣ 2's Complement 加减法

### 加负数 Adding Negative Numbers

**规则：** 把所有数写成 2's complement 形式，直接相加；若产生最终 final carry（最终进位），**discard carry（丢弃进位）**，结果仍正确。

*📄 见文末「原始 Slides」第 12 页：四种 case 的 worked examples（both positive / |正|>|负| / |负|>|正| / both negative），含 Discard carry 粉色标注箭头。*

<aside>
🧠

**加负数三种典型情况：**
· 两正 → 直接相加，无进位。
· 正 + 负（|正|>|负|）→ 有进位，**丢弃**，结果为正值。
· 正 + 负（|负|>|正|）或两负 → 无进位（或有进位丢弃后），MSB = 1 表示负值。

</aside>

### 减法 Subtraction

**核心：** $A - B = A + (-B)$，其中 $-B$ = B 的 2's complement（对 B 取补码）。

**重要注意：必须事先确定位宽（number of bits in advance）！**

*📄 见文末「原始 Slides」第 13 页：减法 worked example（*$+8 - (+3) = +5$*，含 Discard carry 标注）+ 下方 8 组对比矩阵（不同位宽下正确 vs 溢出，红框标注溢出组）。*

### 溢出 Overflow

**定义：** 两数相加的结果所需位数超过给定位宽，导致 sign bit（符号位）错误。

<aside>
⚠️

**Overflow 只能在两数同号时发生：**
· 两正相加 → sum 可能超过最大正值 → 符号位错误地变 1（负）。
· 两负相加 → sum 可能超出最小负值 → 符号位错误地变 0（正）。
**判断方法：若结果的 sign bit 与两个 operand（操作数）的 sign bit 不同 → overflow！**

</aside>

*📄 见文末「原始 Slides」第 14 页：Overflow condition 示例（*$125 + 58 = 183$*，8-bit 补码* $01111101 + 00111010 = 10110111$*，结果符号位错误；标注 "Sign incorrect" 和 "Magnitude incorrect"）。*

- 📚 拓展 — 硬件如何检测 overflow？
    
    硬件 ALU 用 XOR 门检测 overflow：比较**进入 MSB 的 carry-in** 与**从 MSB 产生的 carry-out**，若 $C_{in} \oplus C_{out} = 1$ 则 overflow。这正是 CPU 里 **overflow flag（溢出标志位 OF）** 的工作原理。例如 x86 的 `JO`（Jump if Overflow）指令就依赖这个标志位。值得注意的是 overflow flag ≠ carry flag（进位标志）——unsigned 运算用 carry flag，signed 运算用 overflow flag。
    

## 4️⃣ 二进制乘法 Binary Multiplication

**前提：** 两种方法都要求先将数字转为 **true uncomplemented form（无符号原码形式）**，完成乘法后再处理符号。

<aside>
💡

**符号规则：** 同号相乘 → 积为正；异号相乘 → 积为负。（与十进制完全相同）

</aside>

### ① 直接加法法 Direct Addition Method

**原理：** 乘法 = 把 multiplicand（被乘数）重复相加 multiplier（乘数）次。如 $8 \times 3 = 8 + 8 + 8 = 24$。

*📄 见文末「原始 Slides」第 15 页：Direct addition method worked example（01001101 × 00000100，即 77 × 4，逐次相加经两次 partial sum，最终 product = 100110100 = 308）。*

### ② 部分积法 Partial Products Method

<aside>
🪜

**五步法（Calculate in uncomplemented form, then convert back）：**
**Step 1：** 判断积的符号（同号→正，异号→负）。
**Step 2：** 把负数转为 uncomplemented form（即再取一次 2's complement）。
**Step 3：** 从 LSB 开始逐位生成 partial product（部分积）：乘数位 = 1 → partial product = multiplicand；乘数位 = 0 → partial product = 0。每个 partial product 依次左移一位。
**Step 4：** 将所有 partial products 累加得最终积。
**Step 5：** 若 Step 1 确定积为负，对积取 2's complement，再 attach（附加）符号位 1。

</aside>

*📄 见文末「原始 Slides」第 17 页：Partial products worked example（01010011 × 11000101，7 个 partial products 逐步累加，Step 2 取反 + Step 5 取反附符号位完整过程）。*

- 📚 拓展 — 为什么先转 uncomplemented form？& Booth 乘法
    
    部分积法的"位移累加"操作对正数（无符号）二进制才有意义。若直接对补码操作，符号位会被误当普通数据位处理。
    后来发展出的 **Booth Multiplication（Booth 乘法）**解决了这个问题——它直接处理 2's complement，无需预先转换；**Modified Booth（改进 Booth）**更进一步，每次处理 2 位，速度提升近一倍，是现代 CPU / DSP 实际采用的乘法器设计。
    

## 5️⃣ 二进制除法 Binary Division

两种方法同样都先将数字转为 uncomplemented form，完成除法后再处理符号。

### ① 暴力法 Brute Force Division（适用于小数）

**原理：** dividend（被除数）÷ divisor（除数）：不断用 2's complement 加法减去 divisor（减法 = 加 divisor 的补码），每减一次 quotient（商）+1，直到 partial remainder（部分余数）为 0 或负。

<aside>
🪜

**三步法：**
**Step 1：** 判断 quotient 的符号；quotient 初始化为 0（全 0）。
**Step 2：** 用 2's complement 加法做第一次减 divisor；若 partial remainder > 0（positive），quotient +1，继续 Step 3；若 ≤ 0，除法完成。
**Step 3：** 继续用 2's complement 减 divisor；若结果 > 0，quotient +1，重复；若 = 0 或 < 0，除法完成。

</aside>

*📄 见文末「原始 Slides」第 19 页：Brute force worked example（01100100 ÷ 00011001，即 100 ÷ 25，5 次迭代逐步演算，最终 quotient = 00000100 = 4）。*

### ② 部分商法 Partial Quotient Method

**原理：** 即十进制手算长除法（long division）的二进制版，每步对齐后试商 1 bit。

*📄 见文末「原始 Slides」第 20 页：Partial quotient method 图示（*$1001 \div 11 = 11$*，即* $9 \div 3 = 3$*，标准长除法竖式，二进制与十进制并排对照）。*

- 📚 拓展 — 更高级的硬件除法 / 乘法算法（Thought Exercises）
    
    了解即可，供有兴趣时探索：
    **硬件除法：**
    · **Restoring Division（恢复余数法）**：每步试商后，若余数为负则"恢复"（加回 divisor），再移位。
    · **Non-Restoring Division（不恢复余数法）**：不恢复，改用 ±1 的商位，减少迭代。
    · **SRT Division**（Digit-Recurrence，Intel / AMD 实际使用）——著名的 Pentium FDIV Bug（1994）就是 SRT lookup table 里有一个错误条目。
    **硬件乘法：**
    · **Booth Multiplication**：直接对补码操作，无需预转换。
    · **Modified Booth（Radix-4 Booth）**：每次处理 2 位，减少约一半加法次数，现代 CPU 乘法器主流方案。
    

## ✅ 本节总结（口诀）

<aside>
📌

1. **补码动机：** 减法变加法；唯一零；8-bit 范围 $-128\sim+127$（多一个 $-128$）。
2. **取补码：** 按位取反再 +1；等价 $N^*=2^n-N$；符号扩展时高位补符号位。
3. **加减法：** 统一加法，丢弃最终进位；**同符号相加且结果符号变 → overflow**。
4. **乘法：** 先转无符号形式；直接加法法 = 重复加；部分积法 = 移位累加，最后补符号。
5. **除法：** 先判符号；暴力法 = 不停减 divisor，quotient 计数；部分商法 = 二进制长除法。
</aside>

## 🚀 下次打开第一步

> 默写 $-6$ 的 8-bit 补码（+6 = 00000110 → 取反 11111001 → 加 1 → **11111010**），再手算一组 overflow 判断：$01111111 + 00000001$（即 $127 + 1$）在 8-bit 补码下结果是什么？是否 overflow？为什么？
> 

## 📎 原始 Slides

[lecture_2_part1.pdf](EE115B%20Lecture2%20Part1%20%E2%80%94%20Binary%20Arithmetic%20%E4%BA%8C%E8%BF%9B%E5%88%B6%E5%8A%A0%E5%87%8F%E4%B9%98%E9%99%A4/lecture_2_part1.pdf)
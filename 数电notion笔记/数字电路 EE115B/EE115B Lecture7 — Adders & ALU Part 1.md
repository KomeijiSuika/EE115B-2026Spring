# EE115B Lecture7 — Adders & ALU Part 1

<aside>
➕

**本节主题：** Combinational Logic Part 1 —— 加法器 Adders 与算术逻辑单元 ALU，数字系统里“算数”的基石。

**讲义来源：** EE115B（Chenxi Xiao），共 23 页；本节为该讲 **Part 1**。

**核心脉络：** 半加器 → 全加器（= 两个半加器）→ 并行加法器：进位纹波 Ripple Carry → 超前进位 Look-Ahead Carry（$C_g, C_p$）→ 超前进位电路 + 74HC283 → ALU（74LS181）。

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md)（组合逻辑部分）；同为 Lecture7：**Part 2** = 编码 / 译码器 见 [EE115B Lecture7 — Encoders & Decoders Part 2](EE115B%20Lecture7%20%E2%80%94%20Encoders%20&%20Decoders%20Part%202.md)、**Part 3** = 比较器 / MUX / Hazard 见 [EE115B Lecture7 — Comparator · MUX / DEMUX · Hazard Part 3](EE115B%20Lecture7%20%E2%80%94%20Comparator%20%C2%B7%20MUX%20DEMUX%20%C2%B7%20Hazard.md)。

</aside>

# ➕ 一、Adders 加法器

## 1️⃣ 半加器 Half-Adder（slide 3）

**半加器 (half adder)：** 两个二进制输入 $A, B$，两个输出——本位和 $\Sigma$ 与进位 $C_{out}$。只管两个输入，**不接受下位进来的进位**，所以叫“半”加器。

$$
\Sigma = A \oplus B = A\bar{B} + \bar{A}B, \qquad C_{out} = AB
$$

![Slide 3 — 半加器：真值表 + XOR/AND 电路](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201/slide_3.png)

Slide 3 — 半加器：真值表 + XOR/AND 电路

## 2️⃣ 全加器 Full-Adder（slides 4–8）

**全加器 (full adder)：** 三个输入 $A, B, C_{in}$（多了下位进位），两个输出 $\Sigma, C_{out}$。

$$
\Sigma = A \oplus B \oplus C_{in}, \qquad C_{out} = AB + (A \oplus B)\,C_{in}
$$

![Slide 4 — 全加器：真值表 + 符号](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201/slide_4.png)

Slide 4 — 全加器：真值表 + 符号

**一个全加器 = 两个半加器 + 一个 OR 门：** 第一个半加器算 $A \oplus B$，第二个再加上 $C_{in}$；两个半加器的进位相或得总进位。

![Slide 8 — 全加器实现（两个半加器）](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201/slide_8.png)

Slide 8 — 全加器实现（两个半加器）

<aside>
💡

**记忆法：** 和 = 三个输入相异或（$A\oplus B\oplus C_{in}$）；进位 = “本位产生”$AB$ 加上“下位进位被传递”$(A\oplus B)C_{in}$。

</aside>

- ❓ Q&A：加法器这些公式怎么记最快？（2026-06-19）
    
    **一句话总纲：和看「奇偶」，进位看「多数 / 闸门」，三组公式其实是一个核心反复用。**
    
    **① 半加器 —— 最直觉，先背它**
    
    - 和 $\Sigma = A\oplus B$：两个数**不一样**才出 1（异或＝“异”就 1）。
    - 进位 $C_{out}=AB$：**两个都是 1** 才进位（AND）。
    
    **② 全加器 —— 记“功能”，别死背布尔式**
    
    - 和 $\Sigma = A\oplus B\oplus C_{in}$ = **奇偶校验 (parity)**：三个输入里 **1 的个数是奇数 → 和为 1**，偶数 → 0。
    - 进位 $C_{out}$ = **多数表决 (majority)**：三个输入里**至少两个是 1 就进位**，展开为
    
    $$
    C_{out}=AB+AC_{in}+BC_{in}
    $$
    
    它和课件的 $C_{out}=AB+(A\oplus B)C_{in}$ 完全等价（slide 15 的练习就是证这个）。
    
    **③ 也可以“拆成两个半加器”记：** 全加器 = 两个半加器 + OR。第 1 个半加器出 $A\oplus B$ 和 $AB$；第 2 个把 $A\oplus B$ 与 $C_{in}$ 再加，出 $\Sigma$ 和 $(A\oplus B)C_{in}$；两个进位 OR 起来就是总进位。
    
    **④ 超前进位 Cg / Cp —— 用“闸门”图像记**
    
    - $C_g=AB$（generate，**g 配 AND**）：和半加器进位**一模一样**——两个都 1，本位**自己涌出**一个进位。
    - $C_p=A+B$（propagate，**p 配 OR**）：只要 A 或 B 有一个是 1，这一位就是一扇**打开的闸门**，让下面的进位**穿过去**。
    - $C_{out}=C_g+C_pC_{in}$：**自己涌出**，或**闸门开着且下面真有进位传上来**。
    
    **⑤ 一条主线串起来：** “两个都 1 才进位”出现了三次——半加器进位 $AB$ ＝ 全加器生成项 ＝ 超前进位 $C_g$，本质同一件事。
    
    **🐈 防丢分提醒：** 写全加器进位别漏项——要么写“多数形”$AB+AC_{in}+BC_{in}$（三项），要么写“半加器形”$AB+(A\oplus B)C_{in}$，**两种各自完整**，别混着写成漏项的两项式。
    

---

# 🔗 二、Parallel Adders 并行加法器

## 3️⃣ 进位纹波 Ripple Carry（slides 9–11）

把 $n$ 个全加器串联：每一位的 $C_{out}$ 接到高一位的 $C_{in}$。

![Slide 11 — 4 位进位纹波加法器（最坏情况进位延迟）](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201/slide_11.png)

Slide 11 — 4 位进位纹波加法器（最坏情况进位延迟）

<aside>
⏱️

**致命缺点 — 进位传播延迟：** 高位的和必须等进位一级一级“纹波”上来才能确定。图中每级 8 ns，4 位最坏情况 = $4 \times 8 = 32$ ns；位数越多延迟越长（线性 $O(n)$）。

</aside>

## 4️⃣ 超前进位 Look-Ahead Carry：原理（slides 12–17）

思路：不要等进位逐级传，而是用**低延迟的** $C_g, C_p$ 直接算出每位进位。

$$
C_g = AB \;(\text{生成}), \qquad C_p = A + B \;(\text{传递}), \qquad C_{out} = C_g + C_p\,C_{in}
$$

![Slide 14 — 进位生成 vs 传递的四种情形](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201/slide_14.png)

Slide 14 — 进位生成 vs 传递的四种情形

| 术语 | 含义 | 表达式 |
| --- | --- | --- |
| 生成 Generated | 本位自己内部产生进位 | $C_g = AB$ |
| 传递 Propagated | 下位进位被本位“透传”出去 | $C_p = A + B$ |
| 输出进位 | 两者合成 | $C_{out} = C_g + C_p C_{in}$ |

### 🔑 逐位递推化简：从「递归」到「两级逻辑」（slides 16–17）

<aside>
🎯

**这一步才是超前进位的灵魂。** 目标：把「每一位进位都依赖前一位进位」的**递归式**，靠代数代入 (substitute) 化简成**只含** $C_g$**、**$C_p$ **和最初进位** $C_{in1}$ **的两级 AND-OR 表达式**，于是所有位的进位能**并行 (in parallel)** 算出，不用再一级一级等。

</aside>

**① 每一位都能写出同一个基本式（slide 16）：** 第 $i$ 位全加器有自己的生成项 $C_{gi}=A_iB_i$、传递项 $C_{pi}=A_i+B_i$，而它的进位输入正是低一位的进位输出（$C_{in(i+1)} = C_{out\,i}$）：

$$
C_{out\,i} = C_{gi} + C_{pi}\,C_{in\,i}
$$

![Slide 16 — 四个全加器各自的 Cg / Cp](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201/slide_16.png)

Slide 16 — 四个全加器各自的 Cg / Cp

<aside>
💡

**关键观察：** $C_{gi}, C_{pi}$ **只由本位的** $A_i, B_i$ **决定**，一级门（AND / OR）就能把所有位的 $C_g, C_p$ **同时**算出来，延迟极低。真正拖慢电路的只有那个「要等下面传上来」的 $C_{in\,i}$。所以化简的全部动机就是——**把每个** $C_{in\,i}$ **一路向下代入，直到式子里只剩最初的** $C_{in1}$**。**

</aside>

**② 逐位代入展开（slide 17 完整过程）：**

**▸ Full-adder 1** —— 进位输入就是最初的 $C_{in1}$，本身已是最简：

$$
C_{out1} = C_{g1} + C_{p1}\,C_{in1}
$$

**▸ Full-adder 2** —— 它的进位输入 $C_{in2} = C_{out1}$，把上式整个代进去，再用分配律 (distributive law) 展开：

$$
\begin{aligned}
C_{out2} &= C_{g2} + C_{p2}\,C_{in2} = C_{g2} + C_{p2}\,C_{out1}\\
&= C_{g2} + C_{p2}\,(C_{g1} + C_{p1}C_{in1})\\
&= C_{g2} + C_{p2}C_{g1} + C_{p2}C_{p1}C_{in1}
\end{aligned}
$$

**▸ Full-adder 3** —— 同理 $C_{in3} = C_{out2}$，把上一行结果代入展开：

$$
\begin{aligned}
C_{out3} &= C_{g3} + C_{p3}\,C_{out2}\\
&= C_{g3} + C_{p3}C_{g2} + C_{p3}C_{p2}C_{g1} + C_{p3}C_{p2}C_{p1}C_{in1}
\end{aligned}
$$

**▸ Full-adder 4** —— 再代一次 $C_{in4} = C_{out3}$：

$$
\begin{aligned}
C_{out4} &= C_{g4} + C_{p4}\,C_{out3}\\
&= C_{g4} + C_{p4}C_{g3} + C_{p4}C_{p3}C_{g2} + C_{p4}C_{p3}C_{p2}C_{g1} + C_{p4}C_{p3}C_{p2}C_{p1}C_{in1}
\end{aligned}
$$

<aside>
🧠

**每一项都有物理意义（这样记最不会忘）——** 以 $C_{out4}$ 为例，从左到右读：

- $C_{g4}$：第 4 位**自己生成 (generated)** 进位；
- $C_{p4}C_{g3}$：第 3 位生成，被第 4 位**传递 (propagated)** 上来；
- $C_{p4}C_{p3}C_{g2}$：第 2 位生成，被第 3、4 位**一路传递**；
- $C_{p4}C_{p3}C_{p2}C_{g1}$：第 1 位生成，被第 2、3、4 位传递；
- $C_{p4}C_{p3}C_{p2}C_{p1}C_{in1}$：最初的 $C_{in1}$ 被**全部四位连续透传**到顶。

**一句话口诀：进位来源只有两类 —— 「某一位自己生成」，或「更低位 / 最初进位生成后，被它上面每一位连续传递」。** 每条传递链就是一串 $C_p$ 连乘。

</aside>

<aside>
⚡

**为什么这样就快了：** 展开后每个 $C_{out\,i}$ 都是标准的**积之和 (sum-of-products, SOP)**，只要 **AND 层 → OR 层两级门**。而所有 $C_{gi}, C_{pi}$ 在第 0 级就并行备好，于是 $C_{out1}\sim C_{out4}$ 可以**同时**算出 —— 进位延迟固定在 ~2 级门，**与位数** $n$ **无关（≈** $O(1)$**）**，彻底干掉了 ripple carry 那条 $O(n)$ 的等待长链。

</aside>

## 5️⃣ 超前进位：电路实现（slide 18）

把上一节化简出的每个 SOP 表达式**直接照搬成电路**：每个乘积项（如 $C_{p4}C_{p3}C_{g2}$）接一个 **AND 门**，再把同一位的全部乘积项喂进一个 **OR 门**，得到该位的 $C_{out}$。因为四位都是统一的两级 AND-OR 结构，$C_{out1}\sim C_{out4}$ **并行**生成、互不等待。

![Slide 18 — 超前进位电路实现（附 64 位 AND 门估算思考题）](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201/slide_18.png)

Slide 18 — 超前进位电路实现（附 64 位 AND 门估算思考题）

<aside>
⚖️

**核心 trade-off：** 超前进位用**面积换速度**。第 $k$ 位的 $C_{out}$ 展开项数随 $k$ 增长，门数是 $O(n^2)$：64 位加法器光进位 AND 门约 $1+2+\dots+64 = 2080$ 个——代价随位宽平方增长。

</aside>

## 6️⃣ 商用芯片 74HC283（slide 19）

![Slide 19 — 74HC283：4 位并行加法器，可级联扩展](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201/slide_19.png)

Slide 19 — 74HC283：4 位并行加法器，可级联扩展

74HC283 是现成的 4 位并行加法器（内部带超前进位），可级联拼出更高位加法器。

<aside>
🔧

**工程折中：** 纯超前进位在高位数时代价太高；实际常把纹波进位与超前进位**混合**（块内超前、块间纹波）。另一个应用：全加器可用来**数 1 的个数**（slide 20 的低成本投票系统）。

</aside>

---

# 🧮 三、Arithmetic Logic Unit (ALU)

## 7️⃣ ALU 与 74LS181（slides 21–23）

加法器只是 ALU 的一部分。一个完整的 ALU 还需要：

1. **opcode**：选择 $+, -$ 以及位运算（`xor / or / and`）。
2. 针对电路复杂度、功耗、传播延迟、成本、面积做优化。

![Slide 22 — 74LS181 ALU：引脚图 + 功能选择表](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201/slide_22.png)

Slide 22 — 74LS181 ALU：引脚图 + 功能选择表

74LS181 是经典的 4 位 ALU：用 $S_3 S_2 S_1 S_0$ 选功能、$M$ 区分逻辑（$M=H$）/ 算术（$M=L$）操作，$C_n$ 控制是否带进位。一共可做 16 种逻辑 + 16 种算术运算。

---

## 📝 本节总结（记三点就够）

<aside>
🎯

1. **半加器 vs 全加器：** 半加器 $\Sigma=A\oplus B,\ C_{out}=AB$（不收下位进位）；全加器 $\Sigma=A\oplus B\oplus C_{in},\ C_{out}=AB+(A\oplus B)C_{in}$ = 两个半加器 + OR。
2. **Ripple vs Look-Ahead：** 纹波进位电路简单但延迟 $O(n)$；超前进位用 $C_g=AB,\ C_p=A+B,\ C_{out}=C_g+C_pC_{in}$ 把延迟压到 $O(1)$，代价是门数 $O(n^2)$。实际常两者混合（74HC283）。
3. **ALU = 加法器 + opcode 选择逻辑：** 74LS181 用 $S_3..S_0$ / $M$ / $C_n$ 选择几十种算术与逻辑运算。
</aside>

## ✅ 作业 / 待办

- 本节 slides 未给出明确的 Homework / 考试 deadline；拿到 syllabus 后再补 Lab / HW 截止时间。
- [ ]  思考题（slide 18）：估算 64 位超前进位加法器需要多少个 AND 门（提示：$\sum_{k=1}^{64} k = 2080$，$O(n^2)$）。
- [ ]  练习（slide 15）：证明全加器进位的两种写法 $C_{out}=AB+\bar A B C_{in}+A\bar B C_{in}$ 与 $C_{out}=C_g+C_p C_{in}$ 等价。

## 📎 原始 Slides

[lecture_7_part1.pdf](EE115B%20Lecture7%20%E2%80%94%20Adders%20&%20ALU%20Part%201/lecture_7_part1.pdf)
# EE115B Digital Circuit Homework 4

<aside>
📝

**Digital Circuit Homework** — Instructor: Chenxi Xiao · 课程支持（HW3-4）

**Deadline:** 23:59 June 15, 2026

**Total:** 100 pts

</aside>

<aside>
🐈

**本次只做一件事：** 把这 6 道题逐题读懂、判断考点，然后**自己动手做**——不要边做边切到群聊 / 手机。

每题下方的「易错点」折叠卡只在你卡住时再点开，它只给审题方向，不给答案。

先从 Problem 1 开始，按 8–25 分钟一个学习块推进。

</aside>

## Instructions

- Please write your answers clearly and show the main steps of your reasoning.
- Except for the screenshots of the HDLBits programming problem, please submit handwritten solutions.
- For the HDLBits problem, submit screenshots showing successful completion. Include your code if it is not clearly visible in the screenshot.
- Late submissions may result in a score deduction.

---

## Problem 1. [15 pts]

Analyze the synchronous sequential circuit shown below. The circuit contains two positive-edge-triggered D flip-flops. The outputs of the flip-flops are denoted by $Q_1$ and $Q_0$.

![Problem 1 circuit](EE115B%20Digital%20Circuit%20Homework%204/p1_fixed.png)

Problem 1 circuit

**(a)** Derive the Boolean expressions for the D inputs $D_1$ and $D_0$. **[5 pts]**

- ✅ 参考答案 (a)
    
    $D_1 = Q_0$，$D_0 = \overline{Q_1}$
    
    因为 D 触发器满足 $Q^{+} = D$，所以只需照电路把每个 D 端写成现态 $Q$ 的函数。
    

**(b)** Write the complete state transition table. Use $Q_1 Q_0$ as the present state and $Q_1^{+} Q_0^{+}$ as the next state. **[5 pts]**

- ✅ 参考答案 (b)
    
    次态关系：$Q_1^{+} = D_1 = Q_0$，$Q_0^{+} = D_0 = \overline{Q_1}$
    
    | $Q_1$ | $Q_0$ | $Q_1^{+}$ | $Q_0^{+}$ |
    | --- | --- | --- | --- |
    | 0 | 0 | 0 | 1 |
    | 0 | 1 | 1 | 1 |
    | 1 | 0 | 0 | 0 |
    | 1 | 1 | 1 | 0 |

**(c)** Draw the state transition diagram and determine whether the generated state sequence has the Gray-code property. Briefly justify your answer. **[5 pts]**

- ✅ 参考答案 (c)
    
    状态序列（环）：$00 \to 01 \to 11 \to 10 \to 00$
    
    **有格雷码特性（Yes）。** 相邻两状态之间每次跳转都恰好只翻转一位（exactly one bit changes）：00→01 变 $Q_0$；01→11 变 $Q_1$；11→10 变 $Q_0$；10→00 变 $Q_1$。
    
- ⚠️ 易错点 / ADHD 纠错
    - 这类题最容易做错的点：next-state 表的「现态 → 次态」方向写反；漏写某一行状态。
    - 容易看漏的条件 / 单位 / 符号：是 positive-edge-triggered(上升沿触发)；看清图里哪个是 $Q_1$(MSB)、哪个是 $Q_0$。
    - 启动困难时第一步先做什么：照电路图把每个 D 输入用 $Q_1, Q_0$ 写出来，再逐行代入列表。

---

## Problem 2. [15 pts]

Build a circuit that realizes the next-state behavior of a positive-edge-triggered JK flip-flop using one positive-edge-triggered D flip-flop and basic logic gates. Ignore propagation delay, setup time, and hold time.

**(1)** Complete the JK flip-flop next-state table below. **[5 pts]**

| J | K | Current State Q | Next State Q_next |
| --- | --- | --- | --- |
| 0 | 0 | 0 |  |
| 0 | 0 | 1 |  |
| 0 | 1 | 0 |  |
| 0 | 1 | 1 |  |
| 1 | 0 | 0 |  |
| 1 | 0 | 1 |  |
| 1 | 1 | 0 |  |
| 1 | 1 | 1 |  |

**(2)** Derive the simplified Boolean equation for the D input in terms of J, K, and the present state Q. That is, find $D = f(J, K, Q)$. **[5 pts]**

D =

**(3)** Draw the circuit implementation using inputs J and K, one D flip-flop, and NOT, AND, and OR gates. **[5 pts]**

- ⚠️ 易错点 / ADHD 纠错
    - 这类题最容易做错的点：JK 特性记错——J=K=1 是 toggle(翻转)、J=K=0 是 hold(保持)，别和 SR 混。
    - 容易看漏的条件 / 单位 / 符号：题目限定只能用 **1 个** D FF + NOT/AND/OR，不要偷偷再加触发器。
    - 启动困难时第一步先做什么：先把 8 行 next-state 表填满，再对 $Q_{next}$ 做卡诺图化简得到 $D$。

---

## Problem 3. [15 pts]

You are provided with several 32K × 8-bit SRAM chips. Design a memory system with total capacity

$$
64\text{K} \times 16 \text{ bits.}
$$

Assume the memory is organized as 64K addressable locations, and each addressable location stores one 16-bit data word. The CPU has a 16-bit address bus ($A_{15}, A_{14}, \ldots, A_0$), where each address selects one 16-bit memory location. The CPU also has a 16-bit data bus ($D_{15}, D_{14}, \ldots, D_0$).

Each SRAM chip has an active-low chip-select input $\overline{CS}$. You only need to show the address bus, data bus, and chip-select logic; read/write control signals are omitted.

**(a)** Determine the total number of 32K × 8-bit SRAM chips required. Briefly explain how width expansion and depth expansion are achieved. **[5 pts]**

**(b)** Draw a block-level circuit diagram showing the connections of the address bus, data bus, and active-low chip-select signals ($\overline{CS}$). Use the most significant address bit $A_{15}$ and one NOT gate for address decoding. **[10 pts]**

- ⚠️ 易错点 / ADHD 纠错
    - 这类题最容易做错的点：混淆 width expansion(位扩展) 与 depth expansion(字扩展)，导致芯片数算错。
    - 容易看漏的条件 / 单位 / 符号：单片 32K×8、目标 64K×16；$\overline{CS}$ 是 active-low(低有效)；只准用 $A_{15}$ + 一个 NOT 译码。
    - 启动困难时第一步先做什么：分别算「位方向要几片」「字方向要几组」，两者相乘就是总片数。

---

## Problem 4. [20 pts]

A 10-bit Successive Approximation Register (SAR) ADC has an input range $0 \le V_{in} < 5$ V and operates at a clock frequency of 1 MHz.

Assume an ideal straight-binary ADC with

$$
\Delta = \frac{V_{ref}}{2^N},
$$

where $V_{ref} = 5$ V and $\Delta$ is the voltage represented by one least significant bit, LSB.

Assume each SAR bit decision takes exactly one clock cycle. Ignore sampling time, DAC settling time, comparator delay, and all other overhead.

Also assume the output code is obtained by truncation:

$$
N_{out} = \left\lfloor \frac{V_{in}}{\Delta} \right\rfloor.
$$

For reconstruction, use $V_{rec} = N_{out}\,\Delta$.

**(a)** Calculate the minimum conversion time required for one sample, in µs. **[5 pts]**

- 💬 Q&A：(a) 到底在问什么（2026-06-11）
    
    **问题：** conversion time(转换时间) 怎么来的，为什么和时钟有关？
    
    **三句话讲清：**
    
    1. SAR 像猜数字游戏：每个时钟周期问一次「比某个值大吗」，**每问一次确定一位**，从 MSB 到 LSB 逐次逼近。
    2. 题干给定 *each SAR bit decision takes exactly one clock cycle*（每个位判定恰好 1 个时钟周期），且忽略一切 overhead(额外开销) → 总时间 = 问几次 × 每次多久。
    3. 公式主线：$t_{conv} = N \times T_{clk} = N / f_{clk}$，其中 $N$ 是位数、$T_{clk} = 1/f_{clk}$。
    
    **⚠️ 自查点：** 答案应该 = 位数 × 单个时钟周期；只算一个周期就交是最常见的错。注意单位换算 $1\ \text{MHz} = 10^6\ \text{Hz}$，结果用 µs 表示。
    
- ✅ 参考答案 (a)
    
    $t_{conv} = N \times T_{clk} = 10 \times \dfrac{1}{1\ \text{MHz}} = 10 \times 1\ \mu s = \mathbf{10\ \mu s}$
    
    （题干给定每个 bit decision 占 1 个时钟周期，10-bit 共 10 次，忽略一切 overhead。）
    

**(b)** If the analog input voltage is $V_{in} = 3.2$ V, determine the ADC output code in decimal. **[5 pts]**

- 💬 Q&A：(b) 里 $2^N$ 是 10 吗？（2026-06-11）
    
    **问题：** 代公式 $\Delta = V_{ref}/2^N$ 时，$2^N$ 是不是 10？
    
    **答：不是。** $N$ 和 $2^N$ 是两个不同的东西：
    
    - $N$ = **位数**（几个 bit），在指数上 → 本题 $N = 10$。
    - $2^N$ = **能表示的码总数**（台阶数 / levels）→ $2^{10} = 1024$，码范围 0 ~ 1023。
    - 原理：每个 bit 有 0/1 两种取值，10 个 bit 的组合数 = $2^{10}$。和 Lecture10 里「15 根地址线 → $2^{15} = 32768$ 个字」同一个逻辑：**位数在指数上，总数是 2 的幂**。
    
    代入：$\Delta = 5/1024 \approx 4.883$ mV，这是「一个台阶的高度」；再用 $N_{out} = \lfloor V_{in}/\Delta \rfloor$ 往下算。
    
    **⚠️ 易错：** 别把 $2^N$ 写成 10（那是 $N$）；最后取整是 truncation(截断 / 向下取整)，不是四舍五入。
    
    **💡** $N_{out}$ **的意义 + 两条自查（补于同日）：**
    
    - 把 0~5 V 想成 1024 级台阶（每级高 $\Delta$），$N_{out}$ 就是 $V_{in}$ **落在第几级台阶的编号**，也是数字世界（CPU / 存储）真正拿到的那个 10-bit 整数；(c) 用它乘回 $\Delta$ 还原电压。
    - **Range check(范围检查)：** 10-bit 码只能是 $0 \sim 1023$，算出超过 1023（如 1600）必错。
    - **比例检查：** $N_{out}/1024 \approx V_{in}/V_{ref}$，本题应约等于 64%，用它对数量级。
- ✅ 参考答案 (b)
    
    $\Delta = \dfrac{V_{ref}}{2^N} = \dfrac{5}{1024} \approx 4.883$ mV
    
    $N_{out} = \left\lfloor \dfrac{V_{in}}{\Delta} \right\rfloor = \left\lfloor \dfrac{3.2 \times 1024}{5} \right\rfloor = \lfloor 655.36 \rfloor = \mathbf{655}$
    
    （truncation 向下取整，不四舍五入；自查：$655 \le 1023$，且 $655/1024 \approx 64\% = 3.2/5$ ✔️）
    

**(c)** Determine the reconstructed voltage corresponding to the digital output code found in part (b), in volts. **[5 pts]**

- ✅ 参考答案 (c)
    
    $V_{rec} = N_{out}\,\Delta = 655 \times \dfrac{5}{1024} = \dfrac{3275}{1024} \approx \mathbf{3.198\ V}$（精确值 3.19824 V）
    
    （一定略小于 $V_{in} = 3.2$ V：truncation 只会往下靠，还原值永远不超过真实值。）
    

**(d)** Calculate the quantization error, in volts. Define the quantization error as $e_q = V_{in} - V_{rec}$. **[5 pts]**

- ✅ 参考答案 (d)
    
    $e_q = V_{in} - V_{rec} = 3.2 - \dfrac{3275}{1024} = \dfrac{1.8}{1024} \approx \mathbf{1.758 \times 10^{-3}\ V} \;(\approx 1.76\ \text{mV})$
    
    验算：$e_q = 0.36\,\Delta$（正是 (b) 里被砍掉的小数 0.36），满足 $0 \le e_q < \Delta$ ✔️ —— truncation 的量化误差永远小于一个台阶。
    
- ⚠️ 易错点 / ADHD 纠错
    - 这类题最容易做错的点：转换时间忘了乘位数（10-bit 要 10 个时钟）；truncation(截断) 用 floor(向下取整)，不是四舍五入。
    - 容易看漏的条件 / 单位 / 符号：$f_{clk}=1$ MHz、答案要带单位 µs / V；$V_{ref}=5$ V。
    - 启动困难时第一步先做什么：先算出 $\Delta = V_{ref}/2^N$ 的数值，(b)(c)(d) 全部基于它往下推。
- 💬 Q&A：P4 题目翻译与解读（2026-06-10）
    
    **题干翻译：** 一个 10-bit SAR ADC（Successive Approximation Register，逐次逼近寄存器型模数转换器），输入范围 $0 \le V_{in} < 5$ V，时钟频率 1 MHz。
    
    **四个给定设定：**
    
    1. 理想 straight-binary(直接二进制) ADC：$\Delta = V_{ref}/2^N$，其中 $V_{ref}=5$ V、$N=10$；$\Delta$ 是 1 LSB(最低有效位) 对应的电压，即整道题的「最小刻度」。
    2. 每个 bit decision(位判定) 恰好占 1 个时钟周期；忽略采样时间、DAC settling time(建立时间)、比较器延迟等一切 overhead(额外开销)。
    3. 输出码用 truncation(截断) 得到：$N_{out} = \lfloor V_{in}/\Delta \rfloor$ —— 是 floor(向下取整)，不是四舍五入。
    4. reconstruction(重建)：$V_{rec} = N_{out}\,\Delta$，即把数字码乘回刻度，得到「ADC 眼里的电压」。
    
    **各小问在问什么：**
    
    - (a) 转换一个样本的最小 conversion time(转换时间)，单位 µs —— 走「位数 × 时钟周期」这条线。
    - (b) $V_{in}=3.2$ V 时的输出码（十进制）—— 套 truncation 公式。
    - (c) (b) 的码对应的 reconstructed voltage(重建电压)，单位 V。
    - (d) quantization error(量化误差) $e_q = V_{in} - V_{rec}$，单位 V。
    
    **主线：** (b)(c)(d) 是一条链，全部基于 $\Delta$ 往下推；(a) 独立用时钟频率和位数计算。
    

---

## Problem 5. [15 pts]

Consider a synchronous sequential circuit consisting of two D flip-flops, FF1 and FF2, with a combinational logic block between them. The circuit uses a single common clock.

The timing parameters are:

- Clock frequency: $f_{clk} = 50$ MHz
- Flip-flop maximum clock-to-Q propagation delay: $t_{pcq} = 2.5$ ns
- Flip-flop minimum clock-to-Q contamination delay: $t_{ccq} = 1.5$ ns
- Flip-flop setup time: $t_{setup} = 3.0$ ns
- Flip-flop hold time: $t_{hold} = 2.0$ ns

**(a)** Calculate the clock period $T_{clk}$. **[5 pts]**

- ✅ 参考答案 (a)
    
    $T_{clk} = \dfrac{1}{f_{clk}} = \dfrac{1}{50\ \text{MHz}} = 2\times 10^{-8}\ \text{s} = \mathbf{20\ ns}$
    

**(b)** Determine the maximum allowable propagation delay of the combinational logic block, $t_{pd,max}$, so that there is no setup time violation. **[5 pts]**

- ✅ 参考答案 (b)
    
    setup 约束（最慢路径，赶**下一个**时钟沿）：$t_{pcq} + t_{pd} + t_{setup} \le T_{clk}$
    
    $t_{pd,max} = T_{clk} - t_{pcq} - t_{setup} = 20 - 2.5 - 3.0 = \mathbf{14.5\ ns}$
    

**(c)** Determine the minimum required contamination delay of the combinational logic block, $t_{cd,min}$, so that there is no hold time violation. **[5 pts]**

- ✅ 参考答案 (c)
    
    hold 约束（最快路径，**同一个**时钟沿的赛跑，与 $T_{clk}$ 无关）：$t_{ccq} + t_{cd} \ge t_{hold}$
    
    $t_{cd,min} = t_{hold} - t_{ccq} = 2.0 - 1.5 = \mathbf{0.5\ ns}$
    
    **⚠️ 错法警示（本人 2026-06-11 踩过）：** 写成 $t_{cd} + t_{ccq} + t_{hold} = T_{clk}$ 得 16.5 ns 是把 setup 句式套到 hold 上。hold 防的是新数据**跑太快**、在同一沿的 $t_{hold}$ 窗口内冲掉旧数据，跟下个周期无关 —— **hold 式里出现** $T_{clk}$ **立刻报警。**
    
- 💬 Q&A：contamination / violation 是什么（2026-06-11）
    
    **contamination(污染)**：来自 contaminate(污染)。contamination delay $t_{cd}$（触发器的叫 $t_{ccq}$）= 输入变化后，输出**最早**开始变化（旧值开始被“弄脏”）的时间，即**最小延迟**；对比 propagation delay $t_{pd}$ / $t_{pcq}$ = **最大延迟**（输出完全变稳）。
    
    **violation(违例 / 违反)**：来自 violate(违反)。setup time violation = 数据来得太晚，时钟沿前没坐稳 $t_{setup}$；hold time violation = 数据变得太早，时钟沿后没保持够 $t_{hold}$。违例后果：采错值或亚稳态。
    
    **口诀：** setup 查**最慢**路径（$t_{pcq}+t_{pd}+t_{setup} \le T_{clk}$）；hold 查**最快**路径（$t_{ccq}+t_{cd} \ge t_{hold}$，与 $T_{clk}$ 无关）。
    
    **追问：为什么周期公式里永远没有 hold？（2026-06-11）** CS110 的公式也没有 hold（$T_{min} \ge t_{clk\text{-}to\text{-}Q} + t_{comb} + t_{setup}$，slide 35 给的 hold = 1 ns 是干扰量）。原理：setup 是**串联**需求（$t_{pcq} \to t_{pd} \to t_{setup}$ 三段接力占用周期预算）；hold 是**并行**需求，发生在沿之后的小窗口，靠下一批数据自身的爬行时间（$t_{ccq}+t_{cd}$）守住，不消耗周期预算 —— 加进周期公式等于重复计费。
    
- ⚠️ 易错点 / ADHD 纠错
    - 这类题最容易做错的点：setup 用 max 延迟、hold 用 min(contamination) 延迟，两者别用反；hold 分析与时钟周期无关。
    - 容易看漏的条件 / 单位 / 符号：全部单位是 ns；区分 $t_{pcq}$(max) 与 $t_{ccq}$(min)。
    - 启动困难时第一步先做什么：先写出两条约束 $T_{clk}\ge t_{pcq}+t_{pd}+t_{setup}$、$t_{ccq}+t_{cd}\ge t_{hold}$，再代数求解。

---

## Problem 6. [20 pts]

Complete the following three sequential logic exercises on HDLBits. For each exercise, submit a screenshot showing successful completion and your code. The original URLs are provided below.

**(1)** Multiplexer and D Flip-Flop (Mt2015 muxdff) **[7 pts]**

Link: [https://hdlbits.01xz.net/wiki/Mt2015_muxdff](https://hdlbits.01xz.net/wiki/Mt2015_muxdff)

**(2)** Simple FSM 1: Synchronous Reset (Fsm1s) **[7 pts]**

Link: [https://hdlbits.01xz.net/wiki/Fsm1s](https://hdlbits.01xz.net/wiki/Fsm1s)

**(3)** Testbench for T Flip-Flop (Tb/tff) **[6 pts]**

Link: [https://hdlbits.01xz.net/wiki/Tb/tff](https://hdlbits.01xz.net/wiki/Tb/tff)

- 📋 Verilog 速查卡：P6 三题恰好需要的（2026-06-11）
    
    详细版见 [Verilog](https://app.notion.com/p/Verilog) 和 [EE115B Lecture8 — Verilog HDL Part 2：module · 数据类型 · always · 仿真](EE115B%20Lecture8%20%E2%80%94%20Verilog%20HDL%20Part%202%EF%BC%9Amodule%20%C2%B7%20%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B.md)。
    
    **1）铁律：** 组合逻辑 `always @(*)` + 阻塞 `=`；时序逻辑 `always @(posedge clk)` + 非阻塞 `<=`；同块不混用。在 always 里赋值的输出要声明 `output reg`。
    
    **2）muxdff：** MUX 就是三目 `sel ? a : b`；DFF 就是 `always @(posedge clk) q <= d;`；把 mux 结果作为 DFF 的 d 即可。
    
    **3）Fsm1s 同步复位：** reset **不进敏感列表**，只在 `@(posedge clk)` 内 `if (reset) ...`；写成 `or posedge reset` 就变成异步复位，必错。状态机套三段式；组合块开头先给默认值（`next = state;`）防 latch。
    
    **4）Tb/tff 四件套：** 声明（激励 `reg`、观测 `wire`）→ 具名例化 `tff dut (.clk(clk), ...)` → 时钟 `always #5 clk = ~clk;`（clk 记得初始化为 0）→ `initial` 里用 `#延时` 顺序喂激励：先 reset，再让 t 取能翻转的值（T 触发器：t=1 翻转、t=0 保持）。
    
    **5）提交要求：** 每题「成功截图 + 代码」两样都要交。
    
- ⚠️ 易错点 / ADHD 纠错
    - 这类题最容易做错的点：Fsm1s 是 **synchronous reset(同步复位)**，复位要写在 clocked always 里，不能放进敏感列表；Tb/tff 是写 testbench(测试平台)，不是写被测电路。
    - 容易看漏的条件 / 单位 / 符号：每题要交「截图 + 代码」两样；muxdff 看清 mux 的选择端含义。
    - 启动困难时第一步先做什么：先把三道题在 HDLBits 网页打开，逐个本地通过后再截图，不要攒到最后。

---

## 📎 Original PDF

[数字电路_2026_HW4.pdf](EE115B%20Digital%20Circuit%20Homework%204/%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF_2026_HW4.pdf)

## 🐈 下次打开第一步

<aside>
▶️

下次回到这页：直接动手做 **Problem 1(a)** —— 照电路图写出 $D_1, D_0$ 的布尔表达式。先别点开任何「易错点」卡，写完再对照检查。

</aside>

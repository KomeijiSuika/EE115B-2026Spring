# EE115B Lecture9 — Sequential Logic Part 3：Shift Register & Counter

<aside>
🔢

**主题**：寄存器、移位寄存器与计数器（时序逻辑 Part 3）

**教材**：Floyd《Digital Fundamentals》Ch. 9 · ShanghaiTech EE115B

**核心脉络**：用上一节的触发器（D / T / JK）搭出能「存」和「移」的寄存器 → 再用触发器级联出能「数」的计数器 → 分清 **异步（ripple）** 与 **同步** 两条路线 → 最后用 VHDL 行为级描述把它们写出来。

</aside>

# 1️⃣ 寄存器 Registers

寄存器是**一组触发器**，用来存放多位信息：

- **N 位寄存器 = N 个触发器**，每位用一个 D 触发器。
- 所有触发器**共用同一个 Clock 和 Clear**，同时被打入 / 清零。
- 输入 $D_0 \sim D_3$，输出 $Q_0 \sim Q_3$。

![Slide 4 — 4 位寄存器：4 个共享 Clock/Clear 的 D 触发器](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_4.png)

Slide 4 — 4 位寄存器：4 个共享 Clock/Clear 的 D 触发器

# 2️⃣ 移位寄存器 Shift Registers

**移位寄存器**：在普通寄存器基础上，增加了「让内容逐位移动」的能力——把前一级的输出接到后一级的输入，所有触发器共用时钟，每来一个时钟沿数据就整体移一位。

![Slide 5 — 4 位移位寄存器：前级 Q 接后级 D，串行流动](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_5.png)

Slide 5 — 4 位移位寄存器：前级 Q 接后级 D，串行流动

## 电路结构（带异步清零）

4 个 D 触发器首尾相连，`Data In` 从最左进入，逐级传到 `Data Out`；`Clear` 直接连各级 CL 端，是**异步清零**（不等时钟即可生效）。

![Slide 6 — 4 位移位寄存器电路图（异步 Clear）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_6.png)

Slide 6 — 4 位移位寄存器电路图（异步 Clear）

## 时序分析

串入数据 `1 0 0 1`，每个时钟上升沿整体右移一位：

- 红区：数据**刚好全部载入**（load finish）的时刻；
- 蓝区：继续给时钟，数据**逐位移出**（shifting）。

![Slide 8 — 移位寄存器时序图（红=载入完成，蓝=移出中）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_8.png)

Slide 8 — 移位寄存器时序图（红=载入完成，蓝=移出中）

## 右移 vs 左移

- **右移（Shift-right）**：数据从**低位**串入，沿 $Q_A \to Q_B \to Q_C \to Q_D$ 方向流动。
- **左移（Shift-left）**：数据从**高位**串入，方向相反。
- 本质区别只是触发器**互连方向**不同。

![Slide 9 — 右移与左移的互连方向对比](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_9.png)

Slide 9 — 右移与左移的互连方向对比

## 四种类型（按输入/输出方式）

按「串行 / 并行」组合，移位寄存器分四类：

|  | 串行输出 (Serial-Out) | 并行输出 (Parallel-Out) |
| --- | --- | --- |
| 串行输入 (Serial-In) | SISO 串入串出 | SIPO 串入并出 |
| 并行输入 (Parallel-In) | PISO 并入串出 | PIPO 并入并出 |

![Slide 11 — 四种移位寄存器类型框图](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_11.png)

Slide 11 — 四种移位寄存器类型框图

## 例：并入并出（PIPO）

用 `Shift/Load` 控制端选择「移位」还是「并行载入」：每位前面用一组与门 + 或门做二选一多路器，决定 D 端取**串行移位数据**还是**并行输入数据**。

![Slide 12 — 并入并出移位寄存器电路（含 Shift/Load 选择）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_12.png)

Slide 12 — 并入并出移位寄存器电路（含 Shift/Load 选择）

- Q：Slide 12 里的 serial input 是什么？输出会怎么样？
    - **Serial input（串行输入）**就是移位模式下从最左边第一级触发器送进来的那 1 bit 数据。它不是一次性给 4 位，而是**每来一个 clock 只进 1 位**。
    - Slide 12 这个 PIPO / 带 Shift-Load 的寄存器里，每一级 D 端前面都有选择逻辑：
        - `Shift/Load` 选择 **Load** 时：各级直接装入并行输入 $D_A,D_B,D_C,D_D$，输出立刻变成这 4 位并行数据。
        - `Shift/Load` 选择 **Shift** 时：serial input 进入 $Q_A$，原来的 $Q_A$ 移到 $Q_B$，原来的 $Q_B$ 移到 $Q_C$，原来的 $Q_C$ 移到 $Q_D$。
    - 所以若当前输出为 $Q_AQ_BQ_CQ_D = abcd$，下一拍 serial input 为 $s$，右移后输出变为：
    
    $$
    Q_AQ_BQ_CQ_D \leftarrow sabc
    $$
    
    - 最右边原来的 $d$ 会从 serial output / 最右端移出去；如果只看 parallel output，就是四个输出端每拍整体右移一格。
- Q：如果 shift 到一半又出现 parallel load，要怎么理解？
    - Slide 12 的电路**不是同时考虑 serial shifting 和 parallel loading**，而是由 `Shift/Load` 控制端在每个 clock 到来时二选一。
    - 如果前两拍都处在 **Shift** 模式，就按 serial input 一位一位移入；例如初始为 $Q_AQ_BQ_CQ_D=0000$，两拍 serial input 依次为 $1,0$，则：
    
    $$
    0000 \xrightarrow{s=1} 1000 \xrightarrow{s=0} 0100
    $$
    
    - 如果第三拍切到 **Load** 模式，那么这一拍不会继续用 serial input，而是直接把并行输入 $D_A,D_B,D_C,D_D$ 装进寄存器：
    
    $$
    Q_AQ_BQ_CQ_D \leftarrow D_AD_BD_CD_D
    $$
    
    - 所以答案是：**要考虑控制信号每一拍选的是 Shift 还是 Load**。两拍 serial 后如果出现 parallel load，parallel 会覆盖当前移位得到的中间状态。

# 3️⃣ 计数器基础 Counters

计数器是用触发器记录时钟脉冲个数的时序电路，两大分类：

| 类型 | 时钟连接 | 特点 |
| --- | --- | --- |
| **异步 / 行波 (Asynchronous / Ripple)** | 只有第一级接外部 CLK，后级由前级输出触发 | 结构简单，但**逐级传播延迟累加**，高速时易产生毛刺 (glitch) |
| **同步 (Synchronous)** | 所有触发器**共用同一个 CLK** | 各位同时翻转，速度快、无累计延迟，但组合逻辑更复杂 |
- **模 (Modulus)**：计数器经历的状态总数。$n$ 个触发器最多可数 $2^n$ 个状态，故 $\text{modulus} \le 2^n$。

# 4️⃣ 异步计数器 Asynchronous Counters

## 用 T 触发器的异步加 / 减计数器

所有 T 端固定接 `1`（每个时钟沿都翻转）。区别在于**后级时钟从哪取**：

- **加计数器**：后级 CLK 取前级 **Q**，计数 $0\to7\to0$。
- **减计数器**：后级 CLK 取前级 $\bar{Q}$，计数 $7\to0\to7$。

![Slide 16 — 异步加计数器（T 触发器），后级取前级 Q](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_16.png)

Slide 16 — 异步加计数器（T 触发器），后级取前级 Q

![Slide 17 — 异步减计数器（T 触发器），后级取前级 Q̄](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_17.png)

Slide 17 — 异步减计数器（T 触发器），后级取前级 Q̄

## 用 D 触发器的异步加计数器

把每级 $\bar{Q}$ 接回自己的 D（实现翻转），再用 $\bar{Q}$ 触发后级，得到 3 位二进制行波加计数器 $000 \to 111 \to 000$。

![Slide 18 — 异步加计数器（D 触发器）+ 状态表与时序](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_18.png)

Slide 18 — 异步加计数器（D 触发器）+ 状态表与时序

## 异步十进制（Decade）计数器

- 思路：**截断多余状态**——当计到 `10` (1010) 时，用译码与非门检测并产生异步 `CLR` 把计数器清零。
- 缺点：复位脉冲极短，可能产生**毛刺 (Glitch)**。

![Slide 19 — 异步十进制计数器（检测 10 即复位，注意毛刺）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_19.png)

Slide 19 — 异步十进制计数器（检测 10 即复位，注意毛刺）

## 异步模 12 计数器

同样思路：正常计到 `1011` 后下一拍本应是 `1100`，用 12 译码器检测 `1100` 立即异步清零回 `0000`，得到模 12。仍有毛刺风险。

![Slide 20 — 异步模 12 计数器（检测 1100 复位）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_20.png)

Slide 20 — 异步模 12 计数器（检测 1100 复位）

# 5️⃣ 同步计数器 Synchronous Counters

> 同步计数器：所有触发器由**同一个公共时钟脉冲**同时驱动。
> 

## 3 位同步加计数器（JK 触发器）

各级 CLK 并联到公共 CLK。翻转条件用组合逻辑给到 J/K：$J_0K_0 = 1$（每拍翻），$J_1K_1 = Q_0$，$J_2K_2 = Q_0Q_1$。

![Slide 21 — 3 位同步加计数器（JK）电路与时序](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_21.png)

Slide 21 — 3 位同步加计数器（JK）电路与时序

- Q：时钟1上升沿 Q0 变成 1，为什么 Q1 没有同时变 1？是延迟导致「错过」了上升沿吗？
    - **不是延迟的问题，也没有「错过上升沿」。** 三个触发器永远被同一个公共时钟的**同一个上升沿**同时采样、同时翻转。
    - **关键：触发器在时钟沿采样的是「沿到来之前」的输入值。** Q1 的翻转条件是 $J_1=K_1=Q_0$，它看的是**这一拍沿之前**那一刻的 Q0：
        - **时钟1**：沿之前状态是 $Q_2Q_1Q_0=000$，所以 $J_1=K_1=Q_0=0$ → Q1 保持 0；同一拍里 Q0 才翻成 1。结果 $001$。
        - **时钟2**：此时 Q0 早已稳定为 1（时钟1之后就稳了，远早于时钟2的沿），所以 $J_1=K_1=1$ → Q1 翻成 1。结果 $010$。
    - 所以 Q1 比 Q0「晚一拍」是**二进制计数** $001 \to 010$ **的正确行为**，不是 bug。如果 Q1 真在时钟1就和 Q0 一起翻，那会变成 $011$，直接跳掉一个数反而错了。
    - **延迟到底在哪**：Q0 翻转确实有一点传播延迟 $t_{pd}$，但它发生在**时钟1的沿之后**；等时钟2到来时 Q0 早已稳定（满足建立时间 setup time(建立时间)），对 Q1 的采样毫无影响。而且同步里所有 FF 共用一个沿、延迟相同，**不会累加**。
    - **⚠️ 关于「异步(Asy)就没有这个问题」——恰恰相反：**
        - 异步（行波 ripple）计数器同样是 Q1 隔一拍才动，**计数序列和同步完全一样**，并不会让 Q1 和 Q0 同时变 1。
        - 区别在于：异步后级时钟取自前级 $Q$ / $\bar{Q}$，传播延迟是**逐级累加(accumulate)**的（高位越来越晚翻），所以异步的「延后 / 偏移」其实**更严重**，也更容易出毛刺 (glitch)。
        - 一句话：同步是「同一个沿、同时采样旧值」，异步是「前级翻完才轮到后级」；前者延迟不累加，后者累加。异步不是更好，是更差。

## 位翻转规律（用 T 触发器）

**核心口诀：某一位只有在它「前面所有低位都为 1」时才翻转。**

- $Q_0$：每个时钟上升沿都翻；
- $Q_1$：仅当 $Q_0=1$ 时翻；
- $Q_2$：仅当 $Q_0=1$ 且 $Q_1=1$ 时翻。

对应的 T 输入：

$T_0 = 1,\quad T_1 = Q_0,\quad T_2 = Q_0Q_1,\quad T_3 = Q_0Q_1Q_2,\quad \cdots\quad T_n = Q_0 Q_1 \cdots Q_{n-1}$

![Slide 22 — 同步加计数器位翻转规律与 T 输入](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_22.png)

Slide 22 — 同步加计数器位翻转规律与 T 输入

## 4 位同步加计数器（T 触发器）

按上面规律，用**与门**把低位逐级相乘得到各级 T 输入，所有触发器共用时钟，$0 \to 15 \to 0$。

![Slide 24 — 4 位同步加计数器（T 触发器）电路与时序](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_24.png)

Slide 24 — 4 位同步加计数器（T 触发器）电路与时序

- Q：同步计数器用上升沿还是下降沿触发，是不是都可以？
    - **可以，只要所有触发器用同一种边沿**（全上升或全下降）。计数序列 $0 \to 15 \to 0$ 完全一样，区别只是状态在时钟上升 / 下降那一刻更新，差半个周期。
    - **原因**：同步计数器所有 FF 共用一个 CLK，各 T 输入由当前 Q 经与门算出，大家在同一边沿**同时采样、同时翻转**；边沿极性只决定「何时动」，不改变「该不该翻」（低位全 1 才翻的逻辑不变）。
    - **看图判断**：时钟 ">" 三角无气泡 → 上升沿触发；带气泡 ○ → 下降沿触发。
    - **⚠️ 异步 / 行波计数器不一样**：后级时钟取自前级 $Q$ / $\bar{Q}$，边沿极性 + 接 Q 还是 Q̄ 会影响**计数方向（加 / 减）**，不能照搬同步的「无所谓」。

## 4 位同步加计数器（JK 触发器）

同一规律换成 JK 实现：注意级联模式 $Q_0,\ Q_0Q_1,\ Q_0Q_1Q_2$ 逐级与门串接，「全 1 才进位」。

![Slide 25 — 4 位同步加计数器（JK），注意 Q0Q1Q2 全 1 的进位模式](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_25.png)

Slide 25 — 4 位同步加计数器（JK），注意 Q0Q1Q2 全 1 的进位模式

## Enable 与 Clear 功能

在 4 位同步 T 计数器基础上增加控制：

- **Clear = 0**：异步把输出复位到 0；
- T 输入改为：$T_0 = E,\ T_1 = Q_0 \cdot E,\ T_2 = Q_1 Q_0 \cdot E,\ T_3 = Q_2 Q_1 Q_0 \cdot E$；
- **Enable = 1**：正常计数；**Enable = 0**：所有 T = 0，**保持当前状态**。

![Slide 26 — 带 Enable / Clear 的 4 位同步计数器](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_26.png)

Slide 26 — 带 Enable / Clear 的 4 位同步计数器

- Q：CLR / PRE 到底有没有取反？气泡和横杠是不是两次取反？（统一三张图）
    - **一句话：气泡 ○ 和名字上的横杠（如** $\overline{CLR}$**）说的是同一件事——这个脚是 active-low（低电平有效），给 0 才动作。它们不是两次取反，而是同一事实的两种写法。**
    - **梅红字是记号**：它是「引脚名 + 有效电平」的标注，不是某一刻的电平值。$\overline{PRE}$ / $\overline{CLR}$ = 这个端子叫 preset / clear，且低有效；Q / Q̄ 同理是输出脚的名字。
    - **你说的「输入 CLR′、经过气泡取反成 CLR」基本对**：外部线就是 $\overline{CLR}$，要清零就把它拉到 0；引脚上的气泡代表符号内部自带的一次取反，把外部「0 有效」翻成内部「真正执行清零」。这个取反**画在符号里了，不用自己再加反相器**，也不改变「对外要给 0」这件事。
    - **三张图其实是同一套，没有反过来**：
        - 图1 单个 D-FF：$\overline{PRE}$ / $\overline{CLR}$ 带横杠 + 带气泡 → 异步、低有效，标准写法。
        - 图2 异步十进制计数器：那个「10 decoder」是个 **NAND**，检测到计到 1010 时输出跳到 0 = $\overline{CLR}=0$ → 送进各 FF 带气泡的 CLR 脚 → 清零回 0000。低有效的源 → 低有效的脚，完全一致。（NAND 天生「全 1 才出 0」，正好用来产生低有效清零脉冲。）
        - 图3 同步 Enable / Clear：底下「Clear」一样带气泡 → 还是低有效（Clear = 0 才复位）。它**没有反过来**，只是文字标签把横杠省掉了，但气泡还在、含义不变；严格应写 $\overline{Clear}$。
    - **为什么你觉得最后一个反了**：图1/图2 文字带横杠、图3 文字没带。但**判断有效电平要看气泡，不看文字有没有横杠**；三个图气泡都在 → 三个都是低有效 clear。文字横杠只是「提醒」，气泡才是「权威」。
    - **⚠️ 方向别搞反**：「圆圈前」= 外部那根引脚（就是 $\overline{CLR}$ 线本身），「圆圈后」= 芯片内部真正控制清零的信号；圆圈把外部电平取反送进内部。
    
    | 你的意图 | 外部 CLR 引脚（圆圈前） | 圆圈后 → 内部清零信号 | 结果 |
    | --- | --- | --- | --- |
    | 正常工作 / 不清零 | 1 | 0 | 不清零 |
    | 想清零 | 0 | 1 | 执行清零 |
    - 所以正确说法是：**想清零时，外部引脚（圆圈前）给 0，经过圆圈反成 1（内部）→ 清零**。常见混淆点：「内部清零动作 = 1」≠「外部 $\overline{CLR}$ 线 = 1」，两个 CLR 别混。
    - **口诀**：看到气泡 ○ 或横杠 → 低有效 → 给 0 才动作；两者同时出现 = 同一句话说两遍，别当成两次取反。

## 4 位同步十进制计数器（同步复位）

用**同步复位**技术避免毛刺。按 BCD 状态表，用卡诺图推出 JK 输入：

$J_1 = K_1 = Q_0\bar{Q_3}\quad(\text{在 } 1,3,5,7 \text{ 翻，但 9 不翻})$

$J_2 = K_2 = Q_0 Q_1\quad(\text{在 } 3,7 \text{ 翻})$

$J_3 = K_3 = Q_0 Q_1 Q_2 + Q_0 Q_3\quad(\text{在 } 7,9 \text{ 翻})$

![Slide 27 — 4 位同步十进制计数器 + BCD 状态表（含 K-map 练习）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_27.png)

Slide 27 — 4 位同步十进制计数器 + BCD 状态表（含 K-map 练习）

- Q：同步复位是怎么想到的？思维精髓是什么？
    - **先看异步复位坏在哪**：异步清零「一检测到非法态（如 1010）就绕过时钟立刻清零」。问题是——① 各 FF 传播延迟不同，清零不同步 → 出现极短的**毛刺 / 中间态**；② 复位脉冲会**自己掐断自己**（清零后检测条件立刻消失），脉宽不确定、不可靠。
    - **核心转念**：别再「事后补救」，改成「**预判一步 + 纳入时钟节拍**」。不要等数到非法态才反应，而是在**当前还是最后一个合法态**（如 9）时，就先用组合逻辑把「下一拍归零」准备好，等下一个时钟沿和普通状态转移一起干净地完成。
    - **精髓一句话**：**把「复位」从一个绕过时钟的特殊动作，降格成一次普通的、由时钟统一裁决的状态转移**。复位不再是外部强行打断，而是写进了次态逻辑（next-state logic）的一条正常转移：「在状态 9，次态 = 0」。
    - **背后的世界观**：同步设计方法学——**让所有变化都只发生在时钟边沿**。统一节拍 = 没有竞争、没有毛刺、时序可预测可分析。异步是「reactive 事后清零」，同步是「proactive 预判 + 同节拍」。
    - **可迁移到一般 mod-N 设计**：与其「先做满 $2^n$ 再砍掉多余状态」，不如把计数器当成一台**有限状态机**——直接规定合法终态的次态指回起点，复位条件就是次态方程的一部分。模块化并行载入（条件满足时载入 0000）是同一思路的工程化封装。

## 模块化设计 Modularized Design

直接用现成的「计数器模块 + 并行载入」来构造任意模值，简单可靠：

- **Load 用并行载入模式**实现；
- **载入条件**：$Q_2Q_1Q_0 = 101$（即数到 5，模 = 6）；
- 当 $Q_2 = Q_0 = 1$ 时 Load = 1，载入 $D_2D_1D_0 = 000$ 复位；
- **Load 由时钟同步**，所以无毛刺。

![Slide 28 — 模块化设计：并行载入实现模 6](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_28.png)

Slide 28 — 模块化设计：并行载入实现模 6

## 自启动计数器 Self-Starting

- 定义：**无论初始状态如何，最终都能进入正常计数循环**，即称自启动。
- 左图所有状态最终汇入主循环 → 可自启动；右图存在孤立的 `00` 自环，进不去主循环 → 不能自启动。

![Slide 29 — 自启动 vs 不能自启动的状态图对比](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_29.png)

Slide 29 — 自启动 vs 不能自启动的状态图对比

## 同步级联与分频 Cascading / Frequency Divider

- **级联**：把前一模块的进位输出 TC 接到后一模块的使能 CTEN，两个「÷10」级联得到 $f_{in}/100$。
- **分频器**：三级 ÷10 级联，把 1 MHz 依次分频成 100 kHz → 10 kHz → 1 kHz。

![Slide 30 — 同步级联计数器与分频器](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/slide_30.png)

Slide 30 — 同步级联计数器与分频器

- Q：Slide 30 里的 TC / DC 是什么？
    - **TC = Terminal Count（终端计数 / 计满信号）**。它表示当前这个计数器已经数到本轮最后一个状态了。
        - 对一个 ÷10 / decade counter 来说，通常是数到 `9` 时 TC 有效。
        - TC 的作用像「进位信号」：前一级数满一轮，就通知后一级可以加 1。
    - **DC 通常指 Decade Counter（十进制 / 十状态计数器）**，也就是一个 **mod-10 counter**。
        - 它的状态循环是 `0 → 1 → ... → 9 → 0`。
        - 因为 10 个输入 clock 才完成一轮，所以也可以看成一个 **÷10 frequency divider**。
    - Slide 30 的级联逻辑可以理解成：
        - 第一级 DC 每来 10 个输入 clock，TC 触发一次；
        - 这个 TC 接到第二级的 enable，所以第二级每当第一级数满一轮才加 1；
        - 两个 DC 级联：$10 \times 10 = 100$，所以得到 $f_{in}/100$。
    - 类比十进制数字：个位从 0 数到 9 后产生 TC，让十位加 1；这里的每个 DC 就像一位十进制数字。
- Q：为什么 TC 能做到除以 10？
    - 严格说：**不是 TC 本身在除以 10**，而是 **DC / decade counter 先完成 ÷10**；TC 只是把「数满 10 个 clock」这个事件变成一个输出脉冲。
    - 一个 decade counter 的状态循环是：
    
    $$
    0 \to 1 \to 2 \to \cdots \to 9 \to 0
    $$
    
    - 它每来 1 个 input clock 才前进一步；所以从 `0` 回到 `0` 需要 10 个 input clock。
    - TC 在计数器到达 terminal count（通常是 `9`）时有效，并在这一轮结束时给出一次「进位 / 计满」信号。
    - 因此如果只看 TC 脉冲：输入 clock 来了 10 次，TC 才出现 1 次，所以 TC 的重复频率就是：
    
    $$
    f_{TC} = \frac{f_{in}}{10}
    $$
    
    - 类比：个位数字每拨 10 下，十位才动 1 下；**十位收到的进位频率就是个位输入频率的十分之一**。

# 6️⃣ VHDL 行为级描述

> 三段代码都用 `WAIT UNTIL` / `Clock'EVENT AND Clock='1'` 描述时钟上升沿，体现「优先级：复位/载入 > 使能计数」。
> 

## ① 3 位减计数器（模 8，带 Load / Enable）

要点：模 = 8、`E` 使能、`L` 载入、**初值 = modulus−1**。`L=1` 时载入最大值，否则 `E=1` 才减 1。

```vhdl
LIBRARY ieee ;
USE ieee.std_logic_1164.all ;

ENTITY downcnt IS
    GENERIC ( modulus : INTEGER := 8 ) ;
    PORT ( Clock, L, E : IN  STD_LOGIC ;
           Q           : OUT INTEGER RANGE 0 TO modulus-1 ) ;
END downcnt ;

ARCHITECTURE Behavior OF downcnt IS
    SIGNAL Count : INTEGER RANGE 0 TO modulus-1 ;
BEGIN
    PROCESS
    BEGIN
        WAIT UNTIL (Clock'EVENT AND Clock = '1') ;
        IF L = '1' THEN
            Count <= modulus-1 ;
        ELSE
            IF E = '1' THEN
                Count <= Count-1 ;
            END IF ;
        END IF ;
    END PROCESS;
    Q <= Count ;
END Behavior ;
```

## ② 4 位同步加计数器（异步复位 + 使能）

要点：`Resetn` 异步清零（在 process 敏感表里、时钟判断之前），`E` 使能。

```vhdl
LIBRARY ieee ;
USE ieee.std_logic_1164.all ;
USE ieee.std_logic_unsigned.all ;

ENTITY upcount IS
    PORT ( Clock, Resetn, E : IN  STD_LOGIC ;
           Q                : OUT STD_LOGIC_VECTOR (3 DOWNTO 0) ) ;
END upcount ;

ARCHITECTURE Behavior OF upcount IS
    SIGNAL Count : STD_LOGIC_VECTOR (3 DOWNTO 0) ;
BEGIN
    PROCESS ( Clock, Resetn )
    BEGIN
        IF Resetn = '0' THEN
            Count <= "0000" ;
        ELSIF (Clock'EVENT AND Clock = '1') THEN
            IF E = '1' THEN
                Count <= Count + 1 ;
            ELSE
                Count <= Count ;
            END IF ;
        END IF ;
    END PROCESS ;
    Q <= Count ;
END Behavior ;
```

## ③ 4 位同步加计数器（异步复位 + 并行载入）

要点：`L` 载入、`R` 并行数据；优先级 `Resetn` > `L` 载入 > 加 1。

```vhdl
LIBRARY ieee ;
USE ieee.std_logic_1164.all ;

ENTITY upcount IS
    PORT ( R                : IN     INTEGER RANGE 0 TO 15 ;
           Clock, Resetn, L : IN     STD_LOGIC ;
           Q                : BUFFER INTEGER RANGE 0 TO 15 ) ;
END upcount ;

ARCHITECTURE Behavior OF upcount IS
BEGIN
    PROCESS ( Clock, Resetn )
    BEGIN
        IF Resetn = '0' THEN
            Q <= 0 ;
        ELSIF (Clock'EVENT AND Clock = '1') THEN
            IF L = '1' THEN
                Q <= R ;
            ELSE
                Q <= Q + 1 ;
            END IF ;
        END IF ;
    END PROCESS;
END Behavior ;
```

# ✅ 本节总结

<aside>
🧠

- **寄存器**：N 个共享时钟/清零的触发器，存 N 位；**移位寄存器**再加首尾互连，可串行移位（右移从低位入、左移从高位入），按串/并组合分 SISO / SIPO / PISO / PIPO 四类。
- **计数器**分异步与同步：异步（行波）结构简单但有传播延迟与毛刺；同步所有触发器共用时钟，快且干净。模 $\le 2^n$。
- **同步计数核心口诀**：某位只有在「所有低位全为 1」时才翻转 → $T_n = Q_0Q_1\cdots Q_{n-1}$；加 Enable 时各 T 再乘 E，E=0 即保持。
- **截断模值**：异步用检测+异步清零（有毛刺）；推荐**同步复位**或**模块化并行载入**来避免毛刺。
- **自启动**：所有初始状态都能汇入主循环才算自启动；**级联**进位 TC→使能 CTEN，可做大模值或分频器。
</aside>

# 📌 课堂练习 / 待办

- [ ]  **p7**：4 位移位寄存器，串入 `1001`，画出 $Q_A \sim Q_D$ 的时序波形。
- [ ]  **p23**：同步计数器设计练习（见原始 slide）。
- [ ]  **p27**：用卡诺图推导十进制计数器的 $J_1J_2J_3$（验证 $J_1=Q_0\bar{Q_3}$、$J_2=Q_0Q_1$、$J_3=Q_0Q_1Q_2+Q_0Q_3$）。

> ⚠️ 本节 slides 未给出明确的提交截止日期；如有作业 deadline，请以课程平台 / 老师通知为准，不要照搬此处。
> 

# 📎 原始 Slides

[lecture_9 part 3 shifter counter.pdf](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%203%EF%BC%9AShift%20Re/lecture_9_part_3_shifter_counter.pdf)
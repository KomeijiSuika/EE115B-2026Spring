# EE115B Lecture9 — Sequential Logic Part 2：Flip-Flops (D / T / JK)

<aside>
⏱️

**本节主题：** 时序逻辑 Part 2 —— **Flip-Flops（边沿触发触发器）**

**对应教材：** Floyd《Digital Fundamentals》Ch.7（如 Figure 7-14 / Table 7-2）

**承接 Part 1：** Part 1 讲的是 level-sensitive 的 SR latch / gated D latch；本节正式进入 edge-triggered 的 flip-flop。

**核心脉络：**

1. level-sensitive（latch）→ edge-triggered（flip-flop）的本质区别
2. D flip-flop 的行为、真值表与时序
3. 三种实现：master-slave（neg / pos edge）+ edge-triggered（pulse transition detector）
4. VHDL 描述：用 `Clock'EVENT and Clock='1'` 抓上升沿
5. CLEAR / PRESET：异步 vs 同步复位
6. 衍生触发器：T flip-flop、JK flip-flop
</aside>

## 1️⃣ Level-sensitive vs Edge-triggered —— 本节的根

这一节所有内容都建立在一个区别上：**输出由时钟「电平」控制，还是由时钟「边沿」控制。**

|  | Latch（锁存器） | Flip-Flop（触发器） |
| --- | --- | --- |
| 触发方式 | Level-sensitive（电平敏感） | Edge-triggered（边沿敏感） |
| 何时响应输入 | 时钟有效（如 Clk=1）的**整段时间**都在响应 | 仅在时钟**边沿那一瞬间**采样 |
| 输出变化 | 有效期内输入变，输出可**多次**变（透明） | 一个时钟周期内最多变**一次** |
| 是否一定有 clk | 不一定（基本 latch 可无 clk） | 一定有 clk（靠边沿工作） |
| 例子 | Gated SR latch、Gated D latch | D FF、T FF、JK FF |

<aside>
🔑

**口诀：** Latch 看**电平**（打开一扇「透明窗」，窗开着输出就跟着 D 抖）；Flip-Flop 看**边沿**（只在上升/下降沿那一刻「咔嚓」采一个点）。正因为 FF 只采一个点，它天然**抗输入毛刺**，是同步时序电路的基石。

</aside>

## 2️⃣ D Flip-Flop —— 最基础的「存一位」

D（Data）触发器把边沿时刻的 D 值锁进 Q，是寄存器的基本单元。其行为可一句话概括：

$$
Q(t{+}1) = D \quad (\text{在有效时钟边沿采样})
$$

**正边沿 D FF 真值表（Table 7-2）：**

| D | CLK | Q | $\bar{Q}$ | 说明 |
| --- | --- | --- | --- | --- |
| 0 | ↑ | 0 | 1 | RESET |
| 1 | ↑ | 1 | 0 | SET |

（↑ = 时钟由 LOW→HIGH 的上升沿；非边沿时刻 Q 保持不变。）

- ❓ Q&A：输出上的小圆圈是什么意思？是 Q'' = Q 还是 Q'？什么时候画圈？（2026-06-21）
    
    **一句话：小圆圈 = 「一次取反」的符号。画一个圈的那个输出 =** $Q$ **的反 =** $\bar Q$**（也写 Q'，读 not Q）。**
    
    ### 一个圈 = 取反一次
    
    - 触发器有两个互补输出：$Q$ 和 $\bar Q$。下面那个常画一个小圆圈，表示「这是取反的那一端」。
    - **圈一次 → 该输出 = Q'（互补）**，也就是 $\bar Q$。
    
    ### 你问的 Q'' = Q 还是 Q'？
    
    - **圈 + 上划线一起 = 两次取反 = Q'' = Q**（转回原值）。所以**别把圆圈和上划线当成两次取反叠着用**。
    - 标准画法**二选一**：① 画圈、标 $Q$（靠圈取反）；② 不画圈、标 $\bar Q$（靠横线取反）。两种都表示同一个互补输出 $\bar Q$。
    - 教材里有时圈和 $\bar Q$ 标签一起出现，那只是「图形符号 + 名字」同指这一个互补端，仍是 $\bar Q$，不是再取反一次。
    
    ### 什么时候要画圈
    
    - 想表示「这一脚是取反 / 低有效（active-low）」时画：互补输出 $\bar Q$、低有效控制脚（$\overline{CLR}$、$\overline{PRE}$、低有效使能 / 片选）。
    - 普通的 $Q$ 输出、高有效输入**不画圈**。

![Slide 7 — D flip-flop 符号、置位/复位与真值表](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_7.png)

Slide 7 — D flip-flop 符号、置位/复位与真值表

**时序例子（6 个时钟脉冲）：** 关键在于「**只在上升沿看 D**」——

1. 脉冲 1：D=0 → Q 保持 0（RESET）
2. 脉冲 2：D=0 → Q 保持 0（RESET）
3. 脉冲 3：D=1 → Q 跳到 1（SET）
4. 脉冲 4：D=0 → Q 回到 0（RESET）
5. 脉冲 5：D=1 → Q 跳到 1（SET）
6. 脉冲 6：D=1 → Q 保持 1（SET）

![Slide 8 — D flip-flop 6 脉冲时序：边沿采样，沿间 D 怎么抖都不影响 Q](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_8.png)

Slide 8 — D flip-flop 6 脉冲时序：边沿采样，沿间 D 怎么抖都不影响 Q

<aside>
💡

注意脉冲之间即便 D 反复变化，Q 也纹丝不动 —— 这正是「边沿采样」相对 latch「透明」的优势。

</aside>

## 3️⃣ D Latch vs D Flip-Flop —— 同一个 D，三种输出

把同一个 D、同一个 Clock 接到三种器件上，对比它们的输出：

- $Q_a$ **Gated D latch（电平）：** Clock 高电平期间「透明」，D 怎么抖 $Q_a$ 就怎么跟 —— 把毛刺全传过去了。
- $Q_b$ **正边沿 FF：** 只在 Clock 上升沿采 D 的那一个点。
- $Q_c$ **负边沿 FF：** 只在 Clock 下降沿采 D 的那一个点。

![Slide 10 — Gated D latch / 正边沿 FF / 负边沿 FF 对同一 D 的时序对比](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_10.png)

Slide 10 — Gated D latch / 正边沿 FF / 负边沿 FF 对同一 D 的时序对比

<aside>
🔑

**为什么工程上普遍用 FF 而不是 latch 做寄存器？** 因为 latch 在透明窗口内会把输入毛刺、亚稳态直接灌进输出；FF 只在边沿采一个确定点，时序干净、好做静态时序分析（setup/hold）。

</aside>

- ❓ Q&A：怎么一眼区分 D flip-flop 和 latch？（2026-06-19）
    
    **一句话：latch 看电平（透明窗），FF 看边沿（咱喬一下）。下面给 4 个由快到慢的判别法。**
    
    ### ① 看电路符号最快 🔺
    
    时钟输入端有没有那个**小三角 ▷（动态输入符号）**：
    
    - **有 ▷ → flip-flop**（边沿触发）
    - **没有 ▷，只是 EN / Clk 电平输入 → latch**
    
    ### ② 看波形（考试最常用）
    
    让 D 在时钟**有效电平期间**变化，看 Q 怎么反应：
    
    - **Q 在窗口内跟着 D 抖（变多次）→ latch**（透明）
    - **Q 只在边沿那一刻变一次、沿间纹丝不动 → flip-flop**
    
    ### ③ 看 VHDL 代码
    
    - **latch**：敏感表 `(D, Clk)`，判断 `IF Clk='1'`（**只判电平，没有 'EVENT**）。
    - **FF**：敏感表只有 `Clock`，判断 `IF Clock'EVENT AND Clock='1'`（或 `rising_edge(Clock)`）。
    - 想写 FF 却漏了 `'EVENT` → 综合器给你一个**意外 latch**。
    
    ### ④ 看一个时钟周期内能变几次
    
    - **latch**：有效期内可变**多次**（输入变它就变）。
    - **FF**：一个周期内最多变**一次**（只在边沿采样）。
    
    <aside>
    🐈
    
    **判别口诀：三角看符号、抖动看波形、'EVENT 看代码。** 三个里任一个命中就能定性。本质只有一句——**电平透明 = latch，边沿采点 = FF**。
    
    </aside>
    

## 4️⃣ D FF 的三种实现

### 4.1 Master-slave D FF（负边沿）

**结构：** 两个 gated D latch 串联（master + slave）；master 用原时钟，slave 用**取反**时钟。

- **Clock = 1：** master 有效，$Q_m$ 跟随 D；slave 此时关闭，Q 保持不变。
- **Clock = 0：** slave 有效，$Q_s$ 接收 $Q_m$ —— 最终输出 Q 在**时钟下降沿**完成更新。

本质：两级 latch 像「气闸」，前后两扇门永不同时打开，于是把「透明」收窄成了「一个边沿」。

![Slide 12 — Master-slave D FF（负边沿）电路：master 原时钟 + slave 反相时钟](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_12.png)

Slide 12 — Master-slave D FF（负边沿）电路：master 原时钟 + slave 反相时钟

![Slide 13 — Master-slave 工作与时序：Clk=1 时 Qm 跟 D，Q 在负边沿才更新](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_13.png)

Slide 13 — Master-slave 工作与时序：Clk=1 时 Qm 跟 D，Q 在负边沿才更新

### 4.2 Master-slave D FF（正边沿）

只要把时钟反相的位置换一下：**master 用取反时钟、slave 用原时钟**，最终输出就改在**上升沿**更新。

![Slide 14 — Master-slave D FF（正边沿）：反相器移到 master 端](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_14.png)

Slide 14 — Master-slave D FF（正边沿）：反相器移到 master 端

### 4.3 Edge-triggered D FF（pulse transition detector）

另一条实现路线：用一个**脉冲跳变检测器**在时钟边沿生成一个极窄脉冲，去「开一下」后面的 latch。

窄脉冲的原理是经典的「信号与自身延迟取反」做与：

$$
f = A \wedge \bar{A}
$$

理论上 $A \wedge \bar{A} = 0$，但因为反相器有传播延迟 $\Delta t$，$\bar{A}$ 比 $A$ 晚到，于是在边沿处产生一个宽度约为 $\Delta t_1 + \Delta t_2$ 的窄脉冲，恰好用作「边沿触发」的开门信号。

- ❓ Q&A：公式里的 ∧（看着像 ^）是什么？是 AND 吗？（2026-06-21）
    
    **是的。** ∧（LaTeX 写法 `\wedge`，渲染出来很像键盘的 `^`）就是**逻辑与 AND**。所以 $f = A \wedge \bar{A}$ 读作「$A$ 与 $\bar A$」，也就是 $A$ AND $\overline A$。
    
    ### 顺手把本章逻辑符号一次记牡
    
    - **∧**（`\wedge`，像 ^）= **AND 与** —— 全 1 才 1。
    - **∨**（`\vee`，像 v）= **OR 或** —— 有 1 就 1。
    - **⊕**（`\oplus`，圈里一个加号）= **XOR 异或** —— 不同为 1。T FF 的 $Q^+ = T \oplus Q$ 用的就是它，**别和 ∧ 搞混**。
    - **上划线** $\bar A$ **/ 撞号** = **NOT 取反**。
    - 省略号 / 并排写（如 $AB$）也表示 **AND**。
    
    <aside>
    ⚠️
    
    **一个坑：** 数学里 ∧ = AND；但在**代码 / Verilog / C** 里，键盘上的 `^` 是 **XOR（异或）**、`&` 才是 AND。看符号要分清是「数学公式」还是「代码」，别把两套混用。
    
    </aside>
    

![Slide 15 — Edge-triggered D FF：steering gates + latch，右侧为 pulse transition detector 原理](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_15.png)

Slide 15 — Edge-triggered D FF：steering gates + latch，右侧为 pulse transition detector 原理

<aside>
⚖️

**Trade-off：** master-slave = 两级 latch，结构清晰但**延迟大**（两个 stage）；pulse-detector = 靠门延迟造窄脉冲，**更快但更复杂**，且对延迟匹配敏感。

</aside>

- ❓ Q&A：送进 latch 的那个脉冲是谁造的？（是 CLK 变的，不是 D+反相器）（2026-06-20）
    
    **一句话：那个窄脉冲是「pulse transition detector」用 Slide 15 右边那个方法，把时钟 CLK 加工成的（**$A\wedge\bar{A}$ **+ 反相器延迟）；它跟 D 路上那个反相器毫无关系。脉冲来自 CLK，不是 D 造的。**
    
    ### ① 别把两个反相器搞混
    
    电路里有两个不同位置的反相器，干两件完全不同的事：
    
    - **CLK 路（检测器内部）：** 把时钟 $A$ 延迟取反成 $\bar{A}$，再和 $A$ 做与 → 造出**窄脉冲**。管「**什么时候**开门」。
    - **D 路（steering gate 那个）：** 只是把 D 变成 $\bar{D}$，喂给 G2。管「**写成什么**」（0 还是 1）。它**不产生任何脉冲**。
    
    ### ② 脉冲到底怎么从 CLK 变出来（图上右边的方法）
    
    把时钟 $A$ 分两路送进一个 AND：
    
    - 一路：原始 $A$（直连）。
    - 另一路：经反相器变 $\bar{A}$，因为反相器有延迟 $\Delta t$，它**晚到** $\Delta t$。
    
    $f = A\wedge\bar{A}$：
    
    - **稳态**：$A$、$\bar{A}$ 真互补（一个 1 一个 0）→ 与=0 → 无脉冲。
    - **上升沿瞬间**：$A$ 已跳到 1，$\bar{A}$ 还没掉到 0 → 两个都=1 一小会 → 冒出宽度 ≈ $\Delta t$ 的窄脉冲。
    
    这就是送进 latch 的那个脉冲的来源——**纯粹由时钟 CLK 加工而来**。
    
    ### ③ 两件事正交，别再混
    
    - **脉冲（来自 CLK）= 何时采**：只在边沿那一瞬开门。
    - **D /** $\bar{D}$**（来自 D 路反相器）= 采成什么**：决定写进去的是 0 还是 1。
    
    所以「脉冲是不是 D 和反相器造的？」——不是。D 那条路只负责数据，时间节拍完全由 CLK 经检测器产生。
    
    <aside>
    🐈
    
    **记牢：脉冲是 CLK 的产物（**$A\wedge\bar{A}$**），D 路反相器只造** $\bar{D}$ **管数据。一个管「何时」，一个管「啥值」，互不相干。**
    
    </aside>
    

## 5️⃣ VHDL 描述 —— 怎么用代码「抓边沿」

### 5.1 正边沿 D flip-flop

```vhdl
LIBRARY ieee ;
USE ieee.std_logic_1164.all ;

ENTITY flipflop IS
    PORT ( D, Clock : IN  STD_LOGIC ;
           Q        : OUT STD_LOGIC ) ;
END flipflop ;

ARCHITECTURE Behavior OF flipflop IS
BEGIN
    PROCESS ( Clock )                       -- 敏感表只有 Clock
    BEGIN
        IF Clock'EVENT AND Clock = '1' THEN -- 时钟发生变化且现在为 1 → 上升沿
            Q <= D ;
        END IF ;
    END PROCESS ;
END Behavior ;
```

关键点：

- **Sensitivity list 只放 `Clock`** —— 进程只在时钟变化时被唤醒。
- **`'EVENT`** 是信号属性，`Clock'EVENT` 表示「Clock 这一刻发生了跳变」。
- **`Clock'EVENT AND Clock = '1'`** = 跳变 + 现在是 1 = **上升沿**。这正是「边沿触发」在 RTL 里的写法。

### 5.2 对比：gated D latch 的 VHDL

```vhdl
ARCHITECTURE Behavior OF latch IS
BEGIN
    PROCESS ( D, Clk )   -- 敏感表是 D 和 Clk
    BEGIN
        IF Clk = '1' THEN -- 只判电平，没有 'EVENT
            Q <= D ;
        END IF ;
    END PROCESS ;
END Behavior ;
```

Latch 特性表：$Clk=0 \Rightarrow Q(t{+}1)=Q(t)$（保持）；$Clk=1 \Rightarrow Q(t{+}1)=D$（透明）。

<aside>
🔑

**一眼区分 latch / FF 的 VHDL：**
• **Latch：** 敏感表含 `(D, Clk)`，判断 `IF Clk = '1'`（**电平**）。
• **FF：** 敏感表只含 `Clock`，判断 `IF Clock'EVENT AND Clock = '1'`（**边沿**）。
少写了 `'EVENT`，综合器就会综合出一个 latch —— 这是新手最常见的「意外 latch」来源。

</aside>

## 6️⃣ CLEAR & PRESET —— 复位与置位

实际系统常需要强制把 FF 设到初始态：**上电初始化、系统 reset、调试强制置值**。于是加两条控制线：

- **CLEAR**：强制 Q=0
- **PRESET**：强制 Q=1

二者通常是 **active low（低有效）**：

| CLEAR | PRESET | 效果 |
| --- | --- | --- |
| 0 | 1 | Q = 0（清零） |
| 1 | 0 | Q = 1（置位） |
| 1 | 1 | no effect（正常工作） |

![Slide 19 — Master-slave D FF 带 CLEAR / PRESET 的电路符号（负边沿）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_19.png)

Slide 19 — Master-slave D FF 带 CLEAR / PRESET 的电路符号（负边沿）

### 6.1 异步 vs 同步 CLEAR

- **异步 CLEAR：** 只要 CLEAR=0，**立刻**把 Q 清 0，不管时钟在哪 —— 快，但可能引入 race / hazard。
- **同步 CLEAR：** CLEAR=0 后，要等**下一个时钟边沿**才清 0 —— 安全，受时钟节拍约束。

### 6.2 电路实现

**同步**做法：把 $\overline{Clear}$ 揉进 D 的组合逻辑（与 D 相与），等边沿才随采样生效。**异步**做法：直接把 PRE / CLR 接到内部 NAND latch 的置位/复位端，绕过时钟立即起效。

![Slide 21 — 同步 CLEAR（Clear 与 D 相与）+ master-slave 的异步实现](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_21.png)

Slide 21 — 同步 CLEAR（Clear 与 D 相与）+ master-slave 的异步实现

![Slide 22 — Edge-triggered FF 的异步 CLEAR：PRE / CLR 直接接到输出 NAND latch](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_22.png)

Slide 22 — Edge-triggered FF 的异步 CLEAR：PRE / CLR 直接接到输出 NAND latch

**示例时序：** 异步 PRE / CLR 直接「压」住输出，分三段——先 $\overline{PRE}=0$ 期间 Q 被钉在 1（Preset），中间释放后 Q 跟随 D（Follows D），最后 $\overline{CLR}=0$ 把 Q 钉在 0（Clear）。

![Slide 23 — Clear/Preset 异步示例时序：Preset → Follows D → Clear 三段](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_23.png)

Slide 23 — Clear/Preset 异步示例时序：Preset → Follows D → Clear 三段

<aside>
⚖️

**口诀：** 同步复位 = 把 Clear 揉进 D，**等边沿生效**（干净、好做时序分析）；异步复位 = 直拉 set/reset 端，**立刻生效**（快，但有竞争/亚稳态风险，且释放时刻要小心 recovery/removal time）。

</aside>

## 7️⃣ T Flip-Flop —— 可控「翻转器」

T（Toggle）触发器：

- **T = 0：** 状态保持不变
- **T = 1：** 状态翻转

$$
Q(t{+}1) = T \oplus Q(t)
$$

**特性表：** $T=0 \Rightarrow Q(t)$；$T=1 \Rightarrow \bar{Q}(t)$。

![Slide 24 — T flip-flop 符号、特性表与时序（T=1 翻转，T=0 保持）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_24.png)

Slide 24 — T flip-flop 符号、特性表与时序（T=1 翻转，T=0 保持）

**实现：** 用一个 D FF + 组合逻辑，令

$$
D = T\bar{Q} + \bar{T}Q = T \oplus Q
$$

把这个 D 喂回 D FF，就得到 T FF（slide 上用 AND-OR 实现这个异或）。

- ✅ Q&A（修正）：我画的 T flip-flop（NAND + 最后 AND）对吗？——对的！（2026-06-21）
    
    **结论：你的图是对的！我上一版看错了——以为你用「与门 + 或门」，才说反馈要交叉。你实际用的是** NAND + 最后一个 AND**，这种接法下反馈「不交叉」（T 配** $Q$**、**$\bar T$ 配 $\bar Q$）正好就是 $T\oplus Q$。是我之前判断错了，向你道歉 🙏。
    
    ### 你的推导复盘（完全正确）
    
    设上门 = $\mathrm{NAND}(T,Q)$、下门 = $\mathrm{NAND}(\bar T,\bar Q)$、最后一级 = AND：
    
    - **T=1：** 上门 $\mathrm{NAND}(1,Q)=\bar Q$（你说的 Q'）；下门 $\bar T=0$，$\mathrm{NAND}(0,\cdot)=1$；$D=\bar Q\wedge 1=\bar Q$ → **翻转** ✓
    - **T=0：** 上门 $\mathrm{NAND}(0,\cdot)=1$；下门 $\mathrm{NAND}(1,\bar Q)=Q$；$D=1\wedge Q=Q$ → **保持** ✓
    
    ### 为什么「不交叉」也对（De Morgan）
    
    $D=\mathrm{NAND}(T,Q)\wedge\mathrm{NAND}(\bar T,\bar Q)=(\bar T+\bar Q)(T+Q)=T\bar Q+\bar T Q=T\oplus Q$。两个 NAND 各被 De Morgan 翻一次号，再 AND，等价于一个标准 XOR。
    
    <aside>
    🔑
    
    **关键区别（别记混）：**
    • **与门 + 或门**（AND-OR）实现 $T\oplus Q$：反馈要**交叉**（T 配 $\bar Q$、$\bar T$ 配 $Q$）。
    • **NAND + 最后 AND**（你画的）：反馈**不交叉**（T 配 $Q$、$\bar T$ 配 $\bar Q$）。
    同一个 XOR，门一换，连线规则跟着变——这正是 De Morgan 在起作用。
    
    </aside>
    
    <aside>
    🐈
    
    **自检一招（任何实现都通用）：** 画完代 T=1 走一遍——算出 $D=\bar Q$（会翻）就对；再代 T=0 算出 $D=Q$（保持）就对。**看结果对不对，比记「交不交叉」更稳。**
    
    </aside>
    
- ❓ Q&A：为什么我的图没法用 De Morgan 变成 slide 25 那张？（2026-06-21）
    
    **一句话：因为 De Morgan 只会「换门的类型 + 沿原有连线挪小圆圈（取反）」，它从不改变「哪条信号接进哪只门」。你的图和 slide 25 喂给门的信号本来就不一样，所以两张图之间没有 De Morgan 通路——它们是 XOR 的两种不同分解，互相之间靠的是「乘开（分配律）」，不是 De Morgan。**
    
    ### 两张图喂进门的信号不同
    
    - **你的图（不交叉）：** 两只门吃的是 $\{T,Q\}$ 和 $\{\bar T,\bar Q\}$。
    - **Slide 25（交叉）：** 两只门吃的是 $\{T,\bar Q\}$ 和 $\{\bar T,Q\}$。
    - 输入集都不一样 → 不可能是 De Morgan 双胞胎。De Morgan 不能把接在某门上的 $Q$ 凭空换成 $\bar Q$（那是改接线 / 加反相器，不是 De Morgan）。
    
    ### De Morgan 只在「同一种分解」内部换装
    
    - **你的图的真正 De Morgan 双胞胎**：$D=(\bar T+\bar Q)(T+Q)\;\Leftrightarrow\;\mathrm{NAND}(T,Q)\cdot\mathrm{NAND}(\bar T,\bar Q)$ —— 连线不变，只是门换了。✓
    - **Slide 25 的 De Morgan 双胞胎**：$D=T\bar Q+\bar T Q\;\Leftrightarrow\;\mathrm{NAND}(\mathrm{NAND}(T,\bar Q),\mathrm{NAND}(\bar T,Q))$（AND-OR ↔ NAND-NAND，输入仍是交叉的）。
    
    ### 两张图之间靠的是「乘开」，不是 De Morgan
    
    $(\bar T+\bar Q)(T+Q)=\bar T T+\bar T Q+T\bar Q+\bar Q Q=T\bar Q+\bar T Q$（其中 $\bar T T=0$、$\bar Q Q=0$）。
    
    这一步用的是**分配律 + 互补律**（$X\bar X=0$），把 POS 形乘开成 SOP 形——这是另一条代数规则，跟 De Morgan 是两码事。
    
    <aside>
    🔑
    
    **记牢两件工具分工：**
    • **De Morgan** = 在「同一个表达式」里换门 / 挪圈（SOP↔它的 NAND-NAND、POS↔它的 NOR-NOR），**连线不变**。
    • **分配律（乘开 / 提取）** = 在「不同分解」之间走（SOP↔POS），会**改变连线**。
    你的图 ⇄ slide 25 跨的是「分解」，所以要乘开，不是 De Morgan。两者都 = XOR，只是真值表相同、写法不同。
    
    </aside>
    

![Slide 25 — T flip-flop 实现：D = T⊕Q 反馈进 D FF（练习：用 FSM 推导）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_25.png)

Slide 25 — T flip-flop 实现：D = T⊕Q 反馈进 D FF（练习：用 FSM 推导）

- ❓ Q&A：两种 T FF 图都对，是因为 FSM 有很多画法吗？考试都能画吗？（2026-06-21）
    
    **先纠一个点：不是「FSM 有很多种图」。FSM 推导出来的逻辑函数是唯一的（就是 D = T⊕Q）；自由度在「同一个函数可以用很多种门电路实现」这一步。两张图都对，是因为它们算出来都是 T⊕Q——真值表相同 = 同一个函数 = 都是合法 T FF。**
    
    ### 到底哪一步有「多种画法」
    
    - **FSM → 函数**：基本唯一。状态表 → 激励表 → K-map → 得到 $D=T\oplus Q$，这一步答案固定（K-map 化简结果是确定的）。
    - **函数 → 门电路**：自由度在这里。$T\oplus Q$ 可以用 AND-OR、NAND-NAND、NAND+AND、甚至一个 2:1 MUX、一块 XOR 门……无数种等价实现。
    
    <aside>
    🔑
    
    **一句话：** 不是 FSM 多变，是「**同一个布尔函数有无穷多种等价电路**」。只要最终 $D=T\oplus Q$，画法随你。
    
    </aside>
    
    ### 考试能不能两个都画？
    
    - **默认能。** 只要电路正确实现 $D=T\oplus Q$，逻辑等价就给分。
    - **看题目有没有限制**（最关键）：
        - 「用 **slide 的 AND-OR 结构**」/「**只用 NAND** 实现」/「用**最少的门**」 → 必须按要求那种，别的会扣分。
        - 「**用 FSM 推导**」 → 要把推导过程写出来（状态表→激励表→K-map→表达式），再画任一正确实现。光给电路不给推导会丢过程分。
    - **自保动作：** 画完在旁边写一句 $D=T\oplus Q$ 并代 T=0/1 各验一行，让批卷人一眼看出等价。
    
    <aside>
    🐈
    
    **结论：没限制时两种都对、都给分；有限制时按限制来。无论画哪种，附上** $D=T\oplus Q$ **+ 一行真值表自检最稳。**
    
    </aside>
    

<aside>
💡

**典型用途：** T=1 常态下，Q 每个时钟翻一次 → 输出频率是时钟的一半，是**二分频 / 计数器**的基本单元。

</aside>

## 8️⃣ JK Flip-Flop —— 「全能」触发器

JK 把 SR latch 与 T FF 的行为合并：**J = set，K = reset**，并把 SR 的禁止态 (1,1) 改造成「翻转」。

| J | K | Q(t+1) | 功能 |
| --- | --- | --- | --- |
| 0 | 0 | Q(t) | 保持 Hold |
| 0 | 1 | 0 | 复位 Reset |
| 1 | 0 | 1 | 置位 Set |
| 1 | 1 | $\bar{Q}(t)$ | 翻转 Toggle |

激励方程：

$$
Q(t{+}1) = J\bar{Q} + \bar{K}Q
$$

![Slide 26 — JK flip-flop 电路、特性表与符号（作业：推导它为什么是 JK FF）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/slide_26.png)

Slide 26 — JK flip-flop 电路、特性表与符号（作业：推导它为什么是 JK FF）

<aside>
🔑

**口诀：** JK = SR + T 的合体。SR 唯一的「坑」是 (1,1) 禁止态，JK 把它废物利用成 toggle，于是四种输入全部合法 —— 这就是它被称为「全能 FF」的原因。

</aside>

- 🧠 理解式记忆：D / T / JK 三兄弟一次记牢（ADHD 友好）（2026-06-19）
    
    **一句话总纲：所有 flip-flop = 「边沿采样的 1-bit 存储」+ 不同的输入接法。记住 JK 是母版，T 和 D 都是它的简化。**
    
    ### 第一步：先把“边沿”刻进脑子
    
    - **Latch 看电平**：时钟有效的整段时间都“透明”，D 怎么抖 Q 就怎么跟。
    - **Flip-Flop 看边沿**：只在上升/下降沿那一瞬“咱喳”采一个点，沿间 D 怎么变都不管。
    
    <aside>
    🔑
    
    **口诀：窗 vs 点。** Latch 是一扇开着的窗（窗开就跟），FF 是相机快门（只在边沿咱喳一张）。正因为只采一个点，FF 天然抗毛刺 → 同步电路都用它。
    
    </aside>
    
    ### 第二步：三兄弟各记一个动词
    
    - **D = 抄**：$Q^+ = D$。边沿一到，D 是几 Q 就是几。最简单，先背它。
    - **T = 翻**：$Q^+ = T \oplus Q$。T=1 翻转、T=0 保持（翻转＝异或）。
    - **JK = 全能**：$Q^+ = J\overline Q + \overline K Q$。set / reset / hold / toggle 四样都有。
    
    ### 第三步：用“亲缘关系”把三个串成一个（关键记忆桥）
    
    <aside>
    🌳
    
    **JK 是母版，另外两个都是它简化出来的：**
    
    - **T = 把 JK 的两只脚短接**（$J=K=T$）：只剩 hold(00) 和 toggle(11)。
    - **D = 给 JK 加个反相器**（$J=D,\ K=\overline D$）：只剩 set 和 reset = 直接抄 D。
    
    —— 是不是和上一章 “D latch = SR latch + 反相器” 一模一样的套路？同一招用两次。
    
    </aside>
    
    ### 第四步：JK 真值表只背 4 个字
    
    $J$ 像 Set、$K$ 像 Kill（清零）：
    
    - **00 → 保持**（没人管）
    - **01 → 置0**（K 清零）
    - **10 → 置1**（J 置位）
    - **11 → 翻转**（SR 的禁区被废物利用成 toggle）
    
    **口诀：「J置 K清，同0保持，同1翻」。** 为什么方程是 $Q^+=J\overline Q+\overline K Q$？——Q 想变成 1 只有两条路：本来是 0 被 J 置上去（$J\overline Q$），或本来是 1 且 K 没来清它（$\overline K Q$）。
    
    ### 第五步：实现 & 复位，各记一句
    
    - **Master-slave**：两个 latch 串成“气闸”，前后门永不同开 → 把透明收窄成一个边沿。**时钟反相加在哪级，就决定正/负边沿**（slave 最后放行的那个沿 = 输出更新沿）。
    - **Pulse detector**：用 $A\wedge\overline A$ + 反相器延迟造一个窄脉冲当“开门信号” → 更快但更复杂。
    - **CLEAR/PRESET**（通常低有效）：CLEAR→Q=0、PRESET→Q=1。**同步=揉进 D 等边沿（干净）；异步=直拉 set/reset 端立刻生效（快但有竞争风险）**。口诀「同步等节拍，异步插队」。
    
    ### 第六步：VHDL 一眼分辨
    
    - **FF**：敏感表只有 `Clock`，判断 `Clock'EVENT AND Clock='1'`（**边沿**）。
    - **Latch**：敏感表 `(D, Clk)`，判断 `IF Clk='1'`（**电平**）。
    - **漏写 `'EVENT` → 综合出意外 latch**（考试爱考的坑）。
    
    ### 🐈 30 秒回忆链（考前默念）
    
    **边沿采样（窗→点）→ D抄 / T翻 / JK全能 → JK是母版（T=两脚短接, D=加反相器）→ JK表「J置K清同0保持同1翻」→ master-slave气闸定边沿 / 同步异步复位。**
    
- ✏️ Q&A：考试会让我画门电路吗？怎么“推”出来而不是死背图？（2026-06-19）
    
    **结论：很可能考“画/补全门电路”，但几乎都是「构造题」——给你核心件，让你加料搭出来。所以别背整张图，背“加什么”的配方。**
    
    ### A. 按概率预测会让你画什么
    
    - **🔴 高概率**：交叉耦合 SR latch（NAND/NOR）；用 D FF + 逻辑门搭 **T FF**（$D=T\oplus Q$）、搭 **JK FF**（$D=J\overline Q+\overline K Q$）。slide 25 / 26 直接把它们列成作业，考点九成在这。
    - **🟠 中概率**：gated D latch（gated SR + 反相器）、master-slave 框图（两个 latch + 反相时钟）。
    - **🟡 低概率**：完整默画 pulse transition detector 的门级（太细，通常给图让你分析，而非空手画）。
    
    ### B. 一条“生长链”——只需真正会画 1 个，其余全靠加料
    
    <aside>
    🌱
    
    **交叉耦合 SR latch（地基，务必会默画）→ 加把关门 = Gated SR → 加反相器 = Gated D → 串两级 + 反相时钟 = Master-slave FF → 加反馈逻辑 = T / JK FF。** 每一步只记“加了什么”，不用背新图。
    
    </aside>
    
    ### C. 各自的“画图配方”（照着步骤连线即可）
    
    1. **SR latch（NAND 版，低有效）**
        - 画上下两个 NAND。
        - 上门输出记为 $Q$，下门输出记为 $\overline Q$。
        - **交叉**：上门输出连到下门一个输入，下门输出连到上门一个输入。
        - 上门空着的输入 = $\overline S$（因为 S 管 Q），下门空着的 = $\overline R$。
        - （NOR 版同理，只是门换成 NOR、变高有效，S/R 不加反。）
    2. **Gated SR**：在上面两个输入前各加一个门，把 $Clk$ 和 $S$/$R$ 相与（NAND 版加 NAND，NOR 版加 AND）。$Clk=0$ 时喂进“不激活值”→锁。
    3. **Gated D**：Gated SR 基础上，$S$ 端接 $D$、$R$ 端接 $D$ 经一个反相器 → 永远互补，无禁区。
    4. **Master-slave D FF**：画两个 D latch 方块串联（前一个 $Q$ 接后一个 $D$），时钟一个原样、一个经反相器。**反相器在哪级决定正/负边沿。**
    5. **T FF**：画一个 D FF，把 $Q$ 引回来与 $T$ 做 XOR，XOR 输出接 $D$（即 $D=T\oplus Q$）。
    6. **JK FF**：画一个 D FF，用组合逻辑搭出 $D=J\overline Q+\overline K Q$（两个 AND + 一个 OR：$J$ 与 $\overline Q$ 相与、$\overline K$ 与 $Q$ 相与，再 OR），接到 $D$。
    
    ### D. 🐈 考场画图三步法 + 自检
    
    1. **先画骨架**：先把核心（两个交叉门 / 一个 D FF 方块）画出来，别一上来纠结细节。
    2. **再挂输入输出**：按配方连 $S/R/D/T/J/K$、$Clk$、$Q/\overline Q$。
    3. **最后自检**：随手代 1~2 组输入走一遍信号，看 $Q$ 对不对（比如 SR latch 代 $\overline S=0$ 看 Q 是否＝1）。
    
    **心法：画图题 = 把“亲缘关系链”用笔画出来。你能默画交叉耦合 SR latch + 记住每步加什么，这一章所有电路都能现场搭。**
    

## 9️⃣ 本节总结

<aside>
📌

1. **Latch 看电平、FF 看边沿**；FF 只在边沿采一个点 → 天然抗毛刺，是同步时序的基石。
2. **D FF 两条实现路线：** master-slave（两级 latch，慢但清晰）vs pulse-detector（门延迟造窄脉冲，快但复杂）。
3. **复位两味：** 同步（揉进 D，边沿生效，安全）/ 异步（直拉 set-reset，立刻生效，有竞争风险）。
4. **触发器家族：** D = 存一位、T = 可控翻转（分频）、JK = 全能（SR+T，禁止态改 toggle）。
5. **VHDL 抓边沿：** `IF Clock'EVENT AND Clock = '1' THEN` —— 漏写 `'EVENT` 就会综合出意外 latch。
</aside>

## 🔟 作业 / 待办

- [ ]  **Slide 9 练习：** 画出 gated D latch / 正边沿 FF / 负边沿 FF 三者对同一 D 的时序图
- [ ]  **Slide 25 练习：** 用 FSM 推导 T flip-flop 的电路（验证 $D = T \oplus Q$）
- [ ]  **Slide 26 作业：** 推导为什么该电路是 JK flip-flop（核对特性表 $Q(t{+}1)=J\bar{Q}+\bar{K}Q$）

*（slides 中未给出明确 deadline；拿到 syllabus / 作业页后我再补 `<mention-date>` 标记。）*

## 📎 原始 Slides

[EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/lecture_9_part_2.pdf](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%202%EF%BC%9AFlip-Flo/lecture_9_part_2.pdf)
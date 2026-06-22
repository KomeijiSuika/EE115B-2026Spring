# EE115B Lecture9 — Sequential Logic Part 1：SR Latch & Gated D Latch

<aside>
📌

**本节主题：** Sequential Logic 入门 → Basic SR Latch → Gated SR Latch → Gated D Latch

**任课：** Chenxi Xiao（slides 部分引用自 Pearson Ed. / Hengzhao Yang / Zhifeng Zhu / Yajun Ha）

**核心脉络：** 组合 vs 时序 → SR Latch（Active-HIGH NOR / Active-LOW NAND）→ 真值表 & 状态转移 → Race Hazard → 加 Clock = Gated SR Latch → 用反相器简化为 Gated D Latch（D Flip-Flop 的基石）

</aside>

---

## 1️⃣ 为什么需要时序逻辑？

<aside>
🪧

Slide 3-4 原图（组合逻辑局限 + 按按钮翻转灯泡的例子）请见 [lecture_9 part 1](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/lecture_9%20part%201.md) 对应章节 §Limitations of Combinational Logic / §Sequential logic circuits。

</aside>

### 组合逻辑的瓶颈

组合逻辑电路输出**只**与当前输入有关。来一个例子：

- 按一次按钮 → 灯亮（如果之前是灭的）
- 再按一次 → 灯灭（如果之前是亮的）

**组合逻辑做不到** —— 它无法记住"上次按钮按下时灯的状态"。

### 时序逻辑（Sequential Logic）的定义

> Sequential logic circuits have **memory**, and their outputs depend on **both current and past inputs**, allowing the storage and manipulation of information over time.
> 

<aside>
🔑

**口诀**：组合逻辑 = 函数 $y=f(x)$；时序逻辑 = 状态机 $y_{t+1}=f(x_t,\, y_t)$ —— **多了一个"上次"。**

</aside>

---

## 2️⃣ Basic SR Latch — 两种基本实现

SR Latch = 最简单的 1-bit 存储单元，由两个**交叉耦合 (cross-coupled)** 的逻辑门组成。

![Slide 5 — Active-HIGH input S-R latch（NOR 实现）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/imagescacf7e6a-60e6-40a9-82a2-489898761a18-07_401_451_1188_617.jpg)

Slide 5 — Active-HIGH input S-R latch（NOR 实现）

![Slide 7 — Active Low vs Active High SR Latch 完整对比（NAND 与 NOR 两种实现，源自 Wikibooks Digital Circuits/Latches）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide-07.png)

Slide 7 — Active Low vs Active High SR Latch 完整对比（NAND 与 NOR 两种实现，源自 Wikibooks Digital Circuits/Latches）

| 实现 | 逻辑门 | 有效电平 | 稳态条件 |
| --- | --- | --- | --- |
| Active-HIGH | NOR × 2 | $S, R$ 高有效 | $S=R=0$ → 保持 |
| Active-LOW | NAND × 2 | $\overline S, \overline R$ 低有效 | $\overline S=\overline R=1$ → 保持 |

### 真值表（以 Active-LOW $\overline S-\overline R$ Latch 为例）

| $\overline S$ | $\overline R$ | $Q$ | $\overline Q$ | 状态 |
| --- | --- | --- | --- | --- |
| 1 | 1 | NC | NC | 保持（No Change） |
| 0 | 1 | 1 | 0 | **SET** |
| 1 | 0 | 0 | 1 | **RESET** |
| 0 | 0 | 1 | 1 | **Invalid**（$Q=\overline Q=1$ 不再互补） |

<aside>
⚠️

**核心陷阱：** 当 $\overline S=\overline R=0$（Active-LOW）或 $S=R=1$（Active-HIGH）时，两个输出**同时为 1（或 0）**，破坏 $Q=\overline Q$ 的互补约定 → 称为 **Invalid / 禁用输入**。这是 Basic SR Latch 永远要规避的禁区。

</aside>

- 🧠 Q&A：我手画的 SR latch 和 slide 不一样，是画错了吗？（2026-06-21）
    
    **先给结论：大概率没错，只是「画法/朝向」不同；但有一个地方要特别小心 —— 换门类型时 S/R 的位置要跟着换。**
    
    ### 1. 镜像 / 旋转 / 上下翻转都不算错
    
    SR latch 是否正确，只看**拓扑**（哪只门的输出反馈到哪只门、哪个输入接哪只门），不看画在上还是下、左还是右。把整张图上下翻、左右镜像，电路完全等价 —— 只是 $Q$ 和 $\overline Q$ 的位置会跟着换。所以单纯「长得和 slide 不一样」不等于错。
    
    ### 2. 唯一的一致性铁律
    
    - **NOR 版（Active-HIGH）**：$R$ 接「输出是 $Q$」的那只门（$R=1$ 把 $Q$ 砸成 0 = Reset）；$S$ 接「输出是 $\overline Q$」的那只门。→ 习惯画成 **R 在上、S 在下**。
    - **NAND 版（Active-LOW）**：方向反过来，$\overline S$ 接「输出是 $Q$」的那只门（$\overline S=0$ 把 $Q$ 顶成 1 = Set）；$\overline R$ 接另一只。→ 习惯画成 **S 在上、R 在下**。
    
    <aside>
    ⚠️
    
    **最常踩的点（很可能就是你和 slide 的差异）：** 从 NOR 换成 NAND 时，**不能只把门符号换掉、S/R 位置原封不动**。换门必须同时：① 有效电平从高变低（$S,R$ → $\overline S,\overline R$）；② **S 和 R 的上下位置对调**。如果你两张图里 S/R 都放在同样位置，其中一张就会和 slide 对不上。
    
    </aside>
    
    ### 3. 三步自检法（任何朝向都能判对错）
    
    1. **看门型定有效电平**：NOR=高有效（禁区 $S=R=1$）；NAND=低有效（禁区 $\overline S=\overline R=0$）。
    2. **试 Set**：把 S 设成「有效值」，沿着图推，$Q$ 是否变 1？
    3. **试 Reset**：把 R 设成「有效值」，$Q$ 是否变 0？
    
    → 两步都对 = 正确（不管画成什么朝向）；若「Set 反而把 $Q$ 推到 0」= 你把 S/R 接反了，或者 $Q$/$\overline Q$ 标签贴反了。
    
    ### 4. 还要检查：真值表别套错门
    
    你写的真值表（$S=R=1$ 禁用、$S=R=0$ 保持）是 **NOR（高有效）** 的版本。如果把它直接套到 NAND 图上就错了 —— NAND 是低有效，禁区在 $\overline S=\overline R=0$、保持在 $\overline S=\overline R=1$，Set/Reset 的触发值全是 0。对照 slide 5（NOR）和 slide 7（NAND vs NOR 对比）逐栏核一遍即可。
    

---

## 3️⃣ Basic SR Latch 工作原理

### SET 操作 — 无论初态如何都能拉到 $Q=1$

![Slide 8 — Basic SR Latch: How circuit works?（Latch starts out SET 的两种初态分析）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide-08.png)

Slide 8 — Basic SR Latch: How circuit works?（Latch starts out SET 的两种初态分析）

- 若 latch 原本 $Q=1$：拉低 $\overline S$ 也只是"加强"已有状态 → 保持
- 若 latch 原本 $Q=0$：拉低 $\overline S$ → 第一只 NAND 输出强制为 1 → 反馈把另一只 NAND 翻转 → $Q$ 跳到 1

### RESET 操作 — 无论初态如何都能拉到 $Q=0$

![Slide 9 — Basic SR Latch: How circuit works?（Latch starts out RESET 的两种初态分析）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide-09.png)

Slide 9 — Basic SR Latch: How circuit works?（Latch starts out RESET 的两种初态分析）

- 若 latch 原本 $Q=0$：保持
- 若 latch 原本 $Q=1$：拉低 $\overline R$ → $Q$ 翻到 0

<aside>
💡

**理解记忆**：SET / RESET 都是"无论之前在哪个状态，最终都能把 Q 拉到目标态" —— 这就是 latch 的**写入能力**。No-Change 才是它的"存储能力"。

</aside>

### No-Change 与 Invalid（slide 9）

![Slide 10 — Basic SR Latch：No-change（HIGHs on both inputs）与 Invalid（Simultaneous LOWs on both inputs）的电路对比](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide_10.png)

Slide 10 — Basic SR Latch：No-change（HIGHs on both inputs）与 Invalid（Simultaneous LOWs on both inputs）的电路对比

- **No-Change**：$\overline S=\overline R=1$ → 反馈环路稳定，$Q$ 保持原值（**存储**）
- **Invalid**：$\overline S=\overline R=0$ → 两输出同时被强制成 1，**且后续两路同时撤回会产生 race hazard**
- 🧠 理解式记忆：为什么真值表长这样？（不用死背，会推就行）（2026-06-19）
    
    **ADHD 友好心法：不要背 8 行真值表，只背「2 条门规则 + 3 个动作」，其余全部现场推。**
    
    ### 第一步：记死两条门的“脾气”（整章地基）
    
    - **NOR 门：见 1 就出 0。** 只要任何一个输入是 1，输出立刻是 0；只有全 0 才出 1。→ 它的“霸道值”是 **1**。
    - **NAND 门：见 0 就出 1。** 只要任何一个输入是 0，输出立刻是 1；只有全 1 才出 0。→ 它的“霸道值”是 **0**。
    
    <aside>
    💡
    
    **这一条决定了“有效电平”**：用门的“霸道值”去激活它。NOR 霸道值=1 → **用 1 激活 → Active-HIGH**；NAND 霸道值=0 → **用 0 激活 → Active-LOW**。“NOR 高、NAND 低”不是死规定，是从门的脾气推出来的。
    
    </aside>
    
    ### 第二步：看懂交叉耦合在干嘎
    
    两只门头尾相接：每只门的输出，又当成另一只门的输入。
    
    - **没人激活时**（NOR 输入全给 0 / NAND 输入全给 1）：NOR(0,x)=非x，NAND(1,x)=非x → **两只门互相变成反相器**，首尾一接就成了“自锁环”，把上一刻的 $Q$ 一直顶住 → 这就是**记忆/保持 (Hold)** 的来历。
    - 所以 **Hold 不用记**，它就是“两个输入都不激活”的自然结果。
    
    ### 第三步：三个动作，现场推出任何一行
    
    1. **谁负责谁**：$S$（Set）只管把 $Q$ 推到 **1**；$R$（Reset）只管把 $Q$ 推到 **0**。
    2. **怎么激活**：把那条线给成门的“霸道值”。
        - NOR 版：$S=1$ → 强行把 $\overline Q$ 砸成 0 → $Q$ 翻到 1（SET）；$R=1$ → 把 $Q$ 砸成 0（RESET）。
        - NAND 版：$\overline S=0$ → 直接把 $Q$ 顶成 1（SET）；$\overline R=0$ → 把 $Q$ 顶成 0（RESET）。
    3. **两个同时激活 = Invalid**：两只门被同时砸成同一个值（NOR 都成 0 / NAND 都成 1）→ $Q$ 和 $\overline Q$ 不再互补 → 禁区。
    
    <aside>
    ⚡
    
    **所以整张 SR 真值表只有 4 种情况，全靠推：** 都不激活=保持；只激活 S=置1；只激活 R=置0；都激活=禁区。两种实现（NOR/NAND）只是“激活值”从 1 换成 0，结构一模一样。
    
    </aside>
    
    ### 第四步：Gated SR 只是多了“准入闸门”
    
    在前面加一对门，用 $Clk$ 把关：
    
    - $Clk=0$：闸门把 $S/R$ 都变成“不激活值”喂进去 → 锁存器以为没人动它 → **冻结保持**。
    - $Clk=1$：$S/R$ 原样通过 → 退化成普通 SR。
    - $S=R=1$（Clk=1）依然是禁区——闸门不解决冲突，只控制“什么时候允许写”。
    
    **记法：Gated SR = 基本 SR + 一句“只有 Clk=1 才放行”，没有新表要背。**
    
    ### 第五步：Gated D 为什么没有禁区（最优雅的一步）
    
    禁区的唯一来源是“$S$ 和 $R$ 同时激活”。Gated D 用**一个反相器**把它们强行绑成互补：$S=D$、$R=\overline D$。
    
    - $D$ 永远只有一个，$S$ 和 $R$ 必然一个激活一个不激活 → **结构上根本凑不出禁区**。
    - 于是 $Clk=1$ 时 $Q$ 直接等于 $D$（要么 SET 要么 RESET），$Clk=0$ 时保持。
    
    <aside>
    🎯
    
    **Gated D 真值表只要记一句**：$Clk=1$ → $Q=D$（透明跟随）；$Clk=0$ → 保持。不存在禁区，所以没有第三行要背。
    
    </aside>
    
    ### 🐈 一条口诀链串全章
    
    **门脾气（NOR见1出0 / NAND见0出1）→ 霸道值定有效电平 → S推1/R推0 → 同时激活=禁区 / 都不激活=保持 → 加Clk=准入 → 加反相器=消禁区(D)。**
    

---

## 4️⃣ Race Hazard

### 定义

> **Hazard**：digital circuit 输出中一个**不希望的临时变化**（glitch / spike）。
> 

> **Race hazard**：两个或多个信号**同时变化**，因传播延迟不等而互相竞争控制输出 → 结果取决于哪个信号先到 → **不可预测**。
> 

### SR Latch 中的体现

当从 **Invalid** ($\overline S=\overline R=0$) 同时撤回到 **No-Change** ($\overline S=\overline R=1$)：

- 两路输入同时上升
- 谁先到达对方的反馈输入端，谁就决定了最终态
- 因为门延迟不可控 → $Q$ 是 0 还是 1 完全靠运气

![Slide 12 — Race Hazard 实例：AND(A, A非) 产生的毛刺脉冲（左）+ SR Latch 从 Invalid 同时撤回时输出不确定（右）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide_12.png)

Slide 12 — Race Hazard 实例：AND(A, A非) 产生的毛刺脉冲（左）+ SR Latch 从 Invalid 同时撤回时输出不确定（右）

<aside>
⚠️

**结论**：永远不要让 Basic SR Latch 落入 Invalid；更不要从 Invalid 同时撤回 → **这是 Latch 设计必须规避的禁区**。

</aside>

参考：[en.wikipedia.org/wiki/Race_condition](http://en.wikipedia.org/wiki/Race_condition)

---

## 5️⃣ Basic SR Latch 时序图

![Slide 13 — Basic SR Latch Timing Diagram（assume no propagation delay）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide_13.png)

Slide 13 — Basic SR Latch Timing Diagram（assume no propagation delay）

假设无传播延迟，按以下输入序列：

- $S=1, R=0$：$Q$ 立即翻 1（SET）
- $S=0, R=0$：$Q$ 保持
- $S=0, R=1$：$Q$ 立即翻 0（RESET）
- $S=0, R=0$：$Q$ 保持

**要点**：输出只在 SET / RESET 输入有效时改变，其余时间靠"反馈记忆"维持。

---

## 6️⃣ SR Latch 的 VHDL 实现

![Slide 13 — Active-LOW SR Latch + VHDL](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/imagescacf7e6a-60e6-40a9-82a2-489898761a18-14_212_216_527_147.jpg)

Slide 13 — Active-LOW SR Latch + VHDL

```vhdl
entity SRLatch is
    port (SNot, RNot : in    std_logic;
          Q,    QNot : inout std_logic);
end entity SRLatch;

architecture LogicOperation of SRLatch is
begin
    Q    <= QNot nand SNot;   -- 两条 Boolean 表达式
    QNot <= Q    nand RNot;   -- 定义两个互为反馈的输出
end architecture LogicOperation;
```

<aside>
💡

**两个细节**：

- 信号 `SNot, RNot` = $\overline S, \overline R$（Active-LOW）。
- `Q, QNot` 都声明为 **`inout`**，因为它们既是输出，又作为反馈再次进入另一只 NAND 的输入。
</aside>

---

## 7️⃣ 应用：消除按键抖动 (Switch Debounce)

![Slide 15 — Switch contact bounce 波形 + Contact-bounce eliminator circuit（用 SR Latch 去抖）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide_15.png)

Slide 15 — Switch contact bounce 波形 + Contact-bounce eliminator circuit（用 SR Latch 去抖）

![Slide 16 — 74HC279A Logic diagram / Pin diagram + Function Table](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide_16.png)

Slide 16 — 74HC279A Logic diagram / Pin diagram + Function Table

### 问题：机械按键的"脏"信号

机械按键按下/松开时，触点会在毫秒级时间内反复接通-断开多次，组合逻辑会把每次抖动当成一次按键，从而误触发。

### 用 SR Latch 解一刀

- 把按键的两个端子（"按下" / "松开"）分别接到 $\overline S, \overline R$
- **第一次接通就完成一次 SET 或 RESET**
- 后续抖动都对应 $\overline S=\overline R=1$（No-Change）→ $Q$ **不再变化**
- 抖动期间永远不会同时拉低 $\overline S$ 和 $\overline R$ → **不会进入 Invalid**

<aside>
🎯

**SR Latch 的杀手级应用**：把模拟世界的"脏"信号转化成数字世界的"干净"边沿 —— 这是 latch 在嵌入式里最常见的场景之一。

</aside>

### 商用芯片：74HC279A

内部集成 4 个 Active-LOW SR Latch，专门给按键去抖 / set-reset 信号使用。

| $\overline S$ | $\overline R$ | $Q$ | 说明 |
| --- | --- | --- | --- |
| H | H | $Q_0$ | 保持（No-Change） |
| L | H | H | SET |
| H | L | L | RESET |
| L | L | H* | 不可预测（Invalid） |

---

## 8️⃣ Gated SR Latch — 加入 Clock

### 动机：同步化

Basic SR Latch 任何时刻输入变化都立即响应 → glitch 直接传到输出。在多模块系统里（如 bus sender / receiver）需要：

- 只在某个明确的时间窗口（Clock=1）允许写入
- 其他时间锁住状态

### 拓扑：在 SR Latch 前加 AND/NAND 把关

![Slide 17 — Gated SR Latch：Logic diagram + Logic symbol（在 SR Latch 前用 EN/CLK 把关）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide_17.png)

Slide 17 — Gated SR Latch：Logic diagram + Logic symbol（在 SR Latch 前用 EN/CLK 把关）

![Slide 18 — Gated SR Latch 两种实现：NOR gates（左）与 NAND gates（右）+ Characteristic Table](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide_18.png)

Slide 18 — Gated SR Latch 两种实现：NOR gates（左）与 NAND gates（右）+ Characteristic Table

### 特征表 (Characteristic Table)

| Clk | $S$ | $R$ | $Q(t+1)$ | 说明 |
| --- | --- | --- | --- | --- |
| 0 | × | × | $Q(t)$ | **锁住** — 任何输入都被忽略 |
| 1 | 0 | 0 | $Q(t)$ | No-Change |
| 1 | 0 | 1 | 0 | RESET |
| 1 | 1 | 0 | 1 | SET |
| 1 | 1 | 1 | × | **Avoid** — 仍然是禁用态 |

<aside>
🔑

**Clock 的两个职能：**

1. **同步**：所有写入都对齐到 Clock=1 的窗口。
2. **过滤毛刺**：Clock=0 时输入随便变化都不影响 Q。
</aside>

### 时序图

![Slide 19 — Gated SR Latch Timing diagram：Q 只在 CLK=1 的窗口内随 S/R 变化](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide_19.png)

Slide 19 — Gated SR Latch Timing diagram：Q 只在 CLK=1 的窗口内随 S/R 变化

观察重点：$Q$ **只在 CLK=1 的窗口内追随** $S/R$ **变化；CLK=0 时即使** $S/R$ **有跳变，**$Q$ **完全不动。**

---

## 9️⃣ Gated D Latch — 从根上消除 Invalid

### 设计思想

Basic / Gated SR Latch 都有"$S=R=1$ 不可用"的痛点。

**Gated D Latch 用一个反相器把 S 和 R 强制成互补**（$S=D$, $R=\overline D$），**从根上消除 Invalid 输入**。

![Slide 20 — Gated D Latch（完整电路 + 真值表 + 设计理念说明，教材 p.394）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide-20.png)

Slide 20 — Gated D Latch（完整电路 + 真值表 + 设计理念说明，教材 p.394）

### 特征表

| Clk | $D$ | $Q(t+1)$ | 说明 |
| --- | --- | --- | --- |
| 0 | × | $Q(t)$ | **保持**（latched） |
| 1 | 0 | 0 | $Q$ 跟随 $D$ |
| 1 | 1 | 1 | $Q$ 跟随 $D$ |

<aside>
🎯

**Gated D Latch 的三大胜利：**

1. **无 Invalid 态**：$D$ 是单输入，$S=D$ 与 $R=\overline D$ 永远互补。
2. **直觉化语义**：$D$ = 数据，Clk=1 写入，Clk=0 保持 → 接近"内存单元"的概念。
3. **D Flip-Flop 的基石**：下一节会把 D Latch 串联成边沿触发的 D-FF。
</aside>

### Timing Diagram

![Slide 21 — Gated D Latch Timing diagram：Clk=1 时 Q 实时跟随 D，Clk=0 时 Q 冻结在最后值](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide_21.png)

Slide 21 — Gated D Latch Timing diagram：Clk=1 时 Q 实时跟随 D，Clk=0 时 Q 冻结在最后值

要点：CLK=1 期间，$Q$ 像跟随器一样**实时跟踪** $D$；CLK=0 期间 $Q$ 冻结在最后一次的值 —— 这就是 **level-sensitive**（而非 edge-sensitive），这一点和下节的 D Flip-Flop 是关键区别。

### VHDL 实现

![Slide 22 — VHDL code for gated D Latch（电路符号 + 真值表 + process 代码）](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/slide_22.png)

Slide 22 — VHDL code for gated D Latch（电路符号 + 真值表 + process 代码）

```vhdl
library ieee;
use ieee.std_logic_1164.all;

entity latch is
    port (D, Clk : in  std_logic;
          Q      : out std_logic);
end latch;

architecture Behavior of latch is
begin
    process (D, Clk)
    begin
        if Clk = '1' then
            Q <= D;     -- level-sensitive：Clk=1 就一直跟随
        end if;          -- 没有 else → 综合工具自动推断"保持"
    end process;
end Behavior;
```

<aside>
⚠️

**新手陷阱**：这段代码**没有 else 分支**，综合工具会推断出 latch（保持上一次的 Q）。如果你**本来想要的是 flip-flop**，必须用 `rising_edge(Clk)` 而不是 `Clk='1'` —— 这条规则下节课会反复强调。

</aside>

---

## 📝 本节总结

<aside>
🎯

**三条贯穿本节的脉络（记住这三点就够）：**

1. **时序 = 组合 + 反馈**：cross-coupled NAND / NOR 把"上次的 Q"反馈回输入 → 拥有了记忆。
2. **Latch 进化路径**：Basic SR（有 Invalid）→ Gated SR（加 Clock，仍有 Invalid）→ Gated D（用反相器消除 Invalid，level-sensitive 保持）→ 下节 D Flip-Flop（edge-sensitive）。
3. **Clock 是数字系统的心跳**：用它把异步世界（按键、外部信号）转成同步世界（与时钟边沿对齐的写入），是所有大型同步数字系统的根基。
</aside>

---

- 🎯 考试预测 + 速记清单：这一章会怎么考？（2026-06-19）
    
    **结论先行：** 本章在期末属于 🔴 P1 时序逻辑核心，最可能以「**波形题 + 真值表填空 + 概念辨析**」三种形式出现，丢分点几乎全是“小错误”。
    
    ### A. 最可能的考法（按概率排）
    
    1. **🔴 波形 / 时序图题（最高频）**：给 $S/R/Clk$ 或 $D/Clk$ 波形，让你画 $Q$。考点是“什么时候 $Q$ 变、什么时候冻结”。
    2. **🔴 真值表 / 特征表填空**：填 SR Latch、Gated SR、Gated D 的输出列，尤其要标出 **Invalid / No-Change**。
    3. **🟠 概念辨析（选择 / 判断 / 简答）**：组合 vs 时序、level-sensitive vs edge-triggered、NOR 高有效 vs NAND 低有效、为什么 D latch 消除了 Invalid。
    4. **🟠 race hazard 简答**：什么是竞争冒险、SR Latch 从 Invalid 同时撤回为什么不可预测。
    5. **🟡 电路 / VHDL**：默画交叉耦合 latch；判断一段 VHDL 综合出 latch 还是 flip-flop。
    
    ### B. 必背清单（闭眼能默写）
    
    - **SR 两种实现**：NOR 实现 → Active-HIGH（高有效）；NAND 实现 → Active-LOW（低有效）。口诀 **“NOR 高、NAND 低”**。
    - **禁区 Invalid**：NOR / 高有效在 $S=R=1$；NAND / 低有效在 $\overline S=\overline R=0$。记法：两个激活信号同时按下 → 冲突。
    - **Gated SR 特征表**：$Clk=0$ 锁住一切；$Clk=1$ 才按 $S/R$ 动作；$S=R=1$ 仍是禁用（Avoid）。
    - **Gated D**：$S=D,\ R=\overline D$ 永远互补 → 从根上无禁区；$Clk=1$ 透明跟随、$Clk=0$ 保持。
    - **Latch vs FF**：Latch = 电平敏感（高电平期间透明）；Flip-Flop = 边沿敏感。口诀 **“锁存看电平，触发看边沿”**。
    
    ### C. 怎么快速记（ADHD 友好）
    
    - **只背“激活组合”，其余靠推**：SR 真值表其实只需记住 SET（置1）/ RESET（置0）/ 禁区 三行，No-Change 是默认。
    - **画图代替背字**：闭眼默画一次交叉耦合 NAND/NOR，比硬背真值表牢。每天画 1 次，3 天就稳。
    - **一句话主线串全章**：Basic SR（有禁区）→ Gated SR（加时钟，仍有禁区）→ Gated D（反相器消禁区，level-sensitive）。顺这条进化链，每一步“解决了上一步什么痛点”就记住了。
    - **波形题靠口诀**：先看 **Clk/EN** —— 关了就冻结（画水平线）；开了再看 $S/R$ 或 $D$ 决定跳变。
    
    ### D. 🐈 ADHD 防丢分（考场最容易栽的小错）
    
    1. **搞反有效电平**：NAND latch 是**低**有效，别用高有效的真值表去套。
    2. **波形题漏“冻结”**：$Clk=0$ / $EN=0$ 时 $Q$ 必须画成**保持水平**，不是跟随输入。
    3. **level vs edge 混淆**：D **latch** 在 $Clk=1$ 整个高电平期间都透明；D **flip-flop** 只在边沿那一瞬采样。
    4. **VHDL 漏 else → 意外综合出 latch**：想要 FF 必须用 `rising_edge(Clk)`。

---

## 📚 作业 / 待办

- [ ]  复习 Basic SR Latch 的 4 种输入组合，闭眼能写出真值表
- [ ]  自己用 NAND / NOR 重画 Active-HIGH / Active-LOW SR Latch
- [ ]  思考：为什么 Gated D Latch 在 Clk=1 期间是"透明"的？这和 D Flip-Flop 的"上升沿触发"区别在哪？
- [ ]  等 Lecture 9 part 2 来巩固 D Flip-Flop / JK / T 等

---

## 📎 原始 Slides

<aside>
📥

**完整 slide 原图查阅入口** —— 本笔记中未能直接嵌入的 slide 图都在下面这个 Notion Import 子页里：

</aside>

[lecture_9 part 1](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/lecture_9%20part%201.md)

[lecture_9 part 1.pdf](EE115B%20Lecture9%20%E2%80%94%20Sequential%20Logic%20Part%201%EF%BC%9ASR%20Latch/lecture_9_part_1.pdf)
# EE115B Lecture8 — Finite State Machine Part 4：概念 · 编程 · 电路设计

<aside>
🔁

**本节主题：** Finite State Machine（有限状态机）Part 4 —— 概念 / 编程 / 电路设计

**衔接：** 接 Lecture9（Latch / Flip-Flop / Counter），本节把"存储元件"组织成"带控制流的状态机"。

**核心脉络：** 时序电路 → FSM 定义 → Moore vs Mealy → 设计流程（序列检测器）→ 状态图 → HDL 编程（VHDL / Verilog）→ 状态表 → 状态编码 → 卡诺图推导次态 / 输出 → D 触发器实现 → 画电路 → 时序图 → 其他编码（alternative / one-hot）

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md) ｜ 本节为 **Lecture8 Part 4**；同一讲 Part 1 = VHDL 见 [EE115B Lecture8 — VHDL Part 1：entity · architecture · process · testbench](EE115B%20Lecture8%20%E2%80%94%20VHDL%20Part%201%EF%BC%9Aentity%20%C2%B7%20architectur.md)、Part 2 = Verilog 见 [EE115B Lecture8 — Verilog HDL Part 2：module · 数据类型 · always · 仿真](EE115B%20Lecture8%20%E2%80%94%20Verilog%20HDL%20Part%202%EF%BC%9Amodule%20%C2%B7%20%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B.md)、Part 3 = FPGA 见 [EE115B Lecture8 — FPGA Part 3：概念与硬件电路](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF.md)

</aside>

## 🗂 课程行政信息

- 本节对应课程 Project：[EE115B Project — Subway Turnstile Controller](EE115B%20Project%20%E2%80%94%20Subway%20Turnstile%20Controller.md)（slide 14 的 `IDLE / VALID / PASS / CLOSE / ALARM` 就是地铁闸机 FSM 的状态集）。
- [ ]  **Project — Subway Turnstile Controller** 提交：June 5, 2026 11:59 PM

---

# Part 1 — 概念与编程

## 1️⃣ 什么是状态机（slides 3–4）

**时序电路 (Sequential Circuit)：** 输出取决于"过去的行为 + 当前输入"，因此必须有存储（记忆）。

**有限状态机 (FSM)：** 拥有有限个状态、并按规定顺序在状态间转移的时序电路。

<aside>
🛗

**直观例子 — 电梯控制：** 状态 = {Idle, Moving Up, Moving Down, Door Open}；事件触发转移：Idle --楼上呼叫--> Moving Up；到楼层 → Door Open；超时 → Idle。FSM 就是把"现实控制流程"抽象成"状态 + 转移条件"。

</aside>

## 2️⃣ Moore vs Mealy（slides 5–7）

两类基本状态机，区别只在**输出由什么决定**：

| 类型 | 输出依赖 | 特点 |
| --- | --- | --- |
| **Moore** | 仅当前状态 present state | 输出随时钟同步、无毛刺；状态可能多一点 |
| **Mealy** | 当前状态 **+** 当前输入 | 响应快（输入一变输出就变）、状态少；可能有毛刺 |

![Slide 6 — Moore Machine 框图](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_06.png)

Slide 6 — Moore Machine 框图

Moore 框图三块：**transition logic（次态逻辑）→ state memory（触发器存当前状态）→ output logic（只读状态算输出）**。

![Slide 7 — Mealy Machine 框图](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_07.png)

Slide 7 — Mealy Machine 框图

Mealy 的差别：output logic 的输入里**多了一根从 input 直接拉过来的线** → 输出 = f(state, input)。

<aside>
💡

**判别口诀：** 输出框只接"状态" → Moore；输出框还接了"原始 input" → Mealy。本节序列检测器用的是 **Moore**（$z$ 标在状态节点上）。

</aside>

## 3️⃣ 设计流程：序列检测器（slide 8）

**题目规格 (problem statement)：**

- 1 个输入 $w$，1 个输出 $z$。
- 所有变化都发生在**时钟上升沿**。
- 行为：当 $w=1$ **连续保持两个时钟周期**时 $z=1$；否则 $z=0$。

## 4️⃣ 状态图 State Diagram（slides 9–10）

按"检测进度"定义三个状态：

- **State A**（起始 / 复位态，或 $w=0$）：$z=0$
- **State B**：$w=1$ 已持续 **1** 个周期：$z=0$
- **State C**：$w=1$ 已持续 **2** 个周期：$z=1$

![Slide 10 — 序列检测器状态图](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_10.png)

Slide 10 — 序列检测器状态图

- **节点 = 状态**，**有向弧 = 转移**，弧上标注输入条件 $w$。
- 这是 **Moore** 机：$z$ 标在状态里（`A/z=0`、`B/z=0`、`C/z=1`），与输入无关。
- 转移规律：只要 $w=0$ 立刻回到 A（检测被打断）；$w=1$ 就沿 A→B→C 往前推，到 C 后只要 $w$ 仍为 1 就停在 C（持续输出 1）。

## 5️⃣ HDL 编程（slides 11–13）

### VHDL 写法（slides 11–12）

![Slide 11 — VHDL 状态机代码](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_11.png)

Slide 11 — VHDL 状态机代码

典型"双进程"结构：

- **组合进程**（敏感于 `w, y_present`）：用 `CASE y_present` 决定 `y_next`（次态逻辑）。
- **时序进程**（敏感于 `Clock`）：上升沿把 `y_present <= y_next`，并处理 `Resetn` 异步复位。
- 输出：`z <= '1' WHEN y_present = C ELSE '0'`（Moore：输出只看状态）。

<aside>
🧹

slide 12 的改进：把次态 `CASE` 的兜底分支用 **`WHEN OTHERS`** 收掉，避免漏掉未用编码（`11`）导致综合出意外 latch。

</aside>

### Verilog 写法（slide 13）

![Slide 13 — Verilog 状态机代码](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_13.png)

Slide 13 — Verilog 状态机代码

```verilog
module fsm (input clk, reset, w, output reg z);
  reg [1:0] state;
  parameter A = 2'b00, B = 2'b01, C = 2'b10;

  // 状态转移（时序）
  always @(posedge clk or posedge reset) begin
    if (reset) state <= A;
    else case (state)
      A: state <= w ? B : A;
      B: state <= w ? C : A;
      C: state <= w ? C : A;
      default: state <= A;
    endcase
  end

  // 输出控制（组合，Moore）
  always @(*) begin
    case (state)
      C: z = 1'b1;
      default: z = 1'b0;
    endcase
  end
endmodule
```

<aside>
🔑

**两段式模板要记牢：** 一个 `always @(posedge clk)` 管"状态转移"，一个 `always @(*)` 管"输出"。Moore 的输出 `case` 只看 `state`；若 `case` 里还引用了 `w`，那就变成 Mealy。

</aside>

### Course Project（slide 14）

课程项目（地铁闸机）就是一个更大的 FSM：状态集 `IDLE / VALID / PASS / CLOSE / ALARM / …`。设计套路同上：先画状态图 → 写两段式 HDL → 仿真测试每条转移弧。

---

# Part 2 — 设计状态机电路（手工综合）

把上面的状态图，一步步综合成门级电路。

## 6️⃣ 状态表 State Table（slide 16）

![Slide 16 — 状态表](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_16.png)

Slide 16 — 状态表

状态表是状态图的**结构化等价表示**：行 = 现态 (Node)，列 = 不同输入下的次态 (Arrow) 与输出 (Output)。

| 现态 | 次态 ($w=0$) | 次态 ($w=1$) | $z$ |
| --- | --- | --- | --- |
| A | A | B | 0 |
| B | A | C | 0 |
| C | A | C | 1 |

## 7️⃣ Step 1：状态编码（slide 17）

- 每个状态用一组**状态变量**编码。3 个状态 → 需要 $\lceil \log_2 3\rceil = 2$ 个变量。
- 现态变量：$y_1, y_2$；次态变量：$Y_1, Y_2$。
- 取 **A: 00，B: 01，C: 10**（按 $y_2 y_1$），编码 **11 未用** → 当作 don't care，给化简留弹药。

## 8️⃣ Step 2：推导输出 / 次态表达式（slides 18–21）

![Slide 18 — 带编码的状态表](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_18.png)

Slide 18 — 带编码的状态表

把状态名换成 $y_2 y_1$ 得到真值表，再用卡诺图分别求 $z, Y_1, Y_2$。**充分利用未用编码 11 的 don't care 可显著化简。**

![Slide 19 — 输出 z 的卡诺图](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_19.png)

Slide 19 — 输出 z 的卡诺图

$$
z_{\text{忽略 don't care}} = \bar{y}_1\, y_2 \qquad\Longrightarrow\qquad z_{\text{利用 don't care}} = y_2
$$

![Slide 20 — 次态 Y₁ 的卡诺图](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_20.png)

Slide 20 — 次态 Y₁ 的卡诺图

$$
Y_1 = w\,\bar{y}_1\,\bar{y}_2
$$

（该项相邻格全是真实状态的 0，don't care 帮不上忙，化简前后一致。）

![Slide 21 — 次态 Y₂ 的卡诺图](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_21.png)

Slide 21 — 次态 Y₂ 的卡诺图

$$
Y_{2,\text{忽略}} = w\,y_1\,\bar{y}_2 + w\,\bar{y}_1\,y_2
\;\Longrightarrow\;
Y_{2,\text{利用 don't care}} = w\,y_1 + w\,y_2 = w\,(y_1 + y_2)
$$

<aside>
💡

**don't care 的价值：** $z$ 从 $\bar y_1 y_2$ 简化成 $y_2$、$Y_2$ 合并成 $w(y_1+y_2)$ —— 未用状态编码留出的 d 项就是化简的关键弹药。

</aside>

## 9️⃣ Step 2：用 D 触发器存状态（slide 22）

![Slide 22 — D 触发器](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_22.png)

Slide 22 — D 触发器

状态需要存储 → 用 **D 触发器**（每个存 1 bit）。正沿触发：上升沿时 $Q \leftarrow D$。

- $D=1$ → 上升沿 SET（$Q=1$）
- $D=0$ → 上升沿 RESET（$Q=0$）

把次态变量直接接到 D：$D_1 = Y_1,\ D_2 = Y_2$，触发器输出 $Q$ 就是现态 $y_1, y_2$。

## 🔟 Step 3：画出电路（slide 23）

![Slide 23 — 综合后的状态机电路](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_23.png)

Slide 23 — 综合后的状态机电路

整合三块：

$$
Y_1 = w\,\bar{y}_1\,\bar{y}_2,\qquad
Y_2 = w\,(y_1 + y_2),\qquad
z = y_2
$$

次态逻辑（与 / 或门）→ 两个 D-FF（state memory）→ 输出 $z=y_2$ 直接从 $y_2$ 引出；`Clock` / `Resetn` 接到两个触发器。

## 1️⃣1️⃣ 时序图验证（slide 24）

![Slide 24 — 时序波形](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_24.png)

Slide 24 — 时序波形

观察 $w$ 连续两拍为 1 时：$y_1, y_2$ 沿 A→B→C 演进，到达 C（$y_2=1$）时 $z$ 拉高，正好满足"连续两周期 $w=1$ → $z=1$"。

## 1️⃣2️⃣ 其他设计选择：换个状态编码（slides 25–26）

![Slide 25 — 不同状态编码对比](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_25.png)

Slide 25 — 不同状态编码对比

状态编码不唯一：

- 原方案：A: 00, B: 01, **C: 10**（"11" 未用）
- 备选方案：A: 00, B: 01, **C: 11**（"10" 未用）

![Slide 26 — 备选编码的表达式与电路](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_26.png)

Slide 26 — 备选编码的表达式与电路

备选编码（C: 11）推得：

$$
Y_1 = D_1 = w,\qquad Y_2 = D_2 = w\,y_1,\qquad z = y_2
$$

<aside>
⚖️

**重点 trade-off：** 同一个状态图，**不同状态编码 → 不同的逻辑表达式 / 电路复杂度**。这里 C:11 的方案比 C:10 更简单（$Y_1=w$）。状态编码是 FSM 综合里一个真实的优化自由度。

</aside>

## 1️⃣3️⃣ One-hot 编码（slides 27–29）

<aside>
🔥

**One-hot：** 状态变量个数 = 状态个数；每个状态只有**一个**变量为 1，其余全 0。

</aside>

![Slide 28 — One-hot 状态表](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_28.png)

Slide 28 — One-hot 状态表

3 个状态用 3 个变量 $y_3 y_2 y_1$：**A: 001，B: 010，C: 100**，其余组合都是 don't care。

![Slide 29 — One-hot 表达式](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/slide_29.png)

Slide 29 — One-hot 表达式

$$
Y_1 = \bar{w},\qquad Y_2 = w\,y_1,\qquad Y_3 = w\,\bar{y}_1,\qquad z = y_3
$$

- 本例 one-hot **电路并没有更简单**（多用了一个触发器）。
- 但 one-hot 在很多场景很有用：次态 / 输出逻辑常更浅更快（无需译码），时序更好、调试直观 —— 在 FPGA 上尤其常见。

---

## 📝 本节总结（记三点就够）

<aside>
🎯

1. **FSM = 时序电路 + 有限状态 + 转移规则**；输出只看状态 = **Moore**，还看输入 = **Mealy**。本节序列检测器是 Moore。
2. **手工综合五步：** 状态图 → 状态表 → 状态编码 → 用卡诺图求 $Y_i / z$（善用未用编码的 don't care）→ D 触发器 + 次态逻辑画电路，最后用时序图验证。
3. **状态编码是优化自由度：** binary 编码（C:10 vs C:11）影响逻辑复杂度；one-hot 用 #状态 个触发器换取更浅更快的组合逻辑。HDL 实现牢记"两段式"模板。
</aside>

## ✅ 作业 / 待办

- [ ]  复盘课程 Project：[EE115B Project — Subway Turnstile Controller](EE115B%20Project%20%E2%80%94%20Subway%20Turnstile%20Controller.md)，把 `IDLE/VALID/PASS/CLOSE/ALARM` 画成状态图再写两段式 HDL（截止 June 5, 2026 11:59 PM）。
- 本节未单独布置 Homework；拿到 syllabus 后补 Lab / HW deadline。

## 📎 原始 Slides

[FSM_part1.pdf](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7/FSM_part1.pdf)
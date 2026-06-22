# EE115B Lecture8 — VHDL Part 1：entity · architecture · process · testbench

<aside>
📘

**本节主题：** VHDL 入门 —— 用 `entity`（接口）+ `architecture`（实现）两大building block 描述硬件，一路到 `process`、`component` 与 testbench 仿真。

**讲义来源：** EE115B《VHDL》slides（Chenxi Xiao；素材含 © Pearson Education、Hengzhao Yang、Zhifeng Zhu、Yajun Ha）。

**核心脉络：** ① `entity` 定接口 + `architecture` 定功能 → ② 选信号类型（`std_logic`）→ ③ 并发 / 条件赋值（`<=`、`when else`、`with select`）→ ④ `component` 复用模块 → ⑤ `process` 写顺序 / 时序逻辑 → ⑥ testbench 仿真验证。

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md) ｜ 本节为 **Lecture8 Part 1**；同一讲 Part 2 = Verilog 见 [EE115B Lecture8 — Verilog HDL Part 2：module · 数据类型 · always · 仿真](EE115B%20Lecture8%20%E2%80%94%20Verilog%20HDL%20Part%202%EF%BC%9Amodule%20%C2%B7%20%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B.md)、Part 3 = FPGA 见 [EE115B Lecture8 — FPGA Part 3：概念与硬件电路](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF.md)、Part 4 = FSM 见 [EE115B Lecture8 — Finite State Machine Part 4：概念 · 编程 · 电路设计](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7.md)

</aside>

## 🧭 行政信息 & DDL

- [ ]  **Project — Subway Turnstile Controller** 截止 June 5, 2026 11:59 PM（可以用 VHDL 的两段式 `process` 实现这个 FSM）
- 在线仿真 / 资源（slides 62–64）：**EDA Playground**（[edaplayground.com](http://edaplayground.com)）、**GHDL**、ModelSim / Quartus II (Altera) / Vivado (Xilinx)；教程见 [web.cs.ucla.edu](http://web.cs.ucla.edu) 的 vhdlintro、[sustechvhdl.readthedocs.io](http://sustechvhdl.readthedocs.io)。

## 0️⃣ 课前 Review：组合逻辑器件（slides 1–12）

开头先回顾几类常用组合逻辑器件，作为后面"被 HDL 描述"的对象：

- **Decoder（译码器）：** 检测输入上的特定编码并用对应输出电平指示，如 2-4 / 3-8 / 4-16 译码器（$Y_i = m_i$，输出常为 active-LOW）。
- **Comparator（比较器）：** 判断相等或大小关系。
- **Multiplexer（MUX，数据选择器）/ Demultiplexer（DEMUX，数据分配器）。**

## 1️⃣ VHDL 是什么 & 与 Verilog 对比（slides 14–16）

**HDL（硬件描述语言）** 用来描述并仿真数字电路，最终综合到可编程器件上：

- **FPGA（Field Programmable Gate Array）：** 制造后仍可反复重配置的 IC，灵活、适合并行任务、性能高。
- **CPLD（复杂可编程逻辑器件）：** 相比 FPGA 配置存储非易失、资源更少、更便宜。

VHDL 与 Verilog 都是 HDL，区别主要在语法风格与类型系统：

| 维度 | VHDL | Verilog |
| --- | --- | --- |
| 语法风格 | 类 Ada，**冗长 / 啰嗦** | 类 C，**紧凑** |
| 类型系统 | **强类型**、检查严格 | 相对宽松 |
| 大小写 | **不敏感**（not case sensitive） | 敏感 |
| 本课顺序 | 先讲（Part 1） | 后讲（Part 2） |

## 2️⃣ 两大building block：`entity` + `architecture`（slides 17–21）

一段 VHDL 的最小骨架由两块组成：

- **`entity`（实体）** = 电路的**符号 / 接口**：定义模块名 + 端口（name / mode / type）。
- **`architecture`（结构体）** = 电路的**内部实现**：声明内部 signal + 写功能描述。

![Slides 18–19 — VHDL 程序结构（左 entity，右 architecture）](EE115B%20Lecture8%20%E2%80%94%20VHDL%20Part%201%EF%BC%9Aentity%20%C2%B7%20architectur/overview.png)

Slides 18–19 — VHDL 程序结构（左 entity，右 architecture）

```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;          -- 提供 std_logic 类型
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity circuit1 is                    -- 定义实体：接口
    Port ( a : in  STD_LOGIC;
           b : in  STD_LOGIC;
           c : in  STD_LOGIC;
           f : out STD_LOGIC);
end circuit1;

architecture behv1 of circuit1 is     -- 定义结构体：实现
    -- this is a comment line         (注释以 -- 开头)
    signal f1 : std_logic;            -- 内部信号
    signal f2 : std_logic;
begin
    f1 <= a and b;                    -- 并发赋值
    f2 <= c and not b;
    f  <= f1 or f2;
end behv1;
```

<aside>
⚡

**两个关键直觉：**

- **VHDL 是并发的：** `architecture` 里的这些赋值语句**没有先后**，写成任意顺序电路都一样（它们描述同时存在的硬件连线，不是顺序执行的代码）。
- **VHDL 大小写不敏感**，每条语句以 `;` 结尾，注释用 `--`。
</aside>

## 3️⃣ Entity：端口 mode 与 type（slides 22–27）

### 端口方向 mode

| mode | 含义 |
| --- | --- |
| `IN` | 端口值只能被**读** |
| `OUT` | 端口值只能被**更新（写）** |
| `INOUT` | 双向；可被实体外部驱动，用于多驱动场景（如三态 buffer） |
| `BUFFER` | 是输出，但实体内部也能读（可出现在 `<=` 两侧） |

### 端口 / 信号类型 type

| 类型 | 说明 | 来源 |
| --- | --- | --- |
| `bit` / `bit_vector` | `0` / `1` 及其向量（**不支持算术**） | VHDL 标准 |
| `boolean` | `TRUE` / `FALSE` | VHDL 标准 |
| `integer` | 整数，**支持算术运算** | VHDL 标准 |
| `std_logic` / `std_logic_vector` | 带信号值 + 强度的逻辑类型 | 需 IEEE `std_logic_1164` 包 |

<aside>
🔬

**`std_logic` 的取值（比 `bit` 更贴近真实电路）：** `'0'` 二进制 0、`'1'` 二进制 1、`'Z'` 高阻、`'U'` 未初始化、`'X'` 未知。所以做总线 / 三态 / 仿真时几乎都用 `std_logic`，而不是只有 0/1 的 `bit`。

</aside>

向量下标方向看声明：`std_logic_vector(1 to 4)` 是升序，`std_logic_vector(3 downto 0)` 是降序（`b(0)` 为 LSB）。

## 4️⃣ Architecture：`signal` 与赋值语句（slides 28–36）

- 一个 `entity` 可以有**多个** `architecture`（行为级 Behavioral / RTL / 门级 Gate level），但同一时刻只有一个被激活。
- **`signal`** 是基本对象，代表硬件元件之间的**连线（wire）**：`signal <名字> : <类型>;`。

### 直接赋值（并发）

`<target> <= <expression>;` —— target 可以是内部 signal 或输出端口；该赋值是**并发**的。

### 条件赋值

```vhdl
-- when / else（按条件，类似优先级链）
f <= "00" when s = "00" else
     "01" when s = "01" else
     "10";

-- with / select（按选择子，类似查表）
with s select
    f <= a when "00",
         b when "01",
         c when others;     -- others 兜底，防止漏分支
```

<aside>
🧭

**when else vs with select：** 两者都用来"多选一"。`when else` 像优先级链（从上往下第一个为真者生效）；`with select` 像查表（对一个选择子穷举，务必用 `when others` 收尾）。slide 36 的 2-to-1 MUX 就是典型例子。

</aside>

## 5️⃣ 运算符与优先级（slide 37）

| 优先级 | 类别 | 运算符 |
| --- | --- | --- |
| 最高 ↑ | Miscellaneous | 取反 / 绝对值 / 幂 `NOT` `abs` `**` |
|  | Multiplying | 乘除模 `*` `/` `mod` `rem` |
|  | Sign | 正负号 `+` `-` |
|  | Adding | 加减与拼接 `+` `-` `&` |
|  | Shift | 移位 `sll` `srl` `sla` `sra` `rol` `ror` |
| ↓ 最低 | Relational | 关系 `=` `/=` `<` `<=` `>` `>=` |
|  | Logical | 逻辑 `AND` `OR` `NAND` `NOR` `XOR` `XNOR` |

注意：`<=` 既是信号赋值符，也是关系运算符"小于等于"，靠上下文区分；不等号写作 `/=`。

## 6️⃣ Component：复用已有模块（slides 38–41）

一个文件里定义好的 `entity`，可以在另一个文件里当**组件 component** 复用。三步走：

1. **设计**好子模块（如 1-bit 全加器 `fulladd`）。
2. 在 `architecture` 声明区 **declare** 这个 component。
3. 在 `architecture` body 里 **instantiate**（实例化）。

端口映射两种写法：**位置关联**（按端口顺序）与**名字关联**（`端口 => 信号`，更安全、可读）。

![Slide 41 — 4-bit 加法器：component 声明 + 位置 / 名字关联实例化](EE115B%20Lecture8%20%E2%80%94%20VHDL%20Part%201%EF%BC%9Aentity%20%C2%B7%20architectur/component.png)

Slide 41 — 4-bit 加法器：component 声明 + 位置 / 名字关联实例化

```vhdl
-- 名字关联（推荐）
stage3 : fulladd PORT MAP (
    Cin => c3, Cout => Cout,
    x => x3, y => y3, s => s3 );
```

## 7️⃣ `PROCESS`：在并发框架里写"顺序"逻辑（slides 42–49）

前面的并发赋值像硬件一样同时发生；但**寄存器 / 计数器 / 状态机**这种"随时钟一步步更新"的行为，用并发赋值很难表达 —— 这就要用 `process`。

- **多个 `process` 之间是并发的**；**`process` 内部的语句是顺序执行的**。
- **敏感列表 sensitivity list：** `process (a, b)` —— 列表里任一信号变化，整个 process 就被触发并从头顺序执行一遍。

```vhdl
process (a, b, c)         -- 敏感列表
begin
    if c = '1' then
        y <= a;
    else
        y <= b;
    end if;
end process;
```

<aside>
🪤

**敏感列表要写全：** 组合逻辑若漏掉某个输入信号，仿真行为会与真实硬件不一致（甚至综合出意外锁存器）。另一种触发方式是 `wait` 语句（见下表）；一个 process **不能同时**既有敏感列表又有 `wait`。

</aside>

| 写法 | 可综合？ |
| --- | --- |
| `wait until rising_edge(clk)` | ✅ 可以 |
| `wait for 10 ns` | ❌ 不可（仅仿真） |
| `wait on a, b, c` | ⚠️ 取决于工具 |

<aside>
📦

**signal vs variable：** `process` 内还能声明 **variable**（用 `:=` 立即赋值、顺序生效），而 signal 赋值带延迟语义。变量虽好理解，但课件提示**不推荐**滥用 —— 硬件映射不直观，能用 signal 就用 signal。

</aside>

## 8️⃣ `PROCESS` 内的语句：IF / CASE / LOOP（slides 50–58）

`IF` / `CASE` / `WAIT` / `LOOP` **只能出现在 `process` 内部**。

```vhdl
-- IF：4-to-1 MUX
process (w0, w1, w2, w3, s)
begin
    if    s = "00" then f <= w0;
    elsif s = "01" then f <= w1;     -- 注意是 elsif（没有第二个 e）
    elsif s = "10" then f <= w2;
    else                f <= w3;
    end if;
end process;

-- 时钟边沿（只能在 process 内）
process (clk)
begin
    if rising_edge(clk) then         -- 上升沿；下降沿用 falling_edge(clk)
        q <= d;
    end if;
end process;

-- CASE：用 when others 兜底
case sel is
    when "00"   => f <= w0;
    when "01"   => f <= w1;
    when others => f <= w2;
end case;
```

- **FOR LOOP：** 在 `process` 内重复若干次；**范围在编译期确定**时可综合（如按位算 parity）。
- **WHILE LOOP：** 按条件循环；若迭代次数编译期不可定，**通常不可综合**。

<aside>
⏱

**记牢时钟写法：** 时序逻辑统一用 `if rising_edge(clk) then ... end if;`（或 `falling_edge`），且只能写在 `process` 里。`elsif` 拼写没有第二个 e —— 这是高频笔误。

</aside>

## 9️⃣ Testbench：仿真验证（slides 59–61）

Testbench 是**不可综合**的 VHDL：负责生成输入激励、并检查输出是否正确。

```vhdl
reset <= '1', '0' after 1 us;     -- 1us 后从 1 变 0
clock <= not clock after 10 ns;   -- 自激时钟，每 10ns 翻转

wait for 10 ns;                   -- 等一段时间
wait until (reset = '0');         -- 等到条件成立
wait on sig_a, sig_b;             -- 等某些信号变化
wait;                             -- 永远等待（停住）

-- 断言：条件为假就报告
assert (q_out = '0')
    report "Fail 0/0" severity error;   -- severity: note/warning/error/failure
```

- `report "<信息>" [severity <级别>];`：级别有 `note` / `warning` / `error` / `failure`；`'image` 属性可把 integer 转成字符串拼进信息里。

<aside>
🧪

**Direct entity instantiation：** testbench 里实例化被测设计时，推荐直接用 `entity work.example_design(rtl)` 这种"直接实体实例化"，而非老式 `component` 风格（`component` 仍可用，但课件标注为 outdated）。

</aside>

## 🎯 本节总结

<aside>
🧠

1. **`entity` = 接口（电路符号），`architecture` = 实现（电路图）；默认所有语句并发，VHDL 大小写不敏感。**
2. **信号类型优先 `std_logic` / `std_logic_vector`（需 IEEE 库，含 `0/1/Z/U/X`）；并发赋值用 `<=`，多选一用 `when else` 或 `with select`（记得 `when others`）。**
3. **顺序 / 时序逻辑必须写进 `process`：敏感列表 + `rising_edge(clk)`；testbench 不可综合，用激励 + `assert` / `report` 验证。**
</aside>

## ✅ 作业 / 待办

- [ ]  用 VHDL 的两段式 `process` 实现 Project 的 turnstile **FSM**（DDL June 5, 2026 11:59 PM）
- [ ]  在 **EDA Playground** 上跑通一个 `entity` + `architecture` + testbench 的小例子（如 2-to-1 MUX）巩固

## 📎 原始 Slides

[VHDL.pdf](EE115B%20Lecture8%20%E2%80%94%20VHDL%20Part%201%EF%BC%9Aentity%20%C2%B7%20architectur/VHDL.pdf)
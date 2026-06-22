# EE115B Lecture8 — Verilog HDL Part 2：module · 数据类型 · always · 仿真

<aside>
💻

**本节主题：** Verilog HDL 入门 —— 从 `module` 结构、数据类型（`wire` / `reg`）、`assign` 与 `always`，到 testbench 与仿真指令的完整链路。

**讲义来源：** EE115B《Verilog》slides（Chenxi Xiao；素材含 © Pearson Education、Nandland、HDLBits）。

**核心脉络：** ① 用 `module` 描述硬件 → ② 选对数据类型（`wire` vs `reg`）→ ③ 用 `assign` / `always` 写组合与时序逻辑 → ④ 写 testbench + 仿真指令验证波形。

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md) ｜ 本节为 **Lecture8 Part 2**；同一讲 Part 1 = VHDL 见 [EE115B Lecture8 — VHDL Part 1：entity · architecture · process · testbench](EE115B%20Lecture8%20%E2%80%94%20VHDL%20Part%201%EF%BC%9Aentity%20%C2%B7%20architectur.md)、Part 3 = FPGA 见 [EE115B Lecture8 — FPGA Part 3：概念与硬件电路](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF.md)、Part 4 = FSM 见 [EE115B Lecture8 — Finite State Machine Part 4：概念 · 编程 · 电路设计](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7.md)

</aside>

## 🧭 行政信息 & DDL

- [ ]  **Project — Subway Turnstile Controller** 截止 June 5, 2026 11:59 PM（要用 Verilog 实现一个 FSM，正好用上本节全部内容）
- 自学资源（slide 41）：**HDLBits** 在线练习、`asic-world` 的 *Verilog in One Day*、*Verilog HDL Basics*。

## 1️⃣ 什么是 Verilog & `module` 概念

Verilog 是一种 **HDL（hardware description language）**，比 VHDL 年轻，相较 VHDL 的改进：语法更简单、更易用、工具链（IDE / 仿真器）体验更好。

几条铁律：

- **case sensitive**（大小写敏感）。
- 每条语句以 `;` 结尾。
- 注释：单行 `//`，块注释 `/* ... */`。

Verilog 里硬件的基本单位叫 **module**，一个 module 通常包含：端口声明、内部变量、行为描述、以及对其他 module 的实例化。

```verilog
module module_name (list_of_ports);
    // input / output 声明
    // local net 声明      (wire)
    // local variable 声明 (reg)
    // 连续赋值            (assign ...)
    // 过程块              (always / initial)
    // 实例化其它 module
endmodule
```

下面这页把一个完整 module 的各个部分都标注了出来（端口、内部变量、assign、always、实例化、输出回连）：

![Slide 4 — 一个完整 Verilog 程序的结构注解](EE115B%20Lecture8%20%E2%80%94%20Verilog%20HDL%20Part%202%EF%BC%9Amodule%20%C2%B7%20%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B/slide_04.png)

Slide 4 — 一个完整 Verilog 程序的结构注解

<aside>
📝

**Verilog-2001 ANSI 风格：** 从 Verilog-2001 起，端口方向 + 类型可以直接写在 port list 里，不必在 module body 内再声明一遍。

</aside>

## 2️⃣ 端口（ports）与数据类型

### 端口类型

- `input` —— 类型只能是 `wire`。
- `output` —— 类型可以是 `wire` 或 `reg`。
- `inout` —— 类型只能是 `wire`。

```verilog
// 旧风格 (Verilog-1995)：端口要声明两次
module simpleand (f, x, y);
    input  x, y;
    output f;
    assign f = x & y;        // Simple AND gate
endmodule

// 新风格 (Verilog-2001, ANSI)：方向 + 类型写进 port list
module simpleand (input x, y, output f);
    assign f = x & y;
endmodule
```

### 两类数据类型：`wire` vs `reg`

| 类型 | 特性 | 典型用途 | 声明关键字 |
| --- | --- | --- | --- |
| **Wire（线网）** | 必须被**持续驱动**，自己不存值 | 连续赋值、module 之间的连线 | `wire` |
| **Register（寄存器型）** | **保留**最后一次赋的值 | 过程块里赋值的变量、存储元件 | `reg` / `integer` |

```verilog
wire  a, b;        // 单 bit wire
reg   x, y;        // 单 bit reg
reg [15:0] bus;    // 16-bit 总线，bus[15] 为 MSB
integer count;     // integer 默认 32-bit
```

<aside>
⚠️

**最大陷阱：`reg` 不等于真实寄存器。** 综合时，`reg` 到底映射成 *wire（组合逻辑）* 还是 *storage cell（存储单元）*，取决于它在什么上下文里被赋值。在组合 `always @(*)` 里赋值的 `reg`，综合后其实是 wire，并不会生成触发器。`reg` 与 `integer` 都支持算术运算。

</aside>

## 3️⃣ 常量、`parameter`、`localparam` 与 define 宏

### 常量取值与初始值

| 值 | 含义 |
| --- | --- |
| `0` | logic-0 / FALSE |
| `1` | logic-1 / TRUE |
| `x` | unknown / don't care（不关心） |
| `z` | high impedance（高阻） |

初始值约定：所有 **net（wire）默认 `z`**，所有 **register 变量默认 `x`**。硬件里初值是真实的 0/1，但会随硬件状态变化。

常量写法 `<size>'<base><number>`：

```verilog
8'b01110011   // 8-bit 二进制
12'hA2D       // 12-bit 十六进制
12'hC5        // 12-bit 十六进制
25            // 有符号，默认 32-bit
1'b0          // logic 0
1'b1          // logic 1
```

### 三种「常量 / 宏」对比

```verilog
// parameter：可定制常量，实例化时可被 override
module counter #(parameter WIDTH = 4) (...);
    ...
endmodule
counter #(.WIDTH(8)) my_counter (...);   // 覆盖默认值

// localparam：module 内部常量，不可被 override
localparam MAX_COUNT = TIMEOUT - 1;

// `define：预处理宏（类似 C/C++ 的 #define），全局共享、跨文件
`define DATA_WIDTH 8
module register (input [`DATA_WIDTH-1:0] d, output [`DATA_WIDTH-1:0] q);
    assign q = d;
endmodule
```

<aside>
🔑

**选用口诀：** 想让外部使用者定制 → parameter；只在本 module 内用、不准被改 → localparam；想跨文件 / 跨 module 全局生效 → define 宏。

</aside>

## 4️⃣ `assign`：连续赋值（组合逻辑）

- `assign` 用于**连续赋值**，通常描述组合逻辑。
- `assign` 左侧**只能是 `wire`** 类型。

```verilog
assign a = b >> 1;            // 移位
assign f = {a, b};            // 拼接 (concatenation)
assign f = {x[2], y[0], a};   // 位选 + 拼接
assign f = {4{a}};            // 复制 4 次 (replication)
assign f = {2'b10, 3{2'b01}, x};
assign out = sel ? a : b;     // 条件赋值 = 一个 2-to-1 MUX
```

## 5️⃣ 运算符（operators）

| 类别 | 运算符 |
| --- | --- |
| Arithmetic 算术 |   `•  -  *  /  %` |
| Logical 逻辑 | `!`  `&&`  `||` |
| Relational 关系 | `>  <  >=  <=  ==  !=` |
| Bitwise 位 | `~`  `&`  `|`  `^`  `~^` |
| Shift 移位 | `>>  <<` |
| Concatenation / Replication | `{}`  /  `{n{}}` |
| Conditional 条件 | `? :` |

<aside>
⚠️

**几个坑：**

- 算术表达式里只要出现 `x` 或 `z`，整个结果就变成未知 `x`。
- 逻辑运算符和关系运算符的结果都是 **1-bit**。
- Boolean：`false` = `1'b0`，`true` = `1'b1`。
- 优先级容易记错 —— **多打括号**强制优先级最稳。
</aside>

## 6️⃣ 过程块：`always` / `initial`

过程块（procedural block）定义一段**顺序执行**的语句区域，语句按书写顺序执行。Verilog 有两类：

- **`always`**：永不终止的连续循环（描述真实硬件）。
- **`initial`**：仿真开始时只执行一次（多用于 testbench）。

### 敏感列表（sensitivity list）

```verilog
// ① Clocked / 边沿触发
always @(posedge clk or posedge rst) begin
    if (rst) q <= 0;
    else     q <= d;
end

// ② 组合逻辑：@(*) 自动推断敏感信号
always @(*) begin
    out = a & b;
end

// ③ 电平敏感（不完整会综合出 latch）
always @(enable or d) begin
    if (enable) q = d;   // 没有 else → 推断出锁存器
end
```

<aside>
🪤

**Latch 陷阱：** 电平敏感的 `always` 如果分支不完整（缺 `else`、或 `case` 缺 `default`），综合工具会替你补一个 **latch**。组合逻辑务必写全所有分支。`@(*)` 会自动把块内用到的所有变量纳入敏感列表，省心又防漏。

</aside>

### 阻塞 `=` vs 非阻塞 `<=`

```verilog
// 阻塞 '='：顺序生效，立刻更新
always @(posedge clk) begin
    r_Test_1 = r_Test_2;
    r_Test_2 = r_Test_3;
    r_Test_3 = 1'b1;     // 1'b1 只需 1 个时钟就到 r_Test_3
end

// 非阻塞 '<='：先采样所有右值，再一起赋值
always @(posedge clk) begin
    r_Test_1 <= r_Test_2;
    r_Test_2 <= r_Test_3;
    r_Test_3 <= 1'b1;    // 1'b1 需 3 个时钟才移到 r_Test_3（移位寄存器）
end
```

| 维度 | 阻塞 `=` | 非阻塞 `<=` |
| --- | --- | --- |
| 行为 | 立即生效，影响后续语句 | 右值整体采样后并行赋值 |
| 适用 | **组合逻辑** `always @(*)` | **时序逻辑** `always @(posedge clk)` |
| 上例结果 | 1 拍到位 | 3 拍移位 |

<aside>
🚦

**铁律：** 同一个 `always` 块里**不要混用** `=` 和 `<=`，否则行为不可预测。组合用 `=`，时序用 `<=`。

</aside>

### `begin ... end` 与分支语句

`begin ... end` 用来把多条语句组合在一起，相当于 C/C++/Java 的 `{}`。

```verilog
// if / else if / else（组合逻辑示例）
always @(*) begin
    if      (sel == 2'b00) y = a;
    else if (sel == 2'b01) y = b;
    else                   y = c;
end

// case：ALU 示例
always @(*) begin
    case (op)
        ADD: f = a + b;
        SUB: f = a - b;
        MUL: f = a * b;
        DIV: f = a / b;
        default: f = 0;   // 防 latch
    endcase
end
```

## 7️⃣ 实例化其他 module（instantiation）

实例化让你把已定义好的 module 当作组件用在另一个 module 里：先**定义** module（step 1），再在别处**实例化**（step 2）。

端口映射两种方式：

- **位置关联**（positional）：按端口顺序传。
- **名字关联**（named）：`.port_name(signal_name)`，更安全、可读性更好。

```verilog
// 名字关联（推荐）
adder adder_instance (
    .a   (x),
    .b   (y),
    .sum (s)
);
```

## 8️⃣ Testbench 与仿真指令

**Testbench** 是一段只执行一次的 Verilog（`initial`），用来生成 clock、reset 和测试向量，驱动被测模块（DUT）。

```verilog
module shifter_toplevel;
    reg  clk, clear, shift;
    wire [7:0] data;

    shift_register S1 (clk, clear, shift, data);  // 实例化 DUT

    initial begin
        clear = 0; shift = 0;
    end
    always #10 clk = ~clk;   // 时钟发生器：每 10 个时间单位翻转
endmodule
```

### `timescale` 与仿真指令

```verilog
`timescale 1ns / 1ps   // 时间单位 / 时间精度
//  time unit  = 1ns -> 像 #1 这种延时的基准单位
//  precision  = 1ps -> 仿真能分辨的最小时间

initial begin
    // $display：在执行到该行的那一刻打印一次
    $display("At time %t, sig1=%b, sig2=%d", $time, sig1, sig2);
    // $monitor：任一被监视信号变化时就打印
    $monitor("Time=%0t clk=%b count=%d", $time, clk, count);
    // 记录波形到 VCD，供 GTKWave 等查看
    $dumpfile("waveform.vcd");
    $dumpvars(0, testbench);   // level 0 = 该 scope 下全部信号
    #100 $finish;              // 结束仿真
end
```

格式符：`%t` 当前仿真时间（常配 `$time`）、`%b` 二进制、`%d` 十进制。`$monitor` 可用 `$monitoroff` 暂停。`$dumpvars(level, scope)`：`level=0` 当前 module 及所有子模块全 dump，`1/2/.../n` 控制向下递归的层数。

<aside>
🧪

**Assert & SystemVerilog：** 标准 Verilog **不支持** `assert`。SystemVerilog 作为 Verilog 的扩展，提供断言 / 随机激励等验证特性：`assert (expression) else $fatal("Assertion failed!");`

</aside>

## 🎯 本节总结

<aside>
🧠

1. **连线 `wire`、存值 `reg`；但 `reg` 在组合 `always` 里只是综合成 wire，不等于触发器。**
2. **组合逻辑用 `@(*)` + 阻塞 `=`；时序逻辑用 `@(posedge clk)` + 非阻塞 `<=`；永不在同一块里混用。**
3. **分支写全（`else` / `default`）防 latch；仿真三件套：testbench 喂激励 → `$monitor` 看变化 → `$dumpvars` 存 VCD 用 GTKWave 看波形。**
</aside>

## ✅ 作业 / 待办

- [ ]  用 Verilog 实现 Project 的 turnstile **FSM**（DDL June 5, 2026 11:59 PM）
- [ ]  上 **HDLBits** 刷 `always` / `case` / 移位寄存器相关题巩固

## 📎 原始 Slides

[Verilog.pdf](EE115B%20Lecture8%20%E2%80%94%20Verilog%20HDL%20Part%202%EF%BC%9Amodule%20%C2%B7%20%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B/Verilog.pdf)
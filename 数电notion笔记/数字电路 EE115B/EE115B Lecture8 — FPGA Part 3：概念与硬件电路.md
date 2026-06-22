# EE115B Lecture8 — FPGA Part 3：概念与硬件电路

<aside>
🧩

**本节主题：** Field Programmable Gate Array（FPGA，现场可编程门阵列）—— Part 1 概念 + Part 2 硬件电路。

**⚠️ 考试提示（slides 原文）：** Part 1 大部分内容**不进考试**，仅保留最基础的概念；**Part 2 硬件电路整节不考**。本节偏"拓展视野"。

**参考：** Pearson Education + 任课补充；入门可读 GeekPie [FPGA tutorial](https://shanghaitechgeekpie.github.io/FPGA-tutorial/index.html) 与 [VTR docs](https://docs.verilogtorouting.org/en/latest/quickstart/)。

**核心脉络：** FPGA 是什么 → 内部资源（LUT/FF/LE · 可编程互连 · BRAM/URAM · DSP · MMCM/PLL · IOB）→ 开发流程（RTL → 仿真 → 综合 → 实现 → 时序 → bitstream → 下载）→ 开发方法（RTL/HLS/IP/第三方/AI）→ 板级硬件设计（电源 · IO bank · 配置启动 · 时钟 · 调试 · 模拟 · 外部 RAM · PCB）。

**所属课程：** [数字电路 EE115B](../%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF%20EE115B.md) ｜ 本节为 **Lecture8 Part 3**；同一讲 Part 1 = VHDL 见 [EE115B Lecture8 — VHDL Part 1：entity · architecture · process · testbench](EE115B%20Lecture8%20%E2%80%94%20VHDL%20Part%201%EF%BC%9Aentity%20%C2%B7%20architectur.md)、Part 2 = Verilog 见 [EE115B Lecture8 — Verilog HDL Part 2：module · 数据类型 · always · 仿真](EE115B%20Lecture8%20%E2%80%94%20Verilog%20HDL%20Part%202%EF%BC%9Amodule%20%C2%B7%20%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B.md)、Part 4 = FSM 见 [EE115B Lecture8 — Finite State Machine Part 4：概念 · 编程 · 电路设计](EE115B%20Lecture8%20%E2%80%94%20Finite%20State%20Machine%20Part%204%EF%BC%9A%E6%A6%82%E5%BF%B5%20%C2%B7.md)

</aside>

## 🗂 课程行政信息

- 📣 **课程评教**（slide 1）：老师在最后一节提醒完成评教 → [评教系统](https://evaluation.shanghaitech.edu.cn)（无明确截止日期，未建日历提醒）。
- [ ]  **Project — Subway Turnstile Controller** 提交：June 5, 2026 11:59 PM（详见 [EE115B Project — Subway Turnstile Controller](EE115B%20Project%20%E2%80%94%20Subway%20Turnstile%20Controller.md)）

---

# Part 1 — 概念（Concepts）

## 1️⃣ 什么是 FPGA（slide 4）

![Slide 4 — FPGA 内部结构示意](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF/slide_04.png)

Slide 4 — FPGA 内部结构示意

- **历史：** 1985 年由 **Xilinx** 首次提出。
- **三大构成要素：**
    - **逻辑块阵列（arrays of logic blocks）：** 实现任意逻辑函数。
    - **可编程布线（routing channels）：** 海量可配置连线，把逻辑块连起来。
    - **灵活 I/O：** 可配置的接口逻辑，连接芯片内部与外部世界。

<aside>
⚖️

**FPGA 的本质 trade-off：** 用"可重构的查找表 + 可编程互连"换取**灵活性 / 快速迭代**，代价是相对 ASIC 更高的功耗、面积与单位成本。适合小批量、需频繁改设计、或需要硬件并行加速的场景。

</aside>

## 2️⃣ AMD Xilinx 产品线与资源（slides 5–6）

按定位从高到低：

| 系列 | 定位 |
| --- | --- |
| **Zynq** | FPGA + ARM CPU SoC，主打灵活性 |
| **Virtex** | 高性能、最高逻辑密度，旗舰 |
| **Kintex** | 中高性能，性价比最佳 |
| **Artix** | 中等性能，低功耗 / 低成本 |
| **Spartan** | 低性能，最低成本 |
| **Versal** | ACAP（ARM + PL + AI Engine），AI 加速 |
- **工艺：** 45nm / 28nm / 16nm / 7nm…… 直接影响集成密度、功耗与频率。
- **片上资源：** Logic Elements（高端 >500K）、BRAM / URAM、DSP slices、高速接口（PCIe / GbE transceiver）、时钟（PLL / MMCM）、硬核 CPU（Zynq 内的 ARM）。

## 3️⃣ 核心资源（slides 7–14）

### 3.1 Logic Element：LUT + FF（slide 7）

![Slide 7 — Logic Element（LUT + FF）](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF/slide_07.png)

Slide 7 — Logic Element（LUT + FF）

- 一个 **LE = 4-input LUT 后接一个 D 触发器**（较新的 Xilinx 系列改用 6-input LUT）。
- FF 可选旁路：纯组合输出走 LUT，时序输出经 FF 寄存。
- 4-LUT 能实现任意 4 变量布尔函数；多个 LE 级联可拼出更复杂逻辑（如行波进位加法器）。

### 3.2 LUT 的工作原理（slide 8）

![Slide 8 — 4-input LUT 结构](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF/slide_08.png)

Slide 8 — 4-input LUT 结构

- **LUT 本质 = 一串 SRAM 配置位 + 多路选择器树**：输入信号当作 mux 的选择线，从配置位里选出对应输出。
- "编程 FPGA" ≠ 编程 CPU/微处理器：实际是下载 **bitstream（配置流）**，用它填充每个 LUT 的真值表内容。
- 例：4-LUT 有 16 个配置寄存位，`ABCD=0000` 时把第 1 个寄存位 R 路由到输出 Y。

<aside>
🔑

**记忆点：** LUT = 可写真值表的硬件。给定 N 输入 → $2^N$ 个配置位即可实现任意 N 变量逻辑。这正是 FPGA "可编程" 的物理根源。

</aside>

### 3.3 可编程互连（slide 9）

- **switch matrix + routing channels** 把 CLB / BRAM / DSP 连起来。
- **布线延迟问题：** 现代 FPGA 里，**连线延迟常常比门延迟还大**！
- 这是 **timing closure（时序收敛）** 的关键 → 可通过写高效代码、或加 P&R 物理约束把相关逻辑摆近来优化。
- **全局时钟线（global clock line）：** 树状结构，保证全芯片高精度时钟对齐。

### 3.4 片上存储：RAM Blocks（slide 10）

| 类型 | 构成 | 用途 |
| --- | --- | --- |
| **Distributed RAM** | 用 CLB 里的 LUT 拼成的小存储 | 极小 FIFO / 移位寄存器 |
| **Block RAM (BRAM)** | 硅片内嵌的 18 / 36 Kb 专用 SRAM | 数据缓冲、大查找表、图像行缓冲；支持单口 / 双口 / FIFO |
| **UltraRAM (URAM)** | 新 / 大型号才有，288 Kb 大块 | 海量存储，替代外部 SRAM 芯片 |
- ❓ Q&A：BRAM / SRAM / DRAM / Distributed RAM / URAM 到底是什么？
    
    **关键：先分清「物理存储单元」与「系统角色」。** 片上的 Distributed RAM / BRAM / URAM 全是 **SRAM**；只有外挂 DDR 才是 **DRAM**。
    
    **① 两种底层 memory cell**
    
    - **SRAM（Static RAM）**：1 bit = **6 晶体管（6T）**，交叉耦合反相器组成双稳态锁存器。通电即保持、**无需刷新**；快、密度低、贵。→ 用于 cache、FPGA 片上存储、LUT 配置位。
    - **DRAM（Dynamic RAM）**：1 bit = **1 管 + 1 电容（1T1C）**，靠电容电荷存 0/1。电容漏电 → 必须周期 **refresh**；密度高、便宜、慢。→ 用于内存条、FPGA 外挂 DDR。
    - 口诀：**SRAM 快但贵（片上）；DRAM 慢但量大便宜（片外）**。
    
    **② FPGA 片上三种（同为 SRAM，按颗粒度分级）**
    
    - **Distributed RAM（LUT RAM）**：借用 LUT 内部 SRAM 当微存储；几十~几百 bit，离逻辑近、最快，但**占逻辑资源**。用于微型 FIFO / 移位寄存器。
    - **BRAM（Block RAM）**：硅片专用硬核 SRAM 块，**18/36 Kb 每块**，不占 LUT。可配 single-port / **true dual-port** / FIFO / ROM，位宽深度可调。用于缓冲、图像 line buffer、跨时钟域 FIFO。
    - **URAM（UltraRAM）**：UltraScale+ 才有的大块 SRAM，**288 Kb 每块**，可纵向级联成片上几十 Mb，替代部分外部 SRAM。
    
    **③ 为什么片上不用 DRAM？** DRAM 电容需特殊工艺，与 FPGA 标准 CMOS 逻辑工艺不兼容；SRAM 用普通逻辑工艺即可，更快且免刷新。所以**片上全 SRAM，海量数据才外挂 DDR（DRAM）**。
    
    **④ 对比**
    
    | 名字 | 底层单元 | 位置 | 容量量级 | 典型用途 |
    | --- | --- | --- | --- | --- |
    | Distributed RAM | SRAM（借 LUT） | 片上 · 占逻辑 | 几十~几百 bit | 微型 FIFO / 移位寄存器 |
    | BRAM | SRAM（专用块） | 片上 · 独立 | 18/36 Kb/块 | 缓冲 / line buffer / 双口 FIFO |
    | URAM | SRAM（专用大块） | 片上 · 独立 | 288 Kb/块 | 大容量片上存储 |
    | DDR（外部 RAM） | **DRAM** | 片外芯片 | GB 级 | 主存 / 海量数据 |
- ❓ Q&A：FIFO 在这里是什么意思？
    
    **FIFO = First In First Out（先进先出）**：最先写进去的数据最先被读出，就像排队。相对的是 LIFO（后进先出 = 栈 stack）。
    
    **在这里（BRAM 语境）的含义：** “支持单口 / 双口 / FIFO”指 **BRAM 这块专用 SRAM 可被配置成一个硬件 FIFO 队列**。其内部 = 一块 BRAM + **写指针（write pointer）** + **读指针（read pointer）**；写一个写指针 +1，读一个读指针 +1，到底绕回（环形缓冲 circular buffer）；自带 **full / empty** 状态标志。
    
    **两大用途：**
    
    1. **缓冲 / 速率匹配：** 生产方与消费方速度不一致时，用 FIFO 当“蓄水池”缓存突发数据，避免丢包。
    2. **跨时钟域（CDC）：** 最重要的用法——**异步 FIFO（async FIFO）**。写端用时钟 A、读端用时钟 B，两个时钟频率/相位无关，通过格雷码指针（Gray-code pointer）安全跨时钟域传数据，避免亚稳态（metastability）。
    
    **一句话：** FIFO 不是一种存储介质，而是**把 BRAM 这块 SRAM 当成“先进先出的硬件队列”来用的工作模式**，主力场景是缓冲与跨时钟域。
    
- ❓ Q&A：ROM 是什么？和 RAM 有什么区别？
    
    **名字会骗人：** RAM（Random Access Memory）字面是“随机等速访问”，ROM（Read-Only Memory）字面是“只读”。但 ROM 其实也是随机存取的，所以“随机访问”不是真正区别。口语里的 RAM vs ROM 真正说的是下面两个维度：
    
    **① 可写性：** RAM 可读可写（运行时随便改）；ROM 运行时只读（内容基本固定）。
    
    **② 易失性（核心）：** RAM **易失 volatile**，一断电数据全没（SRAM/DRAM）；ROM **非易失 non-volatile**，断电内容还在。
    
    **口诀：** RAM = 可读写 + 断电丢（当草稿纸）；ROM = 只读 + 断电留（当出厂说明书）。**易失性才是本质区别**。
    
    **ROM 的几代（从死板到可改写）：** Mask ROM（出厂焊死）→ PROM（烧一次）→ EPROM（紫外擦除）→ EEPROM（电擦写）→ **Flash**（按块电擦写，U 盘/SSD/FPGA 配置芯片都是它）。到 Flash 这代 ROM 早就能写了，所以现在区分主要看易失性。
    
    **⭐ 回到 FPGA（反直觉点）：** 把 BRAM “配成 ROM”，它**物理上仍是 SRAM（易失）**！做法是：你给 BRAM 一份**初始内容**（正弦表/滤波系数/字符点阵）→ 被打进 **bitstream** → 上电配置那一刻写进 BRAM → 运行期逻辑只读不写，逻辑上就像 ROM。但一断电内容就没，下次靠重新加载 bitstream 恢复。
    
    **那 FPGA 真正断电不丢的非易失存储在哪？** 在**板外的配置 Flash 芯片**里，它存 bitstream，每次上电把整个 FPGA（含这些“ROM”内容）重新灌一遍。
    
    **一句话：** 在 FPGA 里，“ROM” 是一种**用法**（只读 + 上电初始化）而非物理介质；物理介质还是易失的 SRAM，真正的非易失 ROM 是片外那颗存 bitstream 的 Flash。
    

### 3.5 DSP Slices（slide 11）

- 用 LUT 搭 48-bit 乘法器既费资源又慢 → **DSP slice 一个时钟周期搞定**。
- 功能：高速乘累加（MAC），用于滤波器、FFT、矩阵运算。
- 例：DSP48E1 一周期完成 $(A \times B) + C$，累加器位宽 48-bit。

### 3.6 时钟管理：PLL 与 MMCM（slide 12）

|  | PLL（锁相环） | MMCM |
| --- | --- | --- |
| 定位 | 较简单的时钟生成 | Xilinx 增强版 PLL |
| 能力 | 倍频（如 50MHz → 200MHz） | 抖动滤除、相位偏移（如移 90° 对齐 DDR）、deskew、安全跨时钟域 CDC |

### 3.7 IOB：输入输出块（slides 13–14）

![Slide 14 — IOB / I-O Tile 结构](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF/slide_14.png)

Slide 14 — IOB / I-O Tile 结构

- IOB 是 FPGA 内部逻辑（CLB）与物理引脚之间的**可编程接口**。
- 关键部件：
    - **IBUF / OBUF：** 可配置支持不同电平标准（LVCMOS33、LVDS…）。
    - **OBUFT（三态控制）：** 让引脚可双向（如 I2C 线）。
    - **IDDR / ODDR：** 紧贴物理引脚的专用 FF，保证快速可预测的 Clock-to-Out 与 setup/hold。
    - **可编程上 / 下拉电阻。**

## 4️⃣ 开发流程（slides 15–16）

1. **Design Entry：** 写 RTL（Verilog / SystemVerilog）或用 Block Design（IP Integrator）。
2. **Simulation：** 跑 testbench 验证逻辑行为（如 Vivado Simulator）。
3. **Synthesis：** 把 Verilog 综合成 FPGA 基本元件（LUT、FF）。
4. **Implementation（Place & Route）：** 把元件映射到芯片物理位置并布线。
5. **Timing Analysis：** 验证布线后能否跑到目标时钟频率。
6. **Bitstream Generation：** 编译成 `.bit` 文件。
7. **Hardware Programming：** 经 USB / JTAG 下载到板子。

<aside>
⏱

**为什么时序分析这么重要：** 综合 + 布线后，信号在 LUT 和长连线上都要花时间。只有 Timing Analysis 通过（满足 setup/hold），设计才能在目标频率稳定工作 —— 这就是 timing closure。

</aside>

## 5️⃣ 开发方法（slide 17）

- **RTL（Register Transfer Level）：** 业界标准，Verilog / VHDL / SystemVerilog，逐周期精确控制硬件时序。
- **HLS（High-Level Synthesis）：** 用 C/C++ 写算法，工具自动翻译成 Verilog；擅长复杂数学，但抽象掉了时序控制。
- **IP Block Design：** 拖拽预制模块（UART、内存控制器、CPU 核）。
- **第三方工具：** Matlab/Simulink HDL Coder、LabVIEW FPGA（测试 / RF 常用）。
- **AI EDA：** 用大语言模型辅助写代码 / 优化。

---

# Part 2 — 硬件电路（Hardware Circuits）

<aside>
🚫

**本部分整节不进考试**（slide 18 明示）。内容是以 **ZYNQ7020 核心板**为例的板级硬件设计速览，帮助建立"FPGA 真正落到 PCB 上长什么样"的认知。

</aside>

## 6️⃣ 电源电路（slides 19–20）

![Slide 19 — FPGA 电源电路原理图](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF/slide_19.png)

Slide 19 — FPGA 电源电路原理图

- `VCCINT`：核心逻辑电源（约 1.0 V），供内部布线与 LUT。
- `VCCBRAM`：Block RAM 电源（约 1.0 V）。
- `VCCAUX`：辅助电源（PLL / JTAG / 配置逻辑，约 1.8 V）。
- `VCCO_XXXX`：I/O bank 电源（电压随 I/O 标准，3.3 / 2.5 / 1.8 V）。
- `VCCBAT`：电池备份（配置与实时时钟）。
- `VCCADC`：ADC 电源。

<aside>
⚠️

**Power Sequencing（上电时序）：** 电源必须按固定顺序上电（通常 VCCINT → VCCAUX → VCCO），否则会产生巨大电流冲击、损坏器件。

</aside>

## 7️⃣ IO Banks（slides 21–22）

![Slide 21 — IO Bank 原理图](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF/slide_21.png)

Slide 21 — IO Bank 原理图

- 引脚按 **bank** 分组，每个 bank 由独立的 `VCCO_XXXX` 供电，电压取决于该 bank 所采用的 I/O 标准 → 同一 bank 内的 I/O 标准要兼容。

## 8️⃣ 配置与启动（slide 23）

- `PROGRAM_B`：拉低时强制器件重新配置。
- `INIT_B`：指示初始化状态与配置错误。
- `DONE`：配置成功完成后拉高。
- `MODE[]`：选择配置模式（JTAG、QSPI、SD…）。

## 9️⃣ 时钟与复位（slide 24）

- `GCLK / MRCC / SRCC`：全局 / 区域时钟输入引脚。
- `REFCLK`：高速 transceiver 的参考时钟输入。
- `PS_RESET_B`（Zynq）：复位处理系统 PS。
- `POR_B`：上电复位输入。

## 🔟 编程 / 调试与高速 I/O（slide 25）

- **JTAG：** `TCK / TMS / TDI / TDO`，用于编程与调试。
- **高速 I/O：** `TXP/TXN、RXP/RXN` 差分 transceiver 对；`MGTAVCC / MGTAVTT` 为多吉比特 transceiver 供电。

## 1️⃣1️⃣ 模拟系统（slide 26）

- `VP / VN`：片上 ADC（XADC）的模拟输入；`DXP / DXN`：外部温度感测输入。
- `GND`：地参考；`VREF`：部分 I/O 标准所需的参考电压。

## 1️⃣2️⃣ 外部 RAM（slide 27）

![Slide 27 — 外部 RAM（DDR）原理图](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF/slide_27.png)

Slide 27 — 外部 RAM（DDR）原理图

- 片上存储有限，大容量数据靠外挂 DDR；原理图里能看到 **DDR 等长 / 地址等长**布线要求 —— 高速信号完整性的典型约束。

## 1️⃣3️⃣ PCB（slide 28）

![Slide 28 — ZYNQ7020 核心板 PCB](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF/slide_28.png)

Slide 28 — ZYNQ7020 核心板 PCB

- 关注点：通过多样接口对外连接、高速信号完整性、电源与散热。想深入硬件 → 选 **EE116** 或参加电子设计竞赛。

---

## 📝 本节总结（记三点）

<aside>
🎯

1. **FPGA = 可编程逻辑块阵列 + 可编程互连 + 灵活 I/O**；最小单元 **LE = LUT（查找表，本质是 SRAM 真值表 + mux 树）+ FF**。"编程 FPGA" = 下载 bitstream 去填 LUT。
2. **资源速记：** LUT/FF 做逻辑、BRAM/URAM 存数据、DSP 做乘累加、MMCM/PLL 管时钟、IOB 接外部引脚；现代 FPGA 里**布线延迟常大于门延迟**，timing closure 是关键。
3. **开发七步：** 设计 → 仿真 → 综合 → 实现(P&R) → 时序分析 → bitstream → 下载；方法上 RTL 精确、HLS 写 C、IP 拖拽。

**考试范围：** Part 1 仅最基础概念，Part 2 不考。

</aside>

## ✅ 作业 / 待办

- [ ]  完成**课程评教**：[evaluation.shanghaitech.edu.cn](http://evaluation.shanghaitech.edu.cn)
- [x]  课程 Project：[EE115B Project — Subway Turnstile Controller](EE115B%20Project%20%E2%80%94%20Subway%20Turnstile%20Controller.md)（截止 June 5, 2026 11:59 PM）
- 选读：GeekPie [FPGA tutorial](https://shanghaitechgeekpie.github.io/FPGA-tutorial/index.html)，跟着上手一遍 Vivado 流程。

## 📎 原始 Slides

[FPGA hardware(1).pdf](EE115B%20Lecture8%20%E2%80%94%20FPGA%20Part%203%EF%BC%9A%E6%A6%82%E5%BF%B5%E4%B8%8E%E7%A1%AC%E4%BB%B6%E7%94%B5%E8%B7%AF/FPGA_hardware(1).pdf)
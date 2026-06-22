# EE115B Lecture10 — 存储器 Memory：PLD · RAM · ROM · 存储扩展

<aside>
💾

**本节主题：** Memory（存储器）—— 从可编程逻辑器件 PLD 出发，串起 **RAM（SRAM / （DRAM）**、**ROM（OTP / EPROM / EEPROM / Flash）**、**存储器扩展**（位扩展 / 字扩展），最后到 HDD / SSD / CD-ROM 三种物理存储介质。

**讲义来源：** EE115B《存储器》slides（Chenxi Xiao；素材含 © Pearson Education、Hengzhao Yang、Zhifeng Zhu、Yajun Ha），共 23 页。

**核心脉络：** *可编程怎么实现 →（易失 vs 非易失）→ RAM 怎么存 → ROM 怎么存 → 怎么把小芯片拼成大存储 → 真实存储介质长什么样*。

</aside>

## 1⃣ 可编程逻辑器件 PLD（slides 3–8）

**PLD（Programmable Logic Device）**：出厂时没有固定逻辑功能，可由用户*编程*实现几乎任意逻辑设计。核心问题只有两个 —— **怎么打开/关闭内部开关？** 以及 **掉电后配置会不会丢？**（即易失 vs 非易失）。

### 1.1 三种「开关」实现技术

| 技术 | 编程方式 | 可重编程？ | 易失？ |
| --- | --- | --- | --- |
| **Fuse 熔丝** | 通大电流「**熔断**」选中熔丝 → 断开连接 | 否（OTP 一次性） | 非易失 |
| **Antifuse 反熔丝** | 加足够高电压「**击穿**」绝缘层 → 接通连接 | 否（OTP 一次性） | 非易失 |
| **SRAM-based** | 用一个 SRAM cell 控制晶体管开/关，连/断行列 | 是（可反复重配） | **易失**（掉电丢配置） |

<aside>
🔑

**记忆点：** Fuse = 本来通、烧断它；Antifuse = 本来断、击穿接通；二者都是 **OTP（One-Time Programmable）**。SRAM-based 可以反复改，但**掉电即失忆** —— 这正是现代 **FPGA** 上电要重新加载配置的原因。

</aside>

![Slide 6 — Fuse Technology（熔丝：通大电流熔断）](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_6.png)

Slide 6 — Fuse Technology（熔丝：通大电流熔断）

![Slide 7 — Antifuse Technology（反熔丝：高压击穿绝缘层）](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_7.png)

Slide 7 — Antifuse Technology（反熔丝：高压击穿绝缘层）

![Slide 8 — SRAM 型可重编程单元（易失）](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_8.png)

Slide 8 — SRAM 型可重编程单元（易失）

## 2⃣ RAM vs ROM 总览（slide 9）

|  | 掉电是否保存 | 速度 | 典型实现 |
| --- | --- | --- | --- |
| **RAM**（随机存取） | ❌ 掉电丢失（**易失**） | 快 | SRAM（晶体管 latch）/ DRAM（电容） |
| **ROM**（只读） | ✅ 掉电保留（**非易失**） | 慢于 RAM | OTP / EPROM / EEPROM / Flash |
- **SRAM**：非常快，用晶体管存储，实现成本高、密度低。
- **DRAM**：比 SRAM 慢，用电容阵列存储，密度高、便宜。
- **ROM**：非易失，速度慢于 RAM。

## 3⃣ RAM：SRAM 与 DRAM（slides 10–12）

### 3.1 SRAM —— 6 管 latch（slide 10）

一个 SRAM cell = **两个反相器交叉耦合**成 latch（共 **6 个晶体管**）＋ 两个由 **word line** 控制的存取管 T1、T2：

- **word line = 0（接地）**：T1、T2 关断，latch 与位线隔离，**保持**当前状态（记忆）。
- **读操作**：拉高 word line 接通 T1、T2。若 cell 存 `1`，则位线 $b$ 为高、$\bar b$ 为低；存 `0` 则相反。$b$ 与 $\bar b$ **恒为互补**。位线末端的 sense/write 电路检测状态并输出。
- **写操作**：sense/write 电路**主动驱动**位线 $b$ 与 $\bar b$，再拉高 word line，把 cell 强制写入目标状态；word line 撤销后状态被锁存保持。

<aside>
📦

存储阵列规模示例：**RAM 32k×8** = $2^{15}$ 个字、每字 8 bit。地址线 $A_0\!-\!A_{14}$（15 根，因 $\log_2 32768 = 15$），数据 I/O 8 根，控制端 $\overline{CS}$（片选）、$\overline{WE}$（写使能）、$\overline{OE}$（输出使能）。

</aside>

![Slide 10 — SRAM cell（6 管交叉耦合 latch）与 4×4 阵列](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_10.png)

Slide 10 — SRAM cell（6 管交叉耦合 latch）与 4×4 阵列

### 3.2 SRAM 读 / 写时序（slide 11）

关键在 **控制信号与数据有效窗口的时序关系**：

- **读周期（**$\overline{WE}$ **HIGH）**：给出 valid address → 拉低 $\overline{CS}$、$\overline{OE}$ → 经过访问延迟 $t_{AQ}/t_{EQ}/t_{GQ}$ 后，数据 $O$ 变为 valid data。
- **写周期（**$\overline{WE}$ **LOW）**：给出 valid address + valid data，注意建立时间 $t_{s(A)}$、写数据窗口 $t_{WD}$ 与保持时间 $t_{h(D)}$。

<aside>
⏱️

**口诀（老师红字强调）：Lock at WE rising edge** —— 数据在 $\overline{WE}$ 的**上升沿**（写使能撤销那一刻）被真正锁进 cell，所以数据必须在该沿之前 setup、之后 hold 住。

</aside>

![Slide 11 — SRAM 读 / 写时序（注意 WE 上升沿锁存）](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_11.png)

Slide 11 — SRAM 读 / 写时序（注意 WE 上升沿锁存）

### 3.3 DRAM —— 1T1C（slide 12）

DRAM cell = **1 个晶体管 + 1 个电容**，结构比 SRAM 简单得多。

- ✅ **密度高**：同样芯片面积下位容量远大于 SRAM。
- ⚠️ **访问慢**：access time 长于 SRAM。
- ⚠️ 电容会漏电 → 必须周期性 **refresh**（刷新）才能保住数据。

![Slide 12 — DRAM cell（单管 + 电容）](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_12.png)

Slide 12 — DRAM cell（单管 + 电容）

<aside>
⚖️

**SRAM vs DRAM trade-off：** SRAM 快、不用刷新、但 6 管/位贵且占面积 → 做 **Cache**；DRAM 1 管+电容、密度高、便宜但要刷新且慢 → 做 **主存**。

</aside>

## 4⃣ ROM 家族：从一次性到电可擦（slides 13–16）

### 4.1 OTP ROM（slide 13）

通过 **行（ROW）/ 列（COLUMN）** 选中交叉点，写入时「烧熔丝」固定每一位；读出时用行列寻址、列端经下拉读取熔丝状态。一次性写死、之后只读。

![Slide 13 — OTP ROM 行列阵列（烧熔丝写入）](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_13.png)

Slide 13 — OTP ROM 行列阵列（烧熔丝写入）

### 4.2 EPROM（slide 14）

**Erasable PROM**：核心是 **浮栅晶体管（Floating-Gate transistor）**，靠在浮栅里**囤积电子**表示数据。可用 **紫外线（UV）照射**整片擦除后重新编程（芯片上有石英窗）。

![Slide 14 — EPROM 浮栅晶体管（UV 擦除）](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_14.png)

Slide 14 — EPROM 浮栅晶体管（UV 擦除）

### 4.3 EEPROM（slide 15）

**Electrically Erasable PROM**：可以**电擦除、电重编程**，不再需要 UV 光或专用设备，可按字节级别擦写，使用更灵活。

![Slide 15 — EEPROM（电擦除 / 电重编程）](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_15.png)

Slide 15 — EEPROM（电擦除 / 电重编程）

### 4.4 Flash（slide 16）

基于**单管浮栅**结构，既**非易失**又**可重编程**。属于 EEPROM 的一类，但**写入更快、密度更高**。擦写靠 **Fowler–Nordheim（FN）电子隧穿** 把电子打进/拉出浮栅。

![Slide 16 — Flash（单管浮栅 + FN 隧穿）](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_16.png)

Slide 16 — Flash（单管浮栅 + FN 隧穿）

<aside>
🧬

**ROM 演化主线：** OTP（烧一次）→ EPROM（UV 整片擦）→ EEPROM（电擦、字节级）→ **Flash**（电擦、块级、快且密）。一句话：*可擦性越来越强、颗粒越来越细/块、速度密度越来越好*。

</aside>

## 5⃣ 存储器扩展（slides 17–20）

单片存储芯片容量/位宽不够时，用多片拼接。容量公式：一片 $n$ 根地址线 → $2^n$ 个字；总容量 $= 2^n \times (\text{字长 bits})$。

- 🧩 别混：「数据多少位」和「地址多少根 / 要不要 $A_{16}$」是两回事
    - **数据宽度** = D 线根数 = 每字几 bit。要 16 位就是 $D_0\text{–}D_{15}$，和地址无关。
    - **地址线根数** = A 线根数 = 能存几个字（$2^{\text{根数}}$）。
    - **位扩展**：只加宽 D（拼数据位），地址照旧、所有片共用同一 CS，**不需要反相器、也不会出现更高地址位**。
    - **字扩展**：要扩容量（叠片），才需要**多一根更高地址位**当选片位（上片直连、下片反相），用它 + $\overline{CS}$ 选片。
    - **一句话**：只想要"更宽" → 位扩展（不冒 $A_{16}$）；想要"更深 / 更大" → 字扩展（才会冒出选片位 $A_{16}$）。

### 5.1 位扩展 Word-Length Expansion（slides 17–18）

**目标：加宽每个字的位数，地址空间不变。** 把多片**共用同一组地址线 + 同一片选**，各自负责数据总线的不同位段，输出拼起来。

- 例：两片 $65{,}536\times4$ 的 ROM → 拼成 $65{,}536\times8$。地址线仍是 $A_0\!-\!A_{15}$（16 根），数据从 4 位变 8 位（$O_0\!-\!O_7$）。

![Slide 18 — 位扩展：两片 65,536×4 → 65,536×8](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_18.png)

Slide 18 — 位扩展：两片 65,536×4 → 65,536×8

### 5.2 字扩展 Word-Capacity Expansion（slides 19–20）

**目标：增加字的数量（扩地址空间），位宽不变。** 关键是**多出来的高位地址线**经译码/使能去**选片**：高位选中哪一片，剩余低位在片内寻址。

- 例：两片各 **19 根**地址线（$2^{19}$ 字）→ 拼出 **20 根**地址线接口（$2^{20}$ 字）；多出的最高位 $A_{19}$ 经 $\overline{E}$ 控制（一片直连、一片取反），实现二选一。
- 同理两片各 **20 根** → 拼出 **21 根**地址线。

<aside>
📐

**别搞混：** 位扩展 = 共享地址、**拼数据位**（变宽）；字扩展 = **用高位地址选片**、拼地址空间（变深）。老师提示「**Pay attention to address**」—— 字扩展的难点全在地址线如何分配与译码。

</aside>

![Slide 20 — 字扩展：两片 19 位地址 → 20 位地址接口](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_20.png)

Slide 20 — 字扩展：两片 19 位地址 → 20 位地址接口

- ❓ Q：控制总线 $\overline{E}$ 连到两个 & 门，就是 CS（片选）口吗？
    - **不完全是。** $\overline{E}$ 是整组存储器的**公共使能（overall enable）**，被同时送进两个 & 门——它一旦无效（拉高），两片芯片全部失能；有效（拉低）时才允许工作。它本身**不是**某一片的片选，而是"整体开不开"的总闸。
    - **真正的 CS / 片选 = & 门的输出 EN。** 每个门 $\text{EN}_i = \overline{E}\;\wedge\;(\text{高位地址选中本片})$，门的输出才接到对应 ROM 的片选（CS / EN）脚。
    - **谁区分两片？高位地址线**（图里最高位那根 $A$）。一片直接接、一片经反相（两门输入端的小圆圈 = 取反）→ 任一时刻**只有一片**被选中，互斥。
    - **一句话**：$\overline{E}$ 提供「整体开不开」，高位地址提供「开哪一片」，二者经 & 门合成后，输出才是真正的片选 CS。
- 🛠️ 自检：画字扩展的 CS / 片选电路，最容易错的 5 点
    - **选片位不能同时进片内地址**：用作选片的高位必须在芯片地址范围**之上**。若每片 64K（$A_0\text{–}A_{15}$），选片位得是 $A_{16}$；若每片 32K（$A_0\text{–}A_{14}$），才用 $A_{15}$ 选片，且它**只进使能门、不进地址脚**。别让同一根 $A_{15}$ 既进地址又兼职选片。
    - **选片位要同时接到「上片 + 下片」两个使能门**：上片接原码、下片接反码（加反相器）。漏接其中一片，会出现某片"永远使能"，与另一片抢同一数据总线。
    - **反相器加在选片位上，不是加在** $\overline{CS}$ **上**。
    - **极性配套**：$\overline{CS}$ 与片使能都低有效时，用 OR 门合成 $\text{EN}_i = \overline{CS}\ \text{OR}\ (\text{选片位极性})$，只有「总片选有效且本片被选中」才拉低使能。
    - **位扩展多字节时**：左右各字节列要用**同一根选片位、同一极性配对**（左上⇄右上、左下⇄右下），否则同一地址读不出对齐的完整宽位字。

## 6⃣ 物理存储介质（slides 21–23）

### 6.1 磁硬盘 Magnetic Hard Disk（slide 21）

靠磁头在旋转盘片的磁性涂层上**磁化方向**记录 0/1，机械寻道、非易失、容量大但有机械延迟。

![Slide 21 — Magnetic Hard Disk](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_21.png)

Slide 21 — Magnetic Hard Disk

### 6.2 固态硬盘 SSD（slide 22）

基于 **Flash（NAND）** 颗粒，无机械结构，随机读写快、抗震、功耗低。

![Slide 22 — Solid State Drive](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_22.png)

Slide 22 — Solid State Drive

### 6.3 CD-ROM（slide 23）

盘面刻有长短不一的 **pit（凹坑）/ land（平台）**。盘片旋转时激光束经棱镜（Prism）照射轨道，**光电二极管**检测反射光强差异，从而读出与 pit/land 排列对应的一串 1 / 0。

![Slide 23 — CD-ROM（激光 + 棱镜 + 光电检测）](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/slide_23.png)

Slide 23 — CD-ROM（激光 + 棱镜 + 光电检测）

## 🎯 本节总结

<aside>
🧠

1. **易失 vs 非易失** 是贯穿全章的主线：RAM / SRAM-based PLD 掉电就丢；ROM / Flash / 磁盘掉电仍在。
2. **SRAM = 6 管 latch（快、贵、做 Cache）；DRAM = 1T1C（密、慢、要刷新、做主存）**。SRAM 写入「**Lock at WE rising edge**」。
3. **ROM 演化：OTP → EPROM(UV) → EEPROM(电擦字节) → Flash(电擦块、快密)**；都靠浮栅囤电子（OTP 除外，是烧熔丝）。
4. **扩展两件事别混：位扩展共享地址拼数据位（变宽）；字扩展用高位地址译码选片（变深）**。
</aside>

## 📎 原始 Slides

[存储器.pdf](EE115B%20Lecture10%20%E2%80%94%20%E5%AD%98%E5%82%A8%E5%99%A8%20Memory%EF%BC%9APLD%20%C2%B7%20RAM%20%C2%B7%20ROM%20%C2%B7%20%E5%AD%98%E5%82%A8/%E5%AD%98%E5%82%A8%E5%99%A8.pdf)
# EE115B Lecture11 — ADC/DAC：数模与模数转换

<aside>
🎚

**主题：** ADC / DAC —— 模拟世界与数字世界的接口电路

**来源：** EE115B（Chenxi Xiao）· slides 部分来自 © Pearson Education；采样与傅里叶的原理课为 EE150 *Signals and Systems*

**核心脉络：** 1⃣ Op-Amp(运放) 复习（follower / 放大器 / comparator(比较器)）→ 2⃣ DAC：binary-weighted(二进制加权) 电阻网络 → 3⃣ ADC：Flash 与 SAR(逐次逼近) 两种架构 → 4⃣ Quantization(量化) 与量化误差 → 5⃣ Fourier 与 Nyquist 采样定理

</aside>

<aside>
📌

**行政信息：** 本节 slides 无新增 DDL。但 **HW4 的 P4 正是 SAR ADC ＋ 量化误差题**，截止 June 15, 2026 11:59 PM（已在课程页与日历）——写题前先把本页 3⃣ 和 4⃣ 过一遍。

</aside>

## 1⃣ Review of Op-Amps：运放三种用法复习

### 1.1 Voltage Follower 电压跟随器

![Slide 3 — Voltage Follower](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_3.png)

Slide 3 — Voltage Follower

- 核心式：$V_{out} = V_{in}$，闭环增益 = 1。
- **为什么有用**：把放大器前 / 后级电路解耦，可以 separately(分开地) 设计——前级只看到运放的高输入阻抗，后级由运放的低输出阻抗驱动。
- 常用作 output buffer(输出缓冲器)，reduce output impedance(降低输出阻抗)。

### 1.2 Non-inverting Amplifier 同相放大器

![Slide 4 — Non-inverting Amplifier](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_4.png)

Slide 4 — Non-inverting Amplifier

- 输入信号加在同相端 (+)，反馈网络 $R_f, R_1$ 把输出分压送回反相端。
- 由虚短 $V_- = V_+ = V_{in}$ 与分压关系 $V_- = \frac{R_1}{R_1 + R_f} V_{out}$ 推出：

$$
A_v = \frac{V_{out}}{V_{in}} = 1 + \frac{R_f}{R_1}
$$

- 增益 ≥ 1，且只由电阻比决定——与运放本身巨大的开环增益无关，这就是负反馈的威力。

### 1.3 Inverting Amplifier（带求和）反相求和放大器

![Slide 5 — Inverting Amplifier with Sum](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_5.png)

Slide 5 — Inverting Amplifier with Sum

- 虚地 (virtual ground)：$V_- \approx 0$，各输入支路电流 $V_i / R_i$ 全部汇入 $R_f$，互不干扰：

$$
V_{out} = -\left( \frac{R_f}{R_1} V_1 + \frac{R_f}{R_2} V_2 \right)
$$

- **关键直觉**：反相求和放大器就是硬件版「加权求和(weighted sum)」机器——这正是 DAC 的数学核心。

### 1.4 开环运放 ＝ Comparator(比较器)

![Slide 6 — 开环特性：线性区与饱和](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_6.png)

Slide 6 — 开环特性：线性区与饱和

- linear region(线性区)：$V_{out} = A(V_+ - V_-)$，直流下 $A$ huge(极大)（$10^5$ 或更高）。
- saturation(饱和)：

$$
V_{out} = \begin{cases} V_{sat+}, & V_+ > V_- \\ V_{sat-}, & V_+ < V_- \end{cases}
$$

$V_{sat\pm}$ 主要由电源电压决定。

- 线性区窄到可以忽略 → 输出 essentially(本质上) 是 digital output：**开环运放就是一个 1-bit 判决器，这里是模电与数电的交接点。**

![Slide 7 — Op-Amp 作 Comparator 例题](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_7.png)

Slide 7 — Op-Amp 作 Comparator 例题

- 例题套路：一端接固定参考电压、另一端接缓变模拟信号；先用分压求出阈值，再分段写输出贴哪条电源轨。

<aside>
🧠

**口诀：** 闭环负反馈 → 放大器（虚短虚断成立）；开环无反馈 → 比较器（输出只剩两条轨）。

</aside>

## 2⃣ DAC：Binary-Weighted-Input DAC

![Slide 9 — 4-bit Binary-Weighted DAC 例](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_9.png)

Slide 9 — 4-bit Binary-Weighted DAC 例

- 思想：用阻值代表输入位二进制权重(binary weights) 的电阻网络 ＋ 反相求和放大器。
- 输入码 $b_3 b_2 b_1 b_0$（$b_3$ 为 MSB），每位电压 $V_i = b_i V_H$（$V_H$ 为高电平逻辑电压）。
- 电阻从 MSB 到 LSB 依次为 $R, 2R, 4R, 8R$，套用 1.3 的求和公式：

$$
V_{out} = -\left( V_3 + \frac{V_2}{2} + \frac{V_1}{4} + \frac{V_0}{8} \right) = -\frac{V_H}{8}\left( 2^3 b_3 + 2^2 b_2 + 2^1 b_1 + 2^0 b_0 \right)
$$

- 即 $V_{out} = \text{constant} \times$（输入二进制码的十进制值）——输出与码值严格 proportional to(成正比)，verify(验证) 了它是合格的 DAC。

<aside>
⚠️

**易错点：** MSB 接的是**最小**电阻 $R$（电流最大 → 权重最大），LSB 接最大电阻 $8R$，方向别记反；另外输出带**负号**（反相结构）。

</aside>

- ❓ Q&A — 本节讲的是 binary-weighted DAC，R-2R ladder DAC 出现过吗？
    
    **问：** 「R-2R ladder DAC 相比 binary-weighted-resistor DAC 的主要优点」这个考点，在本节出现过吗？又提到过这个名词吗？
    
    **答：本节只讲了 binary-weighted DAC，从头到尾没有出现 “R-2R ladder” 这个名词。**
    
    - 本节 2⃣ 讲的是 **binary-weighted-input DAC**：电阻按二进制权重取 $R, 2R, 4R, 8R$，阻值范围随位数指数增大。
    - **R-2R ladder 是另一种（改进型）DAC 拓扑**，slides 没覆盖——它只用 $R$ 和 $2R$ 两种阻值搭成梯形网络。
    - **R-2R 的主要优点（模拟卷 Part I 第 7 题答案 = B）：** 只需两种 precise(精确) 阻值 → matching(电阻匹配) 好、易 fabricate(制造)，尤其适合集成电路；而 binary-weighted 在高位数时需要跨好几个数量级的精密电阻，很难做准。
    - ⚠️ 题面笔误：第 7 题勾打在了 D “infinite resolution” 上，应为 **B**——任何有限位 DAC 分辨率都是有限的 $V_{ref}/2^N$，不存在无限分辨率。

## 3⃣ ADC：两种经典架构

### 3.1 Flash ADC：并行比较，空间换时间

![Slide 11 — Flash ADC](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_11.png)

Slide 11 — Flash ADC

- n-bit 转换 in general(一般地) 需要 $2^n - 1$ 个 comparators：电阻串分压出 $2^n - 1$ 个阈值，$V_{in}$ **同时**与所有阈值比较。
- 比较器输出（温度计码）再经 priority encoder(优先编码器) 压成 n-bit 二进制码——编码器设计回看 Lecture7；输出 V 位表示 valid or not(结果是否有效)。
- 特点：**Ultra-fast(极快)**，一步出码；代价是比较器数量随位数**指数爆炸**。
- ❓ Q&A — Flash ADC 里 encoder 接收的是数字信号还是电压？
    
    **问：** Flash ADC 里 encoder 接收的不是数字信号吧，是电压吧？
    
    **答：理解反了——接收模拟电压的是比较器，不是 encoder。**
    
    - 信号链：$V_{in}$(模拟电压) → comparators(比较器) → 温度计码(数字) → priority encoder → n-bit 二进制码。
    - **模→数转换发生在比较器这一步**：每个比较器只输出高 / 低两种电平，本质是 1-bit 数字判决（见 1.4 开环运放 = comparator）。
    - 一排比较器的输出叠起来就是 **thermometer code(温度计码)**，已经是数字信号（一串 1 / 0）。
    - **encoder 接收的就是这串数字温度计码**，它是纯数字逻辑电路，把 $2^n-1$ 位温度计码压成 n-bit 二进制。
    - ⚠️ 易混点：比较器输出的高 / 低物理上也是电压，但代表逻辑 1 / 0，对 encoder 来说就是数字输入，而不是待量化的连续模拟电压。

### 3.2 Successive-Approximation ADC（SAR）：二分查找，时间换空间

![Slide 12 — SAR ADC 框图](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_12.png)

Slide 12 — SAR ADC 框图

- 结构：1 个 comparator ＋ SAR(Successive Approximation Register, 逐次逼近寄存器) ＋ 内部 DAC，构成反馈环。
- DAC 的输入位 one at a time(一次一位) 被 enabled(置 1)，让 DAC 输出逐步逼近 $V_{in}$。

![Slide 13 — SAR 逐次逼近过程（Vref = 15 V 例）](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_13.png)

Slide 13 — SAR 逐次逼近过程（Vref = 15 V 例）

- 流程就是 binary search(二分查找)：
    1. 先试 MSB（相当于猜 $V_{ref}/2$）；
    2. comparator 判断：DAC 输出不超过 $V_{in}$ → 该位保留 1，否则清 0；
    3. 移到下一位重复，直到 LSB。
- **每个时钟周期定 1 bit → n-bit 需要 n 个周期**（HW4 P4 考点：10-bit SAR → 10 个周期的 conversion time）。
- ❓ Q&A — SAR 的原理是什么？
    
    **一句话：** 用二分查找(binary search)，**每个时钟周期定 1 个 bit**。
    
    **结构（反馈环）：** 1 个 comparator ＋ SAR 寄存器 ＋ 内部 DAC。SAR 控制 DAC 的输入码，让 DAC 输出电压去逼近 $V_{in}$。
    
    **流程（n-bit）：**
    
    1. 先猜 MSB：最高位置 1、其余清 0 → DAC 输出 $V_{ref}/2$。
    2. comparator 判断：DAC 输出 $\le V_{in}$ → 该位**保留 1**；否则**清 0**。
    3. 移到下一位重复，每轮把搜索区间**砍一半**，直到 LSB。
    
    **关键点：**
    
    - 本质是二分查找，逐位逼近 $V_{in}$。
    - n-bit 需 n 个时钟周期（HW4 P4：10-bit → 10 周期）。
    - 对比：Flash 空间换时间（一步出码、$2^n-1$ 个比较器）；SAR 时间换空间（1 个比较器、多比几轮）。
- ❓ Q&A — SAR 内部具体怎么猜 / 清空 / 比较？
    
    **内部 5 块：**
    
    - **S/H 采样保持**：转换开始瞬间把 $V_{in}$ 冻结，保证 n 个周期被比的电压不变。
    - **SAR 寄存器 + 控制逻辑**：存当前码，有个指针从 MSB 逐位移到 LSB。
    - **内部 DAC**：把当前码转成 $V_{dac}$。
    - **comparator**：比 $V_{in}$ 与 $V_{dac}$，输出 1 位决策。
    - **控制 / 时钟**：排好 MSB→LSB，n 周期后拉高 EOC 并锁存输出。
    
    **每个周期三步（针对当前位）：**
    
    1. **猜（试置 1）**：当前位试探性置 1，低位仍为 0。
    2. **比**：DAC 出 $V_{dac}$，comparator 判断：$V_{dac}\le V_{in}$ → 输出 1；$V_{dac}>V_{in}$ → 输出 0。
    3. **留或清**：输出 1 → 该位保留 1；输出 0 → 该位清回 0（“清空”指只退这一位，已定高位不动）；然后指针移到下一位。
    
    **数值例（4-bit，**$V_{ref}=16\text{V}$**，**$V_{in}=11\text{V}$**，DAC**$=8b_3+4b_2+2b_1+b_0$**）：**
    
    - 周期1 试 b₃：`1000`→$V_{dac}=8$，$8\le11$ → 留→ `1000`
    - 周期2 试 b₂：`1100`→$12$，$12>11$ → 清→ `1000`
    - 周期3 试 b₁：`1010`→$10$，$10\le11$ → 留→ `1010`
    - 周期4 试 b₀：`1011`→$11$，$11\le11$ → 留→ `1011`
    - 结果 `1011` = 11，4 周期定 4 位。本质是逐位二分查找，区间每轮砍一半。

|  | Flash ADC | SAR ADC |
| --- | --- | --- |
| 转换时间 | 一步出码，ultra-fast | n bit 需 n 个时钟周期 |
| 硬件开销 | 2ⁿ−1 个比较器 ＋ 优先编码器 | 1 个比较器 ＋ DAC ＋ SAR |
| 随位数增长 | 指数（硬件爆炸） | 线性（多比几轮而已） |
| 典型场景 | 高速采样（示波器、射频） | 通用 MCU、中速中精度 |

<aside>
🧠

**口诀：** Flash 用空间换时间，一眼全比完；SAR 用时间换空间，一轮定一位（binary search）。

</aside>

## 4⃣ Quantization 量化与量化误差

![Slide 14 — Quantization 与量化误差](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_14.png)

Slide 14 — Quantization 与量化误差

- **Quantization(量化)**：把连续的模拟输入范围映射到有限个离散数字电平的过程。
- **Resolution(分辨率)**：N bits → $2^N$ 个 distinct levels(不同电平)，

$$
\text{LSB (resolution)} = \frac{V_{ref}}{2^N}
$$

- **Quantization error(量化误差)**：实际模拟输入电压与数字化输出所代表电压之差。

### 数值例（3-bit ADC，slide 例重排）

- $V_{ref} = 8\,\text{V}$，levels $= 2^3 = 8$，$\text{LSB} = 8/8 = 1\,\text{V}$。
- 输入 $2.6\,\text{V}$ → 量化到最近电平 $3\,\text{V}$；误差 $= 3 - 2.6 = +0.4\,\text{V}$。
- 最大可能误差 $\pm 0.5\,\text{V}$，即 $\pm\tfrac{1}{2}\,\text{LSB}$。

<aside>
⚠️

**易错点（直接关系 HW4）：** 量化有两种约定——本节 slide 用 **rounding(四舍五入到最近电平)**，最大误差 ±½ LSB；而 HW4 P4 用 **truncation(截断 / 向下取整)** $N_{out} = \lfloor V_{in}/\Delta \rfloor$，误差落在 0 到 1 LSB 之间。做题先看清用哪种！

</aside>

## 5⃣ 采样：Fourier Transform 与 Nyquist 定理

### 5.1 Fourier Transform 直觉

![Slide 16 — Fourier Series / Transform](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_16.png)

Slide 16 — Fourier Series / Transform

- Fourier transform：把实值函数表示为一组幅度与频率 suitably-chosen(选取得当) 的正弦 / 余弦的 superposition(叠加，求和 / 积分)。
- Fourier series 处理周期信号；FT 处理 continuous, aperiodic(连续、非周期) 信号。
- 原理推导超出本课范围 → 去修 EE150 Signals and Systems。

### 5.2 Nyquist–Shannon Sampling Theorem 采样定理

![Slide 17 — Nyquist 采样定理与混叠](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/slide_17.png)

Slide 17 — Nyquist 采样定理与混叠

- 采样率必须**至少是信号 bandwidth(带宽) 的两倍**，才能 accurately reconstruct(准确重建) 波形；否则高频成分会在 passband(通带) 内产生 **alias(混叠假频)**。
- 例：音频内容到 20 kHz → 采样率至少 40 kHz（实际用 44.1 / 48 kHz）；并在采样前加 cutoff(截止频率) ≈ 20 kHz 的 **anti-aliasing(抗混叠) low-pass filter**。

<aside>
🧠

**口诀：** 先滤波、再采样；$f_s \ge 2 \times BW$，否则高频「假装」成低频混进通带（alias）。

</aside>

## 6⃣ What's next：课程展望（非考点）

- 后续相关课程：数字集成电路、CA(计算机体系结构)、FPGA、嵌入式系统、板级电路设计实践；以及「一生一芯」计划。
- 可参与活动：电子设计竞赛、RoboMaster、InterStudio、SIST 实验室科研实习。
- Xiao 老师的 RIM Lab（Robot Interaction and Manipulation）招本科实习生：方向 tactile perception(触觉感知)、robot interaction / manipulation(机器人交互 / 操作)；地点 SIST 1D-301A / 1D-303，联系邮箱 [xiaochx@shanghaitech.edu.cn](mailto:xiaochx@shanghaitech.edu.cn)。

## ✅ 本节总结

<aside>
🎯

1. **运放两副面孔**：闭环负反馈 ＝ 放大器（虚短虚断）；开环 ＝ 比较器（1-bit 判决、数字输出）。
2. **DAC ＝ 加权求和**：binary-weighted 电阻网络 ＋ 反相求和放大器，输出正比于输入码十进制值；MSB 配最小电阻。
3. **ADC 双雄**：Flash 空间换时间（2ⁿ−1 个比较器、一步出码）；SAR 时间换空间（二分查找、n bit n 周期）。
4. **数字化两步走**：采样守 Nyquist（$f_s \ge 2 \times BW$ ＋ 抗混叠滤波），量化看 LSB（rounding 最大误差 ±½ LSB）。
</aside>

## 📌 作业 / 待办

- [ ]  完成 HW4 P4（SAR ADC ＋ 量化误差），截止 June 15, 2026 11:59 PM——先复习本页 3⃣ 的周期数与 4⃣ 的 rounding vs truncation 易错点
- [ ]  期末复习：把 Flash vs SAR 对比表和 Nyquist 音频例子各口头复述一遍

<aside>
🐈

**下次打开第一步：** 只看 Slide 13 那张 SAR 逐次逼近图，花 30 秒口头复述「二分查找逐位确定」的流程，再决定要不要继续——启动就这么小。

</aside>

## 📎 原始 Slides

[ADC_DAC.pdf](EE115B%20Lecture11%20%E2%80%94%20ADC%20DAC%EF%BC%9A%E6%95%B0%E6%A8%A1%E4%B8%8E%E6%A8%A1%E6%95%B0%E8%BD%AC%E6%8D%A2/ADC_DAC.pdf)
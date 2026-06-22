# EE115B Lecture1 Part2 — Introductory Concepts 模拟数字系统与时序基础

<aside>
📶

**本节主题：** Introductory Concepts（导论概念）——analog(模拟) vs digital(数字) 的区别、logic level(逻辑电平)、digital waveform(数字波形)、pulse(脉冲) 参数、timing diagram(时序图)，以及 serial / parallel data(串行 / 并行数据)。

**讲义范围：** 本 PDF 对应 **Lecture 1 Part 2**，共 15 页。

**核心脉络：** ① 为什么数字系统值得学 → ② bit 到底如何落在真实电压上 → ③ 数字波形有哪些关键时域参数 → ④ timing diagram 怎么读 → ⑤ 实际器件为什么必须看 datasheet → ⑥ serial 和 parallel 各有什么 trade-off(权衡)。

</aside>

## 1️⃣ Analog vs Digital：数字系统到底好在哪？

<aside>
💡

**这一节只处理 Lecture1 Part2。** 先抓主线：数字系统的优势，不在于“更真实”，而在于**更容易存储、抗噪、计算、复制与传输**。

</aside>

slides 先从自然界里的 **analog quantity(模拟量)** 讲起：温度、声音、电压变化等大多是**连续**的；而数字系统把连续量离散化后，只处理一组有限状态。

### Analog system 的挑战

根据 slides，模拟系统的典型困难有三类：

- **Storage(存储)**：连续值难以长期无损保存，复制也容易失真
- **Noise and accuracy(噪声与精度)**：信号一旦被噪声污染，很难“完美恢复”
- **Computation(计算)**：复杂运算往往更难稳定实现

### Digital system 的核心优势

数字系统虽然不能直接表示“连续无限精细”的数值，但可以：

- 更高效地 **process(处理)** / **store(存储)** / **transmit(传输)** 数据
- 用 0 / 1 两种状态提高抗干扰能力
- 容易复制、纠错、编程和自动化处理

*📄 见文末「原始 Slides」第 3 页：analog quantity 与 digital quantity 的直观温度曲线对比。*

### Analog 与 Digital（Hybrid）System 比较

现实世界里，很多系统其实是 **hybrid system(混合系统)**：

- 外界信号可能是 analog（例如声音）
- 中间的存储 / 处理部分可能是 digital
- 输出给人时又可能重新转回 analog

例如 CD 音频系统就是：

$$
\text{Digital Data} \rightarrow \text{DAC} \rightarrow \text{Analog Signal} \rightarrow \text{Speaker}
$$

*📄 见文末「原始 Slides」第 4 页：microphone / amplifier / speaker 与 CD + DAC 的对比图。*

### 对比表

|  | Analog | Digital |
| --- | --- | --- |
| 信号取值 | 连续 | 离散 |
| 抗噪声 | 较弱，误差会累积 | 较强，只要还在判决区间内就能识别 0/1 |
| 存储复制 | 容易失真 | 易复制、易保存 |
| 计算实现 | 复杂系统不易扩展 | 适合逻辑、编程、自动控制 |
| 典型场景 | 传感器原始信号、射频、放大器 | CPU、存储器、数字通信、逻辑控制 |

<aside>
📌

**一句话记忆：** 模拟更接近物理世界，数字更适合工程处理。

</aside>

- 📚 拓展 — 为什么数字系统抗噪更强？
    
    数字系统并不是“没有噪声”，而是它把很多小扰动都视作“还属于同一个逻辑状态”。比如某个逻辑 1 允许是 3.0V、3.1V、3.2V……只要仍落在 HIGH 判定区间，就都算 1。这种 **threshold-based decision(阈值判决)** 正是数字系统鲁棒性的来源。
    

## 2️⃣ How to Represent Digital Signals：bit 不是抽象符号，而是电压区间

要表示 digital signal，最终必须回答一个问题：**0 和 1 在电路里到底长什么样？**

slides 这里承接了后续的数制内容：bit 不是凭空存在，而是要先有“如何表示”的规则。

*📄 见文末「原始 Slides」第 5 页：decimal / binary / octal / hex 对照表，说明 bits 可以被组织成更高层的数字表示。*

## 3️⃣ Binary Digits and Logic Levels：0 / 1 如何映射到真实硬件？

### ① bit 的物理含义

在二进制里，一个 **bit(binary digit, 二进制位)** 只有两种可能：0 或 1。

但在电路里，并不是“看见某个唯一精确电压才算 1”。相反，数字电路会预先定义两个区间：

- **LOW**
- **HIGH**

中间还会留一段 **invalid / undefined region(无效 / 不确定区间)**。

### ② 为什么需要 invalid region？

因为真实电路有噪声、有延迟、有压降，不可能要求：

- 0 永远严格等于 0V
- 1 永远严格等于某个固定 VDD

因此通常只要求：

$$
V \le V_{L(\max)} \Rightarrow \text{LOW}
$$

$$
V \ge V_{H(\min)} \Rightarrow \text{HIGH}
$$

而中间区域不保证逻辑正确。

*📄 见文末「原始 Slides」第 6 页：HIGH / LOW / Invalid 三段式示意图。*

### ③ 不同技术的 logic level 不同

slides 给了 CMOS 与 TTL 的例子，说明 **logic family(逻辑家族)** 不同，HIGH / LOW 的电平标准也不同。

例如：

- **CMOS**：通常按 VDD 的比例来判定
- **TTL**：则常按固定电压范围判定

这意味着：

> “1 是多少伏？”这个问题**没有通用唯一答案**，要看技术标准和 datasheet。
> 

*📄 见文末「原始 Slides」第 7 页：CMOS / TTL 的 logic level 表格，以及 single-ended / differential signaling 示意。*

### ④ 单端与差分

slides 还展示了两类很常见的传输方式：

- **single-ended signaling(单端信号)**：相对于地参考
- **differential signaling(差分信号)**：看两根线之间的电压差

<aside>
🧠

**差分的核心好处：** 对共模噪声更不敏感，更适合高速 / 长距离传输。

</aside>

- 📚 拓展 — 为什么差分信号更抗干扰？
    
    若两根线同时被外界噪声抬高 0.1V，那么单端信号的判决可能被直接影响；但差分接收器只关心 $V_+ - V_-$，若两边一起抬高，差值几乎不变，因此更稳。这正是 LVDS、USB、PCIe、以太网等高速接口广泛采用差分的原因。
    

## 4️⃣ Digital Waveforms：从“电平”走向“随时间变化的信号”

数字波形不是静止的 0/1，而是 **LOW 和 HIGH 随时间切换** 的过程。

### 正脉冲与负脉冲

- **positive-going pulse(正向脉冲)**：LOW → HIGH → LOW
- **negative-going pulse(负向脉冲)**：HIGH → LOW → HIGH

同时要认识两种边沿：

- **rising / leading edge(上升沿 / 前沿)**
- **falling / trailing edge(下降沿 / 后沿)**

*📄 见文末「原始 Slides」第 8 页：positive-going 与 negative-going pulse 图。*

<aside>
📌

**记忆口诀：** 看波形先看“平”再看“沿”——先分 HIGH/LOW，再看 rising / falling。

</aside>

## 5️⃣ Pulse Definitions：真实脉冲从来不是“方得完美”

理想方波只存在于黑板上；真实世界里的 pulse 会有各种非理想效应。

### ① 常见参数

对于一个 pulse，slides 重点给出这些量：

- **Amplitude(幅度)**：从 base line 到脉冲顶的高度
- **Rise time** $t_r$**(上升时间)**：通常按 10% → 90% 定义
- **Fall time** $t_f$**(下降时间)**：通常按 90% → 10% 定义
- **Pulse width** $t_w$**(脉宽)**：脉冲保持在“有效高电平”附近的时间
- **Base line(基线)**：原始参考电平

### ② 真实波形里的常见失真

- **Overshoot(过冲)**：超过目标电平
- **Undershoot(下冲)**：跌到目标以下
- **Ringing(振铃)**：来回震荡
- **Droop(下垂)**：平台不够平，慢慢掉下去

*📄 见文末「原始 Slides」第 9 页：rise time / fall time / overshoot / ringing / droop 全部标注在一张波形上。*

### 为什么这些量重要？

因为电路不只关心“最后是不是 1”，还关心：

- 什么时候到达 1？
- 能稳定多久？
- 是否会因为过冲 / 振铃误触发别的门？

<aside>
⚠️

**考试和工程里都要记住：** “逻辑值正确” ≠ “时序一定安全”。

</aside>

- 📚 拓展 — rise time 太慢为什么危险？
    
    若上升沿过慢，信号会在 invalid region 停留更久，后级门电路更容易误判或产生额外功耗；同时慢边沿也更容易受噪声影响。这也是高速数字设计里常常要控制 edge rate(边沿速率) 的原因。
    

## 6️⃣ Periodic Pulse Waveforms：周期、频率、时钟

### ① period 与 frequency

对于重复波形：

$$
f = \frac{1}{T},\qquad T = \frac{1}{f}
$$

其中：

- $T$ = **period(周期)**
- $f$ = **frequency(频率)**

slides 的例子：

$$
f = 3.2\ \text{GHz}
\Rightarrow
T = \frac{1}{3.2\times10^9}\approx 313\ \text{ps}
$$

*📄 见文末「原始 Slides」第 10 页：3.2 GHz 对应 313 ps 的例题。*

### ② 时钟 clock 的地位

**clock(时钟)** 是数字系统里最基础的 periodic waveform。

很多时序逻辑不是“随时都响应”，而是：

- 在某个上升沿采样
- 或在某个下降沿更新

因此频率越高，意味着单位时间内可完成更多操作，但也意味着电路必须更快、更稳。

### ③ duty cycle(占空比)

另一个常见参数是：

$$
D = \frac{t_w}{T}
$$

其中 $D$ 是 **duty cycle(占空比)**。

它表示：

> 一个周期内，信号处于有效脉冲状态的比例。
> 

*📄 见文末「原始 Slides」第 11 页：period、pulse width、amplitude、duty cycle 的总图；右上角还有 PWM 控制舵机的例子。*

<aside>
🧠

**占空比直觉：** 周期不变时，脉宽越大，占空比越高；波形“高着”的时间就越久。

</aside>

- 📚 拓展 — 为什么 PWM 能控制舵机或平均功率？
    
    PWM(Pulse Width Modulation, 脉宽调制) 不一定改变振幅，而是通过调节 $t_w$ 或 duty cycle，让接收端看到不同的“平均效果”。这在电机控制、LED 调光、开关电源和舵机控制里都极其常见。
    

## 7️⃣ Timing Diagrams：数字系统真正的“语言”

**timing diagram(时序图)** 用来展示两个或多个数字波形之间的时间关系。

它不是只看某一根线高还是低，而是看：

- 谁先变？
- 谁后变？
- 哪个信号和 clock 对齐？
- 哪些变化有先后依赖？

*📄 见文末「原始 Slides」第 12 页：Clock、A、B、C 多条波形的时序图。*

### 读 timing diagram 的步骤

1. 先找 **time axis(时间轴)**
2. 再找 **clock**
3. 看关键边沿（上升沿 / 下降沿）
4. 再比较其他信号相对这些边沿何时变化

### 为什么 timing diagram 重要？

因为很多数字电路功能不是“静态真值表”能讲清的，而是：

> 只有放到时间维度里，功能才真正成立。
> 

例如寄存器、总线协议、串口收发、读写存储器等，全都要靠 timing diagram 来理解。

<aside>
📌

**口诀：** 真值表回答“是什么”，时序图回答“什么时候发生”。

</aside>

## 8️⃣ Datasheet Example：为什么工程上必须看 AC characteristics？

slides 用 **HV513 datasheet** 举例，提醒一个非常重要的工程事实：

> 实际器件不仅有“功能”，还有**时序约束**。
> 

### Datasheet 里常见的 AC characteristics

会给出类似这些参数：

- clock frequency 上限
- setup time
- hold time
- pulse width
- output delay
- rise / fall time

这些量决定：

- 你能不能把这个器件跑到某个频率
- 输入数据何时必须稳定
- 输出多久以后才可信

*📄 见文末「原始 Slides」第 13 页：HV513 的时序图 + AC electrical characteristics 表格。*

### 这节最关键的工程意识

只会看“逻辑功能图”不够，真正连器件时还必须看 datasheet 的 timing specification(时序规范)。

- 📚 拓展 — setup time / hold time 为什么后面会反复出现？
    
    后续学 flip-flop、register、memory interface、FSM 时，**setup / hold** 会成为时序分析的核心。它们本质上回答的是：
    
    “在某个采样边沿到来之前和之后，输入数据必须稳定多久？”
    
    这也是数字设计从“会画逻辑图”走向“能跑起来”的关键门槛。
    

## 9️⃣ Serial and Parallel Data：串行与并行怎么取舍？

### ① 基本定义

- **Serial transfer(串行传输)**：数据按位一个接一个发送
- **Parallel transfer(并行传输)**：多位同时走多根线发送

*📄 见文末「原始 Slides」第 14 页：computer→modem 的串行图，与 computer→printer 的并行图。*

### ② 各自特点

|  | Serial | Parallel |
| --- | --- | --- |
| 线数 | 少 | 多 |
| 布线复杂度 | 低 | 高 |
| 同步难度 | 相对容易长距离传输 | 多位必须对齐，偏斜(skew)更麻烦 |
| 典型场景 | UART、USB、SPI、I²C、PCIe | SRAM 数据总线、并口、部分片内总线 |

### ③ slides 的例子

- **SRAM: parallel data** —— 因为要同时传多位数据与地址
- **UART: serial data** —— 用更少的线完成设备间通信

*📄 见文末「原始 Slides」第 15 页：SRAM 并行接口与 UART 串行通信板卡示例。*

<aside>
⚖️

**trade-off(权衡)：** 并行不是“总是更快”，串行也不是“总是更省事”。高速系统里，很多现代接口反而偏向少线高速串行，因为并行线一多，时序对齐和布线成本会急剧上升。

</aside>

- 📚 拓展 — 为什么现代高速接口很多都从并行转向串行？
    
    当频率越来越高时，多根并行线之间很难保证完全同步，会出现 **skew(线间偏斜)**、串扰、布线长度不匹配等问题。于是工程上常把“宽并行、低速”转为“窄串行、高速”，再靠更高时钟 / 编码 / 时钟恢复技术把吞吐量补回来。这也是 UART、USB、SATA、PCIe 等接口设计思路的重要背景。
    

## ✅ 本节总结（考前速记）

<aside>
📌

1. **模拟连续，数字离散**；数字系统赢在存储、抗噪、复制与计算。

2. **bit = 电压区间的判决结果**，不是某个唯一精确电压。

3. **波形要看时间参数**：rise / fall / pulse width / period / frequency / duty cycle。

4. **时序图是数字电路的语言**，datasheet 决定器件能否真正稳定工作。

5. **串行省线，并行同时多位**；实际选型永远看距离、速度、同步难度与成本。
</aside>

## 🚀 下次打开第一步

> 先自己回答 3 个问题：① 为什么数字系统比模拟系统更抗噪？② 为什么逻辑 1 不是“唯一某个电压值”？③ 如果频率翻倍，周期会怎样变化？答完这三个，再回看本页会顺很多。
> 

## 📎 原始 Slides

[lecture_1_p2.pdf](EE115B%20Lecture1%20Part2%20%E2%80%94%20Introductory%20Concepts%20%E6%A8%A1%E6%8B%9F%E6%95%B0%E5%AD%97/lecture_1_p2.pdf)
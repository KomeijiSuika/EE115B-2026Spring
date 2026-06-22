# EE115B Lecture3 Part3 — Fixed-Function Logic Gates 74 系列固定功能逻辑门

<aside>
📟

**本节主题：** Fixed-Function Logic Gates —— 74 系列固定功能逻辑门（命名规则、常见 AND / NAND 配置、封装 DIP/SOIC、如何读 datasheet）。

**参考教材：** Floyd《Digital Fundamentals》Ch.3，Figure 3–59（AND）、Figure 3–60（NAND）；datasheet 实例 = **MC54/74HC00A** Quad 2-input NAND。

**核心脉络：** 命名 $74\,\text{xx}\,yy$ → 器件配置（quad / triple / dual / single × N-input）→ 封装（DIP vs SOIC）→ 看懂 datasheet 四张表（Maximum / Recommended / DC / AC）。

</aside>

## 1⃣ 74 系列命名规则 $74\,\text{xx}\,yy$

74 系列是业界标准的**固定功能（fixed-function）逻辑器件**：某种逻辑门已被固化在封装里，拿来即用。型号由两段构成：

- **xx —— 工艺/技术族（technology family）**：决定速度、功耗、电平。
    - `HC` = High-speed CMOS（高速 CMOS）
    - `LS` = Low-power Schottky（低功耗肖特基，属 bipolar / TTL）
- **yy —— 逻辑功能（logic function）**：决定这颗芯片是什么门、几路。
    - 例：`74HC04` = 含 **6 个反相器（hex inverter）** 的 CMOS 器件，`04` 即代表 inverter。

![Slide 3 — 74xxyy 命名规则](EE115B%20Lecture3%20Part3%20%E2%80%94%20Fixed-Function%20Logic%20Gates/slide_3.png)

Slide 3 — 74xxyy 命名规则

<aside>
⚠️

**踩坑：CMOS 与 TTL 阈值不兼容。** HC（CMOS）和 LS（bipolar/TTL）的输入判决阈值不同，直接互连时一方输出的"高/低"可能落进另一方的不确定区导致误判。跨族混用要确认电平兼容或加电平转换。

</aside>

## 2⃣ 常见门器件：AND 与 NAND

同一逻辑功能，74 系列按"**每片几门 × 每门几输入**"提供多种配置。封装统一 14 脚：**VCC = pin 14，GND = pin 7**。

### 2.1 AND 门（Figure 3–59），$Y = A\cdot B$

![Slide 4 — 74 系列 AND 门配置与引脚](EE115B%20Lecture3%20Part3%20%E2%80%94%20Fixed-Function%20Logic%20Gates/slide_4.png)

Slide 4 — 74 系列 AND 门配置与引脚

| 器件号 | 配置 | 含义 |
| --- | --- | --- |
| 74xx08 | Quad 2-input | 4 个 2 输入 AND |
| 74xx11 | Triple 3-input | 3 个 3 输入 AND |
| 74xx21 | Dual 4-input | 2 个 4 输入 AND |

### 2.2 NAND 门（Figure 3–60），$Y = \overline{A\cdot B}$

![Slide 5 — 74 系列 NAND 门配置与引脚](EE115B%20Lecture3%20Part3%20%E2%80%94%20Fixed-Function%20Logic%20Gates/slide_5.png)

Slide 5 — 74 系列 NAND 门配置与引脚

| 器件号 | 配置 | 含义 |
| --- | --- | --- |
| 74xx00 | Quad 2-input | 4 个 2 输入 NAND |
| 74xx10 | Triple 3-input | 3 个 3 输入 NAND |
| 74xx20 | Dual 4-input | 2 个 4 输入 NAND |
| 74xx30 | Single 8-input | 1 个 8 输入 NAND |

<aside>
🧠

**记忆规律：** 总 I/O 端子受可用引脚约束。14 脚封装扣掉 VCC、GND 还剩 12 脚做 I/O，所以"门数 ×(输入+1 输出)"基本把 12 脚用满（如 74xx00：4×(2+1)=12）。后两位 `00 = 四2输入NAND`、`08 = 四2输入AND` 要背下来。

</aside>

## 3⃣ 封装 Packages

![Slide 6 — DIP 与 SOIC 封装尺寸](EE115B%20Lecture3%20Part3%20%E2%80%94%20Fixed-Function%20Logic%20Gates/slide_6.png)

Slide 6 — DIP 与 SOIC 封装尺寸

两种典型 14 脚封装，靠 **pin 1 identifier（圆点 / 缺口 notch）** 定位 1 号脚：

| 封装 | 全称 | 安装方式 | 特点 |
| --- | --- | --- | --- |
| DIP | Dual In-line Package | 通孔 feedthrough（插装） | 引脚间距 0.100 in，体积大，便于手插/面包板 |
| SOIC | Small Outline IC | 表面贴装 surface mount | 引脚间距 0.050 in，体积小、密度高，适合量产 |

## 4⃣ 读懂 Datasheet：MC54/74HC00A（Quad 2-input NAND）

### 4.1 功能、引脚与封装（Slide 7）

逻辑功能 $Y = \overline{A\cdot B}$，与 LS00 引脚兼容。关键特性：

- 驱动能力 **10 LSTTL loads**；输出可直接接 CMOS / NMOS / TTL。
- 工作电压 **2–6 V**，输入电流 ~1 µA，CMOS 高噪声容限。
- 复杂度：**32 FETs / 8 等效门**。
- 4 种封装后缀：`J`=陶瓷、`N`=塑料 DIP、`D`=SOIC、`DT`=TSSOP。

![Slide 7 — HC00A 逻辑图 / 引脚 / 功能表](EE115B%20Lecture3%20Part3%20%E2%80%94%20Fixed-Function%20Logic%20Gates/slide_7.png)

Slide 7 — HC00A 逻辑图 / 引脚 / 功能表

功能表（真值表）：

| A | B | Y |
| --- | --- | --- |
| L | L | H |
| L | H | H |
| H | L | H |
| H | H | L |

### 4.2 Maximum Ratings（极限值，Slide 8）

| 符号 | 参数 | 极限值 | 单位 |
| --- | --- | --- | --- |
| $V_{CC}$ | DC 供电电压 | −0.5 ~ +7.0 | V |
| $V_{in},V_{out}$ | DC 输入/输出电压 | −0.5 ~ $V_{CC}+0.5$ | V |
| $I_{in}$ / $I_{out}$ | 每脚输入/输出电流 | ±20 / ±25 | mA |
| $I_{CC}$ | VCC/GND 脚电流 | ±50 | mA |
| $P_D$ | 功耗（DIP/SOIC/TSSOP） | 750 / 500 / 450 | mW |
| $T_{stg}$ | 存储温度 | −65 ~ +150 | °C |

<aside>
🚨

**Maximum Ratings ≠ 工作区。** 这是"超过就可能永久损坏"的红线，不是正常使用值；实际使用必须落在下面 Recommended Operating Conditions 内。封装还有 derating：如塑料 DIP 在 65°C 以上每升 1°C 需降额 10 mW/°C。

</aside>

### 4.3 Recommended Operating Conditions（推荐工作条件，Slide 9）

| 符号 | 参数 | Min | Max | 单位 |
| --- | --- | --- | --- | --- |
| $V_{CC}$ | 供电电压 | 2.0 | 6.0 | V |
| $V_{in},V_{out}$ | 输入/输出电压 | 0 | $V_{CC}$ | V |
| $T_A$ | 工作温度 | −55 | +125 | °C |
| $t_r,t_f$ | 输入上升/下降时间 @4.5V | 0 | 500 | ns |

注：$t_r,t_f$ 上限随 $V_{CC}$ 变化（2 V→1000 ns，4.5 V→500 ns，6 V→400 ns）：电压越高，对输入边沿越苛刻。

### 4.4 DC Characteristics（直流特性 / 噪声容限，Slide 10）

取最常用的 $V_{CC}=4.5\text{V}$、−55~25°C 档（4 mA 负载）：

| 符号 | 含义 | 限值 @4.5V |
| --- | --- | --- |
| $V_{IH}$ | 最小高电平输入 | ≥ 3.15 V |
| $V_{IL}$ | 最大低电平输入 | ≤ 1.35 V |
| $V_{OH}$ | 最小高电平输出 | ≥ 3.98 V（轻载 20µA 时 4.4 V） |
| $V_{OL}$ | 最大低电平输出 | ≤ 0.26 V（轻载时 0.1 V） |
| $I_{CC}$ | 静态电源电流 | 1.0 µA @25°C |

噪声容限（noise margin）由这些电平算出：

$$
NM_H = V_{OH(min)} - V_{IH(min)}, \qquad NM_L = V_{IL(max)} - V_{OL(max)}
$$

代入 4.5 V（4 mA 负载）：$NM_H = 3.98-3.15 = 0.83\text{V}$，$NM_L = 1.35-0.26 = 1.09\text{V}$；轻载时两者都 ≈ 1.25 V，体现 CMOS 噪声容限大且接近对称。

### 4.5 AC Characteristics（交流/时序，Slide 11）

测试条件 $C_L = 50\text{pF}$、$t_r=t_f=6\text{ns}$：

| 符号 | 含义 | @4.5V |
| --- | --- | --- |
| $t_{PLH},t_{PHL}$ | 传播延迟 A/B→Y（最大） | 15 ns |
| $t_{TLH},t_{THL}$ | 输出转换时间 | 15 ns |
| $C_{in}$ | 输入电容 | 10 pF |
| $C_{PD}$ | 每门功耗等效电容 | 22 pF |

平均工作电流（每门）：

$$
I_{CC(opr)} = C_{PD}\,V_{CC}\,f_{IN} + \frac{I_{CC}}{6}
$$

其中动态部分 $C_{PD}V_{CC}f_{IN}$ 随频率线性增长。传播延迟随 $V_{CC}$ 升高而下降（2 V→75 ns，4.5 V→15 ns，6 V→13 ns）。

<aside>
⚖️

**Trade-off：**$V_{CC}$ **越高越快，但功耗更大。** 动态功耗 $P \approx C_{PD}\,V_{CC}^{2}\,f$ 与电压平方、频率成正比；缩短 $t_{PD}$ 提速是用功耗换来的。

</aside>

## 🎯 本节总结

<aside>
📟

1. **命名** $74\,\text{xx}\,yy$**：** xx=工艺族（HC 高速CMOS / LS 低功耗TTL），yy=逻辑功能；HC 与 LS 阈值不兼容，混接要小心。
2. **配置看后两位：** 00=四2输入NAND、08=四2输入AND、30=单8输入NAND；14 脚封装 VCC=14、GND=7；封装 DIP（插装）vs SOIC（表贴），靠 pin 1 圆点/缺口定位。
3. **Datasheet 四张表：** Maximum Ratings（红线，别超）→ Recommended（实际工作区）→ DC（电平 & 噪声容限 $NM_H=V_{OH}-V_{IH}$）→ AC（延迟；$V_{CC}\!\uparrow$ 更快但 $P\propto V_{CC}^2 f$）。
</aside>

## 📎 原始 Slides

[lecture_3_part3 .pdf](EE115B%20Lecture3%20Part3%20%E2%80%94%20Fixed-Function%20Logic%20Gates/lecture_3_part3_.pdf)
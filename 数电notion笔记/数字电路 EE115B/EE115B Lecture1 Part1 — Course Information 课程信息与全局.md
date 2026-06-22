# EE115B Lecture1 Part1 — Course Information 课程信息与全局导览

<aside>
🧭

**本节主题：** Course Information（课程信息）——为什么要学 digital circuits（数字电路）、这门课在 EE 体系里的位置、课程老师 / 教材 / 评分 / office hour / 资源渠道，以及整门课的章节地图。

**讲义范围：** 本 PDF 对应 **Lecture 1 Part 1**，共 19 页。

**核心脉络：** ① 为什么 digital circuits 无处不在 → ② 很多真实系统其实是 hybrid（混合） → ③ EE115B 在课程链条中的位置 → ④ 课程怎么上、怎么评分、怎么联系老师 → ⑤ 这一学期会依次学哪些章节。

</aside>

## 1️⃣ Why digital circuits：为什么数字电路值得学？

<aside>
💡

**这一节只处理 Lecture1 Part1。** 先锁主线：这部分不是在讲具体公式，而是在建立一整门课的“地图感”。

</aside>

slides 一开头先回答一个最朴素的问题：**为什么要学 digital circuits？**

### ① 数字芯片真的 everywhere(无处不在)

从游戏主机、手机主板，到 CPU、GPU、RAM、Flash，现代电子设备的核心几乎都离不开数字芯片。

- 手机内部有 application processor、memory、interface 芯片
- 计算设备依赖 processor 做 computation(计算)
- RAM / Flash 负责 storage(存储)
- 外设与系统之间还要靠大量数字接口协同工作

*📄 见文末「原始 Slides」第 3–4 页：PlayStation / iPhone 主板实例，以及 Processor / RAM / Flash 的直观例子。*

### ② 为什么这些器件都偏向 digital？

因为数字系统特别擅长：

- **computation(计算)**
- **storage(存储)**
- **communication(通信)**
- **control(控制)**

也就是说，digital circuits 不是某个小方向，而是几乎所有现代电子系统的“通用基础设施”。

<aside>
📌

**一句话记忆：** 学数字电路，不只是为了“会几种门电路”，而是为了理解现代电子系统为什么能被大规模构建、复制、编程和控制。

</aside>

- 📚 拓展 — 为什么数字芯片会成为现代电子系统的中心？
    
    因为数字系统可编程(programmable)、可复制(reproducible)、易集成(scalable)，而且适合用标准化流程进行 IC 设计与制造。换句话说，它不仅是“能工作”，更是“适合工业化大规模做出来”。这也是从手机到服务器都高度依赖数字芯片的根本原因。
    

## 2️⃣ Many Systems are Hybrid：很多真实系统其实不是“纯数字”

slides 特别强调一个很重要的工程观念：

> 很多系统表面看起来是智能设备，内部其实是 **hybrid system(混合系统)**。
> 

### 常见 hybrid 系统例子

- **Robots(机器人)**：机械运动、传感器输入、控制算法、执行器输出同时存在
- **Sensors(传感器系统)**：感知世界往往是 analog，但处理与传输常是 digital
- **MCU with ADC/DAC**：微控制器本体偏数字，但要通过 ADC / DAC 和模拟世界交互
- **Earphones / audio devices**：音频链路里会频繁发生模数 / 数模转换

*📄 见文末「原始 Slides」第 5 页：Robots、Sensors、MCU with ADC/DAC、Earphones 的拼图式示例。*

### 这对学习路径意味着什么？

这门课虽然叫 Digital Circuits，但它并不意味着你以后只看 0 / 1：

- 你仍然要理解 analog world(模拟世界) 的来源
- 也要理解 digital processing(数字处理) 的优势
- 更要学会二者之间如何 interface(接口衔接)

<aside>
🧠

**工程直觉：** 真实世界往往是 analog，计算与控制往往是 digital，产品系统通常是 hybrid。

</aside>

- 📚 拓展 — 为什么 hybrid 视角很重要？
    
    如果只把数字电路当“逻辑门拼图”，就很容易忽略它与传感器、执行器、电源、时钟、接口之间的真实关系。以后学 ADC、DAC、embedded systems、FPGA、board-level design 时，这种 hybrid 视角会越来越重要。
    

## 3️⃣ The position of this course：EE115B 在整个 EE 课程体系里的位置

slides 明确把 EE115B 放进了整个 EE 课程链里。

### 课程链条

- **EE111 Electric Circuits**
- **EE115A Analog Circuits**
    - 进一步走向 **EE112 Analog Integrated Circuits**
- **EE115B Digital Circuits**
    - 进一步走向 **EE113 Digital Integrated Circuits**
    - **Embedded Systems**
    - **FPGA**
    - **Board level circuit design**

*📄 见文末「原始 Slides」第 6 页：EE 课程路径图。*

### 这门课的定位

slides 直接把它称为：

> **A fundamental, EE course**
> 

也就是说，EE115B 不只是“应用小课”，而是很多后续方向的地基。

### 学完后你应该获得什么？

至少会建立起这些基础框架：

- 数字信号如何表示
- 逻辑门与布尔代数如何连接
- 组合逻辑 / 时序逻辑如何区分
- 存储、HDL、信号转换这些主题如何拼成一张完整知识地图

<aside>
📌

**定位口诀：** EE115B = 从“会认 0/1”走向“能读懂数字系统结构”的基础课。

</aside>

## 4️⃣ Course Information：老师、联系方法与基本安排

### 任课老师

- **Course Instructor:** Chenxi Xiao 肖晨曦
- **Office:** SIST 1D-301A
- **Email:** [xiaochx@shanghaitech.edu.cn](mailto:xiaochx@shanghaitech.edu.cn)

### 实验课老师

- **Experimental Course Instructor:** Juan Li 李娟
- **Office:** 1B-204
- **Email:** [lijuan1@shanghaitech.edu.cn](mailto:lijuan1@shanghaitech.edu.cn)

*📄 见文末「原始 Slides」第 7 页：老师信息与课程时间截图。*

### 一个很实际的提醒

课程信息页通常不考概念，但它决定你：

- 遇到问题该找谁
- 什么事该邮件、什么事该群里问
- 实验和理论部分分别由谁负责

<aside>
⚠️

**ADHD 友好提醒：** 老师邮箱、课程支持分工、office hour 这种信息最容易“以为以后再看”，结果真需要时找不到。复习期前最好先把这些入口记熟。

</aside>

## 5️⃣ Textbooks：两本教材各自意味着什么？

slides 给了两本主要教材：

- **Thomas L. Floyd, Digital Fundamentals**
- **阎石《数字电路技术基础》**

*📄 见文末「原始 Slides」第 8 页：两本教材封面。*

### 可能的使用方式

- **Digital Fundamentals**：更偏英文体系、概念组织清晰、例图较多
- **阎石**：中文体系里很经典，适合补基础和查常见题型

### 学习策略建议

如果英文 slides 读起来卡顿，可以：

1. 先看课堂 slides 抓主线
2. 再用中文教材补逻辑链
3. 最后回英文教材认术语与标准表达
- 📚 拓展 — 为什么要同时保留英文术语？
    
    数字电路大量概念在 datasheet、HDL、EDA 工具、英文教材里都会直接出现英文，如 combinational logic、flip-flop、setup time、duty cycle。只记中文容易“会意思但不认识词”，考试、查资料和做工程时都容易卡住。
    

## 6️⃣ Syllabus：这门课学什么，怎么评分？

### 评分构成 Grading Scheme

- **Attendance:** 5%
- **Homework:** 25%
- **Laboratory:** 15%
- **Midterm Exam:** 25%
- **Final Exam:** 30%

*📄 见文末「原始 Slides」第 9 页：grading scheme 与章节总表。*

### 这意味着什么？

从权重看：

- **考试（Midterm + Final）= 55%** → 说明概念体系必须会
- **Homework + Lab = 40%** → 说明不能只听懂，还要会做、会实现
- **Attendance = 5%** → 虽然比重不高，但白送分不要丢

### 成绩说明与 Integrity

slides 还强调：

- **Letter grade is based on ranking**
- **Do not copy other people's homework**
- **Responsible use of tools (Including AI)**

也就是：

1. 成绩不是只看绝对分，还要看排名
2. 工具可以用，但不能代替你的学术责任

*📄 见文末「原始 Slides」第 10 页：Grade 与 Integrity 说明。*

<aside>
🚨

**重点：** “可以用 AI” 不等于“让 AI 替你做作业”。真正安全的用法是：帮你梳理知识、解释概念、找盲点、做复习结构，而不是直接交付作业答案。

</aside>

## 7️⃣ Office Hours：遇到问题找谁？

### 老师 office hour

- **Friday 9:55 am – 10:25 am**
- **Appointment based, immediately after class**

### 课程支持与分工

- **课程支持** — Exams
- **课程支持** — HW1-2
- **课程支持** — Projects
- **课程支持** — HW3-4

且 slides 明确写了：**Send email first**。

*📄 见文末「原始 Slides」第 11 页：office hour 与课程支持信息。*

### 这页信息的真正价值

这其实是在告诉你课程支持系统怎么运转：

- 考试问题找对应支持渠道
- 不同 homework 找不同支持渠道
- project 也有明确负责人

所以问问题前先分类，比“群里乱问一遍”更高效。

<aside>
📌

**实用口诀：** 先判断问题类别，再找对应的人，而不是想到谁就问谁。

</aside>

## 8️⃣ Resources：Blackboard 与 Feishu 各干什么？

slides 把课程资源分成两类：

### Blackboard

- **Official announcements**
- **Publish course slides**
- **Homework submission**

### Feishu Group

- **General, unofficial QA**
- **No important announcements**
- **For grade-related questions, please inquiry via email**

*📄 见文末「原始 Slides」第 12 页：Blackboard 界面与 Feishu 群二维码。*

### 使用策略

这页最值得记的不是二维码，而是**边界**：

- 正式信息 → 看 Blackboard
- 一般问答 → 可去 Feishu
- 成绩相关 → 用 email，不要混在群里

<aside>
🧠

**边界感很重要：** 正式渠道用于正式事务，群聊渠道用于一般交流。这样能减少信息遗漏，也更符合课程规则。

</aside>

## 9️⃣ Course Roadmap：这一学期会学哪些内容？

slides 后半段其实是在给整门课做路线图。

### Chapter 1: Number Systems and Coding

关键词：digital quantity、binary、octal、hex、coding。

这部分建立“数字信息如何表示”的最底层语言。

*📄 见文末「原始 Slides」第 13 页。*

### Chapter 2–3: Boolean Algebra, Logic Circuit Simplification

关键词：

1. **basic logic**
2. **logical expressions**
3. **simplification**

这一段会把门电路与代数表达真正连起来。

*📄 见文末「原始 Slides」第 14 页。*

### Chapter 4: Combinational Logic

核心特征：

> 输出只取决于 **present input(当前输入)**。
> 

典型内容包括：adder、comparator、encoder、decoder、multiplexer，以及减法、乘法、除法等组合功能模块。

*📄 见文末「原始 Slides」第 15 页。*

### Chapter 6: Sequential Logic

核心特征：

> 输出不仅取决于当前输入，还取决于 **history of the input(输入历史)**。
> 

这里会进入 latch、flip-flop、clock 这些真正体现“时间性”的内容。

*📄 见文末「原始 Slides」第 16 页。*

### Chapter 7: Storage

以 SR / JK / D / T flip-flop 为代表，进一步进入数据保持与状态记忆。

*📄 见文末「原始 Slides」第 17 页。*

### Chapter 5: Hardware Description Language

这里会涉及 HDL（slides 图上更接近 VHDL / ModelSim 语境），帮助你从“画逻辑图”走向“用语言描述电路”。

*📄 见文末「原始 Slides」第 18 页。*

### Chapter 8: Signal Conversion

也就是 ADC / DAC，对应模拟世界与数字世界之间的桥梁。

*📄 见文末「原始 Slides」第 19 页。*

### 用一张表快速串起来

| 章节 | 你会学什么 | 核心问题 |
| --- | --- | --- |
| Ch.1 | 数制与编码 | 数字信息怎么表示？ |
| Ch.2–3 | 布尔代数与化简 | 逻辑关系怎么写、怎么简化？ |
| Ch.4 | 组合逻辑 | 当前输入如何直接决定输出？ |
| Ch.6 | 时序逻辑 | 时间与历史如何进入电路？ |
| Ch.7 | 存储 | 状态如何被保存？ |
| Ch.5 | HDL | 如何用语言描述硬件？ |
| Ch.8 | Signal Conversion | 模拟与数字如何互转？ |
- 📚 拓展 — 为什么这份 roadmap 很重要？
    
    ADHD 学习里最容易出现的问题之一就是：学每一节时只见局部，不知道它到底在整门课中扮演什么角色。这个 roadmap 的作用，就是帮你先知道“这块知识以后会接到哪里去”，从而减少“学完一页却不知道自己在干嘛”的失重感。
    

## ✅ 本节总结（开课导航版）

<aside>
📌

1. **EE115B 是地基课**：后面会连到数字集成、嵌入式、FPGA、板级设计。

2. **真实系统往往是 hybrid**：外界常是 analog，处理常是 digital，中间靠 ADC / DAC 等接口连接。

3. **课程成绩不是只靠考试**：Homework、Lab、Midterm、Final 都有明确比重。

4. **课程资源有边界**：Blackboard 看正式信息，Feishu 做一般问答，成绩问题走 email。

5. **整门课路线很清楚**：表示 → 逻辑 → 组合 → 时序 → 存储 → HDL → 信号转换。
</aside>

## 🚀 下次打开第一步

> 先别急着背细节，先自己回答：① EE115B 后面会通向哪些方向？② combinational logic 和 sequential logic 的核心区别是什么？③ Blackboard 和 Feishu 分别该干什么？如果这三个问题能答顺，整门课的地图就立起来了。
> 

## 📎 原始 Slides

[lecture_1_p1.pdf](EE115B%20Lecture1%20Part1%20%E2%80%94%20Course%20Information%20%E8%AF%BE%E7%A8%8B%E4%BF%A1%E6%81%AF%E4%B8%8E%E5%85%A8%E5%B1%80/lecture_1_p1.pdf)

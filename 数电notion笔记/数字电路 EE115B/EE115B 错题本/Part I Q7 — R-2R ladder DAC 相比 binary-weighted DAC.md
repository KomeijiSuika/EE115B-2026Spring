# Part I Q7 — R-2R ladder DAC 相比 binary-weighted DAC 的主要优点

状态: 🔴 待复盘
知识点: R-2R ladder DAC 只用 R、2R 两种阻值 → 电阻匹配(matching)好、易制造，尤其适合集成电路；这才是它对 binary-weighted 的核心优势。binary-weighted 在高位数时需要跨好几个数量级的精密电阻，很难做准。错选 D「infinite resolution」是坑：任何有限位 DAC 分辨率都是有限的 V_ref/2^N，不存在无限分辨率。正确答案 B。
错误类型: 🔀 概念混淆, 🔢 公式/定义记错
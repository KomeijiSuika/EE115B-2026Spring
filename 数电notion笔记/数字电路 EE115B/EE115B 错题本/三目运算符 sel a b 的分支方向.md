# 三目运算符 sel ? a : b 的分支方向

状态: 🔴 待复盘
知识点: C / Verilog conditional operator；sel=1 取 true 分支
错误类型: 🔀 概念混淆, 🔄 方向/顺序写反

<aside>
🎯

**错因定位：** 对 conditional operator（三目运算符）的 true / false 分支方向不够熟。

</aside>

## 原问题

对于 Verilog 或 C 来说，`sel ? a : b`，`sel` 是 1 的时候是取 `a` 吗？

## 正确结论

是的：

```
sel ? a : b
```

含义是：

```
sel 为 true / 1 → 取 a
sel 为 false / 0 → 取 b
```

C 中：

```c
out = sel ? a : b;
```

Verilog 中：

```verilog
assign out = sel ? a : b;
```

## 易错点

- C 里 `sel` 只要非 0，就算 true。
- Verilog 里若 `sel` 是 `1'bx` 或 `1'bz`，输出可能带不确定 `x`，考试基础题先按 `1 → a, 0 → b` 记。

## 复盘口诀

> 问号前面是条件；冒号左边是 true，冒号右边是 false。
>
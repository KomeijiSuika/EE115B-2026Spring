# VHDL signal 赋值符号：<= vs :=

状态: 🔴 待复盘
知识点: VHDL signal assignment / variable assignment / 时序 process
错误类型: 🔀 概念混淆, 🔢 公式/定义记错

<aside>
🎯

**错因定位：** 把 VHDL 的 signal assignment（信号赋值）和其他语言的赋值符号混在一起。

</aside>

## 原问题

VHDL 时序赋值的符号是什么？

## 正确结论

- VHDL 给 **signal** 赋值用 `<=`。
- 时序逻辑通常写在 `process(clk)` 里，用 `rising_edge(clk)` 抓时钟沿。
- **variable** 赋值才用 `:=`。

```vhdl
process(clk)
begin
	if rising_edge(clk) then
		q <= d;
	end if;
end process;
```

## 易错点

- `<=` 在 VHDL 中既可以表示 **signal assignment**，也可以表示“小于等于”，需要靠上下文区分。
- VHDL 的不等号是 `/=`，不是 `!=`。

## 复盘口诀

> VHDL：signal 用 `<=`，variable 用 `:=`；寄存器更新写在 clock edge 里面。
>
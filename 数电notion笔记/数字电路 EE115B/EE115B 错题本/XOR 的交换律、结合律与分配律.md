# XOR 的交换律、结合律与分配律

状态: 🔴 待复盘
知识点: Boolean algebra；XOR commutative / associative；AND distributes over XOR
错误类型: 🔀 概念混淆, 🔢 公式/定义记错

<aside>
🎯

**错因定位：** 把 associative law（结合律）、commutative law（交换律）和 distributive law（分配律）混在一起。

</aside>

## 原问题

XOR 符合交换律、分配律吗？associate law 呢？

## 正确结论

- XOR 满足 **commutative law**（交换律）。
- XOR 满足 **associative law**（结合律）。
- XOR 一般不能随便对 AND / OR 做分配。
- 但 AND 可以对 XOR 分配。

## 关键式子

$$
A \oplus B = B \oplus A
$$

$$
(A \oplus B) \oplus C = A \oplus (B \oplus C)
$$

AND 对 XOR 分配：

$$
A(B \oplus C)=AB \oplus AC
$$

## 反例：XOR 不对 AND 分配

若令 `A = 1, B = 0, C = 1`：

左边：

$$
1 \oplus (0 \cdot 1)=1
$$

右边：

$$
(1 \oplus 0)(1 \oplus 1)=0
$$

左右不等，所以不能这样分配。

## 复盘口诀

> XOR 可以换顺序、改括号；但不要随便展开分配。
>
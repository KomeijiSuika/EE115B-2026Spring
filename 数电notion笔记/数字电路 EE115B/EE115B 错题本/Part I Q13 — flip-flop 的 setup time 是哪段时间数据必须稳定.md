# Part I Q13 — flip-flop 的 setup time 是哪段时间数据必须稳定

状态: 🔴 待复盘
知识点: setup time（建立时间）= 时钟有效边沿『之前』数据必须保持稳定的一段时间；hold time（保持时间）= 边沿『之后』还要继续稳定的一段时间。错选 A『After the active clock edge』= 把 setup 和 hold 记反了。口诀：setup 在前、hold 在后；数据要『早到（setup）+ 不要太早走（hold）』。正确答案 B。
错误类型: 🔀 概念混淆, 🔄 方向/顺序写反
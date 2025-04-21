import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# 假设 data 是你已经读取的数据
# 示例：data = pd.read_excel("your_file.xlsx", header=None)

# 分离头部与数据
header = data.iloc[:2]  # 前两行为列头
body = data.iloc[2:].reset_index(drop=True)

# 填充合并单元格
header.ffill(axis=1, inplace=True)

# 创建多级列索引
multi_cols = pd.MultiIndex.from_arrays(header.values)
body.columns = multi_cols

# 提取 x 轴（第一列）
x = body.iloc[:, 0].astype(float).values
y_data = body.iloc[:, 1:].astype(float)

fig, (ax_low, ax_high) = plt.subplots(
    2, 1,
    sharex=True,
    figsize=(8, 6),
    gridspec_kw={'height_ratios': [1, 3], 'hspace': 0.05}
)

# 设置 y 轴显示范围
ax_low.set_ylim(0, 0.7)
ax_high.set_ylim(0.7, 1.0)

# 画每条线
for label, y in y_dict.items():
    ax_low.plot(x, y, label=label, marker='o')
    ax_high.plot(x, y, marker='o')

# 隐藏高轴底部和低轴顶部的 spines（断轴效果）
ax_high.spines['bottom'].set_visible(False)
ax_low.spines['top'].set_visible(False)

# 添加锯齿线表示断轴（手动画对角线）
d = 0.015
kwargs = dict(transform=ax_low.transAxes, color='k', clip_on=False)
ax_low.plot((-d, +d), (1 - d, 1 + d), **kwargs)
ax_low.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

kwargs.update(transform=ax_high.transAxes)  # 改变参考轴
ax_high.plot((-d, +d), (-d, +d), **kwargs)
ax_high.plot((1 - d, 1 + d), (-d, +d), **kwargs)
fontsize=20
# 图设置
plt.xlabel("Editing Rate", fontsize=fontsize)
plt.xticks(np.arange(x.min(), x.max(), 0.025), fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel("ASR", fontsize=fontsize)
plt.title(y_data.columns[0][0], fontsize=fontsize)  # 第一层（如 KGW）
plt.legend(fontsize=fontsize)
plt.grid(True)
plt.tight_layout()
# plt.show()

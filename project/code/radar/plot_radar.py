import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取原始数据
# data = pd.read_excel("your_file.xlsx", header=None)

# 2. 结构处理
labels = data.iloc[0, 1:].tolist()                  # 每条线的label
dimensions = data.iloc[1:, 0].tolist()              # 维度标签
data_raw = data.iloc[1:, 1:].astype(float)          # 原始数据（不转置）

# 3. 对每一列进行归一化（每个维度单独）
data_normalized = data_raw.copy()
max_per_dimension = data_raw.max(axis=1)
min_per_dimension = data_raw.min(axis=1)

for i in range(data_raw.shape[0]):
    # print(data_raw.iloc[i, :])
    # print(max_per_dimension.iloc[i])
    # data_normalized.iloc[i, :] = (data_raw.iloc[i, :] ) / (max_per_dimension.iloc[i])
    min_t=min_per_dimension.iloc[i]*0.9
    data_normalized.iloc[i, :] = (data_raw.iloc[i, :] -min_t) / (max_per_dimension.iloc[i] -min_t)

# 转置后每行是一个 label 的线
data_plot = data_normalized.values.T

# 4. 角度设置
num_vars = len(dimensions)
angles = np.linspace(np.pi*0.25, 2.25 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

# 5. 画图
show_legend=True  # 是否显示图例
# show_legend=False  # 是否显示图例

if show_legend:
    fig, ax = plt.subplots(figsize=(7.8, 6), subplot_kw=dict(polar=True))
else:
    fig, ax = plt.subplots(figsize=(6.2, 6), subplot_kw=dict(polar=True))

for i, values in enumerate(data_plot):
    values = values.tolist() + [values[0]]  # 闭合
    ax.plot(angles, values, label=str(labels[i]))
    ax.fill(angles, values, alpha=0.05)

# 6. 设置维度标签
ax.set_xticks(angles[:-1])
ax.set_xticklabels(dimensions, fontsize=16)

# 7. 统一极径范围（0-1）但每个维度的原始最大值不同
# ax.set_ylim(0, 1)
# ax.set_yticks([0.25, 0.5, 0.75, 1.0])
# ax.set_yticklabels(['0.25', '0.5', '0.75', '1.0'], fontsize=8)
# ax.set_yticks([])  # 不显示刻度
ax.set_yticklabels([])  # 不显示刻度标签
# ax.yaxis.grid(True) 

# # 可选：打印每个维度的原始最大值
# for angle, dim, max_val in zip(angles, dimensions + [dimensions[0]], max_per_dimension.tolist() + [max_per_dimension.tolist()[0]]):
#     ax.text(angle, 1.1, f"Max={max_val:.2f}", ha='down', va='center', fontsize=8, color='gray')

# 图例不影响图尺寸

if show_legend:
    ax.legend(
        # title="Perturbation",
        loc='upper left',
        bbox_to_anchor=(1.05, 1.0),
        bbox_transform=ax.transAxes,
        frameon=False,
        fontsize=16
    )
plt.title("Unbias",fontsize=18)
plt.tight_layout()
plt.show()

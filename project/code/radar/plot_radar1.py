import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# ========== 1. 读取数据 ==========
# data = pd.read_excel("your_file.xlsx", header=None)
def softmax(x):
    """
    Compute the softmax of a vector or matrix.
    Supports 1D (vector) and 2D (batch of vectors) input.
    """
    import numpy as np
    x = np.array(x)
    
    if x.ndim == 1:
        # 数值稳定性：减去最大值
        x_exp = np.exp(x - np.max(x))
        return x_exp / np.sum(x_exp)
    elif x.ndim == 2:
        # 每行是一个样本
        x_exp = np.exp(x - np.max(x, axis=1, keepdims=True))
        return x_exp / np.sum(x_exp, axis=1, keepdims=True)
    else:
        raise ValueError("Input must be 1D or 2D array.")

# 第一行是模型名，第二行是维度名
model_names = data.iloc[0, 1:].tolist()
dimensions = data.iloc[1, 1:].tolist()
title_models = list(set(model_names))  # 模型名去重

# 第三行开始是扰动强度和数值
perturb_strengths = data.iloc[2:, 0].astype(float).round(2)
values = data.iloc[2:, 1:].astype(float)
data_normalized = values.copy()
max_per_dimension = values.max(axis=1)
min_per_dimension = values.min(axis=1)
# print(values)
for i in range(values.shape[0]):
    # print(values.iloc[i, :])
    # print(max_per_dimension.iloc[i])
    # data_normalized.iloc[i, :] = (data_raw.iloc[i, :] ) / (max_per_dimension.iloc[i])
    # min_t=min_per_dimension.iloc[i]*0.1
    # data_normalized.iloc[i, :] = (values.iloc[i, :] -min_t) / (max_per_dimension.iloc[i] -min_t)
    data_normalized.iloc[i, :] = softmax(values.iloc[i, :]/0.05) 
    # print(data_normalized.iloc[i, :])
values=data_normalized
# 多级列索引：[(model, dimension), ...]
multi_cols = pd.MultiIndex.from_arrays([model_names, dimensions])
values.columns = multi_cols

# 自定义颜色（足够覆盖扰动强度种类）
colors = ['#3480B8', '#9BBF8A', '#FA887B', '#82AFDA', '#F79059', '#AD8DC7', '#FFCC00']
unique_strengths = sorted(perturb_strengths.unique())
color_map = {s: c for s, c in zip(unique_strengths, colors)}

# 雷达图角度设置
dim_names = ['Delete', 'Homoglyph', 'Insertion', 'Swap', 'Typo']
num_dims = len(dim_names)
angles = np.linspace(0, 2 * np.pi, num_dims, endpoint=False).tolist()
angles += angles[:1]  # 闭合

# ========== 2. 画雷达图：每个模型一个图 ==========
fig, axes = plt.subplots(1, len(title_models), figsize=(7 * len(title_models), 6), subplot_kw=dict(polar=True))

if len(title_models) == 1:
    axes = [axes]  # 保证 axes 是列表

for ax, model in zip(axes, title_models):
    y_max = 0  # 每个图单独计算最大 y 值

    for i in range(len(perturb_strengths)):
        strength = round(perturb_strengths.iloc[i], 2)
        raw_values=[]
        min_t=1
        max_t=0
        for dim in dim_names:
            # 提取当前模型和维度的值
            raw_values.append(values[(model, dim)].iloc[i])
            if values[(model, dim)].iloc[i]>max_t:
                max_t=values[(model, dim)].iloc[i]
            if values[(model, dim)].iloc[i]<min_t:
                min_t=values[(model, dim)].iloc[i]
        values_closed = np.array(raw_values + [raw_values[0]])
        # values_closed = (values_closed-min_t)/(max_t-min_t)

        # 更新图最大值
        y_max = max(y_max, max(raw_values))

        # 画雷达线
        color = color_map[strength]
        ax.plot(angles, values_closed, label=f'{strength:.2f}', color=color)
        ax.fill(angles, values_closed, alpha=0.05, color=color)

        # 标出最大值点（用星号）
        max_idx = np.argmax(raw_values)
        max_angle = angles[max_idx]
        max_val = raw_values[max_idx]
        ax.plot(max_angle, max_val, marker='*', color=color, markersize=12, markeredgecolor='black', zorder=10)

    # Y轴设置（自适应最大值）
    y_max *= 1.1  # 留白空间
    ax.set_ylim(0, y_max)
    yticks = np.linspace(0, y_max, 5)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f'{y:.2f}' for y in yticks], fontsize=20)

    # 坐标轴标签 & 标题
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dim_names, fontsize=20)
    ax.set_title(model, size=20, y=1.1)

    # 图例放图外，不影响图尺寸
    # ax.legend(
    #     title="Perturbation",
    #     loc='upper left',
    #     bbox_to_anchor=(1.05, 1.0),
    #     bbox_transform=ax.transAxes,
    #     borderaxespad=0.,
    #     frameon=False,
    #     fontsize=20,
    #     title_fontsize=20
    # )

plt.rcParams['font.size'] = 20
plt.tight_layout()
plt.show()

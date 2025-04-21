import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# 读取数据

# 数据整理
models = data.iloc[0, 1:]
dimensions = data.iloc[1, 1:]
perturb_strengths = data.iloc[2:, 0].astype(float)
values = data.iloc[2:, 1:].astype(float)

# 多级列索引
multi_cols = pd.MultiIndex.from_arrays([models, dimensions])
values.columns = multi_cols

# 模型和维度选择
model_names = ['KGW', 'DIP', 'SynthID', 'Unigram', 'Unbiased']
dim_names = ['Delete', 'Homoglyph', 'ZWC', 'Swap', 'Typo']

# 雷达图角度
num_dims = len(dim_names)
angles = np.linspace(0, 2 * np.pi, num_dims, endpoint=False).tolist()
angles += angles[:1]

# 构建颜色映射
unique_strengths = perturb_strengths.unique()

cmap1 = ['#3480B8','#9BBF8A', '#FA887B', '#82AFDA',  '#F79059', '#82AFDA',  '#F79059']#cm.get_cmap('viridis', len(unique_strengths))
color_map={}
for i, strength in enumerate(sorted(unique_strengths)):
    color_map[strength]=cmap1[i]
# color_map = {strength: cmap1(i) for i, strength in enumerate(sorted(unique_strengths))}

# 画图
fig, axes = plt.subplots(1, 5, figsize=(25, 5), subplot_kw=dict(polar=True))

for ax, model in zip(axes, model_names):
    for i, strength in enumerate(perturb_strengths):
        data_l=[]
        for dim in dim_names:
            data_l.append(values[model][dim])
        data_l += data_l[:1]
        color = color_map[strength]
        ax.plot(angles, data_l, label=f'{strength:.2f}', color=color)
        # ax.fill(angles, data_l, alpha=0.05, color=color)

    ax.set_title(model, size=14, y=1.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dim_names, fontsize=9)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['0', '0.25', '0.5', '0.75', '1.0'], fontsize=8)

# 绘制统一图例（只画一次）
handles=[]
for s in sorted(unique_strengths):
    handles.append(plt.Line2D([0], [0], color=color_map[s], label=f'{s:.2f}'))
# handles = [plt.Line2D([0], [0], color=color_map[s], label=f'{s:.2f}') for s in sorted(unique_strengths)]
fig.legend(handles=handles, title="Perturb strength", loc='upper right', bbox_to_anchor=(1.12, 1.0))

plt.tight_layout()
plt.show()

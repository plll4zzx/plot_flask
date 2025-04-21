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

# 画图
plt.figure(figsize=(8, 6))
markers = ['o', 's', 'D', '^', 'v']
y_max=0
for idx, col in enumerate(y_data.columns):
    label = col[1]  # 第二层是 "Delete" 等类型
    linewidth=2
    if label=='Homoglyph':
        linewidth=4
    plt.plot(x, y_data[col], label=label, linewidth=linewidth, marker=markers[idx])
    if  y_data[col].max()>y_max:
        y_max= y_data[col].max()
fontsize=20
# 图设置
plt.xlabel("Editing Rate", fontsize=fontsize)
plt.xticks(np.arange(x.min(), x.max(), 0.025), fontsize=fontsize)
if y_max>0.7:
    sparse_ticks = [0.2, 0.45, 0.7]       # 小于 0.7 的稀疏刻度
    dense_ticks = np.arange(0.7, 1.01, 0.1)  # 大于等于 0.7 的密集刻度
    all_ticks = sparse_ticks + dense_ticks.tolist()
    
    plt.yticks(all_ticks, fontsize=fontsize)
else:
    plt.yticks(fontsize=fontsize)
plt.ylabel("ASR", fontsize=fontsize)
plt.title(y_data.columns[0][0], fontsize=fontsize)  # 第一层（如 KGW）
plt.legend(fontsize=fontsize)
plt.grid(True)
plt.tight_layout()
# plt.show()

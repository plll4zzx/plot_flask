
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# 前两行是表头数据
header_data = data.iloc[:2].copy()

# 数据从第三行开始
data_data = data.iloc[2:].reset_index(drop=True)

# 填充合并单元格产生的NaN（前向填充）
header_data.ffill(axis=1, inplace=True)

# 创建多级索引
multi_columns = pd.MultiIndex.from_arrays(header_data.values)

# 将多级索引赋值给数据部分
data_data.columns = multi_columns

# 检查结构
print(data_data.head())

# 提取第一列 (editing_distance)
editing_distance = data_data.iloc[:, 0].astype(float).to_numpy()

# wm_names = data_data.columns.levels[0][1:].tolist()
wm_names = ['KGW','Unigram','SynthID','Unbiased','DIP']#data_data.columns.levels[0][1:].tolist()
# 其他数据保存到字典
data_dict = {}
for first_key in wm_names:  # 跳过第一列
    data_dict[first_key] = {}
    for second_key in ['token', 'char']:
        data_dict[first_key][second_key] = data_data[(first_key, second_key)].astype(float).to_numpy()

# 输出结果验证
print("Editing Distance:\n", editing_distance)
print("\nData Dictionary:\n", data_dict)

# 调整为灰色调的颜色列表
colors = ['#3480B8','#9BBF8A', '#FA887B', '#82AFDA',  '#F79059']
markers = ['o', 's', '*', 'D', 'x']
# wm_names = data_data.columns.levels[0][1:].tolist()
fig = plt.figure(figsize=(12, 10))
y_positions = np.arange(len(wm_names))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=20, azim=290)
for idx, (first_key, second_dict) in enumerate(data_dict.items()):
    color = colors[idx % len(colors)]
    marker = markers[idx % len(markers)]
    xs = editing_distance
    ys = np.full_like(xs, y_positions[idx])  # 固定在某一Y轴位置
    y_token = second_dict['token']
    y_char = second_dict['char']
    ax.plot(xs, ys, y_token, 
             linestyle='--', linewidth=1.5, markersize=6,
             color=color, alpha=0.5, label=f"{first_key}-token")
    ax.plot(xs, ys, y_char, 
             linestyle='-', linewidth=3, markersize=9,
             color=color, alpha=0.7, label=f"{first_key}-char")
    # ax.plot(xs, ys, np.zeros_like(y_char), color=color, linestyle='dashed', alpha=0.7, label='Shadow')
    verts1 = [list(zip(xs, ys, y_char)) + list(zip(xs[::-1], ys[::-1], y_token[::-1]))]
    poly1 = Poly3DCollection(verts1, color=color, alpha=0.5, edgecolor='none')
    ax.add_collection3d(poly1)
    verts2 = [list(zip(xs, ys, y_token)) + list(zip(xs[::-1], ys[::-1], np.zeros_like(y_token)))]
    poly2 = Poly3DCollection(verts2, color=color, alpha=0.1, edgecolor='none')
    ax.add_collection3d(poly2)


# 图例、坐标轴标签和网格
ax.set_xlabel("Editing Distance", fontsize=14)
ax.set_yticks(np.arange(5))
#+['','']
print(wm_names)
ax.set_yticklabels(wm_names)
ax.set_zlabel("ASR")
plt.rcParams['font.size'] = 16
plt.tight_layout()

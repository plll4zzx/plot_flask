

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

# 其他数据保存到字典
data_dict = {}
for first_key in data_data.columns.levels[0][1:]:  # 跳过第一列
    data_dict[first_key] = {}
    for second_key in ['token', 'char']:
        data_dict[first_key][second_key] = data_data[(first_key, second_key)].astype(float).to_numpy()

# 输出结果验证
print("Editing Distance:\n", editing_distance)
print("\nData Dictionary:\n", data_dict)

# 定义颜色和marker的循环列表
colors = ['b', 'g', 'r', 'c', 'm', 'y']
markers = ['o', 's', 'D', '^', 'v', 'P']

plt.figure(figsize=(10, 6))

# 遍历绘制数据
for idx, (first_key, second_dict) in enumerate(data_dict.items()):
    color = colors[idx % len(colors)]     # 按顺序选择颜色
    marker = markers[idx % len(markers)]  # 按顺序选择marker
    
    for second_key, y_data in second_dict.items():
        linestyle = '--' if second_key == 'token' else '-'  # token虚线, char实线
        label = f"{first_key}-{second_key}"
        
        plt.plot(editing_distance, y_data,
                 linestyle=linestyle,
                 color=color,
                 marker=marker,
                 label=label)

# 图例和坐标轴
plt.xlabel("Editing Distance", fontsize=14)
plt.ylabel("Value", fontsize=14)
plt.title("Editing Distance vs Metrics", fontsize=14)
plt.grid(True)
plt.legend(loc="lower right")
plt.tight_layout()
plt.title("Editing Distance vs Metrics", fontsize=14)
plt.grid(True)
plt.legend(loc="lower right")
plt.tight_layout()
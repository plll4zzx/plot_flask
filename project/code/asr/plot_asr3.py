

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


colors = ['#3480B8','#9BBF8A', '#FA887B', '#82AFDA',  '#F79059']
# colors = ['#3480B8', '#9BBF8A', 'red', 'purple', '#F79059']
markers = ['o', 's', 'D', '^', 'v']
tittle='OPT'
tittle='LLaMA'
if tittle=='LLaMA':
   show_legend=True
else:
    show_legend=False

if show_legend:
    plt.figure(figsize=(11.1, 6))
else:
    plt.figure(figsize=(7.9, 6))

for idx, (first_key, second_dict) in enumerate(data_dict.items()):
    color = colors[idx % len(colors)]
    marker = markers[idx % len(markers)]
    
    x = editing_distance
    y_token = second_dict['token']
    y_char = second_dict['char']

    # token 曲线（灰色虚线）
    plt.plot(x, y_token, 
             linestyle='--', linewidth=3, marker=marker, markersize=9,
             color=color, alpha=0.7, label=f"{first_key}-token")

    # char 曲线（灰色实线）
    plt.plot(x, y_char, 
             linestyle='-', linewidth=3, marker=marker, markersize=9,
             color=color, alpha=0.9, label=f"{first_key}-char")

    # 使用细斜线填充阴影区域 (hatch='///')
    plt.fill_between(x, y_token, y_char, 
                     facecolor=color, alpha=0.15,
                     hatch='///', edgecolor=color, linewidth=0)

# 控制图例
fontsize=20
if show_legend:
    plt.legend(
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        bbox_transform=plt.gca().transAxes,
        frameon=False,
        fontsize=fontsize,
        # title="Legend"
    )
plt.xlabel("Text Length", fontsize=fontsize)
plt.ylabel("ASR", fontsize=fontsize)
plt.title(tittle, fontsize=fontsize)
plt.rcParams['font.size'] = fontsize
plt.grid(True)
plt.tight_layout()

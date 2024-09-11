import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 准备数据
data = {
    'Country': ['China', 'Canada', 'United States of America', 'South Korea'],
    'Species_Count': [32, 31, 4, 8]
}

df = pd.DataFrame(data)

# 加载世界地图数据
world = gpd.read_file('/Users/nannan/Desktop/soft/packages/Natural_Earth_quick_start/110m_cultural/ne_110m_admin_0_countries.shp')

# 确保国家名称匹配
world = world.rename(columns={'NAME': 'Country'})

# 手动检查并更新台湾的名称匹配
world.loc[world['Country'] == 'Taiwan', 'Country'] = 'China'

# 合并数据
world_data = world.merge(df, on='Country', how='left')

# 设置默认值为0
world_data['Species_Count'] = world_data['Species_Count'].fillna(0)

# 创建一个新的列来区分这四个国家
world_data['highlight'] = world_data['Species_Count'] > 0

# 设置绘图参数
fig, ax = plt.subplots(1, 1, figsize=(15, 10))

# 绘制背景地图（其他国家为白色）
world.boundary.plot(ax=ax, color='black', linewidth=0.5)
world.plot(ax=ax, color='#d3d3d3', edgecolor='black', linewidth=0.5)

# 定义四个国家的颜色
colors = {
    'China': '#DB4D47',
    'Canada': '#A1752D',
    'United States of America': '#F59132',
    'South Korea': '#9CD0A2'
}

# 绘制四个国家（使用不同的颜色）
for country, color in colors.items():
    world_data[world_data['Country'] == country].plot(ax=ax, color=color, edgecolor='black', linewidth=0.5)

# 移除坐标轴
ax.set_axis_off()

# 添加标题
plt.title('Species Distribution by Country')

# 创建内嵌图框并绘制饼图（嵌入左下区域）
ax_inset = inset_axes(ax, width="30%", height="30%", bbox_to_anchor=(0.00, 0.2, 1.1, 1.1), bbox_transform=ax.transAxes, loc='lower left')
sizes = df['Species_Count']
labels = df['Country']
color_values = [colors[country] for country in labels]
ax_inset.pie(sizes, labels=labels, colors=color_values, autopct=lambda pct: f'{pct:.1f}%', startangle=140, textprops={'fontsize': 7})

# 确保饼图为圆形
ax_inset.axis('equal')

# 显示地图和嵌入的饼图
plt.show()

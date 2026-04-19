import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pvlib
from shapely.geometry import Polygon
from shapely.ops import unary_union
from matplotlib.patches import Polygon as MplPolygon
from datetime import datetime
import pytz
from pylab import mpl

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False
# —— 1. 参数设置 同前 —— #

latitude, longitude = 27.99, 120.67
tz = 'Asia/Shanghai'
floor_height = 3
n_floors = 6
total_height = floor_height * n_floors

half_x, half_y = 12/2, 9/2
base = Polygon([(-half_x, -half_y), ( half_x, -half_y),
                ( half_x,  half_y), (-half_x,  half_y)])

# —— 2. 生成时间点 —— #
date = pd.Timestamp('2025-05-19', tz=tz)
times = pd.date_range(date.replace(hour=5), date.replace(hour=19),
                      freq='1H', tz=tz)

# —— 3. 计算太阳位置 —— #
solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude)
solpos = solpos[solpos['apparent_elevation'] > 0]

# —— 4. 绘图 —— #
fig, ax = plt.subplots(figsize=(8,8))

# 先画建筑底面
base_patch = MplPolygon(np.array(base.exterior.coords),
                        closed=True,
                        facecolor='lightgrey', edgecolor='black', alpha=0.3)
ax.add_patch(base_patch)

for idx, row in solpos.iterrows():
    elev = np.deg2rad(row['apparent_elevation'])
    azim = np.deg2rad(row['azimuth'])
    d = total_height / np.tan(elev)
    dx = -d * np.sin(azim)
    dy = -d * np.cos(azim)

    # 生成阴影多边形
    shadow_poly = Polygon([(x+dx, y+dy) for x,y in base.exterior.coords])
    # 合并并取凸包避免自交
    shadow = unary_union([base, shadow_poly]).convex_hull

    # 如果是 MultiPolygon，就逐个画；否则直接画
    geoms = shadow.geoms if shadow.geom_type=='MultiPolygon' else [shadow]
    for geom in geoms:
        patch = MplPolygon(np.array(geom.exterior.coords),
                           closed=True,
                           facecolor='orange', edgecolor=None, alpha=0.2)
        ax.add_patch(patch)

    # 可选：在图中央标注时间
    cx, cy = base.centroid.coords[0]
    ax.text(cx, cy, idx.strftime('%H:%M'),
            ha='center', va='center', fontsize=8, color='brown')

# —— 5. 美化 —— #
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_title('2025-05-19 建筑阴影日照分析图（1h 间隔）')
ax.set_aspect('equal')
ax.grid(True)
plt.show()

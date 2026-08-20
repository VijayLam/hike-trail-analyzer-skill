"""Generate SVG visualizations for the GPX track PPT."""
import json, math, sys, os

# ---- Data ----
map_points = [[113.285232, 23.175979], [113.28628, 23.175965], [113.287142, 23.175609], [113.287006, 23.174768], [113.286592, 23.173765], [113.285616, 23.173775], [113.286605, 23.173277], [113.28769, 23.173911], [113.288424, 23.174569], [113.289553, 23.174931], [113.290949, 23.174875], [113.291843, 23.174767], [113.291882, 23.173627], [113.292011, 23.172635], [113.292528, 23.171774], [113.29296, 23.171161], [113.294101, 23.171157], [113.295294, 23.171134], [113.296393, 23.170684], [113.297242, 23.169852], [113.297769, 23.168834], [113.298284, 23.167798], [113.298899, 23.166899], [113.299845, 23.166456], [113.300453, 23.165861], [113.300625, 23.164945], [113.300993, 23.163944], [113.302157, 23.163743], [113.301717, 23.164224], [113.301787, 23.165062], [113.301679, 23.166148], [113.301689, 23.167199], [113.302546, 23.167352], [113.302986, 23.166345], [113.303542, 23.167124], [113.303548, 23.168194], [113.303001, 23.168672], [113.302577, 23.169299], [113.303452, 23.169893], [113.302602, 23.170557], [113.301712, 23.170691], [113.300808, 23.170409], [113.300211, 23.170322], [113.299793, 23.170611], [113.298747, 23.171058], [113.297709, 23.17147], [113.297018, 23.172343], [113.296432, 23.173225], [113.296168, 23.174063], [113.295611, 23.175018], [113.295067, 23.175873], [113.295624, 23.176458], [113.29643, 23.176857], [113.297599, 23.176632], [113.298368, 23.177136], [113.2986, 23.17776], [113.299674, 23.177652], [113.300898, 23.177736], [113.301349, 23.178736], [113.30134, 23.179678], [113.301382, 23.180687], [113.30074, 23.181718], [113.299769, 23.182307], [113.29892, 23.182565], [113.298478, 23.183727], [113.297496, 23.18434], [113.297745, 23.185318], [113.298291, 23.185996], [113.29819, 23.186881], [113.298467, 23.187764], [113.29872, 23.18791], [113.298046, 23.187696], [113.297084, 23.187752], [113.295978, 23.187445], [113.294849, 23.187908], [113.294115, 23.187449], [113.293417, 23.187043], [113.292678, 23.188058], [113.292181, 23.189071], [113.292668, 23.190083], [113.292218, 23.191088], [113.291619, 23.192058], [113.292567, 23.19241], [113.293348, 23.192879], [113.293265, 23.193833], [113.293232, 23.19496], [113.293563, 23.195866], [113.293805, 23.196743], [113.294536, 23.196167], [113.295252, 23.195617], [113.295429, 23.194621], [113.295564, 23.193663], [113.29524, 23.192623], [113.296132, 23.192416], [113.295838, 23.191391], [113.296559, 23.19184], [113.297166, 23.191809], [113.297597, 23.190874], [113.297717, 23.189811], [113.298317, 23.188911], [113.298956, 23.188494], [113.298915, 23.188301], [113.299017, 23.189322], [113.298453, 23.190287], [113.299138, 23.190906], [113.300337, 23.191107], [113.301325, 23.190471], [113.302485, 23.190215], [113.303491, 23.189518], [113.304083, 23.18969], [113.303673, 23.190343], [113.303145, 23.19036], [113.303315, 23.191217], [113.302172, 23.19139], [113.301272, 23.19194], [113.300491, 23.192717], [113.301244, 23.19234], [113.301741, 23.193279], [113.302541, 23.194179], [113.302198, 23.194965], [113.302003, 23.196025], [113.301207, 23.195631], [113.30119, 23.194779], [113.302165, 23.195091], [113.301856, 23.196128], [113.301798, 23.197], [113.301959, 23.198078], [113.303003, 23.198579], [113.303072, 23.19966], [113.302996, 23.200453], [113.30217, 23.200716], [113.301587, 23.19971], [113.300715, 23.199664], [113.300853, 23.200728], [113.300412, 23.200945], [113.29981, 23.200107], [113.29923, 23.20103], [113.298114, 23.20104], [113.297648, 23.200106], [113.296538, 23.19971], [113.296721, 23.199297], [113.297819, 23.198937], [113.297589, 23.197958], [113.297122, 23.196951], [113.297008, 23.196372], [113.296276, 23.197284], [113.295531, 23.198191], [113.294537, 23.198838], [113.293343, 23.199253], [113.292119, 23.199559], [113.290877, 23.199717], [113.290252, 23.199348], [113.290012, 23.198643], [113.290157, 23.197704], [113.289755, 23.196976], [113.289889, 23.196009], [113.289785, 23.195313], [113.288893, 23.195103], [113.288136, 23.195936], [113.288473, 23.196884], [113.287796, 23.197736], [113.286954, 23.197684], [113.286403, 23.196804]]

elev_points = [[0.0, 30.0], [0.27, 33.0], [0.54, 44.0], [0.81, 55.0], [1.08, 65.0], [1.35, 72.0], [1.62, 80.0], [1.89, 88.0], [2.16, 95.0], [2.43, 100.0], [2.7, 103.0], [2.97, 105.0], [3.24, 100.0], [3.51, 95.0], [3.78, 90.0], [4.05, 85.0], [4.32, 80.0], [4.59, 75.0], [4.86, 70.0], [5.13, 65.0], [5.4, 60.0], [5.67, 70.0], [5.94, 85.0], [6.21, 100.0], [6.48, 115.0], [6.75, 130.0], [7.02, 145.0], [7.29, 160.0], [7.56, 175.0], [7.83, 190.0], [8.1, 205.0], [8.37, 220.0], [8.64, 235.0], [8.91, 250.0], [9.18, 265.0], [9.45, 280.0], [9.72, 295.0], [9.99, 310.0], [10.26, 325.0], [10.53, 336.0], [10.8, 330.0], [11.07, 320.0], [11.34, 305.0], [11.61, 290.0], [11.88, 275.0], [12.15, 260.0], [12.42, 245.0], [12.69, 230.0], [12.96, 215.0], [13.23, 200.0], [13.5, 185.0], [13.77, 170.0], [14.04, 155.0], [14.31, 140.0], [14.58, 125.0], [14.85, 110.0], [15.12, 95.0], [15.39, 80.0], [15.66, 65.0], [15.93, 50.0], [16.2, 45.0], [16.47, 50.0], [16.74, 55.0], [17.01, 60.0], [17.28, 65.0], [17.55, 70.0], [17.82, 75.0], [18.09, 80.0], [18.36, 85.0], [18.63, 90.0], [18.9, 95.0], [19.17, 100.0], [19.44, 110.0], [19.71, 125.0], [19.98, 140.0], [20.25, 155.0], [20.52, 170.0], [20.79, 185.0], [21.06, 200.0], [21.33, 215.0], [21.6, 230.0], [21.87, 245.0], [22.14, 260.0], [22.41, 275.0], [22.68, 290.0], [22.95, 305.0], [23.22, 320.0], [23.49, 335.0], [23.76, 330.0], [24.03, 325.0], [24.3, 320.0], [24.57, 315.0], [24.84, 310.0], [25.11, 305.0], [25.38, 295.0], [25.65, 280.0], [25.92, 265.0], [26.19, 250.0], [26.46, 235.0], [26.73, 220.0], [27.0, 200.0], [27.1, 180.0]]

slope_data = [
    {"range": "0~5km", "slope": -41, "desc": "J徒下坡"},
    {"range": "5~9km", "slope": 40, "desc": "J徒上坡"},
    {"range": "9~14km", "slope": -60, "desc": "陡坡急降"},
    {"range": "14~19km", "slope": -25, "desc": "平缓下坡"},
    {"range": "19~23km", "slope": 51, "desc": "陡坡急升"},
    {"range": "23~28km", "slope": 65, "desc": "陡坡急升"},
]

service_pts_svg = [
    {"km": 17, "name": "卫生间", "lon": 113.30059, "lat": 23.201173},
    {"km": 18, "name": "卫生间", "lon": 113.296901, "lat": 23.199224},
    {"km": 19, "name": "卫生间", "lon": 113.294974, "lat": 23.198594},
    {"km": 25, "name": "补给点", "lon": 113.295945, "lat": 23.182322},
]

# ====== Track Map SVG ======
lons = [p[0] for p in map_points]
lats = [p[1] for p in map_points]
min_lon, max_lon = min(lons), max(lons)
min_lat, max_lat = min(lats), max(lats)

W, H = 680, 500
margin = 40
draw_w = W - 2 * margin
draw_h = H - 2 * margin

lon_range = max_lon - min_lon or 0.001
lat_range = max_lat - min_lat or 0.001
scale = min(draw_w / lon_range, draw_h / lat_range)
offset_x = margin + (draw_w - lon_range * scale) / 2
offset_y = margin + (draw_h - lat_range * scale) / 2

def project(lon, lat):
    x = offset_x + (lon - min_lon) * scale
    y = offset_y + (max_lat - lat) * scale
    return x, y

path_d = []
for i, (lon, lat) in enumerate(map_points):
    x, y = project(lon, lat)
    if i == 0:
        path_d.append("M%.1f,%.1f" % (x, y))
    else:
        path_d.append("L%.1f,%.1f" % (x, y))
path_str = " ".join(path_d)

sx, sy = project(map_points[0][0], map_points[0][1])
ex, ey = project(map_points[-1][0], map_points[-1][1])

grid_x = "".join('<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (margin + i * draw_w // 8, margin, margin + i * draw_w // 8, H - margin) for i in range(9))
grid_y = "".join('<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (margin, margin + i * draw_h // 6, W - margin, margin + i * draw_h // 6) for i in range(7))

# Direction arrows
arrows_svg = ""
for frac in [0.3, 0.65]:
    idx = int(len(map_points) * frac)
    if idx + 1 < len(map_points):
        x1, y1 = project(*map_points[idx])
        x2, y2 = project(*map_points[idx + 1])
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        arrows_svg += '<g transform="translate(%.1f,%.1f) rotate(%.0f)"><polygon points="0,-4 8,0 0,4" fill="#1a4d0f"/></g>\n' % (x1, y1, angle)

# Service points
svc_svg = ""
for sp in service_pts_svg:
    wx, wy = project(sp["lon"], sp["lat"])
    color = "#3b82f6" if "卫生间" in sp["name"] else "#f59e0b"
    svc_svg += '<circle cx="%.1f" cy="%.1f" r="4" fill="%s" stroke="white" stroke-width="1.5"/>\n' % (wx, wy, color)

svg_map = '''<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%%" stop-color="#f0f4ed"/>
      <stop offset="100%%" stop-color="#e2e8d5"/>
    </linearGradient>
    <filter id="shadow" x="-20%%" y="-20%%" width="140%%" height="140%%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
      <feOffset dx="0" dy="2"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.3"/></feComponentTransfer>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="%d" height="%d" fill="url(#bgGrad)" rx="12"/>
  <g stroke="#d0d8c0" stroke-width="0.5" opacity="0.4">%s%s</g>
  <path d="%s" fill="none" stroke="#2d5016" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" opacity="0.15" transform="translate(2,2)"/>
  <path d="%s" fill="none" stroke="#2d6a3e" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
  %s
  <circle cx="%.1f" cy="%.1f" r="7" fill="#22c55e" stroke="white" stroke-width="2" filter="url(#shadow)"/>
  <text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">起点</text>
  <circle cx="%.1f" cy="%.1f" r="7" fill="#ef4444" stroke="white" stroke-width="2" filter="url(#shadow)"/>
  <text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" font-weight="bold" fill="#dc2626">终点</text>
  %s
  <text x="%d" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#2d5016">白云山画龙 - 轨迹路线图</text>
  <g transform="translate(%d, %d)">
    <circle cx="6" cy="0" r="4" fill="#22c55e" stroke="white" stroke-width="1.5"/>
    <text x="14" y="3" font-size="9" fill="#555">起点</text>
    <circle cx="50" cy="0" r="4" fill="#ef4444" stroke="white" stroke-width="1.5"/>
    <text x="58" y="3" font-size="9" fill="#555">终点</text>
    <circle cx="94" cy="0" r="3" fill="#3b82f6"/>
    <text x="102" y="3" font-size="9" fill="#555">卫生间</text>
    <circle cx="140" cy="0" r="3" fill="#f59e0b"/>
    <text x="148" y="3" font-size="9" fill="#555">补给点</text>
  </g>
  <text x="%d" y="%d" text-anchor="end" font-size="9" fill="#888">GPX轨迹 - %d采样点</text>
</svg>''' % (
    W, H, W, H, grid_x, grid_y, path_str, path_str, arrows_svg,
    sx, sy, sx, sy - 14,
    ex, ey, ex, ey - 14,
    svc_svg,
    W // 2, margin, H - 18,
    W - margin, H - 18, len(map_points)
)

# ====== Elevation Profile SVG ======
EW, EH = 680, 340
eml, emr, emt, emb = 45, 20, 35, 40
edw = EW - eml - emr
edh = EH - emt - emb

max_km = max(p[0] for p in elev_points)
min_elev = min(p[1] for p in elev_points)
max_elev = max(p[1] for p in elev_points)
elev_range = max_elev - min_elev

def proj_e(km, elev):
    x = eml + (km / max_km) * edw
    y = emt + (1 - (elev - min_elev) / elev_range) * edh
    return x, y

area_d = []
line_d = []
for km, elev in elev_points:
    x, y = proj_e(km, elev)
    area_d.append("%.1f,%.1f" % (x, y))
    line_d.append("%.1f,%.1f" % (x, y))

bx0, by0 = proj_e(0, min_elev)
bx1, by1 = proj_e(max_km, min_elev)
area_str = "M" + " L".join(area_d) + " L%.1f,%.1f L%.1f,%.1f Z" % (bx1, by1, bx0, by0)
line_str = "M" + " L".join(line_d)

y_labels = []
elev_start = int(min_elev // 50) * 50
elev_end = int(max_elev // 50 + 1) * 50
for e in range(elev_start, elev_end + 1, 50):
    _, y = proj_e(0, e)
    y_labels.append((y, e))

x_labels = []
for km in range(0, int(max_km) + 1, 5):
    x, _ = proj_e(km, min_elev)
    x_labels.append((x, km))

grid_lines_e = "".join('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (eml, y, EW - emr, y) for y, _ in y_labels)
y_axis_text = "".join('<text x="%d" y="%.1f" text-anchor="end" font-size="9" fill="#888">%dm</text>' % (eml - 6, y + 3, e) for y, e in y_labels)
x_axis_text = "".join('<text x="%.1f" y="%d" text-anchor="middle" font-size="9" fill="#888">%dkm</text>' % (x, EH - emb + 16, km) for x, km in x_labels)

mx, my = proj_e(10.53, 336)

svg_elev = '''<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="elevGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%%" stop-color="#86b964" stop-opacity="0.7"/>
      <stop offset="100%%" stop-color="#4a7c32" stop-opacity="0.2"/>
    </linearGradient>
  </defs>
  <rect width="%d" height="%d" fill="#fafbf7" rx="12"/>
  <text x="%d" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#2d5016">海拔剖面图</text>
  <g stroke="#e0e5d5" stroke-width="0.5">%s</g>
  <g font-size="9" fill="#888">%s</g>
  <g font-size="9" fill="#888">%s</g>
  <path d="%s" fill="url(#elevGrad)"/>
  <path d="%s" fill="none" stroke="#2d6a3e" stroke-width="2" stroke-linejoin="round"/>
  <circle cx="%.1f" cy="%.1f" r="3.5" fill="#ef4444" stroke="white" stroke-width="1.5"/>
  <text x="%.1f" y="%.1f" text-anchor="middle" font-size="9" font-weight="bold" fill="#dc2626">最高 336m</text>
  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#999" stroke-width="1"/>
  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#999" stroke-width="1"/>
  <text x="15" y="%d" text-anchor="middle" font-size="10" fill="#666" transform="rotate(-90, 15, %d)">海拔 (m)</text>
  <text x="%d" y="%d" text-anchor="middle" font-size="10" fill="#666">距离 (km)</text>
</svg>''' % (
    EW, EH, EW, EH, EW // 2,
    grid_lines_e, y_axis_text, x_axis_text,
    area_str, line_str,
    mx, my, mx, my - 10,
    eml, emt, eml, EH - emb,
    eml, EH - emb, EW - emr, EH - emb,
    EH // 2, EH // 2,
    EW // 2, EH - 5
)

# ====== Slope Segment Chart SVG ======
SW, SH = 680, 300
sml, smr, smt, smb = 50, 20, 35, 35
sdw = SW - sml - smr
sdh = SH - smt - smb

seg_w = sdw / len(slope_data)
max_abs_slope = max(abs(s["slope"]) for s in slope_data)
y_mid = smt + sdh / 2

bars_svg = ""
for i, seg in enumerate(slope_data):
    x = sml + i * seg_w
    s = seg["slope"]
    bar_h = abs(s) / max_abs_slope * (sdh / 2 - 5)
    if s > 0:
        by = y_mid - bar_h
        fill = "url(#upGrad)"
        label_y = by - 6
        text_color = "#dc2626"
    else:
        by = y_mid
        fill = "url(#downGrad)"
        label_y = by + bar_h + 12
        text_color = "#2563eb"
    
    bars_svg += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" rx="3"/>\n' % (x + 8, by, seg_w - 16, bar_h, fill)
    bars_svg += '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" font-weight="bold" fill="%s">%d%%</text>\n' % (x + seg_w / 2, label_y, text_color, abs(s))
    bars_svg += '<text x="%.1f" y="%d" text-anchor="middle" font-size="8" fill="#666">%s</text>\n' % (x + seg_w / 2, SH - smb + 14, seg["range"])
    bars_svg += '<text x="%.1f" y="%d" text-anchor="middle" font-size="7" fill="#999">%s</text>\n' % (x + seg_w / 2, SH - smb + 25, seg["desc"])

svg_slope = '''<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="upGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%%" stop-color="#ef4444" stop-opacity="0.85"/>
      <stop offset="100%%" stop-color="#f87171" stop-opacity="0.3"/>
    </linearGradient>
    <linearGradient id="downGrad" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%%" stop-color="#3b82f6" stop-opacity="0.85"/>
      <stop offset="100%%" stop-color="#60a5fa" stop-opacity="0.3"/>
    </linearGradient>
  </defs>
  <rect width="%d" height="%d" fill="#fafbf7" rx="12"/>
  <text x="%d" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#2d5016">分段坡度分析</text>
  <line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#ccc" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="%d" y="%.1f" text-anchor="end" font-size="9" fill="#999">0%%</text>
  %s
  <g transform="translate(%d, %d)">
    <rect x="0" y="-8" width="10" height="8" fill="url(#upGrad)" rx="2"/>
    <text x="13" y="-1" font-size="9" fill="#666">上坡</text>
    <rect x="50" y="-8" width="10" height="8" fill="url(#downGrad)" rx="2"/>
    <text x="63" y="-1" font-size="9" fill="#666">下坡</text>
  </g>
</svg>''' % (
    SW, SH, SW, SH, SW // 2,
    sml, y_mid, SW - smr, y_mid,
    sml - 8, y_mid + 4,
    bars_svg,
    sml, smt - 5
)

# Write all SVGs
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, "track_map.svg"), "w", encoding="utf-8") as f:
    f.write(svg_map)
with open(os.path.join(out_dir, "elevation_profile.svg"), "w", encoding="utf-8") as f:
    f.write(svg_elev)
with open(os.path.join(out_dir, "slope_chart.svg"), "w", encoding="utf-8") as f:
    f.write(svg_slope)

print("All 3 SVGs generated successfully!")
print("Map points: %d, Elev points: %d" % (len(map_points), len(elev_points)))

"""
Generate a professional hiking PPT from GPX data using python-pptx native shapes.
Outdoor sport style - green theme.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import math
import json

# ===== Color Palette - Outdoor Green Theme =====
C_BG = RGBColor(0xF0, 0xF4, 0xED)        # Light green-gray background
C_BG_DARK = RGBColor(0xE2, 0xE8, 0xD5)    # Darker green-gray
C_PRIMARY = RGBColor(0x2D, 0x6A, 0x3E)    # Forest green
C_DARK = RGBColor(0x1A, 0x3D, 0x10)       # Dark green
C_ACCENT = RGBColor(0x4A, 0x7C, 0x32)     # Olive green
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_BLACK = RGBColor(0x22, 0x22, 0x22)
C_GRAY = RGBColor(0x66, 0x66, 0x66)
C_LIGHT_GRAY = RGBColor(0xAA, 0xAA, 0xAA)
C_RED = RGBColor(0xDC, 0x26, 0x26)
C_BLUE = RGBColor(0x25, 0x63, 0xEB)
C_ORANGE = RGBColor(0xF5, 0x9E, 0x0B)
C_GREEN_BRIGHT = RGBColor(0x22, 0xC5, 0x5E)
C_PANEL = RGBColor(0xFF, 0xFF, 0xFF)
C_PANEL_BORDER = RGBColor(0xD0, 0xD8, 0xC0)
C_UP = RGBColor(0xEF, 0x44, 0x44)         # Red for uphill
C_DOWN = RGBColor(0x3B, 0x82, 0xF6)        # Blue for downhill

# ===== GPX Data =====
stat = {
    "total_distance_km": 27.1,
    "uphill_m": 1820,
    "downhill_m": 1825,
    "max_elevation": 336,
    "min_elevation": 33,
}

slope_segs = [
    {"range": "0~5 km", "slope": -41, "desc": "较陡下坡，控制步伐防滑"},
    {"range": "5~9 km", "slope": 40, "desc": "较陡上坡，体力消耗较大"},
    {"range": "9~14 km", "slope": -60, "desc": "陡坡急降，易打滑，谨慎慢行"},
    {"range": "14~19 km", "slope": -25, "desc": "平缓路段，行进较为轻松"},
    {"range": "19~23 km", "slope": 51, "desc": "陡坡急升，量力而行"},
    {"range": "23~28 km", "slope": 65, "desc": "陡坡急升，量力而行"},
]

service_points = [
    {"km": 17, "name": "卫生间", "type": "卫生间"},
    {"km": 18, "name": "卫生间", "type": "卫生间"},
    {"km": 19, "name": "卫生间", "type": "卫生间"},
    {"km": 25, "name": "补给点", "type": "补给"},
]

time_info = {
    "start": "2024-09-28 08:26",
    "end": "2024-09-28 19:20",
    "duration_hours": 10.9,
}

# Elevation sample data (km, elevation_m)
elev_points = [
    [0.0, 30.0], [0.27, 33.0], [0.54, 44.0], [0.81, 55.0], [1.08, 65.0],
    [1.35, 72.0], [1.62, 80.0], [1.89, 88.0], [2.16, 95.0], [2.43, 100.0],
    [2.7, 103.0], [2.97, 105.0], [3.24, 100.0], [3.51, 95.0], [3.78, 90.0],
    [4.05, 85.0], [4.32, 80.0], [4.59, 75.0], [4.86, 70.0], [5.13, 65.0],
    [5.4, 60.0], [5.67, 70.0], [5.94, 85.0], [6.21, 100.0], [6.48, 115.0],
    [6.75, 130.0], [7.02, 145.0], [7.29, 160.0], [7.56, 175.0], [7.83, 190.0],
    [8.1, 205.0], [8.37, 220.0], [8.64, 235.0], [8.91, 250.0], [9.18, 265.0],
    [9.45, 280.0], [9.72, 295.0], [9.99, 310.0], [10.26, 325.0], [10.53, 336.0],
    [10.8, 330.0], [11.07, 320.0], [11.34, 305.0], [11.61, 290.0], [11.88, 275.0],
    [12.15, 260.0], [12.42, 245.0], [12.69, 230.0], [12.96, 215.0], [13.23, 200.0],
    [13.5, 185.0], [13.77, 170.0], [14.04, 155.0], [14.31, 140.0], [14.58, 125.0],
    [14.85, 110.0], [15.12, 95.0], [15.39, 80.0], [15.66, 65.0], [15.93, 50.0],
    [16.2, 45.0], [16.47, 50.0], [16.74, 55.0], [17.01, 60.0], [17.28, 65.0],
    [17.55, 70.0], [17.82, 75.0], [18.09, 80.0], [18.36, 85.0], [18.63, 90.0],
    [18.9, 95.0], [19.17, 100.0], [19.44, 110.0], [19.71, 125.0], [19.98, 140.0],
    [20.25, 155.0], [20.52, 170.0], [20.79, 185.0], [21.06, 200.0], [21.33, 215.0],
    [21.6, 230.0], [21.87, 245.0], [22.14, 260.0], [22.41, 275.0], [22.68, 290.0],
    [22.95, 305.0], [23.22, 320.0], [23.49, 335.0], [23.76, 330.0], [24.03, 325.0],
    [24.3, 320.0], [24.57, 315.0], [24.84, 310.0], [25.11, 305.0], [25.38, 295.0],
    [25.65, 280.0], [25.92, 265.0], [26.19, 250.0], [26.46, 235.0], [26.73, 220.0],
    [27.0, 200.0], [27.1, 180.0],
]

# Map points (lon, lat) - sampled
map_points = [
    [113.285232, 23.175979], [113.28628, 23.175965], [113.287142, 23.175609],
    [113.287006, 23.174768], [113.286592, 23.173765], [113.285616, 23.173775],
    [113.286605, 23.173277], [113.28769, 23.173911], [113.288424, 23.174569],
    [113.289553, 23.174931], [113.290949, 23.174875], [113.291843, 23.174767],
    [113.291882, 23.173627], [113.292011, 23.172635], [113.292528, 23.171774],
    [113.29296, 23.171161], [113.294101, 23.171157], [113.295294, 23.171134],
    [113.296393, 23.170684], [113.297242, 23.169852], [113.297769, 23.168834],
    [113.298284, 23.167798], [113.298899, 23.166899], [113.299845, 23.166456],
    [113.300453, 23.165861], [113.300625, 23.164945], [113.300993, 23.163944],
    [113.302157, 23.163743], [113.301717, 23.164224], [113.301787, 23.165062],
    [113.301679, 23.166148], [113.301689, 23.167199], [113.302546, 23.167352],
    [113.302986, 23.166345], [113.303542, 23.167124], [113.303548, 23.168194],
    [113.303001, 23.168672], [113.302577, 23.169299], [113.303452, 23.169893],
    [113.302602, 23.170557], [113.301712, 23.170691], [113.300808, 23.170409],
    [113.300211, 23.170322], [113.299793, 23.170611], [113.298747, 23.171058],
    [113.297709, 23.17147], [113.297018, 23.172343], [113.296432, 23.173225],
    [113.296168, 23.174063], [113.295611, 23.175018], [113.295067, 23.175873],
    [113.295624, 23.176458], [113.29643, 23.176857], [113.297599, 23.176632],
    [113.298368, 23.177136], [113.2986, 23.17776], [113.299674, 23.177652],
    [113.300898, 23.177736], [113.301349, 23.178736], [113.30134, 23.179678],
    [113.301382, 23.180687], [113.30074, 23.181718], [113.299769, 23.182307],
    [113.29892, 23.182565], [113.298478, 23.183727], [113.297496, 23.18434],
    [113.297745, 23.185318], [113.298291, 23.185996], [113.29819, 23.186881],
    [113.298467, 23.187764], [113.29872, 23.18791], [113.298046, 23.187696],
    [113.297084, 23.187752], [113.295978, 23.187445], [113.294849, 23.187908],
    [113.294115, 23.187449], [113.293417, 23.187043], [113.292678, 23.188058],
    [113.292181, 23.189071], [113.292668, 23.190083], [113.292218, 23.191088],
    [113.291619, 23.192058], [113.292567, 23.19241], [113.293348, 23.192879],
    [113.293265, 23.193833], [113.293232, 23.19496], [113.293563, 23.195866],
    [113.293805, 23.196743], [113.294536, 23.196167], [113.295252, 23.195617],
    [113.295429, 23.194621], [113.295564, 23.193663], [113.29524, 23.192623],
    [113.296132, 23.192416], [113.295838, 23.191391], [113.296559, 23.19184],
    [113.297166, 23.191809], [113.297597, 23.190874], [113.297717, 23.189811],
    [113.298317, 23.188911], [113.298956, 23.188494], [113.298915, 23.188301],
    [113.299017, 23.189322], [113.298453, 23.190287], [113.299138, 23.190906],
    [113.300337, 23.191107], [113.301325, 23.190471], [113.302485, 23.190215],
    [113.303491, 23.189518], [113.304083, 23.18969], [113.303673, 23.190343],
    [113.303145, 23.19036], [113.303315, 23.191217], [113.302172, 23.19139],
    [113.301272, 23.19194], [113.300491, 23.192717], [113.301244, 23.19234],
    [113.301741, 23.193279], [113.302541, 23.194179], [113.302198, 23.194965],
    [113.302003, 23.196025], [113.301207, 23.195631], [113.30119, 23.194779],
    [113.302165, 23.195091], [113.301856, 23.196128], [113.301798, 23.197],
    [113.301959, 23.198078], [113.303003, 23.198579], [113.303072, 23.19966],
    [113.302996, 23.200453], [113.30217, 23.200716], [113.301587, 23.19971],
    [113.300715, 23.199664], [113.300853, 23.200728], [113.300412, 23.200945],
    [113.29981, 23.200107], [113.29923, 23.20103], [113.298114, 23.20104],
    [113.297648, 23.200106], [113.296538, 23.19971], [113.296721, 23.199297],
    [113.297819, 23.198937], [113.297589, 23.197958], [113.297122, 23.196951],
    [113.297008, 23.196372], [113.296276, 23.197284], [113.295531, 23.198191],
    [113.294537, 23.198838], [113.293343, 23.199253], [113.292119, 23.199559],
    [113.290877, 23.199717], [113.290252, 23.199348], [113.290012, 23.198643],
    [113.290157, 23.197704], [113.289755, 23.196976], [113.289889, 23.196009],
    [113.289785, 23.195313], [113.288893, 23.195103], [113.288136, 23.195936],
    [113.288473, 23.196884], [113.287796, 23.197736], [113.286954, 23.197684],
    [113.286403, 23.196804],
]

# Service point coordinates
svc_coords = [
    {"lon": 113.30059, "lat": 23.201173, "type": "卫生间", "km": 17},
    {"lon": 113.296901, "lat": 23.199224, "type": "卫生间", "km": 18},
    {"lon": 113.294974, "lat": 23.198594, "type": "卫生间", "km": 19},
    {"lon": 113.295945, "lat": 23.182322, "type": "补给点", "km": 25},
]

# ===== Helper Functions =====

def add_bg(slide, color=C_BG):
    """Add full-slide background rectangle."""
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    bg.shadow.inherit = False
    return bg

def add_text(slide, left, top, width, height, text, font_size=18, bold=False,
             color=C_BLACK, align=PP_ALIGN.LEFT, font_name="Microsoft YaHei"):
    """Add a text box with formatting."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = align
    return txBox

def add_panel(slide, left, top, width, height, fill_color=C_PANEL, border_color=C_PANEL_BORDER):
    """Add a rounded panel."""
    panel = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    panel.fill.solid()
    panel.fill.fore_color.rgb = fill_color
    panel.line.color.rgb = border_color
    panel.line.width = Pt(1)
    panel.shadow.inherit = False
    return panel

def add_metric_card(slide, left, top, width, height, icon, value, unit, label, color=C_PRIMARY):
    """Add a metric card with icon, value, unit, and label."""
    add_panel(slide, left, top, width, height)
    # Icon
    add_text(slide, left + Inches(0.15), top + Inches(0.1), Inches(0.5), Inches(0.5), icon, font_size=22, bold=False, align=PP_ALIGN.LEFT)
    # Value
    val_text = str(value)
    add_text(slide, left + Inches(0.15), top + Inches(0.35), width - Inches(0.3), Inches(0.55), val_text, font_size=28, bold=True, color=color, align=PP_ALIGN.LEFT)
    # Unit
    val_width = len(str(value)) * Inches(0.22)
    add_text(slide, left + Inches(0.15) + val_width, top + Inches(0.5), Inches(0.6), Inches(0.3), unit, font_size=12, bold=False, color=C_GRAY, align=PP_ALIGN.LEFT)
    # Label
    add_text(slide, left + Inches(0.15), top + height - Inches(0.35), width - Inches(0.3), Inches(0.3), label, font_size=10, bold=False, color=C_GRAY, align=PP_ALIGN.LEFT)

def add_freeform_track(slide, points, left, top, width, height):
    """Draw the track as a freeform shape."""
    if not points:
        return

    lons = [p[0] for p in points]
    lats = [p[1] for p in points]
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)

    lon_range = max_lon - min_lon or 0.001
    lat_range = max_lat - min_lat or 0.001
    scale = min(width / lon_range, height / lat_range)
    ox = left + (width - lon_range * scale) / 2
    oy = top + (height - lat_range * scale) / 2

    def proj(lon, lat):
        x = ox + (lon - min_lon) * scale
        y = oy + (max_lat - lat) * scale
        return int(x), int(y)

    # Draw as connected line segments
    prev_x, prev_y = proj(points[0][0], points[0][1])
    for i in range(1, len(points)):
        cx, cy = proj(points[i][0], points[i][1])
        line = slide.shapes.add_connector(
            1,  # straight connector
            prev_x, prev_y, cx, cy
        )
        line.line.color.rgb = C_PRIMARY
        line.line.width = Pt(2.5)
        line.shadow.inherit = False
        prev_x, prev_y = cx, cy

    # Start point
    sx, sy = proj(points[0][0], points[0][1])
    start_dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, sx - Emu(50000), sy - Emu(50000), Emu(100000), Emu(100000))
    start_dot.fill.solid()
    start_dot.fill.fore_color.rgb = C_GREEN_BRIGHT
    start_dot.line.color.rgb = C_WHITE
    start_dot.line.width = Pt(2)
    start_dot.shadow.inherit = False
    add_text(slide, sx - Inches(0.4), sy - Inches(0.5), Inches(0.8), Inches(0.25), "起点", font_size=9, bold=True, color=C_GREEN_BRIGHT, align=PP_ALIGN.CENTER)

    # End point
    ex, ey = proj(points[-1][0], points[-1][1])
    end_dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, ex - Emu(50000), ey - Emu(50000), Emu(100000), Emu(100000))
    end_dot.fill.solid()
    end_dot.fill.fore_color.rgb = C_RED
    end_dot.line.color.rgb = C_WHITE
    end_dot.line.width = Pt(2)
    end_dot.shadow.inherit = False
    add_text(slide, ex - Inches(0.4), ey - Inches(0.5), Inches(0.8), Inches(0.25), "终点", font_size=9, bold=True, color=C_RED, align=PP_ALIGN.CENTER)

    # Service points
    for sp in svc_coords:
        wx, wy = proj(sp["lon"], sp["lat"])
        color = C_BLUE if "卫生间" in sp["type"] else C_ORANGE
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, wx - Emu(30000), wy - Emu(30000), Emu(60000), Emu(60000))
        dot.fill.solid()
        dot.fill.fore_color.rgb = color
        dot.line.color.rgb = C_WHITE
        dot.line.width = Pt(1.5)
        dot.shadow.inherit = False

    return (sx, sy, ex, ey)

def draw_elevation_chart(slide, data, left, top, width, height):
    """Draw elevation profile using freeform connectors."""
    if not data:
        return

    max_km = max(p[0] for p in data)
    min_elev = min(p[1] for p in data)
    max_elev = max(p[1] for p in data)
    elev_range = max_elev - min_elev

    m_l = Emu(200000)  # left margin
    m_r = Emu(100000)
    m_t = Emu(150000)
    m_b = Emu(200000)

    chart_w = width - m_l - m_r
    chart_h = height - m_t - m_b

    def proj(km, elev):
        x = left + m_l + int((km / max_km) * chart_w)
        y = top + m_t + int((1 - (elev - min_elev) / elev_range) * chart_h)
        return x, y

    # Grid lines and Y labels
    elev_start = int(min_elev // 50) * 50
    elev_end = int(max_elev // 50 + 1) * 50
    for e in range(elev_start, elev_end + 1, 50):
        _, y = proj(0, e)
        line = slide.shapes.add_connector(1, left + m_l, y, left + m_l + chart_w, y)
        line.line.color.rgb = RGBColor(0xE0, 0xE5, 0xD5)
        line.line.width = Pt(0.5)
        line.shadow.inherit = False
        add_text(slide, left, y - Inches(0.08), m_l, Inches(0.16), str(e) + "m", font_size=8, color=C_LIGHT_GRAY, align=PP_ALIGN.RIGHT)

    # X labels
    for km in range(0, int(max_km) + 1, 5):
        x, _ = proj(km, min_elev)
        add_text(slide, x - Inches(0.3), top + m_t + chart_h + Inches(0.02), Inches(0.6), Inches(0.16), str(km) + "km", font_size=8, color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

    # Draw elevation line
    prev_x, prev_y = proj(data[0][0], data[0][1])
    for i in range(1, len(data)):
        cx, cy = proj(data[i][0], data[i][1])
        line = slide.shapes.add_connector(1, prev_x, prev_y, cx, cy)
        line.line.color.rgb = C_PRIMARY
        line.line.width = Pt(2)
        line.shadow.inherit = False
        prev_x, prev_y = cx, cy

    # Max elevation marker
    mx, my = proj(10.53, 336)
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, mx - Emu(35000), my - Emu(35000), Emu(70000), Emu(70000))
    dot.fill.solid()
    dot.fill.fore_color.rgb = C_RED
    dot.line.color.rgb = C_WHITE
    dot.line.width = Pt(1.5)
    dot.shadow.inherit = False
    add_text(slide, mx - Inches(0.6), my - Inches(0.45), Inches(1.2), Inches(0.2), "最高 336m", font_size=8, bold=True, color=C_RED, align=PP_ALIGN.CENTER)

def draw_slope_chart(slide, data, left, top, width, height):
    """Draw slope segment bar chart."""
    m_l = Emu(200000)
    m_r = Emu(100000)
    m_t = Emu(250000)
    m_b = Emu(300000)

    chart_w = width - m_l - m_r
    chart_h = height - m_t - m_b
    seg_w = chart_w / len(data)
    max_abs = max(abs(s["slope"]) for s in data)
    y_mid = top + m_t + chart_h // 2

    # Zero line
    line = slide.shapes.add_connector(1, left + m_l, y_mid, left + m_l + chart_w, y_mid)
    line.line.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
    line.line.width = Pt(1)
    line.line.dash_style = 4  # dashed
    line.shadow.inherit = False
    add_text(slide, left, y_mid - Inches(0.08), m_l, Inches(0.16), "0%", font_size=8, color=C_LIGHT_GRAY, align=PP_ALIGN.RIGHT)

    for i, seg in enumerate(data):
        x = left + m_l + i * seg_w
        s = seg["slope"]
        bar_h = int(abs(s) / max_abs * (chart_h / 2 - 50000))

        if s > 0:
            by = y_mid - bar_h
            color = C_UP
        else:
            by = y_mid
            color = C_DOWN

        bar = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            x + int(seg_w * 0.1), by,
            int(seg_w * 0.8), bar_h
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()
        bar.shadow.inherit = False

        # Value label
        label_y = by - Inches(0.25) if s > 0 else by + bar_h + Inches(0.02)
        label_color = C_RED if s > 0 else C_BLUE
        add_text(slide, x, label_y, seg_w, Inches(0.2), str(abs(s)) + "%", font_size=11, bold=True, color=label_color, align=PP_ALIGN.CENTER)

        # Range label
        add_text(slide, x, top + m_t + chart_h + Inches(0.02), seg_w, Inches(0.16), seg["range"], font_size=8, color=C_GRAY, align=PP_ALIGN.CENTER)
        # Desc label
        add_text(slide, x, top + m_t + chart_h + Inches(0.18), seg_w, Inches(0.14), seg["desc"][:6], font_size=7, color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

# ====== Build PPT ======
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# ---- Slide 1: Cover ----
s = prs.slides.add_slide(blank_layout)
add_bg(s, C_PRIMARY)

# Decorative top bar
top_bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
top_bar.fill.solid()
top_bar.fill.fore_color.rgb = C_GREEN_BRIGHT
top_bar.line.fill.background()
top_bar.shadow.inherit = False

# Title
add_text(s, Inches(1), Inches(1.8), Inches(11.333), Inches(1.2),
         "白云山画龙", font_size=54, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

# Subtitle
add_text(s, Inches(1), Inches(3.1), Inches(11.333), Inches(0.6),
         "GPX 轨迹徒步分析报告", font_size=22, bold=False, color=RGBColor(0xC8, 0xE6, 0xC8), align=PP_ALIGN.CENTER)

# Info bar
add_text(s, Inches(1), Inches(4.2), Inches(11.333), Inches(0.5),
         "2024-09-28（周六）| 广州白云山 | 27.1 km | 累计爬升 1820 m", font_size=16, color=RGBColor(0xA8, 0xD8, 0xA8), align=PP_ALIGN.CENTER)

# Bottom decoration
bot_bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.42), Inches(13.333), Inches(0.08))
bot_bar.fill.solid()
bot_bar.fill.fore_color.rgb = C_GREEN_BRIGHT
bot_bar.line.fill.background()
bot_bar.shadow.inherit = False

# ---- Slide 2: Key Metrics ----
s = prs.slides.add_slide(blank_layout)
add_bg(s)

add_text(s, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.6),
         "核心数据总览", font_size=28, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)
add_text(s, Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.4),
         "Key Metrics Summary", font_size=12, color=C_GRAY, align=PP_ALIGN.LEFT)

# Metric cards row 1
card_w = Inches(2.7)
card_h = Inches(1.6)
gap = Inches(0.25)
start_x = Inches(0.8)
y1 = Inches(1.7)

add_metric_card(s, start_x + 0*(card_w+gap), y1, card_w, card_h, "\U0001F9CE", "27.1", "km", "全程里程", C_PRIMARY)
add_metric_card(s, start_x + 1*(card_w+gap), y1, card_w, card_h, "\U00002B06", "1820", "m", "累计爬升", C_RED)
add_metric_card(s, start_x + 2*(card_w+gap), y1, card_w, card_h, "\U00002B07", "1825", "m", "累计下降", C_BLUE)
add_metric_card(s, start_x + 3*(card_w+gap), y1, card_w, card_h, "\U0001F3D4", "336", "m", "最高海拔", C_ORANGE)

# Row 2
y2 = Inches(3.6)
add_metric_card(s, start_x + 0*(card_w+gap), y2, card_w, card_h, "\U0001F4C8", "33", "m", "最低海拔", C_ACCENT)
add_metric_card(s, start_x + 1*(card_w+gap), y2, card_w, card_h, "\U000023F1", "10.9", "h", "运动时长", C_PRIMARY)
add_metric_card(s, start_x + 2*(card_w+gap), y2, card_w, card_h, "\U0001F6A6", "2.5", "km/h", "平均配速", C_ACCENT)
add_metric_card(s, start_x + 3*(card_w+gap), y2, card_w, card_h, "\U0001F6A9", "89", "%", "难度指数", C_RED)

# Difficulty assessment panel
add_panel(s, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.5))
add_text(s, Inches(1.0), Inches(5.6), Inches(2.5), Inches(0.4),
         "\U0001F4CA 难度评估", font_size=14, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)
add_text(s, Inches(1.0), Inches(6.0), Inches(11.3), Inches(0.9),
         "难度系数 89%（挑战级）。测算公式：(里程 27.1km + 累计爬升 1820m / 100) / 25km * 100%。\n该路线适合有经验的徒步队伍，请做好充分准备。全程累计爬升较大，需合理分配体力。",
         font_size=12, color=C_GRAY, align=PP_ALIGN.LEFT)

# ---- Slide 3: Track Map ----
s = prs.slides.add_slide(blank_layout)
add_bg(s)

add_text(s, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.6),
         "轨迹路线图", font_size=28, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)
add_text(s, Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.4),
         "Track Map - GPX 轨迹可视化", font_size=12, color=C_GRAY, align=PP_ALIGN.LEFT)

# Map panel
map_left = Inches(0.8)
map_top = Inches(1.6)
map_w = Inches(11.7)
map_h = Inches(5.5)
add_panel(s, map_left, map_top, map_w, map_h, C_BG, C_PANEL_BORDER)

# Draw track
add_freeform_track(s, map_points, map_left + Inches(0.2), map_top + Inches(0.3), map_w - Inches(0.4), map_h - Inches(0.6))

# Legend
legend_y = map_top + map_h - Inches(0.45)
add_text(s, map_left + Inches(0.3), legend_y, Inches(1.5), Inches(0.25),
         "\U0001F7E2 起点  \U0001F534 终点  \U0001F535 卫生间  \U0001F7E1 补给点", font_size=10, color=C_GRAY, align=PP_ALIGN.LEFT)

# ---- Slide 4: Elevation Profile ----
s = prs.slides.add_slide(blank_layout)
add_bg(s)

add_text(s, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.6),
         "海拔剖面图", font_size=28, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)
add_text(s, Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.4),
         "Elevation Profile - 海拔随距离变化", font_size=12, color=C_GRAY, align=PP_ALIGN.LEFT)

# Chart panel
chart_left = Inches(0.8)
chart_top = Inches(1.6)
chart_w = Inches(11.7)
chart_h = Inches(5.5)
add_panel(s, chart_left, chart_top, chart_w, chart_h, C_BG, C_PANEL_BORDER)

draw_elevation_chart(s, elev_points, chart_left + Inches(0.2), chart_top + Inches(0.15), chart_w - Inches(0.4), chart_h - Inches(0.3))

# Y-axis label
add_text(s, chart_left + Inches(0.1), chart_top + Inches(2.0), Inches(0.5), Inches(0.3),
         "海拔(m)", font_size=9, color=C_GRAY, align=PP_ALIGN.LEFT)
# X-axis label
add_text(s, chart_left + chart_w / 2 - Inches(0.5), chart_top + chart_h - Inches(0.15), Inches(1.0), Inches(0.25),
         "距离 (km)", font_size=9, color=C_GRAY, align=PP_ALIGN.CENTER)

# ---- Slide 5: Slope Analysis ----
s = prs.slides.add_slide(blank_layout)
add_bg(s)

add_text(s, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.6),
         "分段坡度分析", font_size=28, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)
add_text(s, Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.4),
         "Slope Analysis - 全程等分6段，坡度为段内最陡处推算值", font_size=12, color=C_GRAY, align=PP_ALIGN.LEFT)

# Chart panel
sl_chart_left = Inches(0.8)
sl_chart_top = Inches(1.6)
sl_chart_w = Inches(11.7)
sl_chart_h = Inches(3.5)
add_panel(s, sl_chart_left, sl_chart_top, sl_chart_w, sl_chart_h, C_BG, C_PANEL_BORDER)

draw_slope_chart(s, slope_segs, sl_chart_left + Inches(0.2), sl_chart_top + Inches(0.15), sl_chart_w - Inches(0.4), sl_chart_h - Inches(0.3))

# Legend
add_text(s, sl_chart_left + Inches(0.3), sl_chart_top + Inches(0.15), Inches(2.0), Inches(0.2),
         "\U0001F7E5 上坡  \U0001F7E6 下坡", font_size=10, color=C_GRAY, align=PP_ALIGN.LEFT)

# Slope details table
table_top = Inches(5.3)
add_text(s, Inches(0.8), table_top, Inches(11.7), Inches(0.35),
         "分段路况详情", font_size=14, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)

for i, seg in enumerate(slope_segs):
    col = i % 3
    row = i // 3
    x = Inches(0.8) + col * Inches(3.9)
    y = table_top + Inches(0.4) + row * Inches(0.8)

    add_panel(s, x, y, Inches(3.7), Inches(0.7), C_PANEL)
    slope_color = C_RED if seg["slope"] > 0 else C_BLUE
    sign = "+" if seg["slope"] > 0 else ""
    add_text(s, x + Inches(0.15), y + Inches(0.05), Inches(1.2), Inches(0.3),
             seg["range"], font_size=11, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)
    add_text(s, x + Inches(1.3), y + Inches(0.05), Inches(0.8), Inches(0.3),
             sign + str(seg["slope"]) + "%", font_size=11, bold=True, color=slope_color, align=PP_ALIGN.LEFT)
    add_text(s, x + Inches(0.15), y + Inches(0.38), Inches(3.4), Inches(0.25),
             seg["desc"], font_size=9, color=C_GRAY, align=PP_ALIGN.LEFT)

# ---- Slide 6: Service Points & Safety ----
s = prs.slides.add_slide(blank_layout)
add_bg(s)

add_text(s, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.6),
         "沿途设施与风险提示", font_size=28, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)
add_text(s, Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.4),
         "Service Points & Safety Tips", font_size=12, color=C_GRAY, align=PP_ALIGN.LEFT)

# Left: Service points
add_panel(s, Inches(0.8), Inches(1.6), Inches(5.5), Inches(5.5))
add_text(s, Inches(1.0), Inches(1.7), Inches(5.0), Inches(0.4),
         "\U0001F6BE 沿途卫生间与补给点", font_size=16, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)

for i, sp in enumerate(service_points):
    y = Inches(2.3) + i * Inches(0.6)
    icon = "\U0001F6BE" if sp["type"] == "卫生间" else "\U0001F3EA"
    color = C_BLUE if sp["type"] == "卫生间" else C_ORANGE
    add_text(s, Inches(1.2), y, Inches(0.5), Inches(0.4), icon, font_size=18, align=PP_ALIGN.LEFT)
    add_text(s, Inches(1.8), y, Inches(1.5), Inches(0.4), sp["type"], font_size=12, bold=True, color=color, align=PP_ALIGN.LEFT)
    add_text(s, Inches(3.3), y, Inches(2.0), Inches(0.4), "约 " + str(sp["km"]) + " km处", font_size=12, color=C_GRAY, align=PP_ALIGN.LEFT)

add_text(s, Inches(1.0), Inches(4.9), Inches(5.0), Inches(0.35),
         "汇总：卫生间 3 处 | 补给点 1 处", font_size=11, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)
add_text(s, Inches(1.0), Inches(5.3), Inches(5.0), Inches(1.5),
         "轨迹标注的设施点有限，建议出行前用地图App确认沿途位置，自备充足饮水食物。部分区域手机信号较弱，建议提前导入离线导航。",
         font_size=10, color=C_GRAY, align=PP_ALIGN.LEFT)

# Right: Risk tips & gear
add_panel(s, Inches(6.5), Inches(1.6), Inches(6.0), Inches(5.5))
add_text(s, Inches(6.7), Inches(1.7), Inches(5.5), Inches(0.4),
         "\U000026A0 风险提示与装备建议", font_size=16, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)

tips = [
    "长距离爬升路段体力消耗集中，整体行进节奏需要合理把控，避免前期体力透支。",
    "提前规划沿途水源补给，出行人员自备充足饮用水。",
    "部分区域手机信号较弱，建议提前把轨迹导入离线导航软件。",
    "野外路段存在碎石、树根，行走时注意脚下，下坡放慢步伐，防止滑倒崴脚。",
    "注意日落时间，预留返程缓冲时长，头灯建议随身携带。",
]

for i, tip in enumerate(tips):
    y = Inches(2.3) + i * Inches(0.5)
    add_text(s, Inches(6.7), y, Inches(0.3), Inches(0.35), str(i+1) + ".", font_size=10, bold=True, color=C_RED, align=PP_ALIGN.LEFT)
    add_text(s, Inches(7.0), y, Inches(5.2), Inches(0.45), tip, font_size=10, color=C_GRAY, align=PP_ALIGN.LEFT)

add_text(s, Inches(6.7), Inches(5.0), Inches(5.5), Inches(0.35),
         "\U0001F392 装备清单", font_size=14, bold=True, color=C_DARK, align=PP_ALIGN.LEFT)
add_text(s, Inches(6.7), Inches(5.4), Inches(5.5), Inches(0.3),
         "\u2705 必备：防滑徒步鞋、登山杖、头灯、足量饮用水、路餐、防晒用品", font_size=10, color=C_GRAY, align=PP_ALIGN.LEFT)
add_text(s, Inches(6.7), Inches(5.8), Inches(5.5), Inches(0.3),
         "\U0001F7E1 可选：简易净水工具、急救包、便携雨具、充电宝", font_size=10, color=C_GRAY, align=PP_ALIGN.LEFT)

# ---- Slide 7: Summary ----
s = prs.slides.add_slide(blank_layout)
add_bg(s, C_PRIMARY)

add_text(s, Inches(1), Inches(2.0), Inches(11.333), Inches(1.0),
         "行程总结", font_size=40, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

add_text(s, Inches(2), Inches(3.2), Inches(9.333), Inches(1.5),
         "本次白云山画龙徒步全程 27.1 公里，累计爬升 1820 米，\n运动时长 10.9 小时，最高海拔 336 米，难度指数 89%。\n\n轨迹整体呈画龙形态，途经白云山多个山头，\n含连续爬升与陡坡急降路段，属挑战级路线。",
         font_size=16, color=RGBColor(0xC8, 0xE6, 0xC8), align=PP_ALIGN.CENTER)

# Disclaimer
add_text(s, Inches(1), Inches(6.0), Inches(11.333), Inches(0.8),
         "本报告由 GPX 轨迹数据自动生成，路况结果仅由海拔数据推算，仅作出行规划参考。\n山区天气多变，出行前请核实最新气象预警，注意户外安全。",
         font_size=10, color=RGBColor(0x88, 0xB8, 0x88), align=PP_ALIGN.CENTER)

# Bottom bar
bot_bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.42), Inches(13.333), Inches(0.08))
bot_bar.fill.solid()
bot_bar.fill.fore_color.rgb = C_GREEN_BRIGHT
bot_bar.line.fill.background()
bot_bar.shadow.inherit = False

# ====== Save ======
output_path = "/Users/vinc/hike-trail-analyzer-skill/output/白云山画龙_徒步分析报告.pptx"
prs.save(output_path)
print("PPT saved to:", output_path)
print("Total slides:", len(prs.slides))

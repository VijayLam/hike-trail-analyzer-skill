"""
hike-trail-analyzer · 纯文本专业路书生成器
Author: Vijay
"""
import unicodedata
from datetime import datetime

MAX_REPORT_CHARS = 1000
MIN_REPORT_CHARS = 980


def get_difficulty_level(score: int):
    if score <= 20:
        return "休闲"
    elif score <= 40:
        return "简单"
    elif score <= 55:
        return "中等"
    elif score <= 70:
        return "较难"
    elif score <= 85:
        return "困难"
    else:
        return "极难"


def assess_difficulty(stat: dict, sustained_grade_p95: float = None):
    """按里程、累计爬升和持续上坡坡度计算 0～100 综合难度。"""
    dist_km = max(0.0, float(stat.get("total_distance_km", 0)))
    uphill_m = max(0.0, float(stat.get("uphill_m", 0)))
    grade_p95 = max(0.0, float(sustained_grade_p95 or 0))

    # 三项先分别归一化到 0～10，再按 35/35/30 加权，避免单项直接把总分打满。
    distance_component = min(10.0, 10 * (dist_km / 25) ** 0.8) if dist_km else 0.0
    elevation_component = min(10.0, 10 * (uphill_m / 2000) ** 0.75) if uphill_m else 0.0
    slope_component = min(10.0, max(0.0, (grade_p95 - 5) / 2.5))

    contributions = [
        ("全程里程", distance_component * 10 * 0.35),
        ("累计爬升", elevation_component * 10 * 0.35),
        ("持续上坡P95", slope_component * 10 * 0.30),
    ]
    contributions.sort(key=lambda item: item[1], reverse=True)
    score = round(sum(value for _, value in contributions))
    return {
        "dist_km": dist_km,
        "uphill_m": uphill_m,
        "sustained_grade_p95": grade_p95,
        "distance_component": distance_component,
        "elevation_component": elevation_component,
        "slope_component": slope_component,
        "score": score,
        "level": get_difficulty_level(score),
        "top3": contributions,
    }


def build_difficulty_lines(a: dict):
    contribution_map = {name: value for name, value in a["top3"]}
    return [
        f"📊整体难度：{a['score']}分｜{a['level']}",
        "评分构成："
        f"里程{a['distance_component']:.1f}/10（贡献{contribution_map['全程里程']:.0f}分）｜"
        f"爬升{a['elevation_component']:.1f}/10（贡献{contribution_map['累计爬升']:.0f}分）｜"
        f"持续坡度P95 {a['sustained_grade_p95']:.1f}%（坡度分{a['slope_component']:.1f}/10）",
    ]


def estimate_water_liters(stat: dict, temps: list):
    if not temps:
        return None
    max_t = max(temps)
    duration_h = stat["total_distance_km"] / 4 + stat["uphill_m"] / 600
    rate = 0.7 if max_t >= 32 else (0.6 if max_t >= 28 else (0.4 if max_t < 10 else 0.5))
    total = duration_h * rate
    lo = max(0.5, round(total * 0.85 * 2) / 2)
    hi = max(lo + 0.5, round(total * 1.15 * 2) / 2)
    lo = min(lo, 5.5)
    hi = min(hi, 6)
    fmt = lambda value: f"{value:g}"
    return f"{fmt(lo)}～{fmt(hi)}L"


def _display_width(text: str):
    return sum(2 if unicodedata.east_asian_width(c) in "FW" else 1 for c in text)


def _to_fullwidth(text: str):
    result = []
    for c in text:
        code = ord(c)
        if c == " ":
            result.append("　")
        elif 33 <= code <= 126:
            result.append(chr(code + 0xFEE0))
        else:
            result.append(c)
    return "".join(result)


def render_table(headers: list, rows: list):
    all_rows = [[_to_fullwidth(c) for c in row] for row in [headers] + rows]
    widths = [max(_display_width(r[i]) for r in all_rows) for i in range(len(headers))]
    last = len(widths) - 1

    def render_row(row):
        parts = []
        for i, cell in enumerate(row):
            if i == last:
                parts.append(cell)
            else:
                parts.append(cell + "　" * ((widths[i] + 2 - _display_width(cell)) // 2))
        return "".join(parts)

    return [render_row(row) for row in all_rows]


def _weather_lines(waypoint_weather: list):
    labels = ["起点", "中途", "高点", "关键点", "终点"]
    lines = ["🌤沿途天气（按预计到达时刻）"]
    for idx, row in enumerate(waypoint_weather):
        if not row:
            continue
        temp = f"，约{row['temp_c']}℃" if row.get("temp_c") is not None else ""
        lines.append(
            f"{labels[idx]} {row['arrive_hm']}：{row['weather']}{temp}，降雨概率{row['rain_prob']}；路况平稳。"
        )
    if len(lines) == 1:
        lines.append("天气接口暂未返回有效点位数据，出发前请重新查询并核实预警。")
    lines.append("天气仅供参考；山区小气候变化快，出发前核实预警，持续降雨或雷雨时调整行程。")
    return lines


def _slope_lines(slope_segment_list: list):
    lines = ["🛤分段坡度（最陡值仅作局部风险提示）"]
    if not slope_segment_list:
        return lines + ["轨迹未提供足够坡度数据，请以现场路况为准。"]
    for segment in slope_segment_list:
        lines.append(f"{segment['range']}：最陡{segment['slope']:+d}%；{_compact_slope_desc(segment['desc'])}")
    return lines


def _compact_slope_desc(description: str):
    replacements = {
        "平缓路段，行进较为轻松": "平缓，保持节奏",
        "陡坡急降，易打滑，谨慎慢行": "陡降，防滑慢行",
        "较陡下坡，控制步伐防滑": "陡降，防滑慢行",
        "小爬升，保持节奏": "小爬升，稳步行进",
        "小下降，留意脚下": "小下降，留意脚下",
    }
    return replacements.get(description, description) + "。"


def _route_advice(stat: dict, slope_segment_list: list, water_text: str):
    steep_down = [abs(seg["slope"]) for seg in slope_segment_list if seg["slope"] < -40]
    steep_up = [seg["slope"] for seg in slope_segment_list if seg["slope"] > 40]
    slope_advice = "路线有明显陡降段，" if steep_down else "路线坡度变化相对平稳，"
    if steep_up:
        slope_advice += "上坡段不要一开始冲速度。"
    else:
        slope_advice += "仍需按节奏推进。"
    return [
        "🏃行进建议：前段先用能完整说话的节奏热身，爬升集中处采用小步幅、稳定呼吸，必要时短暂停留补水；不要因为前段顺利就透支体力。",
        f"下坡建议提前收小步、脚掌落稳并使用登山杖，{slope_advice}",
        f"预计正常用时接近半天，建议{water_text or '携带足量饮水'}，路餐分次食用；手机导入离线轨迹，确认返程交通和日落余量。",
    ]


def _fit_report(lines: list):
    """以 1000 个字符为目标；超限按整行压缩，不足补充可执行信息。"""
    lines = list(lines)
    replacements = [
        ("GPX轨迹自动分析｜出行规划参考", "GPX轨迹分析｜规划参考。"),
        ("GPX轨迹分析｜规划参考", "GPX轨迹分析｜规划参考。"),
        ("建议加带雨具、急救包和充电宝", "另带雨具、急救包、充电宝"),
        ("手机提前导入离线轨迹，出发前确认返程交通和日落余量", "手机导入离线轨迹，确认返程交通和日落余量"),
        ("天气仅供路线规划参考，山区小气候变化快，出发前应再次查看最新预警；若遇持续降雨或雷雨，优先调整行程。", "天气仅供参考；山区小气候变化快，出发前核实预警，持续降雨或雷雨时调整行程。"),
        ("🛤分段坡度路况（分段最陡值只用于局部风险提示，不直接决定综合难度）", "🛤分段坡度（最陡值仅作局部风险提示）"),
        ("轨迹未标注相关点位，出发前用地图确认，并自备饮水和路餐", "轨迹未标注，出发前地图确认，自备饮水路餐"),
    ]
    lines = [
        next((line.replace(old, new) for old, new in replacements if old in line), line)
        for line in lines
    ]
    text = "\n".join(lines)

    # 这些是可删的重复补充，不影响路线、天气、难度和安全核心信息。
    for prefix in ("📌同行：", "📌安全："):
        if len(text) <= MAX_REPORT_CHARS:
            break
        lines = [line for line in lines if not line.startswith(prefix)]
        text = "\n".join(lines)

    if len(text) > MAX_REPORT_CHARS:
        # 只压缩坡度描述，不删除各段的坡度数值和方向。
        lines = [
            "🛤坡度：详见各段最陡值；局部陡坡注意防滑。" if line.startswith("🛤分段坡度") else line
            for line in lines
        ]
        text = "\n".join(lines)
    if len(text) > MAX_REPORT_CHARS:
        raise ValueError(f"路书超过 {MAX_REPORT_CHARS} 字符，无法在保留核心信息的前提下压缩")

    # 当前路线通常经过上面的整行压缩后接近 1000；不足时补充具体安全动作。
    additions = [
        "📌出发前核对天气、鞋底抓地力、登山杖、手机电量和离线轨迹。",
        "📌每小时主动饮水，观察同行者状态，保持队伍联系，不擅自离队。",
        "📌天气恶化或身体不适时及时停下评估，必要时原路返回或联系救援。",
    ]
    for addition in additions:
        candidate = f"{text}\n{addition}"
        if len(candidate) <= MAX_REPORT_CHARS:
            text = candidate
        if len(text) == MAX_REPORT_CHARS:
            return text

    # 最后一字符用完整句号收尾；不会截断任何句子或制造半行内容。
    if len(text) == MAX_REPORT_CHARS - 1:
        return text + "。"
    if len(text) < MIN_REPORT_CHARS:
        raise ValueError(f"路书只有 {len(text)} 字符，未达到 {MIN_REPORT_CHARS} 字符目标")
    raise ValueError(f"路书为 {len(text)} 字符，未精确达到 {MAX_REPORT_CHARS} 字符")


def build_report(route_name: str, stat: dict, waypoint_weather: list,
                 slope_segment_list: list, time_estimate: dict,
                 start_datetime: datetime = None, service_points: list = None,
                 meeting_point: str = None, sustained_grade_p95: float = None):
    difficulty = assess_difficulty(stat, sustained_grade_p95)
    temps = [w["temp_c"] for w in waypoint_weather if w and w.get("temp_c") is not None]
    water_text = estimate_water_liters(stat, temps)
    lines = [f"🥾{route_name}｜徒步路书"]
    if start_datetime is not None:
        week_day = "周" + "一二三四五六日"[start_datetime.weekday()]
        lines.append(f"📅出行：{start_datetime.strftime('%Y-%m-%d')}（{week_day}）{start_datetime.strftime('%H:%M')}出发")
    if meeting_point:
        lines.append(f"📍集合点：{meeting_point}")
    lines.extend([
        "GPX轨迹分析｜规划参考",
        "📈路线总览",
        f"全程{stat['total_distance_km']}km｜累计爬升{stat['uphill_m']}m｜累计下降{stat['downhill_m']}m｜海拔{stat['min_elevation']}～{stat['max_elevation']}m",
        f"⏱预计用时：休闲{time_estimate['leisure']}｜正常{time_estimate['normal']}｜较快{time_estimate['fast']}",
        f"📊整体难度：{difficulty['score']}分｜{difficulty['level']}",
        "评分口径：里程35%＋累计爬升35%＋持续上坡P95 30%；P95按平滑海拔和约200米窗口计算，分段最陡值只作风险提示。",
        f"评分构成：里程{difficulty['distance_component']:.1f}/10｜爬升{difficulty['elevation_component']:.1f}/10｜持续坡度P95 {difficulty['sustained_grade_p95']:.1f}%（坡度{difficulty['slope_component']:.1f}/10）。",
    ])
    lines.extend(_weather_lines(waypoint_weather))
    lines.extend(_slope_lines(slope_segment_list))
    if service_points:
        service_text = "；".join(f"约{s['km']}km {s['name']}（{s['type']}）" for s in service_points)
        lines.append(f"🚻卫生间/补给：{service_text}。")
    else:
        lines.append("🚻卫生间/补给：轨迹未标注，出发前地图确认，自备饮水路餐。")
    lines.extend(_route_advice(stat, slope_segment_list, water_text))
    lines.append("📌安全：每小时主动饮水，观察同行者状态。")
    lines.append(f"🎒装备：防滑徒步鞋、登山杖、头灯、{water_text or '足量饮用水'}、路餐、防晒用品；另带雨具、急救包、充电宝。")
    lines.append("📌同行：保持队伍联系，勿单独离队。")
    lines.append("⚠免责声明：海拔、坡度和天气均为自动估算，不能代替现场路况与实时预警；遇恶劣天气或身体不适应及时撤退。")
    lines.append("📝本路书由 Vijay 开发的 hike-trail-analyzer 自动生成。")
    return _fit_report(lines)

"""
hike-gpx-analyzer-skill · Markdown专业报告生成器
Author: Vijay
"""
from datetime import datetime

def build_markdown_report(route_name:str,stat:dict,waypoint_weather:list,slope_segment_list:list,time_estimate:dict,start_datetime:datetime=None,service_points:list=None):
    date_text=None
    if start_datetime is not None:
        week_day="周"+"一二三四五六日"[start_datetime.weekday()]
        date_text=f"{start_datetime.strftime('%Y-%m-%d')}（{week_day}）{start_datetime.strftime('%H:%M')}"
    lines=[]
    lines.append(f"# 🥾{route_name} · 徒步出行分析报告")
    if date_text:
        lines.append(f"\n**📅出行日期：{date_text} 出发**")
    lines.append("> GPX轨迹自动分析 · 出行规划参考\n")

    lines.append("## 📈路线总览")
    lines.append("| 全程里程 | 累计爬升 | 累计下降 | 最高海拔 | 最低海拔 |")
    lines.append(f"| **{stat['total_distance_km']}** km | **{stat['uphill_m']}** m | **{stat['downhill_m']}** m | **{stat['max_elevation']}** m | **{stat['min_elevation']}** m |")
    lines.append(f"**⏱预估用时**：休闲 {time_estimate['leisure']} ｜ 正常 {time_estimate['normal']} ｜ 较快 {time_estimate['fast']}")
    level_text,diff_basis=get_difficulty_text(stat["total_distance_km"],stat["uphill_m"])
    lines.append(f"**📊整体难度**：{level_text}")
    lines.append(f"> {diff_basis}\n")

    lines.append("## 🌤沿途气象预估")
    lines.append("> 按预估到达时刻逐点查询，未指定出行日期时默认明天出发，可自定义出发时间重新测算；山区小气候变化较快，仅作规划参考\n")
    lines.append("| 点位位置 | 预估到达时刻 | 天气状况 | 降雨概率 | 出行提示 |")
    wp_labels=["起点","中途位置","海拔高点","关键路径点","终点"]
    for idx,row in enumerate(waypoint_weather):
        if row:
            lines.append(f"| {wp_labels[idx]} | {row['arrive_hm']} | {row['weather']} | {row['rain_prob']} | {row['risk']} |")
    lines.append("**📌气象综合建议**：出行前再次查看当地实时气象，山区天气变化较快，爬升阶段合理分配体力，定时补充饮用水，做好防晒。\n")

    lines.append("## 🛤分段坡度路况")
    lines.append(f"> 按全程里程等分{len(slope_segment_list)}段，坡度为段内最陡处推算值，不等于实地路况\n")
    lines.append("| 里程区间 | 最陡坡度 | 路况提示 |")
    for seg in slope_segment_list:
        lines.append(f"| {seg['range']} | {seg['slope']}% | {seg['desc']} |")
    lines.append("")

    lines.append("## 🚻沿途卫生间与补给点")
    if service_points:
        lines.append("| 大约位置 | 点位 | 类型 |")
        for s in service_points:
            lines.append(f"| 约{s['km']}km | {s['name']} | {s['type']} |")
        t_count=len([s for s in service_points if s["type"]=="🚻卫生间"])
        s_count=len([s for s in service_points if s["type"]=="🏪补给"])
        lines.append(f"**📌汇总**：卫生间共 {t_count} 处 ｜ 补给点共 {s_count} 处")
    else:
        lines.append("> 轨迹未标注卫生间/补给点，建议出行前用地图App确认沿途位置，并自备充足饮水食物")
    lines.append("")

    lines.append("## ⚠风险提示与装备建议")
    tips = [
        "长距离爬升路段体力消耗集中，整体行进节奏需要合理把控，避免前期体力透支。",
        "提前规划沿途水源补给，出行人员自备充足饮用水。",
        "部分区域手机信号较弱，建议提前把轨迹导入离线导航软件。",
        "野外路段存在碎石、树根，行走时注意脚下，下坡放慢步伐，防止滑倒崴脚。",
        "注意日落时间，预留返程缓冲时长，头灯建议随身携带。"
    ]
    for i,t in enumerate(tips,1):
        lines.append(f"{i}. {t}")
    lines.append("**🎒装备清单**")
    lines.append("✅必备：防滑徒步鞋、登山杖、头灯、足量饮用水、路餐、防晒用品")
    lines.append("🟡可选：简易净水工具、急救包、便携雨具、充电宝\n")

    lines.append("> ⚠免责声明")
    lines.append("> 路况结果仅由GPX轨迹海拔数据自动推算，无法识别实地路面情况，只可作为出行规划参考。")
    lines.append("> 气象预报存在误差，山区局部天气多变，请出行前核实最新气象预警，注意户外出行安全。")
    lines.append("> 📝 本报告由 Vijay 开发的 hike-gpx-analyzer-skill 自动生成")

    return "\n".join(lines)

def get_difficulty_text(distance:float,uphill:int):
    eff_km=distance+uphill/100
    intensity=uphill/distance if distance>0 else 0
    if eff_km<6 and intensity<40:
        level="轻松，适合大多数出行人员"
    elif eff_km<12 and intensity<70:
        level="中等，需要一定徒步体能基础"
    elif eff_km<18 and intensity<100:
        level="较高，对体能有一定要求，请评估自身状态"
    else:
        level="挑战级，适合有经验的徒步队伍，请做好充分准备"
    basis=f"测算依据：当量距离 {eff_km:.1f} km（里程 {distance} km + 累计爬升 {uphill} m÷100 折算）· 平均爬升强度 {intensity:.0f} m/km"
    return level,basis

"""
hike-gpx-analyzer-skill · Markdown专业报告生成器
Author: Vijay
"""
from datetime import datetime

def build_markdown_report(route_name:str,stat:dict,waypoint_weather:list,slope_segment_list:list,time_estimate:dict,start_datetime:datetime=None):
    date_text=None
    if start_datetime is not None:
        week_day="周"+"一二三四五六日"[start_datetime.weekday()]
        date_text=f"{start_datetime.strftime('%Y-%m-%d')}（{week_day}）{start_datetime.strftime('%H:%M')}"
    lines=[]
    lines.append(f"# 🥾徒步轨迹出行分析报告")
    if date_text:
        lines.append(f"\n**📅 出行日期：{date_text} 出发**")
    lines.append(f"> GPX轨迹自动分析 · 出行规划参考\n")

    lines.append("## 📈路线基础概况")
    lines.append(f"- 路线名称：{route_name}")
    lines.append(f"- 全程里程：{stat['total_distance_km']} km")
    lines.append(f"- 累计爬升：{stat['uphill_m']} m")
    lines.append(f"- 累计下降：{stat['downhill_m']} m")
    lines.append(f"- 最高海拔：{stat['max_elevation']} m")
    lines.append(f"- 最低海拔：{stat['min_elevation']} m\n")

    lines.append("## ⏱预估全程用时参考")
    lines.append(f"- 休闲节奏：{time_estimate['leisure']}")
    lines.append(f"- 正常节奏：{time_estimate['normal']}")
    lines.append(f"- 较快节奏：{time_estimate['fast']}\n")

    lines.append("## 📊路线整体难度评估")
    total_km=stat["total_distance_km"]
    up_m=stat["uphill_m"]
    level_text=get_difficulty_text(total_km,up_m)
    lines.append(f"{level_text}\n")

    lines.append("---\n")
    lines.append("## 🌤沿途关键点位气象预估（按预估到达时刻查询）")
    if date_text:
        lines.append(f"> **📅 出行日期：{date_text} 出发**，气象按预估到达时刻逐点查询")
    lines.append("> 未指定出行日期时默认明天出发，可自定义出发时间重新测算")
    lines.append("> 气象数据来源于公开逐小时预报，山区小气候变化较快，仅作为规划参考\n")
    lines.append("| 点位位置 | 预估到达时刻 | 天气状况 | 降雨概率 | 出行提示 |")
    lines.append("|---|---|---|---|---|")
    wp_labels=["起点","中途位置","海拔高点","关键路径点","终点"]
    for idx,row in enumerate(waypoint_weather):
        if row:
            lines.append(f"| {wp_labels[idx]} | {row['arrive_hm']} | {row['weather']} | {row['rain_prob']} | {row['risk']} |")
    lines.append("\n📌气象综合建议")
    lines.append("出行前再次查看当地实时气象，山区天气变化较快，爬升阶段合理分配体力，定时补充饮用水，做好防晒。\n")

    lines.append("---\n")
    lines.append("## 🛤分段路况坡度参考（轨迹数据推算，仅供参考）")
    lines.append("> 按全程里程等分10段，坡度为段内最陡处推算值，不等于实地路况\n")
    lines.append("| 里程区间 | 最陡坡度 | 路况提示 |")
    lines.append("|---|---|---|")
    for seg in slope_segment_list:
        lines.append(f"| {seg['range']} | {seg['slope']}% | {seg['desc']} |")
    lines.append("\n")

    lines.append("---\n")
    lines.append("## ⚠整体出行风险与注意事项")
    tips = [
        "长距离爬升路段体力消耗集中，整体行进节奏需要合理把控，避免前期体力透支。",
        "提前规划沿途水源补给，出行人员自备充足饮用水。",
        "部分区域手机信号较弱，建议提前把轨迹导入离线导航软件。",
        "野外路段存在碎石、树根，行走时注意脚下，下坡放慢步伐，防止滑倒崴脚。",
        "注意日落时间，预留返程缓冲时长，头灯建议随身携带。"
    ]
    for i,t in enumerate(tips,1):
        lines.append(f"{i}. {t}")

    lines.append("\n## 🎒参考装备清单")
    lines.append("✅必备：防滑徒步鞋、登山杖、头灯、足量饮用水、路餐、防晒用品")
    lines.append("🟡可选：简易净水工具、急救包、便携雨具、充电宝\n")

    lines.append("> ⚠免责声明")
    lines.append("> 路况结果仅由GPX轨迹海拔数据自动推算，无法识别实地路面情况，只可作为出行规划参考。")
    lines.append("> 气象预报存在误差，山区局部天气多变，请出行前核实最新气象预警，注意户外出行安全。")
    lines.append("> 📝 本报告由 Vijay 开发的 hike-gpx-analyzer-skill 自动生成")

    return "\n".join(lines)

def get_difficulty_text(distance:float,uphill:int):
    score=0
    if distance>12:
        score+=2
    elif distance>6:
        score+=1
    if uphill>800:
        score+=2
    elif uphill>350:
        score+=1
    if score<=1:
        return "整体难度：轻松，适合大多数有基础的出行人员"
    elif score<=3:
        return "整体难度：中等，需要一定徒步体能基础"
    else:
        return "整体难度：较高，对体能有一定要求，请出行人员评估自身状态"

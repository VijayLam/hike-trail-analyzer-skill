"""
hike-gpx-analyzer-skill · 纯文本专业报告生成器
Author: Vijay
"""
import math
import unicodedata
from datetime import datetime

KM_TO_MI=0.621371
M_TO_FT=3.28084
TECH_LEVELS={"T1":10,"T2":25,"T3":45,"T4":65,"T5":85,"T6":100}

def get_slope_factor(avg_slope_pct:float):
    if avg_slope_pct<5: return 1.00
    elif avg_slope_pct<10: return 1.05
    elif avg_slope_pct<15: return 1.10
    elif avg_slope_pct<20: return 1.20
    elif avg_slope_pct<30: return 1.30
    else: return 1.45

def get_altitude_factor(max_elev_m:int):
    if max_elev_m<1500: return 1.00
    elif max_elev_m<2000: return 1.03
    elif max_elev_m<2500: return 1.06
    elif max_elev_m<3000: return 1.10
    elif max_elev_m<3500: return 1.15
    elif max_elev_m<4000: return 1.22
    else: return 1.30

def infer_tech_level(steepest_slope_pct:float):
    s=abs(steepest_slope_pct)
    if s<10: return "T1"
    elif s<25: return "T2"
    elif s<40: return "T3"
    elif s<55: return "T4"
    elif s<70: return "T5"
    else: return "T6"

def get_difficulty_level(score:int):
    if score<=20: return "休闲"
    elif score<=40: return "简单"
    elif score<=60: return "中等"
    elif score<=75: return "较难"
    elif score<=90: return "困难"
    else: return "极难"

def assess_difficulty(stat:dict,steepest_slope_pct:float,tech_level:str=None):
    dist_km=stat["total_distance_km"]
    uphill_m=stat["uphill_m"]
    max_elev_m=stat["max_elevation"]
    dist_mi=dist_km*KM_TO_MI
    uphill_ft=uphill_m*M_TO_FT
    load=math.sqrt(2*dist_mi*uphill_ft)
    base_score=min(100,load/1.2)
    avg_slope=uphill_m/(dist_km*1000)*100 if dist_km>0 else 0
    slope_f=get_slope_factor(avg_slope)
    alt_f=get_altitude_factor(max_elev_m)
    tech=tech_level if tech_level in TECH_LEVELS else infer_tech_level(steepest_slope_pct)
    tech_score=TECH_LEVELS[tech]
    score=min(100,round(base_score*slope_f*alt_f*0.8+tech_score*0.2))
    if tech_score>=90:
        score=max(score,85)
    elif tech_score>=80:
        score=max(score,75)
    physical_part=base_score*slope_f*alt_f*0.8
    contributions=[
        ("累计爬升",physical_part*0.5),
        ("全程里程",physical_part*0.5),
        ("坡度修正",base_score*(slope_f-1)*alt_f*0.8),
        ("海拔修正",base_score*slope_f*(alt_f-1)*0.8),
        ("技术难度",tech_score*0.2),
    ]
    contributions.sort(key=lambda x:x[1],reverse=True)
    return {
        "dist_km":dist_km,"uphill_m":uphill_m,"max_elev_m":max_elev_m,"avg_slope":avg_slope,
        "dist_mi":dist_mi,"uphill_ft":uphill_ft,"load":load,"base_score":base_score,
        "slope_f":slope_f,"alt_f":alt_f,"tech":tech,"tech_score":tech_score,
        "steepest":steepest_slope_pct,"score":score,"level":get_difficulty_level(score),
        "top3":[c for c in contributions if c[1]>0][:3],
    }

def build_difficulty_lines(a:dict):
    return [
        f"📊整体难度：{a['score']}分 ｜ {a['level']}",
        "主要影响因素：" + "、".join(f"{name}（贡献约{v:.0f}分）" for name,v in a["top3"]),
    ]

def _display_width(text:str):
    return sum(2 if unicodedata.east_asian_width(c) in "FW" else 1 for c in text)

def _to_fullwidth(text:str):
    result=[]
    for c in text:
        code=ord(c)
        if c==" ":
            result.append("　")
        elif 33<=code<=126:
            result.append(chr(code+0xFEE0))
        else:
            result.append(c)
    return "".join(result)

def render_table(headers:list,rows:list):
    all_rows=[[_to_fullwidth(c) for c in row] for row in [headers]+rows]
    widths=[max(_display_width(r[i]) for r in all_rows) for i in range(len(headers))]
    last=len(widths)-1
    def render_row(cells):
        parts=[]
        for i,c in enumerate(cells):
            if i==last:
                parts.append(c)
            else:
                parts.append(c+"　"*((widths[i]+2-_display_width(c))//2))
        return "".join(parts)
    return [render_row(r) for r in all_rows]

def build_report(route_name:str,stat:dict,waypoint_weather:list,slope_segment_list:list,time_estimate:dict,start_datetime:datetime=None,service_points:list=None,meeting_point:str=None,steepest_slope:float=0):
    date_text=None
    if start_datetime is not None:
        week_day="周"+"一二三四五六日"[start_datetime.weekday()]
        date_text=f"{start_datetime.strftime('%Y-%m-%d')}（{week_day}）{start_datetime.strftime('%H:%M')}"
    lines=[]
    lines.append(f"🥾{route_name} · 徒步出行分析报告")
    if date_text:
        lines.append(f"\n📅出行日期：{date_text} 出发")
    if meeting_point:
        lines.append(f"📍集合点：{meeting_point}")
    lines.append("GPX轨迹自动分析 · 出行规划参考\n")

    lines.append("📈路线总览")
    lines.append(f"全程里程：{stat['total_distance_km']} km")
    lines.append(f"累计爬升：{stat['uphill_m']} m")
    lines.append(f"累计下降：{stat['downhill_m']} m")
    lines.append(f"最高海拔：{stat['max_elevation']} m")
    lines.append(f"最低海拔：{stat['min_elevation']} m")
    lines.append(f"⏱预估用时：休闲 {time_estimate['leisure']} ｜ 正常 {time_estimate['normal']} ｜ 较快 {time_estimate['fast']}")
    lines+=build_difficulty_lines(assess_difficulty(stat,steepest_slope))
    lines.append("")

    lines.append("🌤沿途气象预估")
    lines.append("按预估到达时刻逐点查询，未指定出行日期时默认明天出发，可自定义出发时间重新测算；山区小气候变化较快，仅作规划参考\n")
    wp_labels=["起点","中途位置","海拔高点","关键路径点","终点"]
    weather_rows=[[wp_labels[idx],row['arrive_hm'],row['weather'],row['rain_prob'],row['risk']] for idx,row in enumerate(waypoint_weather) if row]
    lines+=render_table(["点位位置","预估到达时刻","天气状况","降雨概率","出行提示"],weather_rows)
    lines.append("📌气象综合建议：出行前再次查看当地实时气象，山区天气变化较快，爬升阶段合理分配体力，定时补充饮用水，做好防晒。\n")

    lines.append("🛤分段坡度路况")
    lines.append(f"按全程里程等分{len(slope_segment_list)}段，坡度为段内最陡处推算值，不等于实地路况\n")
    lines+=render_table(["里程区间","最陡坡度","路况提示"],[[seg['range'],f"{seg['slope']}%",seg['desc']] for seg in slope_segment_list])
    lines.append("")

    lines.append("🚻沿途卫生间与补给点")
    if service_points:
        lines+=render_table(["大约位置","点位","类型"],[[f"约{s['km']}km",s['name'],s['type']] for s in service_points])
        t_count=len([s for s in service_points if s["type"]=="🚻卫生间"])
        s_count=len([s for s in service_points if s["type"]=="🏪补给"])
        lines.append(f"📌汇总：卫生间共 {t_count} 处 ｜ 补给点共 {s_count} 处")
    else:
        lines.append("轨迹未标注卫生间/补给点，建议出行前用地图App确认沿途位置，并自备充足饮水食物")
    lines.append("")

    lines.append("⚠风险提示与装备建议")
    tips = [
        "长距离爬升路段体力消耗集中，整体行进节奏需要合理把控，避免前期体力透支。",
        "提前规划沿途水源补给，出行人员自备充足饮用水。",
        "部分区域手机信号较弱，建议提前把轨迹导入离线导航软件。",
        "野外路段存在碎石、树根，行走时注意脚下，下坡放慢步伐，防止滑倒崴脚。",
        "注意日落时间，预留返程缓冲时长，头灯建议随身携带。"
    ]
    for i,t in enumerate(tips,1):
        lines.append(f"{i}. {t}")
    lines.append("🎒装备清单")
    lines.append("✅必备：防滑徒步鞋、登山杖、头灯、足量饮用水、路餐、防晒用品")
    lines.append("🟡可选：简易净水工具、急救包、便携雨具、充电宝\n")

    lines.append("⚠免责声明")
    lines.append("1. 路况结果仅由GPX轨迹海拔数据自动推算，无法识别实地路面情况，只可作为出行规划参考。")
    lines.append("2. 气象预报存在误差，山区局部天气多变，请出行前核实最新气象预警，注意户外出行安全。")
    lines.append("📝本报告由 Vijay 开发的 hike-gpx-analyzer-skill 自动生成")

    return "\n".join(lines)

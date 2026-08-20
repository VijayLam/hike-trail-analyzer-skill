"""
hike-gpx-analyzer-skill · 主入口
Author: Vijay
"""
from gpx_engine import load_gpx,extract_all_track_points,get_basic_statistic,sample_way_points,segment_slope_analysis
from weather_provider import fetch_point_weather
from report_builder import build_markdown_report
from settings import DEFAULT_START_HOUR,SPEED_LEISURE_KMH,SPEED_NORMAL_KMH,SPEED_FAST_KMH,SAMPLE_KEY_POINT_COUNT,SLOPE_INTERVAL_STEP
from datetime import datetime,timedelta
import os

def run_hike_analysis(gpx_file_path:str,route_name:str="未命名路线",start_datetime:datetime=None):
    if start_datetime is None:
        today=datetime.now().date()
        start_datetime=datetime.combine(today,datetime.min.time())+timedelta(hours=DEFAULT_START_HOUR)

    gpx=load_gpx(gpx_file_path)
    stat=get_basic_statistic(gpx)
    all_points=extract_all_track_points(gpx)
    key_points=sample_way_points(all_points,SAMPLE_KEY_POINT_COUNT)
    slope_segs=segment_slope_analysis(all_points,SLOPE_INTERVAL_STEP)
    total_km=stat["total_distance_km"]

    time_est={
        "leisure":f"{round(total_km/SPEED_LEISURE_KMH,1)}～{round(total_km/SPEED_LEISURE_KMH+1.0,1)} h",
        "normal":f"{round(total_km/SPEED_NORMAL_KMH,1)}～{round(total_km/SPEED_NORMAL_KMH+0.8,1)} h",
        "fast":f"{round(total_km/SPEED_FAST_KMH,1)}～{round(total_km/SPEED_FAST_KMH+0.6,1)} h"
    }

    weather_result=[]
    for idx,pt in enumerate(key_points):
        progress_ratio=(idx+1)/len(key_points)
        travel_h=total_km*progress_ratio/SPEED_NORMAL_KMH
        arrive_dt=start_datetime+timedelta(hours=travel_h)
        w_data=fetch_point_weather(pt["lat"],pt["lon"],arrive_dt)
        weather_result.append(w_data)

    md_output=build_markdown_report(route_name,stat,weather_result,slope_segs,time_est)
    os.makedirs("output",exist_ok=True)
    out_path=os.path.join("output","hike_report.md")
    with open(out_path,"w",encoding="utf-8") as f:
        f.write(md_output)
    print(f"✅分析报告已输出至 {out_path}")
    return {"markdown":md_output,"statistic":stat}

if __name__=="__main__":
    res=run_hike_analysis("./sample/trace.gpx",route_name="测试徒步路线")
    print(res["statistic"])

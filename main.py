"""
hike-trail-analyzer · 主入口
Author: Vijay
"""
import sys
from track_engine import (load_track_file,extract_all_track_points,get_basic_statistic,sample_way_points,
                          segment_slope_analysis,compute_cumulative_km,compute_sustained_grade_p95,
                          extract_waypoints,find_service_points,find_meeting_point)
from weather_provider import fetch_point_weather
from report_builder import build_report
from settings import (DEFAULT_START_HOUR,SPEED_LEISURE_KMH,SPEED_NORMAL_KMH,SPEED_FAST_KMH,
                      SAMPLE_KEY_POINT_COUNT,SEGMENT_COUNT,SLOPE_SAMPLE_STEP,
                      TOILET_KEYWORDS,SUPPLY_KEYWORDS,INVALID_MEETING_KEYWORDS,
                      INVALID_MEETING_EXACT,PLACE_NAME_CHARS)
from datetime import datetime,timedelta

def run_hike_analysis(gpx_file_path:str,route_name:str="未命名路线",start_datetime:datetime=None):
    if start_datetime is None:
        tomorrow=datetime.now().date()+timedelta(days=1)
        start_datetime=datetime.combine(tomorrow,datetime.min.time())+timedelta(hours=DEFAULT_START_HOUR)

    track=load_track_file(gpx_file_path)
    stat=get_basic_statistic(track)
    all_points=extract_all_track_points(track)
    key_points=sample_way_points(all_points,SAMPLE_KEY_POINT_COUNT)
    slope_segs=segment_slope_analysis(all_points,SEGMENT_COUNT,SLOPE_SAMPLE_STEP)
    sustained_grade_p95=compute_sustained_grade_p95(all_points)
    cum_km=compute_cumulative_km(all_points)
    waypoints=extract_waypoints(track)
    service_points=find_service_points(waypoints,all_points,cum_km,TOILET_KEYWORDS,SUPPLY_KEYWORDS)
    meeting_point=find_meeting_point(waypoints,all_points[0],INVALID_MEETING_KEYWORDS,INVALID_MEETING_EXACT,PLACE_NAME_CHARS)
    total_km=stat["total_distance_km"]

    time_est={
        "leisure":f"{round(total_km/SPEED_LEISURE_KMH,1)}～{round(total_km/SPEED_LEISURE_KMH+1.0,1)} h",
        "normal":f"{round(total_km/SPEED_NORMAL_KMH,1)}～{round(total_km/SPEED_NORMAL_KMH+0.8,1)} h",
        "fast":f"{round(total_km/SPEED_FAST_KMH,1)}～{round(total_km/SPEED_FAST_KMH+0.6,1)} h"
    }

    weather_result=[]
    n=len(key_points)
    for idx,pt in enumerate(key_points):
        progress_ratio=idx/(n-1) if n>1 else 0
        travel_h=total_km*progress_ratio/SPEED_NORMAL_KMH
        arrive_dt=start_datetime+timedelta(hours=travel_h)
        w_data=fetch_point_weather(pt["lat"],pt["lon"],arrive_dt)
        weather_result.append(w_data)

    md_output=build_report(route_name,stat,weather_result,slope_segs,time_est,start_datetime,service_points,meeting_point,sustained_grade_p95)
    print(md_output)
    return {"markdown":md_output,"statistic":stat}

def parse_start_datetime(date_arg:str,time_arg:str=None):
    start=datetime.strptime(date_arg,"%Y-%m-%d")
    if time_arg:
        start=datetime.combine(start.date(),datetime.strptime(time_arg,"%H:%M").time())
    else:
        start+=timedelta(hours=DEFAULT_START_HOUR)
    return start

if __name__=="__main__":
    if len(sys.argv)<2:
        print("用法: python main.py <gpx文件路径> [路线名称] [出发日期YYYY-MM-DD] [出发时刻HH:MM]",file=sys.stderr)
        sys.exit(1)
    route_name=sys.argv[2] if len(sys.argv)>2 else "未命名路线"
    start_datetime=parse_start_datetime(sys.argv[3],sys.argv[4] if len(sys.argv)>4 else None) if len(sys.argv)>3 else None
    run_hike_analysis(sys.argv[1],route_name=route_name,start_datetime=start_datetime)

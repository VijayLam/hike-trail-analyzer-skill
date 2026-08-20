"""
hike-gpx-analyzer-skill · GPX解析与坡度分析核心引擎
Author: Vijay
"""
import gpxpy
import gpxpy.gpx
from typing import List, Dict

def load_gpx(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)
    return gpx

def extract_all_track_points(gpx) -> List[Dict]:
    point_list = []
    for track in gpx.tracks:
        for seg in track.segments:
            for p in seg.points:
                point_list.append({
                    "lat": p.latitude,
                    "lon": p.longitude,
                    "elevation": p.elevation if p.elevation is not None else 0,
                    "time": p.time
                })
    return point_list

def get_basic_statistic(gpx):
    moving = gpx.get_moving_data()
    elev_ext = gpx.get_elevation_extremes()
    return {
        "total_distance_km": round(moving.moving_distance / 1000, 1),
        "uphill_m": int(moving.uphill),
        "downhill_m": int(moving.downhill),
        "max_elevation": int(elev_ext.maximum if elev_ext.maximum else 0),
        "min_elevation": int(elev_ext.minimum if elev_ext.minimum else 0)
    }

def sample_way_points(points: List[Dict], sample_count: int):
    total = len(points)
    if total <= sample_count:
        return points
    step = total // sample_count
    result = []
    for i in range(0, total, step):
        result.append(points[i])
        if len(result) >= sample_count:
            break
    return result

def segment_slope_analysis(points: List[Dict], interval: int):
    output = []
    for i in range(interval, len(points), interval):
        p0 = points[i - interval]
        p1 = points[i]
        delta_h = p1["elevation"] - p0["elevation"]
        dist_m = 1000
        if dist_m <= 0:
            slope_percent = 0
        else:
            slope_percent = round((delta_h / dist_m) * 100, 2)
        desc = get_slope_description(slope_percent)
        output.append({
            "index": i,
            "slope": slope_percent,
            "desc": desc
        })
    return output

def get_slope_description(slope: float):
    if slope < -15:
        return "陡坡下行，容易打滑，注意控制步伐"
    elif slope < -6:
        return "缓下坡路段，留意脚下碎石"
    elif slope <= 6:
        return "平缓路段，行进较为轻松"
    elif slope <=15:
        return "缓上坡，持续消耗体力"
    else:
        return "较陡上坡，体力消耗较大"

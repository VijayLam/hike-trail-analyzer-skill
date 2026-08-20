"""
hike-gpx-analyzer-skill · GPX解析与坡度分析核心引擎
Author: Vijay
"""
import gpxpy
import gpxpy.gpx
from bisect import bisect_left
from gpxpy.geo import haversine_distance
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
    updown = gpx.get_uphill_downhill()
    elev_ext = gpx.get_elevation_extremes()
    return {
        "total_distance_km": round(moving.moving_distance / 1000, 1),
        "uphill_m": int(updown.uphill),
        "downhill_m": int(updown.downhill),
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

def segment_slope_analysis(points: List[Dict], segment_count: int, sample_step: int):
    total = len(points)
    if total < 2:
        return []
    cum_km = [0.0]
    for k in range(1, total):
        d = haversine_distance(points[k - 1]["lat"], points[k - 1]["lon"], points[k]["lat"], points[k]["lon"])
        cum_km.append(cum_km[-1] + d / 1000)
    seg_km = cum_km[-1] / segment_count
    output = []
    for i in range(1, segment_count + 1):
        seg_start = min(bisect_left(cum_km, (i - 1) * seg_km), total - 1)
        seg_end = min(bisect_left(cum_km, i * seg_km), total - 1)
        max_slope = 0.0
        for j in range(seg_start, seg_end, sample_step):
            p0 = points[j]
            p1 = points[min(j + sample_step, seg_end)]
            if p1 is p0:
                continue
            delta_h = p1["elevation"] - p0["elevation"]
            dist_m = haversine_distance(p0["lat"], p0["lon"], p1["lat"], p1["lon"])
            if dist_m <= 0:
                continue
            slope = delta_h / dist_m * 100
            if abs(slope) > abs(max_slope):
                max_slope = slope
        output.append({
            "range": f"{cum_km[seg_start]:.1f}～{cum_km[seg_end]:.1f} km",
            "slope": round(max_slope, 2),
            "desc": get_slope_description(max_slope)
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

"""
hike-gpx-analyzer-skill · 轨迹解析与坡度分析核心引擎（支持GPX/KML/KMZ）
Author: Vijay
"""
import zipfile
import xml.etree.ElementTree as ET
import gpxpy
import gpxpy.gpx
from bisect import bisect_left
from gpxpy.geo import haversine_distance
from typing import List, Dict

KML_NS = {"kml": "http://www.opengis.net/kml/2.2"}

def load_gpx(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)
    return gpx

def parse_kml_text(kml_text: str):
    root = ET.fromstring(kml_text)
    track_points = []
    for line_string in root.iter("{http://www.opengis.net/kml/2.2}LineString"):
        coords = line_string.find("kml:coordinates", KML_NS)
        if coords is None or not coords.text:
            continue
        for tok in coords.text.split():
            parts = tok.split(",")
            if len(parts) >= 2:
                ele = float(parts[2]) if len(parts) >= 3 and parts[2] else None
                track_points.append({"lat": float(parts[1]), "lon": float(parts[0]), "elevation": ele, "time": None})
    for track in root.iter("{http://www.google.com/kml/ext/2.2}Track"):
        for coord in track.iter("{http://www.google.com/kml/ext/2.2}coord"):
            parts = coord.text.split()
            if len(parts) >= 2:
                ele = float(parts[2]) if len(parts) >= 3 and parts[2] else None
                track_points.append({"lat": float(parts[1]), "lon": float(parts[0]), "elevation": ele, "time": None})
    waypoints = []
    for placemark in root.iter("{http://www.opengis.net/kml/2.2}Placemark"):
        name_el = placemark.find("kml:name", KML_NS)
        point = placemark.find("kml:Point", KML_NS)
        if point is None:
            continue
        coords = point.find("kml:coordinates", KML_NS)
        if coords is None or not coords.text or name_el is None or not name_el.text:
            continue
        tok = coords.text.split()[0].split(",")
        if len(tok) >= 2:
            waypoints.append({"name": name_el.text.strip(), "lat": float(tok[1]), "lon": float(tok[0])})
    return track_points, waypoints

class _GpxCompatible:
    def __init__(self, track_points: List[Dict], waypoints: List[Dict]):
        class _P:
            def __init__(self, p):
                self.latitude = p["lat"]
                self.longitude = p["lon"]
                self.elevation = p["elevation"]
                self.time = p.get("time")
        class _Seg:
            points = [_P(p) for p in track_points]
        class _Track:
            segments = [_Seg()]
        class _Wpt:
            def __init__(self, w):
                self.name = w["name"]
                self.latitude = w["lat"]
                self.longitude = w["lon"]
        self.tracks = [_Track()]
        self.waypoints = [_Wpt(w) for w in waypoints]
        pts = _Seg.points
        dist = sum(haversine_distance(a.latitude, a.longitude, b.latitude, b.longitude) for a, b in zip(pts, pts[1:]))
        up = down = 0.0
        for a, b in zip(pts, pts[1:]):
            if a.elevation is None or b.elevation is None:
                continue
            delta = b.elevation - a.elevation
            if delta > 0:
                up += delta
            else:
                down -= delta
        elevations = [p.elevation for p in pts if p.elevation is not None]
        class _Moving:
            moving_distance = dist
        class _UpDown:
            uphill = up
            downhill = down
        class _Extremes:
            maximum = max(elevations) if elevations else None
            minimum = min(elevations) if elevations else None
        self._moving = _Moving()
        self._updown = _UpDown()
        self._extremes = _Extremes()
    def get_moving_data(self):
        return self._moving
    def get_uphill_downhill(self):
        return self._updown
    def get_elevation_extremes(self):
        return self._extremes

def load_track_file(file_path: str):
    lower = file_path.lower()
    if lower.endswith(".kmz"):
        with zipfile.ZipFile(file_path) as z:
            kml_names = sorted([n for n in z.namelist() if n.lower().endswith(".kml")],
                               key=lambda n: (not n.lower().endswith("doc.kml"), len(n)))
            with z.open(kml_names[0]) as f:
                track_points, waypoints = parse_kml_text(f.read().decode("utf-8", errors="ignore"))
        return _GpxCompatible(track_points, waypoints)
    if lower.endswith(".kml"):
        with open(file_path, "r", encoding="utf-8") as f:
            track_points, waypoints = parse_kml_text(f.read())
        return _GpxCompatible(track_points, waypoints)
    return load_gpx(file_path)

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

def compute_cumulative_km(points: List[Dict]):
    cum_km=[0.0]
    for k in range(1,len(points)):
        d=haversine_distance(points[k-1]["lat"],points[k-1]["lon"],points[k]["lat"],points[k]["lon"])
        cum_km.append(cum_km[-1]+d/1000)
    return cum_km

def extract_waypoints(gpx) -> List[Dict]:
    result=[]
    for w in gpx.waypoints:
        name=(w.name or "").strip()
        if not name:
            continue
        result.append({"name":name,"lat":w.latitude,"lon":w.longitude})
    return result

def is_valid_meeting_name(name:str,invalid_keywords:List[str],invalid_exact:List[str],place_chars:str):
    if len(name)<2 or name in invalid_exact:
        return False
    lower=name.lower()
    if any(kw in lower for kw in invalid_keywords):
        return False
    return any(c in place_chars for c in name)

def find_meeting_point(waypoints: List[Dict], start_point: Dict, invalid_keywords: List[str], invalid_exact: List[str], place_chars: str, max_distance_m: float = 500):
    best_name=None
    best_d=max_distance_m
    for w in waypoints:
        d=haversine_distance(w["lat"],w["lon"],start_point["lat"],start_point["lon"])
        if d<best_d and is_valid_meeting_name(w["name"],invalid_keywords,invalid_exact,place_chars):
            best_d=d
            best_name=w["name"]
    coord=f"（{start_point['lat']:.5f}, {start_point['lon']:.5f}）"
    if best_name:
        return f"{best_name}{coord}"
    return f"待定{coord}"

def find_service_points(waypoints: List[Dict],points: List[Dict],cum_km: List[float],toilet_keywords: List[str],supply_keywords: List[str]):
    result=[]
    seen=set()
    for w in waypoints:
        key=(w["name"],round(w["lat"],5),round(w["lon"],5))
        if key in seen:
            continue
        seen.add(key)
        name_lower=w["name"].lower()
        if any(kw in name_lower for kw in toilet_keywords):
            wtype="🚻卫生间"
        elif any(kw in name_lower for kw in supply_keywords):
            wtype="🏪补给"
        else:
            continue
        result.append({"km":round(nearest_track_km(w,points,cum_km)),"name":w["name"],"type":wtype})
    result.sort(key=lambda g:g["km"])
    return result

def nearest_track_km(wpt: Dict,points: List[Dict],cum_km: List[float]):
    best_i=0
    best_d=float("inf")
    for i,p in enumerate(points):
        d=haversine_distance(wpt["lat"],wpt["lon"],p["lat"],p["lon"])
        if d<best_d:
            best_d=d
            best_i=i
    return cum_km[best_i]

def segment_slope_analysis(points: List[Dict], segment_count: int, sample_step: int):
    total = len(points)
    if total < 2:
        return []
    cum_km = compute_cumulative_km(points)
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
            if dist_m < 30:
                continue
            slope = max(-100.0, min(100.0, delta_h / dist_m * 100))
            if abs(slope) > abs(max_slope):
                max_slope = slope
        slope_int = round(max_slope)
        output.append({
            "range": f"{round(cum_km[seg_start])}～{round(cum_km[seg_end])} km",
            "slope": slope_int,
            "desc": get_slope_description(slope_int)
        })
    return output

def get_slope_description(slope: float):
    s=abs(slope)
    if s<30:
        return "平缓路段，行进较为轻松"
    elif s<40:
        return "小爬升，保持节奏" if slope>0 else "小下降，留意脚下"
    elif s<50:
        return "较陡上坡，体力消耗较大" if slope>0 else "较陡下坡，控制步伐防滑"
    else:
        return "陡坡急升，量力而行" if slope>0 else "陡坡急降，易打滑，谨慎慢行"

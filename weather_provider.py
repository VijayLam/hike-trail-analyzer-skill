"""
hike-gpx-analyzer-skill · open-meteo气象数据模块
Author: Vijay
"""
import sys
import requests
from datetime import datetime
from typing import Optional, Dict

def fetch_point_weather(lat: float, lon: float, target_time: datetime) -> Optional[Dict]:
    base_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,precipitation_probability,weather_code"
        f"&timezone=Asia/Shanghai"
    )
    try:
        resp = requests.get(base_url, timeout=15)
        data = resp.json()
        hourly = data["hourly"]
        time_arr = hourly["time"]
        rain_prob_arr = hourly["precipitation_probability"]
        code_arr = hourly["weather_code"]
        target_str = target_time.strftime("%Y-%m-%dT%H:00")
        try:
            pos = time_arr.index(target_str)
        except ValueError:
            return None
        w_code = code_arr[pos]
        weather_text = map_weather_code(w_code)
        rain_p = rain_prob_arr[pos]
        risk_note = build_risk_note(rain_p)
        return {
            "arrive_hm": target_time.strftime("%H:%M"),
            "weather": weather_text,
            "rain_prob": f"{rain_p}%",
            "risk": risk_note
        }
    except Exception as e:
        print("天气获取异常：", str(e), file=sys.stderr)
        return None

def map_weather_code(code: int):
    if code == 0:
        return "晴"
    elif 1 <= code <=3:
        return "多云"
    elif 45 <= code <=48:
        return "有雾"
    elif 51 <= code <= 67 or 80 <= code <= 82:
        return "降雨"
    else:
        return "天气状况未知"

def build_risk_note(rain_prob:int):
    if rain_prob >= 60:
        return "降雨可能性高，土路湿滑，务必携带防雨装备，谨慎行进"
    elif rain_prob >=30:
        return "存在局部降雨概率，建议备好雨具，留意天气变化"
    else:
        return "气象条件整体平稳，正常行进"

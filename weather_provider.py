"""
hike-trail-analyzer · wttr.in 公开气象数据模块
Author: Vijay
"""
import sys
from datetime import datetime
from typing import Dict, Optional

import requests

WTTR_URL = "https://wttr.in/{lat:.5f},{lon:.5f}"
REQUEST_TIMEOUT_SECONDS = 20


def fetch_point_weather(lat: float, lon: float, target_time: datetime) -> Optional[Dict]:
    """查询指定坐标在目标时刻附近的天气预报。

    wttr.in 不需要 API Key，返回当地日期和 3 小时粒度的预报；
    路书使用目标时刻所在日期中距离最近的预报时段。
    """
    url = WTTR_URL.format(lat=lat, lon=lon)
    try:
        response = requests.get(
            url,
            params={"format": "j1"},
            headers={"User-Agent": "hike-trail-analyzer/1.0"},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()

        target_date = target_time.strftime("%Y-%m-%d")
        forecast_day = next(
            (day for day in data.get("weather", []) if day.get("date") == target_date),
            None,
        )
        if not forecast_day:
            print(f"天气获取异常：公开接口没有返回 {target_date} 的预报", file=sys.stderr)
            return None

        hourly = forecast_day.get("hourly") or []
        if not hourly:
            return None
        forecast = min(hourly, key=lambda item: abs(_hour_from_wttr(item.get("time")) - target_time.hour))

        description = _first_value(forecast.get("weatherDesc"), "value")
        rain_probability = _to_int(forecast.get("chanceofrain"))
        temperature = _to_float(forecast.get("tempC"))
        risk_note = build_risk_note(rain_probability)
        return {
            "arrive_hm": target_time.strftime("%H:%M"),
            "weather": map_weather_description(description),
            "temp_c": round(temperature) if temperature is not None else None,
            "rain_prob": f"{rain_probability}%" if rain_probability is not None else "—",
            "risk": risk_note,
        }
    except Exception as exc:
        print("天气获取异常：", str(exc), file=sys.stderr)
        return None


def _hour_from_wttr(value) -> int:
    """将 wttr.in 的时间值（如 0、300、1200）转换为小时。"""
    try:
        return (int(str(value)) // 100) % 24
    except (TypeError, ValueError):
        return 0


def _first_value(items, key: str) -> str:
    if isinstance(items, list) and items and isinstance(items[0], dict):
        return str(items[0].get(key) or "")
    return ""


def _to_int(value) -> Optional[int]:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _to_float(value) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def map_weather_description(description: str) -> str:
    text = description.strip().lower()
    if any(word in text for word in ("thunder", "storm")):
        return "雷雨"
    if any(word in text for word in ("snow", "sleet", "ice")):
        return "降雪或雨夹雪"
    if any(word in text for word in ("rain", "shower", "drizzle")):
        return "降雨"
    if any(word in text for word in ("fog", "mist", "haze", "smoke")):
        return "雾/霾"
    if any(word in text for word in ("cloud", "overcast")):
        return "多云"
    if any(word in text for word in ("clear", "sunny", "fair")):
        return "晴"
    return "天气状况未知"


def build_risk_note(rain_probability: Optional[int]) -> str:
    if rain_probability is None:
        return "降雨概率暂无数据，出发前核实天气"
    if rain_probability >= 60:
        return "降雨概率高，防雨防滑慢行"
    if rain_probability >= 30:
        return "或有降雨，建议备好雨具"
    return "气象平稳，正常行进"

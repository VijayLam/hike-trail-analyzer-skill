"""
hike-trail-analyzer · 全局配置
Author: Vijay
"""
# 徒步全局配置参数，可外部传入覆盖
DEFAULT_START_HOUR = 9
SPEED_LEISURE_KMH = 2.5
SPEED_NORMAL_KMH = 3.2
SPEED_FAST_KMH = 4.0
SAMPLE_KEY_POINT_COUNT = 5
SEGMENT_COUNT = 6
SLOPE_SAMPLE_STEP = 12
TOILET_KEYWORDS = ["厕所","卫生间","洗手间","公厕","wc","toilet"]
SUPPLY_KEYWORDS = ["补给","驿站","便利店","商店","小卖部","士多","超市","买水","补水","水站","售货机","贩卖机","餐厅","饭店","农家乐","水果","凉茶"]
INVALID_MEETING_KEYWORDS = ["左","右","上去","下去","向上","向下","往上","往下","往前","往后","前进","返回","回头","直行","商店","洗手间","卫生间","厕所","公厕","wc","toilet","补给","驿站","便利店","小卖部","士多","超市","水站","售货机","贩卖机","餐厅","饭店","农家乐","买水","补水"]
INVALID_MEETING_EXACT = ["起点","终点","入口","出口","停车场","大门","山门","路口","岔口","岔路"]
PLACE_NAME_CHARS = "山岭峰顶坡坪岗亭台楼阁门寺庙庵观祠堂桥洞岩崖壁谷湖潭泉溪河瀑滩村庄寨园苑馆场坊渡码关隘海岛"

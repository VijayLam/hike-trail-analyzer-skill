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
# 综合难度评分：按平滑海拔、等距重采样和持续坡度窗口计算
SLOPE_SMOOTH_WINDOW = 9
SLOPE_RESAMPLE_INTERVAL_M = 30
SUSTAINED_GRADE_WINDOW_M = 200
TOILET_KEYWORDS = ["厕所","卫生间","洗手间","公厕","wc","toilet"]
SUPPLY_KEYWORDS = ["补给","驿站","便利店","商店","小卖部","士多","超市","买水","补水","水站","售货机","贩卖机","餐厅","饭店","农家乐","水果","凉茶"]
INVALID_MEETING_KEYWORDS = ["左","右","上去","下去","向上","向下","往上","往下","往前","往后","前进","返回","回头","直行","商店","洗手间","卫生间","厕所","公厕","wc","toilet","补给","驿站","便利店","小卖部","士多","超市","水站","售货机","贩卖机","餐厅","饭店","农家乐","买水","补水"]
INVALID_MEETING_EXACT = ["起点","终点","入口","出口","停车场","大门","山门","路口","岔口","岔路"]
PLACE_NAME_CHARS = "山岭峰顶坡坪岗亭台楼阁门寺庙庵观祠堂桥洞岩崖壁谷湖潭泉溪河瀑滩村庄寨园苑馆场坊渡码关隘海岛"

# ===== 实测轨迹分析（P0）=====
ACT_STOP_SPEED_KMH = 0.8     # 区间速度低于此值判静止（经两步路真值校准，误差<5%）
ACT_GAP_STOP_SEC = 120       # 相邻点间隔超此值直接计静止（休息时记录器降频产生的空洞）
ACT_MAX_SPEED_KMH = 30       # 超过视为GPS漂移尖点：距离与爬升剔除、时间计静止
ACT_MIN_REST_SEC = 300       # 连续静止达到此秒数才计1次休息（拍照/喘气不计数）
ACT_ELE_SMOOTH_WINDOW = 9    # 海拔平滑移动平均窗口（点数，经两步路爬升真值校准）
ACT_SEGMENT_COUNT = 6        # 实测分段配速的等里程段数
ACT_MIN_CLIMB_RATE_M = 30    # 段爬升低于此米数不显示段爬升速度（平路段无意义）
ACT_HISTORY_PATH = "data/hike_history.json"

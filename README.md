# hike-gpx-analyzer-skill
通用专业徒步轨迹分析Skill

**Author: Vijay** · 由 Vijay 设计开发并维护
功能说明：
导入一份GPX轨迹文件，自动生成一份专业徒步出行分析Markdown报告。
输出内容包含：路线总览（里程/爬升/海拔KPI、预估用时、难度评估）、沿途气象预估、分段坡度路况、卫生间与补给点、风险提示与装备建议。
适合徒步活动组织者做路线规划参考。

## 使用方式
1. 安装依赖
pip install -r requirements.txt
2. 将gpx轨迹文件放入sample目录，命名 trace.gpx
3. 运行
python main.py
报告直接在终端完整输出，可直接复制使用；未指定出发时间时默认明天出发，报告内出行日期加粗标注

## 调用方式
外部可调用 run_hike_analysis(gpx路径,路线名称,可选自定义出发时间)

## 部署
整套工程可以直接上传GitHub，在Claude Code  codex中迭代、测试。

## 作者
Vijay — 本项目及生成的每份分析报告页脚均带 Vijay 署名。

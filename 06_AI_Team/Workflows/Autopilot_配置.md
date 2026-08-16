# Autopilot 配置一览

> 现有自动化任务（Multica 工作区「车轮星系」）。全部为 schedule 触发，时区 Asia/Shanghai；git push 网络失败时保留本地文件、不报错，下次运行补推。

## 1. 个人AI团队机会周报（每周日全网搜索）
- ID：`63e6939a-a49a-4c5c-aa34-d971b50a1b18`
- 触发时间：每周日 12:00（cron `0 12 * * 0`）
- 模式：create_issue（标题模板「个人AI团队机会周报 {{date}}」）
- 产出位置：新建 issue 的评论（5 个可做方向 + TOP 10 清单 + 本周 Top 3）
- 备注：首次运行 2026-08-16 已完成；prompt 中引用路径为 `D:\Personal_AI_OS_System`（旧路径），实际知识库在 `D:\Personal_AI_OS`，待确认是否更新。

## 2. 周报补做保险（每日检查是否漏跑）
- ID：`8914fdba-c07e-4272-acc8-96f1c567c65f`
- 触发时间：每天 00:30 / 12:30（cron `30 */12 * * *`）
- 模式：run_only
- 产出位置：无。只做两个检查（本周是否有周报 issue；主任务本周是否有成功 run），均未命中时才 `multica autopilot trigger 63e6939a-...` 触发主任务补做。
- 备注：绝不重复触发——任一检查命中即结束。

## 3. 每日日志自动记录
- ID：`01f69b7a-5a43-407c-9040-0c3449a865a4`
- 触发时间：每天 21:30（cron `30 21 * * *`）
- 模式：run_only
- 产出位置：`13_Growth/Daily/YYYY-MM-DD.md`（模板见 `00_System/Daily_Log.md`），随后 git commit + push。
- 备注：当天无 Multica 活动时写明「今天没有使用 Multica」；不创建 issue、不打扰用户。

## 4. 个人成长每周复盘
- ID：`f14ae2a3-3d35-46e2-992c-a950a26a9c02`
- 触发时间：每周日 22:00（cron `0 22 * * 0`）
- 模式：create_issue（标题模板「个人成长每周复盘 {{date}}」）
- 产出位置：`13_Growth/Weekly/YYYY-Wxx.md` + issue 评论（本周总结/成长分析/经验沉淀/下周建议），随后 git commit + push。

## 5. 个人成长每月复盘
- ID：`2743895e-0f1f-4add-a3ad-89d2e3c77ba2`
- 触发时间：每月 1 日 22:00（cron `0 22 1 * *`）
- 模式：create_issue（标题模板「个人成长每月复盘 {{date}}」）
- 产出位置：`13_Growth/Monthly/YYYY-MM.md` + issue 评论（月度总结/能力成长/资产积累/问题与调整/下月规划），随后 git commit + push。

## 数据链路
机会周报（周报 issue）→ 每日日志（Daily/ 素材）→ 每周复盘（Weekly/）→ 每月复盘（Monthly/）→ 经验沉淀回 `07_Knowledge` / `00_System/Mistake_Database.md` 等。

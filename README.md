# cf-tunnel-autoreset
A dedicated macOS watchdog script for Cloudflared Tunnel that ensures high availability by real-time monitoring of log patterns (e.g., "Connection terminated") and automatically force-restarting stalled processes. 一个专为 macOS 设计的 Cloudflared Tunnel 守护脚本，通过实时监控日志关键词（如 "Connection terminated"）自动强制重启卡死的进程，确保内网穿透服务的持续高可用。

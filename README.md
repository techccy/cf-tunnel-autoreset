# cf-tunnel-autoreset (macOS)

[「ENGLISH」](README_EN.md)

这是一个专门为 macOS 用户设计的 Cloudflared Tunnel 守护脚本。

### 💡 解决的问题

在网络不稳定的环境下，`cloudflared` 进程有时并不会自动退出，而是进入一种“虽然运行但已断联”的僵死状态。本脚本通过**实时监控日志**，一旦发现关键词（如 `Connection terminated`），立即强制杀死并重启进程。

### ✨ 功能特点

* **实时监控**：基于行缓冲模式，毫秒级捕获错误日志。
* **强杀重启**：针对 macOS 优化，通过 `SIGKILL` 彻底清理僵死进程，避免端口占用。
* **配置简单**：只需修改脚本顶部的配置项即可。

### 🚀 快速开始

1. **下载文件**
```bash
curl -O https://github.com/techccy/cf-tunnel-autoreset/cloudflared_tunnel_protect.py

```


2. **配置脚本**
编辑 `cloudflared_tunnel_protect.py`，修改 `TUNNEL_NAME` 为你的 Tunnel 名称。
3. **后台运行**
使用 `sudo` 以确保拥有杀死进程的权限：
```bash
sudo sh -c 'nohup python3 cloudflared_tunnel_protect.py > tunnel.log 2>&1 &'

```


4. **停止脚本**
```bash
ps aux | grep cloudflared_tunnel_protect.py | awk '{print $2}' | xargs sudo kill -9

```



### 🛠 配置说明

```python
CLOUDFLARED_CMD = ["cloudflared", "tunnel", "run", "你的Tunnel名"]
TARGET_ERROR = "Connection terminated" # 触发重启的关键词
RESTART_DELAY = 3 # 重启前的等待秒数

```
